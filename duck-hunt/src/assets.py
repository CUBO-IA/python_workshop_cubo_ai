"""
Resolución de rutas de Duck Hunt.

El juego se ejecuta de dos maneras distintas y las rutas cambian:

- Desde el repositorio, con ``python run.py``.
- Desde el binario congelado por PyInstaller, donde todo vive dentro de un
  único fichero y los assets se extraen a un directorio temporal.

Este módulo decide cuál de los dos casos es el activo, de forma que ninguna
otra parte del juego tenga que saberlo.
"""

import os
import sys

from pathlib import Path


APP_SLUG = "duck-hunt"


def _frozen_root():
    """Directorio temporal donde PyInstaller extrae los datos empaquetados."""

    return getattr(sys, "_MEIPASS", None)


IS_FROZEN = _frozen_root() is not None


# ============================================================================
# Recursos de solo lectura (assets)
# ============================================================================

if IS_FROZEN:

    # Incluye assets/ dentro del bundle.
    RESOURCE_ROOT = Path(_frozen_root())

else:

    RESOURCE_ROOT = Path(__file__).resolve().parent.parent


PROJECT_ROOT = RESOURCE_ROOT


ASSETS_DIR = RESOURCE_ROOT / "assets"

IMAGES_DIR = ASSETS_DIR / "images"

SOUNDS_DIR = ASSETS_DIR / "sounds"

FONTS_DIR = ASSETS_DIR / "fonts"

ICONS_DIR = ASSETS_DIR / "icons"


# ============================================================================
# Datos de lectura y escritura
# ============================================================================

def _xdg_data_home():
    """``$XDG_DATA_HOME`` con el valor por defecto de la especificación."""

    configured = os.environ.get("XDG_DATA_HOME")

    if configured and os.path.isabs(configured):

        return Path(configured)

    home = os.environ.get("HOME") or os.path.expanduser("~")

    return Path(home) / ".local" / "share"


USER_DATA_DIR = _xdg_data_home() / APP_SLUG

# Los datos de solo lectura que viajan con el juego (atajos de escritorio,
# ficheros de ejemplo) viven en el propio recurso.
DATA_DIR = RESOURCE_ROOT / "data"

LEGACY_DATA_DIR = PROJECT_ROOT / "data"


def ensure_user_data_dir():
    """Crea el directorio de datos del usuario si hace falta."""

    try:

        USER_DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    except OSError:

        # Un sistema de ficheros de solo lectura no debe impedir jugar; el
        # juego sigue funcionando, solo sin récord persistente.
        return False

    return True


def find_readable(*candidates):
    """Devuelve el primer candidato existente, o ``None`` si ninguno lo está."""

    for candidate in candidates:

        if candidate is not None and Path(candidate).exists():

            return Path(candidate)

    return None