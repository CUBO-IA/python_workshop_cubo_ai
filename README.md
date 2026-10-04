# python_workshop_cubo_ai

Material de taller para aprender los **tipos de datos de Python desde cero**,
y dos proyectos construidos con lo aprendido.

El repositorio tiene cuatro partes independientes:

| Carpeta | Qué es | Cómo se estudia |
|---|---|---|
| [`data_types/`](data_types) | Referencia de los 10 tipos de datos | Lectura + ejecutar y comparar la salida |
| [`console/ejercicios/`](console/ejercicios) | 4 ejercicios guiados | Escribir código y ejecutarlo en la terminal |
| [`web/coffee-bit/`](web/coffee-bit) | Tienda de café en Flask | Ejecutar y usar la web |
| [`duck-hunt/`](duck-hunt) | Juego de pygame | Ejecutar y jugar |

Las dos primeras forman el taller y son una continuación natural: los
ejercicios asumen que ya conoces los tipos, y la referencia de tipos cubre la
teoría que los ejercicios dan por sabida. Las dos últimas son proyectos
independientes: no dependen del taller ni entre sí, y cada una tiene su propio
entorno virtual y sus propias dependencias.

---

## Requisitos

Para el taller solo hace falta Python 3. No hay dependencias externas que
instalar.

```bash
python3 --version      # debe ser 3.x
```

Probado con **Python 3.14**. Los scripts usan funciones disponibles desde
Python 3.6, así que deberían funcionar en cualquier 3 moderno.

Los dos proyectos sí necesitan dependencias, y cada uno tiene su propia sección
más abajo con la instalación exacta. En resumen:

| Proyecto | Python | Dependencias |
|---|---|---|
| `web/coffee-bit/` | 3.10+ | Flask, Flask-WTF |
| `duck-hunt/` | 3.13 recomendado | pygame |

---

## Parte 1 — Tipos de datos

Cada archivo se centra en **un solo tipo** y sigue siempre la misma
estructura, para que se pueda estudiar en cualquier orden:

1. Docstring inicial: qué es el tipo y cómo funciona.
2. Secciones numeradas con ejemplos ejecutables y comentado.
3. `practical_examples()` — programas pequeños y reales con ese tipo.
4. `common_mistakes()` — los errores más frecuentes de quien empieza.
5. `best_practices()` — resumen de las reglas del tipo.

Empieza por **[`data_types/intro.md`](data_types/intro.md)**: es la guía
completa con tabla comparativa, explanation de cada tipo y una tabla para
elegir tipo.

### Los 10 archivos

| Archivo | Tipo | Ejemplo | Idea central |
|---|---|---|---|
| [`none.py`](data_types/none.py) | `NoneType` | `None` | La ausencia de valor |
| [`boolean.py`](data_types/boolean.py) | `bool` | `True` | Verdaded, *truthiness* y cortocircuito |
| [`integer.py`](data_types/integer.py) | `int` | `42` | Precisión arbitraria, `/` vs `//` |
| [`float.py`](data_types/float.py) | `float` | `3.14` | El error de `0.1 + 0.2` |
| [`complex.py`](data_types/complex.py) | `complex` | `3 + 4j` | Parte real e imaginaria, módulo `cmath` |
| [`strings.py`](data_types/strings.py) | `str` | `"hola"` | Inmutabilidad, indexado, f-strings |
| [`list.py`](data_types/list.py) | `list` | `[1, 2]` | La colección por defecto, mutable |
| [`tuple.py`](data_types/tuple.py) | `tuple` | `(1, 2)` | Inmutable y *hashable* |
| [`dictionary.py`](data_types/dictionary.py) | `dict` | `{"a": 1}` | Claves únicas, `.get()` seguro |
| [`set.py`](data_types/set.py) | `set` | `{1, 2}` | Sin duplicados, sin orden |

### Cómo ejecutarlos

Cada script es autónomo e imprime su salida comentada:

```bash
cd data_types
python3 boolean.py
```

Los diez están verificados: compilan y se ejecutan sin errores ni advertencias.

> **Nota:** el plural de `strings.py` es intencionado. El archivo se llama
> así para no ensombrecer el módulo `string` de la biblioteca estándar, un
> problema que sí ocurrió aquí. Ningún archivo de `data_types/` colisiona ya,
> así que puedes ejecutarlos desde dentro de la carpeta. El detalle está en
> [`intro.md`](data_types/intro.md#related-notes).

### Ruta de estudio sugerida

1. [`intro.md`](data_types/intro.md) — la vista general y la tabla de decisión.
2. `none.py` y `boolean.py` — la base: ausencia de valor y verdad.
3. `integer.py` → `float.py` → `complex.py` — la torre numérica, de menor a
   mayor rango.
4. `strings.py` — el tipo más usado en la práctica.
5. `list.py` → `tuple.py` → `dictionary.py` → `set.py` — las colecciones.
6. Vuelve a [`intro.md`](data_types/intro.md) y decide tú mismo qué tipo le
   corresponde a cada caso que te encuentres.

---

## Parte 2 — Ejercicios de consola

Los cuatro son interactivos: piden datos por terminal. Cada uno tiene su
explicación completa en el docstring de arriba, con el objetivo, lo que se
practica, cómo ejecutarlo y un ejemplo de salida real.

### [`console_programa.py`](console/ejercicios/console_programa.py)

El punto de partida. Ensaya la lectura por consola y las f-strings.

```bash
cd console/ejercicios
python3 console_programa.py
```

> El error clásico que evitar: `input()` **siempre** devuelve `str`, aunque
> escribas un número. Comparar `"18" < 18` lanza `TypeError`. Hay que
> convertir con `int(...)` o `float(...)`.

### [`boolean.py`](console/ejercicios/boolean.py)

Pide nombre y edad, y responde preguntas de sí/no con variables booleanas de
nombre legible (`es_menor`, `es_exacto_18`). Practica `if` y el operador
ternario.

### [`strings.py`](console/ejercicios/strings.py)

Pide nombre y apellido, y compara las **tres** formas de unirlos: f-string,
`+` y `"".join()`. Luego aplica `.title()`, `.upper()`, `.lower()` y
`.strip()`.

### [`calculadora_imc.py`](console/ejercicios/calculadora_imc.py)

El ejercicio completo, y el más largo. Calcula el Índice de Masa Corporal
siguiendo el ciclo de vida de cualquier programa: **pedir → validar →
calcular → clasificar → mostrar**.

Pide nombre, edad, peso **en libras** y estatura en metros. Si escribes algo
inválido (por ejemplo `ochenta` en la edad), vuelve a preguntar en lugar de
romperse.

```bash
python3 calculadora_imc.py
```

Para probarlo sin escribir nada a mano, alimenta la entrada desde otro
comando. Ojo: el peso es en **libras**, no en kilogramos.

```bash
printf "Ana\n30\n138\n1.68\n" | python3 calculadora_imc.py
```

Qué demuestra con datos reales:

```
  Peso      : 138.0 lb  ->  62.60 kg
  Estatura  : 1.68 m
  IMC       : 22.18   (calculado como 62.60 / 1.68²)
  Categoría : Peso normal
```

> El IMC es una referencia general, **no un diagnóstico médico**.

---

## Parte 3 — Coffee-bit (tienda web en Flask)

Tienda de café con catálogo, carrito con sesión y finalización de pedido.
Catálogo de 4 productos, cada uno con su detalle, su precio y su imagen.

### Instalación

```bash
cd web/coffee-bit
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Ejecución

```bash
python app.py
```

La tienda queda disponible en **<http://127.0.0.1:5808>**.

> Ojo con el puerto: `app.py` arranca en el **5808**. El puerto se fijó a mano
> en la llamada a `app.run()` (`app.py:183`), así que no cambia con
> `FLASK_ENV`. Si el 5808 está ocupado, edita esa línea.

### Variables de entorno

| Variable | Obligatoria | Descripción |
| --- | --- | --- |
| `SECRET_KEY` | Solo fuera de `development` | Clave de firma de la sesión. |
| `FLASK_ENV` | No (`development`) | Si no es `development`, exige `SECRET_KEY`. |

Para arrancar fuera de desarrollo:

```bash
export FLASK_ENV=production
export SECRET_KEY="una-clave-larga-y-aleatoria"
python app.py
```

Si `SECRET_KEY` falta en producción, la aplicación falla al importar
`config.py` en lugar de usar una clave de desarrollo.

### Rutas

| Ruta | Métodos | Descripción |
| --- | --- | --- |
| `/` | GET | Catálogo |
| `/producto/<product_id>` | GET | Detalle de producto (slug) |
| `/carrito` | GET | Ver carrito |
| `/carrito/agregar/<product_id>` | POST | Añadir unidades al carrito |
| `/carrito/actualizar/<product_id>` | POST | Fijar cantidad (0 elimina) |
| `/carrito/eliminar/<product_id>` | POST | Quitar un producto del carrito |
| `/checkout` | GET, POST | Resumen y confirmación del pedido |

### Detalles que conviene conocer antes de tocarla

- Los identificadores de producto son slugs de texto (`semilla-tostada`), por
  eso las rutas usan `<string:product_id>` y no `<int:...>`.
- El carrito vive en `session["cart"]` como un diccionario `{slug: cantidad}`.
- `build_cart()` devuelve `{"lines": [...], "total": n}`. La clave es `lines` y
  no `items` porque en Jinja `cart.items` resolvería al método `dict.items()`
  en vez de a la clave.
- Todos los formularios POST incluyen `csrf_token` y la aplicación tiene
  `CSRFProtect` activo. Si pruebas las rutas con `curl`, tienes que extraer el
  token de la página antes del POST o recibirás un 400.
- `add_to_cart` respeta la cantidad enviada por el formulario; `update_cart`
  fija la cantidad absoluta y elimina si es 0.
- **El pago no está implementado:** confirmar el pedido vacía el carrito y
  muestra el total registrado. No hay pasarela, ni persistencia de pedidos, ni
  control de stock.

El detalle completo está en [`web/coffee-bit/README.md`](web/coffee-bit/README.md).

---

## Parte 4 — Duck Hunt (juego en pygame)

Recreación del clásico de NES: los patos cruzan la pantalla y hay que
eliminarlos antes de que escapen. Cada ronda exige **3 aciertos de 5 patos**,
y los patos vuelan cada vez más rápido.

### Características

- Ventana de 960×720 a 60 FPS, con los patos animados de tres fotogramas y el
  perro saltando en un arco parabólico cuando reacciona a cada pato.
- Reglas del original: diez patos por ronda, seis aciertos para pasar, tres
  disparos por pato y un bonus si los abates todos. Desde la ronda 11 vuelan
  dos patos a la vez, y desde la 21, tres.
- Física real: los patos rebotan contra el techo, escapan al salir de la
  pantalla y al recibir un tiro caen con gravedad mientras giran.
- Los patos pasan por detrás del matorral, como en el juego de NES.
- Todo el arte y el sonido están generados por `tools/generate_assets.py`, que
  los compone con pygame y con la biblioteca estándar: no hay ni un solo
  fichero hecho a mano, ni una fuente TTF de terceros.
- Puntuación de 100 por pato y mejores puntuaciones guardadas en
  `~/.local/share/duck-hunt/` (siguiendo XDG).
- Integración con GNOME: ventana, pausa y salida desde el ciclo de vida de GTK.
- Indicador en la bandeja del sistema con mostrar, pausar, silenciar y salir.
- Pausa con `F10`, silencio con `M` y pantalla completa con `F11`.

### Instalación

El juego usa **pygame**, y su wheel no compila contra las versiones más
recientes de Python. Lo más seguro es fijar la versión:

```bash
cd duck-hunt
uv venv --python 3.13 .venv
uv pip install -r requirements.txt
```

Con `python3 -m venv` también funciona, siempre que el intérprete sea 3.13:

```bash
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Ejecución

```bash
./bin/duck-hunt
```

O directamente, si el entorno ya está activo:

```bash
python run.py
```

También hay un lanzador de escritorio en
`data/com.duckhunt.Game.desktop`, por si prefieres abrirlo desde el menú de
aplicaciones.

> **Por qué existe el lanzador.** Si ejecutas `python3 run.py` con el Python
> del sistema y pygame no se puede importar, `run.py` se relanza solo con
> `.venv/bin/python`, que es el único intérprete con la wheel instalada. Si
> tampoco existe ese `.venv`, el error te dice exactamente qué comando ejecutar.
> `bin/duck-hunt` hace lo mismo desde bash, pero como punto de entrada único.

### Controles

| Acción | Tecla / ratón |
| --- | --- |
| Dispara | Clic izquierdo |
| Elegir opción del menú | `↑` `↓` |
| Empezar partida / siguiente ronda | `Enter` o `Espacio` |
| Volver al menú | `Esc` |
| Minimizar a la bandeja | `Esc` en el menú, o cerrar la ventana |
| Pausa | `F10` (o `Esc` para salir de la pausa) |
| Silenciar | `M` |
| Pantalla completa | `F11` |
| Mostrar / salir desde la bandeja | Menú del indicador |

> El cursor del ratón se oculta (`HIDE_MOUSE_CURSOR`), porque la mira es un
> crosshair dibujado en pantalla. Cierra la ventana y el juego **no** termina:
> se minimiza y sigue vivo en la bandeja. Para salir de verdad, usa `Quit` en
> el indicador.

### Estructura

```
run.py                      Punto de entrada; relanza en el venv si hace falta
bin/duck-hunt               Lanzador en bash
scripts/build.sh            Empaquetado para Linux (.deb, AppImage, Flatpak)
tools/generate_assets.py    Genera sprites, fuente y sonidos
tools/entrypoint.py         Entrada del binario congelado
src/app.py                  Ventana, bucle principal, teclado y ratón
src/game.py                 Reglas: rondas, puntuación y estados
src/config.py               Todas las constantes (tamaño, tiempos, rondas)
src/assets.py               Rutas, tanto en repo como en binario congelado
src/sprites.py              Carga y recorte de imágenes
src/high_scores.py          Persistencia de los récords
src/entities/               duck.py, dog.py, grass.py, bullet.py
src/ui/                     pixel_font.py, fonts.py, crosshair.py, hud.py, screens.py, text.py
src/audio/sound_manager.py  Carga y reproducción de sonidos
src/gnome_app.py            Integración con el ciclo de vida de GTK
src/indicator.py            Indicador de bandeja (AppIndicator)
assets/                     Imágenes, sonidos, fuente e icono (generados)
tests/                      Tests con SDL en modo dummy
packaging/                  Metadatos de los paquetes de Linux
data/com.duckhunt.Game.desktop
```

### Integración con GNOME: opcional a propósito

`gi` (PyGObject) solo está disponible para el intérprete del sistema, no para
el `.venv` del proyecto, que es el que tiene pygame. Por eso tanto
`gnome_app.py` como `indicator.py` envuelven sus imports en `try/except`:
**sin PyGObject el juego funciona igual**, solo se pierde la integración con
el ciclo de vida de GTK y el icono de la bandeja.

Es un límite real de la plataforma, no un descuido: pygame necesita el venv y
GTK necesita el intérprete del sistema, y no se pueden compartir.

### Assets ausentes

`config.py` pide tres sprites del perro: `dog_idle.png`, `dog_happy.png` y
`dog_laugh.png`. **Ninguno está en `assets/images/`.** El juego no falla por
ello: `entities/dog.py` cae en un *fallback* que dibuja el perro con elipses y
polígonos de pygame, un color distinto para cada estado (inactivo, feliz y
riéndose). Se ve, pero es un perro de formas geométricas.

Lo raro es que `assets/images/dog.png` **sí existe** y no lo referencia nada
en `src/`. Probablemente el sprite que falta se debería generar a partir de
ese archivo. Hasta que se cree, el perro se ve provisional.

### Pruebas

Hay dos archivos en `tests/`, pero están **vacíos**: no hay nada que ejecutar
todavía. Los módulos se importan bien y la aplicación se construye sin errores
con pygame 2.6.1.

---

## Estructura del repositorio

```
.
├── README.md                    ← este archivo
├── .gitignore
├── data_types/                  ← referencia de los 10 tipos
│   ├── intro.md                 ← guía completa y punto de entrada
│   ├── none.py       boolean.py     integer.py    float.py
│   ├── complex.py    strings.py     list.py       tuple.py
│   └── dictionary.py set.py
├── console/
│   └── ejercicios/              ← 4 ejercicios interactivos
│       ├── console_programa.py
│       ├── boolean.py
│       ├── strings.py
│       └── calculadora_imc.py
├── web/
│   └── coffee-bit/              ← tienda en Flask
│       ├── app.py               ← rutas, carrito y checkout
│       ├── config.py            ← configuración por entorno
│       ├── requirements.txt
│       ├── data/products.py     ← catálogo
│       ├── templates/           ← Jinja (base, index, product, cart, checkout, 404)
│       └── static/              ← css, js e imágenes
├── duck-hunt/                   ← juego en pygame
│   ├── run.py                   ← punto de entrada
│   ├── bin/duck-hunt            ← lanzador
│   ├── requirements.txt
│   ├── scripts/build.sh         ← empaquetado para Linux
│   ├── tools/                   ← generador de recursos y entrada del binario
│   ├── src/                     ← app, game, entities, ui, audio
│   ├── assets/                  ← imágenes, sonidos, fuente e icono (generados)
│   ├── tests/                   ← tests de duck, game y entidades
│   ├── packaging/               ← metadatos de los paquetes
│   └── data/com.duckhunt.Game.desktop
│   └── tests/                   ← test_duck.py, test_game.py (vacíos)
└── desktop/                     ← andamiaje de scripts de creación
    └── create_project.py
```

Cada entorno virtual (`.venv/`) es local de la máquina y no se versiona.

---

## Convenciones

- **Comentarios en español**, porque es el idioma del taller.
- Código y nombres de identificadores en inglés, siguiendo la convención de
  Python.
- El bucle `if __name__ == "__main__":` protege la parte ejecutable, para que
  los archivos se puedan importar sin que se ejecuten.
- Todo el código está comentado con el porqué, no solo el qué.

---

## Errores conocidos

Ninguno bloquea el estudio, pero conviene conocerlos:

- **Colisión de nombres con la stdlib (resuelta).** Los archivos se llamaban
  `string.py` y chocaban con el módulo estándar `string`. El fallo ocurrió en la
  práctica: el gestor de errores de Python hizo
  `from string import Template` y acabó ejecutando el ejercicio entero. Ambos
  se renombraron a `strings.py`, así que hoy no hay colisión y todo se puede
  ejecutar en su propia carpeta.
- **El ejemplo OOP de `intro.md` no funciona.** El fragmento heredado sobre
  herencia múltiple lanza `TypeError: D() takes no arguments`. Se conserva sin
  tocar a propósito y está documentado en
  [`intro.md`](data_types/intro.md#related-notes).
- **Los ejercicios de consola no se pueden probar con `</dev/null`.** Terminan
  con `EOFError`, porque `input()` no encuentra nada que leer. Es el
  comportamiento esperado, no un fallo del ejercicio.
- **Los tests de Duck Hunt están vacíos.** *(resuelto)* Ahora hay 78 tests que
  cubren el vuelo y la caída del pato, el salto del perro, las reglas de ronda,
  los bonus y los récords. Se ejecutan con `SDL_VIDEODRIVER=dummy`, sin abrir
  ventana, y `pytest` está en `requirements-dev.txt`.
- **El puerto 5808 de Coffee-bit está fijado en el código.** No viene de una
  variable de entorno, así que cambiarlo exige editar `app.py:183`. Ojo: el
  README de esa subcarpeta todavía menciona el puerto antiguo 5707.
- **`duck-hunt/README.md` estaba vacío.** *(resuelto)* El juego se documenta
  ahora también en su propia carpeta.
- **Faltaban los tres sprites del perro en Duck Hunt.** *(resuelto)*
  `tools/generate_assets.py` genera `dog_idle.png`, `dog_happy.png` y
  `dog_laugh.png`, además del resto de sprites, de la fuente de píxeles y de
  los once sonidos. Todos los ficheros de `assets/` que estaban a cero bytes
  han desaparecido.
- **El Flatpak de Duck Hunt no viene compilado.** El manifiesto está escrito y
  pasa el linter de Flathub, pero la compilación necesita que
  `flatpak-builder` vea el SDK, y desde la instalación de usuario no lo ve.
  El `.deb` y el AppImage sí están compilados y verificados. Está explicado en
  `duck-hunt/README.md`.
- **Duck Hunt necesita GTK del sistema y pygame del venv, y no conviven.**
  PyGObject solo existe para el intérprete del sistema, así que la integración
  con la bandeja y con el ciclo de vida de GNOME es opcional por diseño: el
  juego arranca igual sin ella, solo sin icono de bandeja. El binario
  congelado (`.deb` y AppImage) sí puede usarla, porque lleva su propio
  Python.
