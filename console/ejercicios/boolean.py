"""
EJERCICIO: pedir nombre y edad por consola y usar booleanos.

Objetivo
--------
Practicar `input()`, la conversion de texto a numero (`int`) y el uso de
variables booleanas (`True` / `False`) para responder preguntas de si/no.

Que vas a practicar
------------------
1. `input()` para leer datos del teclado. OJO: `input()` SIEMPRE devuelve
   texto (str), aunque escribas un numero. Para poder comparar hay que
   convertirlo: `int(input(...))`.
2. Una comparacion (`<`, `==`) devuelve un booleano: `True` o `False`.
3. Guardar el booleano en una variable con nombre legible
   (`es_menor`, `es_exacto_18`) y despues reutilizarlo con `if`.

Como ejecutarlo
----------------
    python3 boolean.py

Ejemplo de ejecucion
--------------------
    Escribe tu nombre: Ana
    Escribe tu edad: 17
    Hola Ana, eres menor de edad.
    Tu edad es 17: eres menor de edad.
    Es exactamente 18: Falso
"""


# ---------------------------------------------------------------------------
# 1. Lectura de datos por consola
# ---------------------------------------------------------------------------
# `input()` muestra un texto (el "prompt") y espera a que el usuario escriba.
# Siempre devuelve un str, NUNCA un int. Comparar "18" < 18 seria un error
# (TypeError), asi que convertimos con `int(...)`.

nombre = input("Escribe tu nombre: ")
edad = int(input("Escribe tu edad: "))       # str -> int

print("Datos capturados:")
print(f"  nombre -> {nombre!r} ({type(nombre).__name__})")   # str
print(f"  edad   -> {edad!r} ({type(edad).__name__})")       # int


# ---------------------------------------------------------------------------
# 2. PRIMER MENSAJE: usar un booleano para saber si es menor de edad
# ---------------------------------------------------------------------------
# `edad < 18` es una pregunta de si/no, y su respuesta es un booleano.
# Guardarla en una variable con nombre descriptivo hace el codigo mas legible
# que repetir la comparacion una y otra vez.

es_menor = edad < 18        # -> True o False

if es_menor:
    print(f"Hola {nombre}, eres menor de edad.")
else:
    print(f"Hola {nombre}, eres mayor de edad.")


# ---------------------------------------------------------------------------
# 3. SEGUNDO MENSAJE: comprobar si la edad es exactamente 18
# ---------------------------------------------------------------------------
# Mismo mecanismo, pero con `==` (igualdad) en lugar de `<` (menor que).
# El booleano se guarda primero y luego se muestra como "Verdadero"/"Falso",
# porque Python imprime `True`/`False` en ingles.

es_exacto_18 = edad == 18   # -> True o False

if es_exacto_18:
    print(f"¿Tienes exactamente 18 años? {es_exacto_18} (Verdadero)")
else:
    print(f"¿Tienes exactamente 18 años? {es_exacto_18} (Falso)")


# ---------------------------------------------------------------------------
# 4. Resumen de los booleanos usados
# ---------------------------------------------------------------------------
# Los tres datos del ejercicio convertidos a booleano. `type()` confirma que
# son del tipo `bool`.

print("\n--- resumen ---")
print(f"es_menor    = {es_menor}    ({type(es_menor).__name__})")
print(f"es_exacto_18= {es_exacto_18} ({type(es_exacto_18).__name__})")

# Un booleano tambien se puede convertir a texto con str() o, mejor, con
# una expresion condicional (ternario). Un `if` clasico tambien sirve.
print(f"es_menor como texto     -> {str(es_menor)}")
print(f"es_menor con ternario   -> {'Verdadero' if es_menor else 'Falso'}")
print(f"es_exacto_18 como texto -> {'Verdadero' if es_exacto_18 else 'Falso'}")