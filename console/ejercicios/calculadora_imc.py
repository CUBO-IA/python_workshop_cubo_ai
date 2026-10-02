"""
CALCULADORA DE IMC (Índice de Masa Corporal)
============================================

Objetivo
--------
Calcular el estado nutricional de una persona a partir de su peso y su
estatura, siguiendo los pasos de cualquier programa: pedir datos, validarlos,
calcular, clasificar y mostrar el resultado.

Qué es el IMC
-------------
El IMC relaciona el peso con la estatura y NO tiene unidades (kg / m² da
adimensional). Solo sirve para clasificar, no para diagnosticar:

    IMC = peso (kg) / estatura² (m)

    Ejemplo: 154 libras y 1,75 m  ->  69.85 kg / (1.75 ** 2) = 22.80  -> Normal

Unidades: este script pide el peso en LIBRAS y convierte a kilogramos por
dentro, porque la fórmula del IMC está definida en kg. La conversión se hace
en una sola línea (ver `LIBRAS_A_KILOS`):

    1 libra = 0.45359237 kg    ->    peso_kg = peso_libras * 0.45359237

Clasificación (rangos estándar de la OMS)
------------------------------------------
    IMC menor a 18.5 ............... Bajo peso
    de 18.5 hasta 24.9 ............. Peso normal
    de 25.0 hasta 29.9 ............. Sobrepeso
    de 30.0 en adelante ............. Obesidad mórbida

Qué se practica en este script
------------------------------
  1. `input()`  -> leer texto del teclado.
  2. `int()` y `float()` -> convertir texto ("154") a número (154 o 154.0).
  3. Una conversión de unidades: libras -> kilogramos.
  4. `**`      -> el operador de potencia (elevar al cuadrado).
  5. `if / elif / else` -> elegir una única ruta según el valor del IMC.

Nota importante: el IMC no tiene en cuenta la edad, el sexo ni la masa
muscular. En niños, adolescentes, deportistas y adultos mayores los rangos
son distintos. Es una herramienta orientativa, no médica.

Cómo ejecutarlo
---------------
    python3 calculadora_imc.py

Ver la guía completa al final de este archivo.
"""


# ===========================================================================
# 0. DATO FIJO: LA CONSTANTE DE CONVERSIÓN
# ===========================================================================
# 1 libra (lb) equivale a 0.45359237 kilogramos. Es un dato que nunca cambia,
# así que se guarda en una CONSTANTE: un nombre en mayúsculas que deja claro
# que no es una variable cualquiera. Centralizarlo aquí evita repetir el
# número mágico 0.45359237 por todo el programa, y permite cambiarlo en un
# solo sitio si hiciera falta.

LIBRAS_A_KILOS = 0.45359237


# ===========================================================================
# 1. FUNCIONES AUXILIARES
# ===========================================================================
# Antes de escribir el programa principal, definimos pequeñas funciones que
# hacen una sola cosa. Así el flujo principal queda limpio y legible, y el
# programa no se rompe si el usuario escribe algo que no es un número.

def pedir_texto(prompt):
    """Lee un texto. Devuelve '' si el usuario solo pulsa Enter sin escribir."""
    return input(prompt).strip()


def pedir_entero(prompt, mensaje_error):
    """
    Lee un número ENTERO y vuelve a preguntar si no es válido.

    `int()` lanza ValueError si el texto no es un entero (por ejemplo "abc"
    o "20,5"). `try/except` atrapa ese error en lugar de romper el programa.
    Un bucle `while True` repite la pregunta hasta obtener una respuesta
    buena; el `break` es lo que termina el bucle.
    """
    while True:                      # repetir hasta que el dato sea correcto
        try:
            return int(input(prompt))
        except ValueError:
            # Se ejecuta solo si int() falló. `as e` guarda el mensaje del error.
            print(mensaje_error)


def pedir_decimal(prompt, mensaje_error, minimo):
    """
    Lee un número DECIMAL (float) mayor o igual que `minimo`.

    Mismo esquema que pedir_entero, pero además exigimos un valor mínimo
    razonable. Esto evita el error clásico de dividir entre cero: si la
    estatura fuera 0, la fórmula lanzaría ZeroDivisionError.
    """
    while True:
        try:
            valor = float(input(prompt))          # float() acepta "70.5"
            if valor < minimo:
                # El usuario escribió un número, pero no sirve. Se avisa y
                # el `continue` vuelve al inicio del bucle (otra vuelta).
                print(f"  El valor debe ser mayor o igual que {minimo}.")
                continue
            return valor
        except ValueError:
            print(mensaje_error)


def clasificar_imc(imc):
    """
    Devuelve la categoría del IMC usando if / elif / else.

    Reglas de la cadena:
      - `if`     -> la primera condición se evalúa; si es True, se ejecuta
                   su bloque y se SALTAN el resto.
      - `elif`   -> condiciones alternativas; solo se comprueban si la
                   anterior fue False.
      - `else`   -> se ejecuta cuando ninguna condición anterior se cumplió.
    El orden importa: se compara de menor a mayor y en cuanto un rango
    coincide, ya no se siguen evaluando los demás. Por eso el "de 18.5 a
    24.9" se escribe como `imc < 25` -- ya sabemos que es >= 18.5.
    """
    if imc < 18.5:
        categoria = "Bajo peso"
    elif imc < 25:
        categoria = "Peso normal"
    elif imc < 30:
        categoria = "Sobrepeso"
    else:
        # Si ninguna de las anteriores se cumplió, el IMC es >= 30.
        categoria = "Obesidad mórbida"

    return categoria


def recomendaciones(categoria):
    """Devuelve una sugerencia de salud según la categoría obtenida."""
    if categoria == "Bajo peso":
        return "Consulta con un especialista para un aumento de peso adecuado."
    elif categoria == "Peso normal":
        return "Mantén una alimentación equilibrada y actividad física regular."
    elif categoria == "Sobrepeso":
        return "Considera ajustar la dieta y aumentar la actividad física."
    else:
        return "Consulta con un médico: el IMC requiere seguimiento profesional."


# ===========================================================================
# 2. PROGRAMA PRINCIPAL
# ===========================================================================

print("=" * 52)
print("  CALCULADORA DE IMC (Índice de Masa Corporal)")
print("=" * 52)

# --- 2.1. Captura de datos -------------------------------------------------
# Cada `input()` pide un dato y lo devuelve como texto (str). Por eso hay que
# convertirlo: la edad con `int()` y el peso y la estatura con `float()`,
# que aceptan decimales con punto ("1.75").
# El peso se pide en LIBRAS, las unidades que usa quien escribe el programa.

nombre = pedir_texto("Nombre: ")
edad = pedir_entero("Edad (años): ", "  Error: la edad debe ser un número entero. Inténtalo de nuevo.")
peso_libras = pedir_decimal("Peso (libras): ", "  Error: el peso debe ser un número. Inténtalo de nuevo.", minimo=1)
estatura = pedir_decimal("Estatura (m): ", "  Error: la estatura debe ser un número. Inténtalo de nuevo.", minimo=0.1)

# --- 2.2. Conversión de libras a kilogramos -------------------------------
# El usuario piensa en libras, pero la fórmula del IMC está definida en
# kilogramos. Aquí se hace la traducción: se MULTIPLICA por el factor, porque
# 1 libra son 0.45359237 kg (multiplicar por un factor < 1 reduce el valor).

peso_kg = peso_libras * LIBRAS_A_KILOS

# --- 2.3. Cálculo del IMC --------------------------------------------------
# El operador `**` es la potencia: `estatura ** 2` equivale a
# `estatura * estatura`. Paréntesis obligatorios, porque sin ellos Python
# dividiría por la estatura y solo dividiría el resultado entre 2.

imc = peso_kg / (estatura ** 2)

# --- 2.4. Clasificación ----------------------------------------------------
# Se le pasa el IMC a la función y ella devuelve el texto de la categoría.

categoria = clasificar_imc(imc)
consejo = recomendaciones(categoria)

# --- 2.5. Presentación del resultado ---------------------------------------
# Una f-string permite mezclar texto y variables en una sola línea.
# El especificador `:.2f` muestra el número con exactamente 2 decimales.

print("\n" + "=" * 52)
print("  RESUMEN")
print("=" * 52)
print(f"  Nombre    : {nombre}")
print(f"  Edad      : {edad} años")
print(f"  Peso      : {peso_libras:.1f} lb  ->  {peso_kg:.2f} kg")
print(f"  Estatura  : {estatura:.2f} m")
print("-" * 52)
print(f"  IMC       : {imc:.2f}   (calculado como {peso_kg:.2f} / {estatura:.2f}²)")
print(f"  Categoría : {categoria}")
print("-" * 52)
print(f"  Consejo   : {consejo}")
print("=" * 52)

# Aviso de seguridad: el IMC orienta, no reemplaza a un profesional de salud.
print("Recuerda: el IMC es una referencia general, no un diagnóstico médico.")


# ===========================================================================
# GUÍA PARA EJECUTARLO DESDE LA TERMINAL
# ===========================================================================
#
# 1. Ubícate en la carpeta que contiene el archivo. Puedes verificar dónde
#    estás con el comando `pwd` (muestra la ruta actual).
#
#        cd console/ejercicios
#
# 2. Comprueba que tienes Python 3 instalado:
#
#        python3 --version          # en Linux y macOS
#        py --version              # en Windows
#
#    Si el comando es `python` en vez de `python3`, úsalo así.
#
# 3. Ejecuta el script:
#
#        python3 calculadora_imc.py
#
# 4. Escribe los datos que te pida y presiona Enter después de cada uno.
#    Si escribes un valor inválido (por ejemplo "ochenta" en la edad), el
#    programa te avisa y vuelve a preguntar, sin romperse.
#
# 5. Para probarlo sin escribir nada a mano, puedes "alimentar" la entrada
#    desde otro comando (así se automatizan las pruebas). Ojo: el tercer dato
#    es el peso en LIBRAS, no en kilogramos.
#
#        printf "Ana\n30\n138\n1.68\n" | python3 calculadora_imc.py
#
# --- CÓMO FUNCIONA EL FLUJO, EN POCAS PALABRAS ------------------------------
#
#   nombre      = pedir_texto(...)     -> input()   -> devuelve str
#   edad        = pedir_entero(...)    -> input()   -> int()   -> devuelve int
#   peso_libras = pedir_decimal(...)   -> input()   -> float() -> devuelve float
#   estatura    = pedir_decimal(...)   -> input()   -> float() -> devuelve float
#   peso_kg     = peso_libras * LIBRAS_A_KILOS   -> float  (convierte unidades)
#   imc         = peso_kg / (estatura**2) -> float     -> devuelve float
#   categoria   = clasificar_imc(imc)   -> if/elif/else -> devuelve str
#
# La diferencia clave: `input()` SIEMPRE devuelve texto. Sin `int()` o
# `float()`, "138 / 1.68" sería una operación entre cadenas y fallaría.
#
# La conversión de unidades va siempre DESPUÉS de leer el dato y ANTES de
# aplicar la fórmula. Si se hiciera al revés (por ejemplo, convertir el IMC
# ya calculado), el resultado sería un valor sin sentido.