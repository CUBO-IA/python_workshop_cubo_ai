"""
Destello de disparo.

En el Duck Hunt de NES la animación del tiro dura un instante: la mira se
ensancha y se apaga enseguida. Aquí es el mismo efecto, un círculo que se
abre y se desvanece en un puñado de fotogramas.
"""

import math

import pygame

from ..config import (
    COLOR_BLACK,
    COLOR_WHITE,
    SHOT_FLASH_TIME,
)


class ShotFlash:
    """
    Destello que aparece en la posición del disparo.

    No es una bala que viaje por la pantalla: el juego original no la tiene,
    el tiro se resuelve en el mismo fotograma en el que se hace clic.
    """

    def __init__(self):
        self.active = False

        self.timer = 0.0

        self.x = 0

        self.y = 0

        self.radius = 0

    # ======================================================================
    # API
    # ======================================================================

    def trigger(self, position, radius=26):
        """Enciende el destello en ``position``."""

        self.active = True

        self.timer = 0.0

        self.x, self.y = position

        self.radius = radius

    def update(self, delta_time):
        """Avanza la cuenta atrás y apaga el destello al terminar."""

        if not self.active:

            return

        self.timer += delta_time

        if self.timer >= SHOT_FLASH_TIME:

            self.active = False

    # ======================================================================
    # Dibujo
    # ======================================================================

    def draw(self, surface):
        """Dibuja el destello si está activo."""

        if not self.active:

            return

        progress = min(1.0, self.timer / SHOT_FLASH_TIME)

        # El círculo crece mientras se apaga.
        radius = int(self.radius * (0.5 + 0.7 * progress))

        alpha = int(220 * (1.0 - progress))

        if alpha <= 2:

            return

        layer = pygame.Surface(
            (radius * 2, radius * 2),
            pygame.SRCALPHA,
        )

        pygame.draw.circle(
            layer,
            (COLOR_BLACK[0], COLOR_BLACK[1], COLOR_BLACK[2], alpha // 2),
            (radius, radius),
            radius,
            3,
        )

        pygame.draw.circle(
            layer,
            (COLOR_WHITE[0], COLOR_WHITE[1], COLOR_WHITE[2], alpha),
            (radius, radius),
            max(1, radius - 3),
            2,
        )

        # Cuatro brazos en cruz, como el fogonazo de un arma.
        arm = int(radius * 0.7)

        for index in range(4):

            angle = index * math.pi / 2

            x0 = radius + math.cos(angle) * radius * 0.3

            y0 = radius + math.sin(angle) * radius * 0.3

            x1 = radius + math.cos(angle) * arm

            y1 = radius + math.sin(angle) * arm

            pygame.draw.line(
                layer,
                (COLOR_WHITE[0], COLOR_WHITE[1], COLOR_WHITE[2], alpha),
                (x0, y0),
                (x1, y1),
                2,
            )

        surface.blit(
            layer,
            (int(self.x) - radius, int(self.y) - radius),
        )