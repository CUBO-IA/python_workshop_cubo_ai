"""
Pantallas de Duck Hunt.
"""

import pygame

from ..config import (
    COLOR_BLACK,
    COLOR_MENU_BACKGROUND,
    COLOR_MENU_SELECTED,
    COLOR_MENU_TEXT,
    COLOR_MENU_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class ScreenRenderer:
    """
    Renderiza las pantallas que no pertenecen directamente
    al gameplay.
    """

    def __init__(self):

        self.title_font = pygame.font.Font(
            None,
            72,
        )

        self.large_font = pygame.font.Font(
            None,
            48,
        )

        self.font = pygame.font.Font(
            None,
            32,
        )

        self.small_font = pygame.font.Font(
            None,
            24,
        )

    # ======================================================================
    # Fondo
    # ======================================================================

    def draw_background(
        self,
        surface,
    ):

        surface.fill(
            COLOR_MENU_BACKGROUND
        )

    # ======================================================================
    # Menú
    # ======================================================================

    def draw_menu(
        self,
        surface,
        selected_option=0,
    ):

        self.draw_background(
            surface
        )

        # --------------------------------------------------------------
        # Título
        # --------------------------------------------------------------

        self._center_text(
            surface,
            "DUCK HUNT",
            self.title_font,
            COLOR_MENU_TITLE,
            150,
        )

        # --------------------------------------------------------------
        # Opciones
        # --------------------------------------------------------------

        options = [
            "JUGAR",
            "SALIR",
        ]

        start_y = 330

        for index, option in enumerate(
            options
        ):

            color = (
                COLOR_MENU_SELECTED
                if index == selected_option
                else COLOR_MENU_TEXT
            )

            prefix = (
                "> "
                if index == selected_option
                else "  "
            )

            self._center_text(
                surface,
                prefix + option,
                self.font,
                color,
                start_y
                + index * 60,
            )

        # --------------------------------------------------------------
        # Instrucciones
        # --------------------------------------------------------------

        self._center_text(
            surface,
            "↑ ↓ para seleccionar",
            self.small_font,
            COLOR_MENU_TEXT,
            550,
        )

        self._center_text(
            surface,
            "ENTER para confirmar",
            self.small_font,
            COLOR_MENU_TEXT,
            585,
        )

    # ======================================================================
    # Ronda completada
    # ======================================================================

    def draw_round_complete(
        self,
        surface,
        round_number,
        score,
        ducks_hit,
    ):

        self.draw_background(
            surface
        )

        self._center_text(
            surface,
            "RONDA COMPLETADA",
            self.large_font,
            COLOR_MENU_TITLE,
            170,
        )

        self._center_text(
            surface,
            f"RONDA {round_number}",
            self.font,
            COLOR_MENU_TEXT,
            270,
        )

        self._center_text(
            surface,
            f"PATOS: {ducks_hit}",
            self.font,
            COLOR_MENU_TEXT,
            320,
        )

        self._center_text(
            surface,
            f"SCORE: {score:06d}",
            self.font,
            COLOR_MENU_TEXT,
            370,
        )

        self._center_text(
            surface,
            "ENTER - SIGUIENTE RONDA",
            self.small_font,
            COLOR_MENU_SELECTED,
            500,
        )

    # ======================================================================
    # Game over
    # ======================================================================

    def draw_game_over(
        self,
        surface,
        score,
        round_number,
    ):

        self.draw_background(
            surface
        )

        self._center_text(
            surface,
            "GAME OVER",
            self.title_font,
            (220, 70, 70),
            170,
        )

        self._center_text(
            surface,
            f"SCORE FINAL: {score:06d}",
            self.font,
            COLOR_MENU_TEXT,
            300,
        )

        self._center_text(
            surface,
            f"RONDA: {round_number}",
            self.font,
            COLOR_MENU_TEXT,
            350,
        )

        self._center_text(
            surface,
            "ENTER - VOLVER A JUGAR",
            self.small_font,
            COLOR_MENU_SELECTED,
            500,
        )

        self._center_text(
            surface,
            "ESC - SALIR",
            self.small_font,
            COLOR_MENU_TEXT,
            540,
        )

    # ======================================================================
    # Utilidades
    # ======================================================================

    def _center_text(
        self,
        surface,
        text,
        font,
        color,
        y,
    ):

        image = font.render(
            text,
            True,
            color,
        )

        rect = image.get_rect()

        rect.centerx = (
            WINDOW_WIDTH // 2
        )

        rect.centery = y

        surface.blit(
            image,
            rect,
        )
