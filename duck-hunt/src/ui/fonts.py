"""
Selección de fuente de Duck Hunt.

El juego prefiere siempre su fuente de píxeles. Si el atlas no estuviera
disponible (una instalación incompleta, por ejemplo), se recurre a la fuente
por defecto de Pygame con una escala aproximada, para que la interfaz siga
siendo legible en lugar de romperse.
"""

import pygame

from ..config import (
    FONT_SCALE_HUGE,
    FONT_SCALE_LARGE,
    FONT_SCALE_MEDIUM,
    FONT_SCALE_SMALL,
)

from .pixel_font import PixelFont


class ScaledFont:
    """
    Adaptador de ``pygame.font.Font`` a la misma interfaz que ``PixelFont``.

    Existe para que el HUD y las pantallas no tengan que saber con qué fuente
    se están dibujando: ambos llaman a ``render`` esperando una superficie.
    """

    def __init__(self, size):
        """Crea la fuente de sistema al tamaño ``size`` en píxeles."""

        self.size = size

        self._font = pygame.font.Font(None, size)

        self.scale = max(1, round(size / 12))

        self.available = True

    @property
    def height(self):
        return self._font.get_height()

    @property
    def line_height(self):
        return int(self.height * 1.3)

    def measure(self, text):
        """Devuelve el tamaño que ocuparía ``text``."""

        return self._font.size(text)

    def render(self, text, color=(255, 255, 255)):
        """Convierte ``text`` en una superficie, con antialias."""

        return self._font.render(
            text,
            True,
            color,
        )

    def render_shadowed(
        self,
        text,
        color=(255, 255, 255),
        shadow=(0, 0, 0),
        offset=2,
    ):
        """Dibuja el texto con una sombra desplazada."""

        main = self.render(text, color)

        behind = self.render(text, shadow)

        surface = pygame.Surface(
            (
                main.get_width() + offset,
                main.get_height() + offset,
            ),
            pygame.SRCALPHA,
        )

        surface.blit(behind, (offset, offset))

        surface.blit(main, (0, 0))

        return surface


_CACHE = {}

_PIXEL_FONT_READY = None


def pixel_fonts_available():
    """Comprueba una sola vez si el atlas de la fuente está disponible."""

    global _PIXEL_FONT_READY

    if _PIXEL_FONT_READY is None:

        _PIXEL_FONT_READY = PixelFont(scale=1).available

    return _PIXEL_FONT_READY


def load_font(size):
    """
    Devuelve la fuente para un tamaño lógico dado.

    ``size`` es una de las constantes ``FONT_SCALE_*`` de la configuración.
    El resultado se cachea porque construir la fuente recorta todos los
    glifos del atlas.
    """

    cached = _CACHE.get(size)

    if cached is not None:

        return cached

    if pixel_fonts_available():

        font = PixelFont(scale=size)

    else:

        # 8 px de alto por unidad de escala, más un margen razonable.
        font = ScaledFont(size * 12)

    _CACHE[size] = font

    return font


def small_font():
    """Texto de apoyo: instrucciones y etiquetas."""

    return load_font(FONT_SCALE_SMALL)


def medium_font():
    """Texto normal: puntuación, menús."""

    return load_font(FONT_SCALE_MEDIUM)


def large_font():
    """Títulos secundarios."""

    return load_font(FONT_SCALE_LARGE)


def huge_font():
    """Títulos principales."""

    return load_font(FONT_SCALE_HUGE)