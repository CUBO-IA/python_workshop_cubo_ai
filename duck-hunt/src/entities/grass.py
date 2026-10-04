"""
Matorral del escenario.

Se dibuja **después** de los patos, de forma que estos pasan por detrás y
desaparecen a medias, igual que en el Duck Hunt original. El matorral es la
razón por la que un pato que entra desde abajo no es visible hasta que ya ha
subido lo suficiente.
"""

import pygame

from ..config import (
    BUSH_HEIGHT,
    BUSH_WIDTH,
    BUSH_X,
    BUSH_Y,
    COLOR_BLACK,
)


class Grass:
    """Matorral central que oculta a los patos."""

    def __init__(self):
        self.width = BUSH_WIDTH

        self.height = BUSH_HEIGHT

        self.x = BUSH_X

        self.y = BUSH_Y

        self._surface = None

    # ======================================================================
    # Dibujo
    # ======================================================================

    def _build_surface(self):
        """
        Construye el matorral con código.

        Se dibuja una sola vez y se reutiliza: son unos pocos círculos y el
        juego llama a ``draw`` en cada fotograma.
        """

        surface = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA,
        )

        dark = (44, 110, 40)

        mid = (62, 142, 52)

        light = (86, 172, 66)

        # Silueta general: un grupo de lóbulos que arrancan del suelo.
        lobes = (
            (0.12, 0.72, 0.26),
            (0.30, 0.52, 0.30),
            (0.50, 0.40, 0.34),
            (0.70, 0.54, 0.30),
            (0.88, 0.74, 0.24),
        )

        for ratio_x, ratio_y, ratio_r in lobes:

            pygame.draw.circle(
                surface,
                mid,
                (
                    int(self.width * ratio_x),
                    int(self.height * ratio_y),
                ),
                int(self.width * ratio_r * 0.5),
            )

        # Base, para cerrar la figura contra el borde inferior.
        pygame.draw.rect(
            surface,
            mid,
            (0, int(self.height * 0.75), self.width, int(self.height * 0.25)),
        )

        # Luz en la parte alta y sombra en la baja.
        for ratio_x, ratio_y, ratio_r in (
            (0.32, 0.42, 0.20),
            (0.56, 0.32, 0.22),
            (0.72, 0.46, 0.18),
        ):

            pygame.draw.circle(
                surface,
                light,
                (
                    int(self.width * ratio_x),
                    int(self.height * ratio_y),
                ),
                int(self.width * ratio_r * 0.5),
            )

        for ratio_x, ratio_y, ratio_r in (
            (0.18, 0.86, 0.18),
            (0.44, 0.90, 0.20),
            (0.84, 0.88, 0.17),
        ):

            pygame.draw.circle(
                surface,
                dark,
                (
                    int(self.width * ratio_x),
                    int(self.height * ratio_y),
                ),
                int(self.width * ratio_r * 0.5),
            )

        # Briznas que sobresalen por arriba, para que la silueta no quede
        # demasiado regular.
        tip_x = self.width * 0.5

        for offset in range(-7, 8):

            height = self.height * (0.30 - abs(offset) * 0.022)

            pygame.draw.line(
                surface,
                dark,
                (tip_x + offset * self.width * 0.045, self.height * 0.42),
                (
                    tip_x + offset * self.width * 0.060,
                    self.height * 0.42 - height,
                ),
                3,
            )

        # Una sombra muy suave en la base para asentar el matorral.
        pygame.draw.line(
            surface,
            (0, 0, 0, 40),
            (0, self.height - 3),
            (self.width, self.height - 3),
            3,
        )

        return surface

    def draw(self, surface):
        """Dibuja el matorral por delante de los patos."""

        if self._surface is None:

            self._surface = self._build_surface()

        surface.blit(
            self._surface,
            (self.x, self.y),
        )