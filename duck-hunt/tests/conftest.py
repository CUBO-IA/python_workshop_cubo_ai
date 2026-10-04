"""
Configuración común de los tests.

Pygame necesita una ventana para convertir imágenes, así que los tests corren
con el controlador de vídeo ``dummy``: hay superficie, pero no se abre ninguna
ventana real ni se oye nada.
"""

import os
import sys

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent

# Las pruebas no deben escribir en el directorio del usuario ni usar el mixer.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

os.environ.setdefault("DUCK_HUNT_TEST", "1")

if str(ROOT) not in sys.path:

    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def pygame_module():
    """Inicializa Pygame una vez para toda la sesión de tests."""

    import pygame

    pygame.init()

    yield pygame

    pygame.quit()


@pytest.fixture
def surface(pygame_module):
    """Una superficie del tamaño de la ventana del juego."""

    from src.config import (
        WINDOW_HEIGHT,
        WINDOW_WIDTH,
    )

    pygame_module.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    return pygame_module.Surface(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )


@pytest.fixture
def screen(pygame_module, surface):
    """Alias de ``surface`` para los tests que dibujan la partida entera."""

    return surface


@pytest.fixture
def high_scores(tmp_path):
    """Un gestor de récords apuntando a un fichero temporal."""

    from src.high_scores import HighScores

    return HighScores(
        tmp_path / "high_scores.json"
    )


@pytest.fixture
def game(surface, high_scores):
    """Una partida nueva, sin sonido y con récords aislados."""

    from src.game import Game

    return Game(
        sound=None,
        high_scores=high_scores,
    )


@pytest.fixture
def duck(surface):
    """Un pato que entra por la izquierda, para tener una posición conocida."""

    from src.entities.duck import Duck

    return Duck(
        speed_multiplier=1.0,
        side=-1,
    )