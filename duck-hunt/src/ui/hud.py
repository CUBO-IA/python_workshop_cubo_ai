"""
HUD del juego.

Muestra información de la partida.
"""

import pygame

from ..config import (
    COLOR_HUD_BACKGROUND,
    COLOR_HUD_TEXT,
    WINDOW_WIDTH,
)


class HUD:
    """
    Interfaz de información del jugador.
    """

    def __init__(self):

        self.font = pygame.font.Font(
            None,
            26,
        )

        self.small_font = pygame.font.Font(
            None,
            21,
        )

    def draw(
        self,
        surface,
        score,
        round_number,
        bullets,
        ducks_hit,
        ducks_total,
    ):

        self._draw_background(
            surface
        )

        self._draw_text(
            surface,
            f"ROUND {round_number}",
            20,
            12,
            self.font,
        )

        self._draw_text(
            surface,
            f"SCORE {score:06d}",
            20,
            44,
            self.font,
        )

        self._draw_bullets(
            surface,
            bullets,
        )

        self._draw_ducks(
            surface,
            ducks_hit,
            ducks_total,
        )

    def _draw_background(
        self,
        surface,
    ):

        pygame.draw.rect(
            surface,
            COLOR_HUD_BACKGROUND,
            (
                0,
                0,
                WINDOW_WIDTH,
                82,
            ),
        )

    def _draw_text(
        self,
        surface,
        text,
        x,
        y,
        font,
    ):

        image = font.render(
            text,
            True,
            COLOR_HUD_TEXT,
        )

        surface.blit(
            image,
            (
                x,
                y,
            ),
        )

    def _draw_bullets(
        self,
        surface,
        bullets,
    ):

        x = 470
        y = 32

        label = self.small_font.render(
            "BALAS",
            True,
            COLOR_HUD_TEXT,
        )

        surface.blit(
            label,
            (
                x,
                y - 8,
            ),
        )

        start_x = x + 85

        for index in range(3):

            bullet_x = (
                start_x
                + index * 38
            )

            if index < bullets:

                color = (
                    255,
                    220,
                    70,
                )

            else:

                color = (
                    80,
                    80,
                    80,
                )

            pygame.draw.circle(
                surface,
                color,
                (
                    bullet_x,
                    y + 8,
                ),
                9,
            )

    def _draw_ducks(
        self,
        surface,
        ducks_hit,
        ducks_total,
    ):

        text = self.small_font.render(
            f"PATOS {ducks_hit}/{ducks_total}",
            True,
            COLOR_HUD_TEXT,
        )

        rect = text.get_rect()

        rect.right = (
            WINDOW_WIDTH - 20
        )

        rect.centery = 30

        surface.blit(
            text,
            rect,
        )
