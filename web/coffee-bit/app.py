import datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_wtf.csrf import CSRFProtect

from config import Config
from data.products import PRODUCTS


def find_product(product_id):
    return next((item for item in PRODUCTS if item["id"] == product_id), None)


def build_cart():
    """Normaliza la sesion del carrito para las plantillas.

    Descarta los ids que ya no existen en el catalogo y las cantidades no
    positivas, de modo que la sesion y lo que ve el usuario nunca discrepen.

    La clave es 'lines' y no 'items' porque en Jinja ``cart.items`` resolveria
    al metodo ``dict.items()`` en lugar de a la clave del diccionario.
    """
    lines = []
    total = 0

    for product_id, quantity in session.get("cart", {}).items():
        product = find_product(product_id)

        if product is None or quantity <= 0:
            continue

        subtotal = product["price_sat"] * quantity
        total += subtotal
        lines.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return {"lines": lines, "total": total}


def cart_count():
    """Unidades visibles del carrito.

    Se deriva de ``build_cart()`` y no de ``sum(session['cart'].values())``
    porque la sesion puede contener ids obsoletos o cantidades no positivas
    que el carrito no muestra; sumarlos daria un contador que no cuadra.
    """
    return sum(line["quantity"] for line in build_cart()["lines"])


def parse_quantity(raw, default=1):
    try:
        quantity = int(raw)
    except (TypeError, ValueError):
        return default

    return max(quantity, 0)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CSRFProtect(app)

    @app.context_processor
    def inject_globals():
        return {
            "cart_count": cart_count(),
            "current_year": datetime.date.today().year,
        }

    return app


app = create_app()


@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)


@app.route("/producto/<string:product_id>")
def product(product_id):
    product = find_product(product_id)

    if product is None:
        return render_template("404.html"), 404

    return render_template("product.html", product=product)


@app.route("/carrito")
def cart():
    return render_template("cart.html", cart=build_cart())


@app.route("/carrito/agregar/<string:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = find_product(product_id)

    if product is None:
        return render_template("404.html"), 404

    quantity = parse_quantity(request.form.get("quantity", 1), default=0)
    cart = session.get("cart", {})

    if quantity <= 0:
        flash("La cantidad debe ser mayor que cero.", "error")
    else:
        cart[product_id] = cart.get(product_id, 0) + quantity
        session["cart"] = cart
        flash(f"'{product['name']}' agregado al carrito.", "success")

    return redirect(url_for("cart"))


@app.route("/carrito/actualizar/<string:product_id>", methods=["POST"])
def update_cart(product_id):
    if find_product(product_id) is None:
        return render_template("404.html"), 404

    quantity = parse_quantity(request.form.get("quantity", 1), default=0)
    cart = session.get("cart", {})

    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id, None)

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


@app.route("/carrito/eliminar/<string:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(product_id, None)
    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = build_cart()

    if not cart["lines"]:
        return redirect(url_for("cart"))

    if request.method == "POST":
        session.pop("cart", None)
        return render_template(
            "checkout.html",
            cart={"lines": [], "total": 0},
            order_completed=True,
            order_total=cart["total"],
        )

    return render_template(
        "checkout.html",
        cart=cart,
        order_completed=False,
    )


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=5808)
