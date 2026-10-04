"""
Pantallas de Duck Hunt.

Menú, resumen de ronda y fin de partida. Las tres comparten el mismo fondo
azul y el mismo estilo de texto con sombra dura.
"""

import pygame

from ..config import (
    COLOR_GAME_OVER,
    COLOR_MENU_BACKGROUND,
    COLOR_MENU_SELECTED,
    COLOR_MENU_TEXT,
    COLOR_MENU_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)

from ..sprites import load_image

from .fonts import (
    huge_font,
    large_font,
    medium_font,
    small_font,
)

from .text import draw_text_centered


class ScreenRenderer:
    """Renderiza las pantallas que no pertenecen al gameplay."""

    def __init__(self):
        """Prepara fuentes y logo."""

        self.title_font = huge_font()

        self.large_font = large_font()

        self.font = medium_font()

        self.small_font = small_font()

        self.logo = load_image("logo.png")

    # ======================================================================
    # Fondo
    # ======================================================================

    def draw_background(self, surface):
        """Pinta el fondo azul plano de los menús."""

        surface.fill(COLOR_MENU_BACKGROUND)

    # ======================================================================
    # Menú
    # ======================================================================

    def draw_menu(
        self,
        surface,
        selected_index=0,
        high_scores=None,
        options=("JUGAR", "SALIR"),
    ):
        """Menú principal con el logo, las opciones y la tabla de récords."""

        self.draw_background(surface)

        center_x = WINDOW_WIDTH // 2

        if self.logo is not None:

            surface.blit(
                self.logo,
                self.logo.get_rect(
                    center=(
                        center_x,
                        150,
                    )
                ),
            )

        else:

            draw_text_centered(
                surface,
                "DUCK HUNT",
                150,
                COLOR_MENU_TITLE,
                font=self.title_font,
            )

        start_y = 330

        for index, option in enumerate(options):

            selected = index == selected_index

            color = (
                COLOR_MENU_SELECTED
                if selected
                else COLOR_MENU_TEXT
            )

            prefix = (
                "> "
                if selected
                else "  "
            )

            draw_text_centered(
                surface,
                prefix + option,
                start_y + index * 52,
                color,
                font=self.font,
            )

        self._draw_high_scores(
            surface,
            high_scores,
        )

        draw_text_centered(
            surface,
            "FLECHAS PARA ELEGIR   ENTER PARA EMPEZAR",
            WINDOW_HEIGHT - 46,
            COLOR_MENU_TEXT,
            font=self.small_font,
        )

        draw_text_centered(
            surface,
            "RATON PARA DISPARAR   ESC PARA VOLVER",
            WINDOW_HEIGHT - 20,
            (150, 165, 185),
            font=self.small_font,
        )

    def _draw_high_scores(
        self,
        surface,
        high_scores,
    ):
        """Tabla de los cinco mejores resultados."""

        entries = list(high_scores or [])[:5]

        if not entries:

            return

        draw_text_centered(
            surface,
            "MEJORES PUNTUACIONES",
            470,
            COLOR_MENU_TITLE,
            font=self.small_font,
        )

        for index, entry in enumerate(entries):

            draw_text_centered(
                surface,
                f"{index + 1}. {entry['score']:06d}",
                506 + index * 26,
                COLOR_MENU_TEXT,
                font=self.small_font,
            )

    # ======================================================================
    # Fin de ronda
    # ======================================================================

    def draw_round_complete(
        self,
        surface,
        round_number,
        score,
        ducks_hit,
        bonus=0,
    ):
        """Resumen de una ronda superada."""

        self.draw_background(surface)

        draw_text_centered(
            surface,
            "RONDA COMPLETADA",
            180,
            COLOR_MENU_TITLE,
            font=self.large_font,
        )

        draw_text_centered(
            surface,
            f"RONDA {round_number}   PATOS {ducks_hit}",
            270,
            COLOR_MENU_TEXT,
            font=self.font,
        )

        draw_text_centered(
            surface,
            f"PUNTOS {score:06d}",
            320,
            COLOR_MENU_TEXT,
            font=self.font,
        )

        if bonus:

            draw_text_centered(
                surface,
                f"TODOS ABATIDOS  +{bonus}",
                370,
                COLOR_MENU_SELECTED,
                font=self.font,
            )

        draw_text_centered(
            surface,
            "ENTER PARA LA SIGUIENTE RONDA",
            500,
            COLOR_MENU_SELECTED,
            font=self.small_font,
        )

    # ======================================================================
    # Game over
    # ======================================================================

    def draw_game_over(
        self,
        surface,
        score,
        round_number,
        bonus=0,
        high_scores=None,
    ):
        """Fin de partida con el resumen, el bonus y la posición en la tabla."""

        self.draw_background(surface)

        draw_text_centered(
            surface,
            "GAME OVER",
            170,
            COLOR_GAME_OVER,
            font=self.title_font,
        )

        draw_text_centered(
            surface,
            f"PUNTOS {score:06d}",
            280,
            COLOR_MENU_TEXT,
            font=self.large_font,
        )

        draw_text_centered(
            surface,
            f"LLEGASTE A LA RONDA {round_number}",
            330,
            COLOR_MENU_TEXT,
            font=self.font,
        )

        if bonus:

            draw_text_centered(
                surface,
                f"BONUS {bonus:06d}",
                380,
                COLOR_MENU_SELECTED,
                font=self.font,
            )

        self._draw_high_scores(
            surface,
            high_scores,
        )

        draw_text_centered(
            surface,
            "ENTER PARA JUGAR OTRA VEZ",
            WINDOW_HEIGHT - 76,
            COLOR_MENU_SELECTED,
            font=self.small_font,
        )

        draw_text_centered(
            surface,
            "ESC PARA VOLVER AL MENU",
            WINDOW_HEIGHT - 46,
            COLOR_MENU_TEXT,
            font=self.small_font,
        )