"""
HUD del juego.

Barra superior con la ronda y la puntuación, y esquina inferior izquierda con
los patos que quedan por aparecer y los disparos disponibles. El estilo
intenta parecerse al del original: fondo oscuro, texto con sombra dura y
elementos alineados a los bordes.
"""

import pygame

from ..config import (
    COLOR_HUD_BACKGROUND,
    COLOR_HUD_DIM,
    COLOR_HUD_GOLD,
    COLOR_HUD_TEXT,
    SHOTS_PER_DUCK,
    WINDOW_WIDTH,
)

from ..sprites import load_image

from .fonts import (
    medium_font,
    small_font,
)

from .text import draw_text


class HUD:
    """Interfaz de información del jugador."""

    # Altura de la barra superior.
    BAR_HEIGHT = 44

    def __init__(self):
        """
        Prepara las fuentes y el icono de pato.

        El icono se usa para los patos restantes; si no está, se dibuja un
        cuadrado, que es menos bonito pero no rompe nada.
        """

        self.font = medium_font()

        self.small_font = small_font()

        self.duck_icon = load_image("duck_icon.png", (18, 18))

    # ======================================================================
    # Dibujo
    # ======================================================================

    def draw(
        self,
        surface,
        round_number,
        score,
        shots_left,
        ducks_remaining,
    ):
        """Pinta la barra superior y la esquina de abajo."""

        self._draw_top_bar(
            surface,
            round_number,
            score,
        )

        self._draw_ducks(
            surface,
            ducks_remaining,
        )

        self._draw_shots(
            surface,
            shots_left,
        )

    def _draw_top_bar(
        self,
        surface,
        round_number,
        score,
    ):
        """Banda superior con la ronda a la izquierda y la puntuación a la derecha."""

        pygame.draw.rect(
            surface,
            COLOR_HUD_BACKGROUND,
            (0, 0, WINDOW_WIDTH, self.BAR_HEIGHT),
        )

        # Línea de separación, como el borde del marcador original.
        pygame.draw.line(
            surface,
            COLOR_HUD_GOLD,
            (0, self.BAR_HEIGHT - 2),
            (WINDOW_WIDTH, self.BAR_HEIGHT - 2),
            2,
        )

        draw_text(
            surface,
            f"RONDA {round_number}",
            (14, 8),
            COLOR_HUD_TEXT,
            font=self.font,
        )

        self._draw_right_text(
            surface,
            f"{score:06d}",
            14,
            COLOR_HUD_GOLD,
            self.font,
        )

    def _draw_right_text(
        self,
        surface,
        text,
        margin,
        color,
        font,
    ):
        """Etiqueta a la derecha con su valor en dorado, a su izquierda."""

        value = font.render(text, color)

        value_x = WINDOW_WIDTH - margin - value.get_width()

        surface.blit(value, (value_x, 12))

        label = self.small_font.render("PUNTOS", COLOR_HUD_DIM)

        surface.blit(
            label,
            (
                value_x - label.get_width() - 10,
                16,
            ),
        )

    def _draw_ducks(
        self,
        surface,
        ducks_remaining,
    ):
        """Iconos de pato abajo a la izquierda, con los que faltan apagados."""

        y = surface.get_height() - 30

        x = 16

        for index in range(10):

            if index < ducks_remaining:

                if self.duck_icon is not None:

                    surface.blit(
                        self.duck_icon,
                        (x, y),
                    )

                else:

                    pygame.draw.rect(
                        surface,
                        COLOR_HUD_GOLD,
                        (x, y + 4, 14, 14),
                    )

            else:

                pygame.draw.rect(
                    surface,
                    COLOR_HUD_DIM,
                    (x + 3, y + 7, 8, 8),
                )

            x += 22

    def _draw_shots(
        self,
        surface,
        shots_left,
    ):
        """Cápsulas de bala abajo a la derecha."""

        y = surface.get_height() - 26

        total = SHOTS_PER_DUCK

        for index in range(total):

            x = WINDOW_WIDTH - 20 - (total - index) * 26

            if index < shots_left:

                pygame.draw.rect(
                    surface,
                    COLOR_HUD_GOLD,
                    (x, y, 12, 20),
                )

                pygame.draw.rect(
                    surface,
                    COLOR_HUD_BACKGROUND,
                    (x + 3, y + 6, 6, 12),
                )

            else:

                pygame.draw.rect(
                    surface,
                    COLOR_HUD_DIM,
                    (x + 2, y + 2, 8, 16),
                    border_radius=2,
                )