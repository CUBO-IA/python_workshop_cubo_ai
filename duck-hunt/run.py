#!/usr/bin/env python3
"""
Punto de entrada de Duck Hunt.

Si pygame no es importable desde el intérprete actual, este script se
re-ejecuta con el intérprete del entorno virtual del proyecto (``.venv``),
que es el que tiene las wheels instaladas. Así ``python3 run.py`` funciona
aunque el Python del sistema sea demasiado nuevo para una wheel de pygame.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(ROOT, ".venv", "bin", "python")


def _reexec_in_venv():
    """Relanza este script con .venv/bin/python. Devuelve su código de salida."""
    if not os.path.isfile(VENV_PYTHON):
        print(f"Error: pygame no está instalado y no se encontró el entorno virtual en {VENV_PYTHON}.")
        print("Créalo con:  uv venv --python 3.13 .venv && uv pip install -r requirements.txt")
        return 1

    env = dict(os.environ)
    # Evita un bucle de relanzamiento infinito si el intérprete del venv
    # ya es el actual.
    env["DUCK_HUNT_NO_REEXEC"] = "1"
    return subprocess.call([VENV_PYTHON, os.path.abspath(__file__)], env=env)


def main():
    if not os.environ.get("DUCK_HUNT_NO_REEXEC"):
        try:
            import pygame  # noqa: F401
        except ModuleNotFoundError:
            return _reexec_in_venv()

    from src.app import Application

    app = Application()

    app.run()


if __name__ == "__main__":
    sys.exit(main())
