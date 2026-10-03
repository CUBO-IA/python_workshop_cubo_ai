"""
Estados principales de Duck Hunt.
"""

from enum import Enum, auto


class GameState(Enum):
    """
    Estados posibles de la aplicación.
    """

    MENU = auto()

    PLAYING = auto()

    ROUND_COMPLETE = auto()

    GAME_OVER = auto()
