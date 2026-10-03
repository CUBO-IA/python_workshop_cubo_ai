# Coffee-bit

Tienda de café en Flask. Catálogo de productos, carrito con sesión y
finalización de pedido.

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

La aplicación queda disponible en <http://127.0.0.1:5707>.

## Configuración

| Variable    | Obligatoria                  | Descripción                                   |
| ----------- | ---------------------------- | --------------------------------------------- |
| `SECRET_KEY` | Solo fuera de `development`  | Clave de firma de la sesión.                  |
| `FLASK_ENV` | No (`development`)           | Si no es `development`, exige `SECRET_KEY`.    |

Para arrancar fuera de desarrollo:

```bash
export FLASK_ENV=production
export SECRET_KEY="una-clave-larga-y-aleatoria"
python app.py
```

Si `SECRET_KEY` falta en producción, la aplicación falla al importar
`config.py` en lugar de usar una clave de desarrollo.

## Estructura

```
app.py                  Rutas Flask, carrito y checkout
config.py               Configuración por entorno
data/products.py        Catálogo (id, nombre, precio en satoshis, imagen)
templates/              Plantillas Jinja (base, index, product, cart, checkout, 404)
static/css/style.css    Estilos
static/js/main.js       Menú responsive, confirmaciones y contador del carrito
static/images/          Imágenes de producto
```

## Rutas

| Ruta                                   | Métodos      | Descripción                        |
| -------------------------------------- | ------------ | ---------------------------------- |
| `/`                                    | GET          | Catálogo                           |
| `/producto/<product_id>`               | GET          | Detalle de producto (slug)         |
| `/carrito`                             | GET          | Ver carrito                        |
| `/carrito/agregar/<product_id>`        | POST         | Añadir unidades al carrito         |
| `/carrito/actualizar/<product_id>`     | POST         | Fijar cantidad (0 elimina)         |
| `/carrito/eliminar/<product_id>`       | POST         | Quitar un producto del carrito     |
| `/checkout`                            | GET, POST    | Resumen y confirmación del pedido  |

## Notas de implementación

- Los identificadores de producto son slugs de texto
  (`semilla-tostada`), por eso las rutas usan `<string:product_id>`.
- El carrito vive en `session["cart"]` como un diccionario
  `{slug: cantidad}`.
- `build_cart()` devuelve `{"lines": [...], "total": n}`. La clave es
  `lines` y no `items` porque en Jinja `cart.items` resolvería al
  método `dict.items()` en vez de a la clave.
- Todos los formularios POST incluyen `csrf_token` y la aplicación
  tiene `CSRFProtect` activo.
- `add_to_cart` respeta la cantidad enviada por el formulario;
  `update_cart` fija la cantidad absoluta y elimina si es 0.
- El pago no está implementado: confirmar el pedido vacía el carrito y
  muestra el total registrado.

## Estado del proyecto

La compra es funcional de punta a punta salvo el pago: no hay pasarela,
ni persistencia de pedidos, ni control de stock. Los pedidos confirmados
solo se muestran en la respuesta HTTP y no se almacenan.
