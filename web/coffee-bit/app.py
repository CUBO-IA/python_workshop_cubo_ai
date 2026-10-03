from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from data.products import PRODUCTS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

app = create_app()

@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)

@app.route("/producto/<int:product_id>")
def product(product_id):
    product = next(
        (item for item in PRODUCTS if item["id"] == product_id),
        None
    )

    if product is None:
        return "Producto no encontrado", 404

    return render_template("product.html", product=product)

@app.route("/carrito")
def cart():
    cart_items = []
    total = 0

    for product_id, quantity in session.get("cart", {}).items():
        product = next(
            (item for item in PRODUCTS if item["id"] == int(product_id)),
            None
        )

        if product is None:
            continue

        subtotal = product["price"] * quantity
        total += subtotal
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )

@app.route("/carrito/agregar/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = next(
        (item for item in PRODUCTS if item["id"] == product_id),
        None
    )

    if product is None:
        return "Producto no encontrado", 404

    cart = session.get("cart", {})
    product_key = str(product_id)

    cart[product_key] = cart.get(product_key, 0) + 1
    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))

@app.route("/carrito/actualizar/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    product = next(
        (item for item in PRODUCTS if item["id"] == product_id),
        None
    )

    if product is None:
        return "Producto no encontrado", 404

    try:
        quantity = int(request.form.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    cart = session.get("cart", {})
    product_key = str(product_id)

    if quantity > 0:
        cart[product_key] = quantity
    else:
        cart.pop(product_key, None)
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/carrito/eliminar/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("cart"))
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = next(
            (item for item in PRODUCTS if item["id"] == int(product_id)),
            None
        )
        if product is None:
            continue
        subtotal = product["price"] * quantity
        total += subtotal
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })
    if request.method == "POST":
        session.pop("cart", None)
        return render_template(
            "checkout.html",
            cart_items=[],
            total=0,
            order_completed=True
        )
    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total,
        order_completed=False
    )


if __name__ == "__main__":
    app.run(debug=True, port=5707)
