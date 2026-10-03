"""
Punto de mira controlado por el mouse.
"""

import pygame

from ..config import (
    COLOR_BLACK,
    COLOR_WHITE,
    CROSSHAIR_FILE,
    CROSSHAIR_SIZE,
    IMAGES_DIR,
)


class Crosshair:
    """
    Representa el punto de mira del jugador.
    """

    def __init__(self):
        self.image = self._load_image()

        self.rect = self.image.get_rect()

    def _load_image(self):
        """
        Intenta cargar el punto de mira desde un PNG.

        Si no existe, crea uno mediante Pygame.
        """

        path = IMAGES_DIR / CROSSHAIR_FILE

        if path.exists():

            try:

                image = pygame.image.load(
                    path
                ).convert_alpha()

                return pygame.transform.smoothscale(
                    image,
                    (
                        CROSSHAIR_SIZE,
                        CROSSHAIR_SIZE,
                    ),
                )

            except pygame.error:
                pass

        return self._create_fallback()

    def _create_fallback(self):
        """
        Genera un punto de mira temporal.
        """

        size = CROSSHAIR_SIZE

        surface = pygame.Surface(
            (size, size),
            pygame.SRCALPHA,
        )

        center = size // 2

        color = COLOR_WHITE
        shadow = COLOR_BLACK

        line_width = 2
        shadow_width = 4

        # --------------------------------------------------------------
        # Sombra negra
        # --------------------------------------------------------------

        pygame.draw.line(
            surface,
            shadow,
            (center, 3),
            (center, size - 3),
            shadow_width,
        )

        pygame.draw.line(
            surface,
            shadow,
            (3, center),
            (size - 3, center),
            shadow_width,
        )

        pygame.draw.circle(
            surface,
            shadow,
            (center, center),
            10,
            shadow_width,
        )

        # --------------------------------------------------------------
        # Líneas blancas
        # --------------------------------------------------------------

        pygame.draw.line(
            surface,
            color,
            (center, 3),
            (center, size - 3),
            line_width,
        )

        pygame.draw.line(
            surface,
            color,
            (3, center),
            (size - 3, center),
            line_width,
        )

        pygame.draw.circle(
            surface,
            color,
            (center, center),
            10,
            line_width,
        )

        return surface

    def update(self):
        """
        Actualiza la posición del punto de mira según el mouse.
        """

        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.rect.center = (
            mouse_x,
            mouse_y,
        )

    def draw(self, surface):
        """
        Dibuja el punto de mira.
        """

        surface.blit(
            self.image,
            self.rect,
        )
