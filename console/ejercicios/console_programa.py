# ---------------------------------------------------------------------------
# 1. Lectura de datos por consola
# ---------------------------------------------------------------------------
# `input()` muestra un texto (el "prompt") y espera a que el usuario escriba.
# Siempre devuelve un str, NUNCA un int. Comparar "18" < 18 seria un error
# (TypeError), asi que convertimos con `int(...)`.

nombre = input("Escribe tu nombre: ")
edad = int(input("Escribe tu edad: "))       # str -> int

mensaje = f"Mi nombre es {nombre}, y tengo {edad} años de edad."


