# python_workshop_cubo_ai

Material de taller para aprender los **tipos de datos de Python desde cero**.

El repositorio tiene dos partes independientes, pensadas para distintos
momentos del aprendizaje:

| Carpeta | Qué es | Cómo se estudia |
|---|---|---|
| [`data_types/`](data_types) | Referencia de los 10 tipos de datos | Lectura + ejecutar y comparar la salida |
| [`console/ejercicios/`](console/ejercicios) | 4 ejercicios guiados | Escribir código y ejecutarlo en la terminal |

No son dos redes de apoyo: los ejercicios asumen que ya conoces los tipos, y
la referencia de tipos cubre la teoría que los ejercicios dan por sabida.

---

## Requisitos

Solo hace falta Python 3. No hay dependencias externas que instalar.

```bash
python3 --version      # debe ser 3.x
```

Probado con **Python 3.14**. Los scripts usan funciones disponibles desde
Python 3.6, así que deberían funcionar en cualquier 3 moderno.

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
| [`string.py`](data_types/string.py) | `str` | `"hola"` | Inmutabilidad, indexado, f-strings |
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

> **Importante:** ejecútalos desde **fuera** de la carpeta `data_types/`.
> Varios archivos se llaman igual que módulos de la biblioteca estándar
> (por ejemplo `string.py`), y Python puede acabar importando tu archivo en
> lugar del módulo real. Es la razón por la que los archivos de la tabla
> anterior están pensados para leerse, no para importarse. El detalle está
> explicado en [`intro.md`](data_types/intro.md#related-notes).

Si prefieres evitar la colisión de nombres, renombra `string.py` a
`strings.py`.

### Ruta de estudio sugerida

1. [`intro.md`](data_types/intro.md) — la vista general y la tabla de decisión.
2. `none.py` y `boolean.py` — la base: ausencia de valor y verdad.
3. `integer.py` → `float.py` → `complex.py` — la torre numérica, de menor a
   mayor rango.
4. `string.py` — el tipo más usado en la práctica.
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

### [`string.py`](console/ejercicios/string.py)

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

## Estructura del repositorio

```
.
├── README.md                    ← este archivo
├── .gitignore
├── data_types/                  ← referencia de los 10 tipos
│   ├── intro.md                 ← guía completa y punto de entrada
│   ├── none.py       boolean.py     integer.py    float.py
│   ├── complex.py    string.py      list.py       tuple.py
│   └── dictionary.py set.py
└── console/
    └── ejercicios/              ← 4 ejercicios interactivos
        ├── console_programa.py
        ├── boolean.py
        ├── string.py
        └── calculadora_imc.py
```

Las carpetas `desktop/` y `web/` están vacías y se crean automáticamente al
empezar a trabajar en ellas. Git no las versiona mientras no tengan archivos.

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

- **Colisión de nombres con la stdlib.** `data_types/string.py` y
  `console/ejercicios/string.py` se llaman como el módulo estándar `string`.
  Al ejecutar un script desde dentro de esas carpetas, un `import string`
  puede cargar tu archivo y ejecutarlo entero. Se ha observado en la
  práctica: el gestor de errores de Python hizo
  `from string import Template` y acabó ejecutando el ejercicio.
  Solución: ejecutar desde el directorio padre, o renombrar a `strings.py`.
- **El ejemplo OOP de `intro.md` no funciona.** El fragmento heredado sobre
  herencia múltiple lanza `TypeError: D() takes no arguments`. Se conserva sin
  tocar a propósito y está documentado en
  [`intro.md`](data_types/intro.md#related-notes).
- **Los ejercicios de consola no se pueden probar con `</dev/null`.** Terminan
  con `EOFError`, porque `input()` no encuentra nada que leer. Es el
  comportamiento esperado, no un fallo del ejercicio.
