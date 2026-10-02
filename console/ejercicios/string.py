"""
EJERCICIO: pedir nombre y apellido por consola y mostrarlos juntos en una
sola linea.

Objetivo
--------
Practicar `input()` y las formas de unir texto en Python, que es la
operacion mas comun con cadenas.

Que vas a practicar
------------------
1. `input()` lee texto del teclado y SIEMPRE devuelve un `str`.
2. Concatenar (juntar) dos cadenas de tres maneras:
      - con f-strings:      f"{nombre} {apellido}"   <- la moderna
      - con `+`:             nombre + " " + apellido
      - con `"".join([...])`: " ".join([nombre, apellido])
3. `str.title()`, `str.upper()`, `str.lower()` y `str.strip()` para limpiar y
   dar formato al texto.

Como ejecutarlo
----------------
    python3 string.py

Ejemplo de ejecucion
--------------------
    Escribe tu nombre: ana
    Escribe tu apellido: LOPEZ
    Nombre completo: ana LOPEZ
"""


# ---------------------------------------------------------------------------
# 1. Lectura de datos por consola
# ---------------------------------------------------------------------------
# Cada `input()` muestra su prompt y espera una linea de texto.
# Lo que escribe el usuario SIEMPRE llega como str, nunca hay que convertirlo.

nombre = input("Escribe tu nombre: ")
apellido = input("Escribe tu apellido: ")

# Ojo con un error tipico: los prompts se ejecutan en este orden,
#asi que `nombre` todavia no existe cuando se pide el apellido.


# ---------------------------------------------------------------------------
# 2. PRIMERA FORMA de unir: f-string (la recomendada)
# ---------------------------------------------------------------------------
# Una f-string antepuesta a las comillas permite meter variables dentro de
# {} y, entre las llaves, incluso escribir expresiones como `nombre.upper()`.
# Es la forma mas legible y rapida de construir texto en Python actual.

nombre_completo = f"{nombre} {apellido}"       # el espacio va DENTRO del texto

print(f"Nombre completo: {nombre_completo}")   # en una sola linea

# Los f-strings tambien evaluan expresiones:
print(f"En mayusculas: {nombre.upper()} {apellido.upper()}")
# Si el usuario escribe "  ana  ", `nombre[0]` es un espacio, no la letra "a".
# Por eso aqui se limpia ANTES de tomar el indice (se ve mejor en la seccion 4).
inicial_nombre = nombre.strip().title()[0]
inicial_apellido = apellido.strip().title()[0]
print(f"Iniciales: {inicial_nombre}. {inicial_apellido}.")


# ---------------------------------------------------------------------------
# 3. OTRAS FORMAS de unir (para entender la diferencia)
# ---------------------------------------------------------------------------
# La concatenacion con `+` tambien funciona, pero hay que acordarse del
# espacio: "ana" + " " + "lopez". Sin el espacio queda "analopez".
concatenado = nombre + " " + apellido

# `join` mete un separador entre cada elemento de una lista.
# El separador va ADELANTE del punto: " ".join([...])
unido = " ".join([nombre, apellido])

print("\n--- comparando las tres formas ---")
print(f"con f-string       -> {nombre_completo!r}")
print(f"con +              -> {concatenado!r}")
print(f"con join           -> {unido!r}")
print(f"las tres coinciden -> {nombre_completo == concatenado == unido}")

# OJO: `+` NO une un str con un int (TypeError). Para eso estan las f-strings.
# f"Edad: {5}"   -> funciona
# "Edad: " + 5   -> TypeError


# ---------------------------------------------------------------------------
# 4. Limpiar el texto de entrada
# ---------------------------------------------------------------------------
# El usuario puede escribir espacios sobrantes ("  ana  ") o escribir en
# mayusculas. `.strip()` quita los espacios de los extremos y `.title()`
# pone mayuscula la inicial de cada palabra.

nombre_limpio = nombre.strip().title()
apellido_limpio = apellido.strip().title()

print("\n--- entrada sin limpiar vs limpiada ---")
print(f"original  -> {nombre_completo!r}")
print(f"limpiada  -> {nombre_limpio + ' ' + apellido_limpio!r}")

# El resultado final, ya formateado:
print(f"\nNombre completo: {nombre_limpio} {apellido_limpio}")


# ---------------------------------------------------------------------------
# 5. Cosas utiles que se pueden hacer con el resultado
# ---------------------------------------------------------------------------
completo = f"{nombre_limpio} {apellido_limpio}"

print("\n--- resumen ---")
print(f"nombre completo     -> {completo}")
print(f"caracteres          -> {len(completo)}")      # len() cuenta caracteres
print(f"palabras            -> {completo.count(' ') + 1}")
print(f"en mayusculas       -> {completo.upper()}")
print(f"en minusculas       -> {completo.lower()}")
print(f"separado por guion  -> {completo.replace(' ', '-')}")   # los simbolos de ""
print(f"invertido           -> {completo[::-1]}")                # slice al reves