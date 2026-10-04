"""
Fuente de píxeles de Duck Hunt.

El juego usa una fuente de mapa de bits generada por
``tools/generate_assets.py``, en lugar de un TTF: así el aspecto es siempre el
mismo, el binario congelado no depende de las fuentes instaladas en el
sistema y el texto se escala sin suavizado (vecino más próximo), como en el
juego original.

Cada glifo se recorta del atlas y se amplía por entero. Como el color se
aplica después de ampliar, se puede reusar el mismo recorte para cualquier
color y cualquier tamaño, y el resultado siempre queda nítido.
"""

import json

import pygame

from ..assets import FONTS_DIR
from ..config import (
    FONT_ATLAS_FILE,
    FONT_METRICS_FILE,
)


class PixelFont:
    """
    Fuente de mapa de bits con la misma interfaz que ``pygame.font.Font``.

    Se usa así::

        font = PixelFont(scale=3)
        imagen = font.render("SCORE 001200", (255, 255, 255))
    """

    def __init__(self, scale=3):
        """
        Carga el atlas y prepara el recorte de cada glifo.

        Si el atlas no está disponible la instancia se marca como no
        disponible y ``render`` devuelve una superficie vacía; es lo que
        permite que el juego arranque aunque falten los recursos.
        """

        self.scale = max(1, int(scale))

        self.available = False

        self.cell_width = 6

        self.cell_height = 8

        self.glyphs = {}

        self._cache = {}

        self._load()

    # ======================================================================
    # Carga
    # ======================================================================

    def _load(self):
        """Lee el atlas y las métricas, y recorta cada glifo."""

        if not FONT_ATLAS_FILE.exists() or not FONT_METRICS_FILE.exists():

            return

        try:

            with open(FONT_METRICS_FILE, encoding="utf-8") as handle:

                metrics = json.load(handle)

            atlas = pygame.image.load(
                FONT_ATLAS_FILE
            ).convert_alpha()

        except (OSError, ValueError, pygame.error):

            return

        self.cell_width = metrics["cell_width"]

        self.cell_height = metrics["cell_height"]

        for character, position in metrics["glyphs"].items():

            left = position["column"] * self.cell_width

            top = position["row"] * self.cell_height

            if (
                left + self.cell_width > atlas.get_width()
                or top + self.cell_height > atlas.get_height()
            ):

                continue

            self.glyphs[character] = atlas.subsurface(
                pygame.Rect(
                    left,
                    top,
                    self.cell_width,
                    self.cell_height,
                )
            )

        self.available = bool(self.glyphs)

    # ======================================================================
    # Métricas
    # ======================================================================

    @property
    def height(self):
        """Alto en píxeles de una línea de texto."""

        return self.cell_height * self.scale

    @property
    def line_height(self):
        """Alto recomendado para separar dos líneas."""

        return (self.cell_height + 3) * self.scale

    def measure(self, text):
        """Devuelve el tamaño en píxeles que ocuparía ``text``."""

        return (
            len(text) * self.cell_width * self.scale,
            self.cell_height * self.scale,
        )

    # ======================================================================
    # Render
    # ======================================================================

    def _colored_glyph(self, character, color):
        """
        Devuelve el glifo ampliado y coloreado, cacheado por carácter, color
        y tamaño.
        """

        key = (character, tuple(color), self.scale)

        cached = self._cache.get(key)

        if cached is not None:

            return cached

        source = self.glyphs.get(character) or self.glyphs.get("?")

        if source is None:

            return None

        size = (
            self.cell_width * self.scale,
            self.cell_height * self.scale,
        )

        # ``scale`` usa vecino más próximo: mantiene los píxeles duros.
        scaled = pygame.transform.scale(
            source,
            size,
        )

        # Se parte de una superficie opaca del color pedido y se multiplica
        # por la máscara del atlas. Así el RGB queda teñido y el alfa conserva
        # la forma del glifo; con BLEND_RGBA_ADD el texto saldría siempre
        # blanco.
        colored = pygame.Surface(size, pygame.SRCALPHA)

        colored.fill(
            (
                color[0],
                color[1],
                color[2],
                255,
            )
        )

        colored.blit(
            scaled,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT,
        )

        self._cache[key] = colored

        return colored

    def render(self, text, color=(255, 255, 255)):
        """Convierte ``text`` en una superficie lista para blitear."""

        text = text.upper()

        width, height = self.measure(text)

        surface = pygame.Surface(
            (max(1, width), max(1, height)),
            pygame.SRCALPHA,
        )

        if not self.available:

            return surface

        advance = self.cell_width * self.scale

        for index, character in enumerate(text):

            glyph = self._colored_glyph(character, color)

            if glyph is None:

                continue

            surface.blit(
                glyph,
                (
                    index * advance,
                    0,
                ),
            )

        return surface

    def render_shadowed(
        self,
        text,
        color=(255, 255, 255),
        shadow=(0, 0, 0),
        offset=2,
    ):
        """
        Igual que ``render`` pero con la sombra dura típica de los arcades.

        Se pinta primero la copia desplazada y encima el texto, en un solo
        blit para no crear dos superficies por fotograma.
        """

        text = text.upper()

        width, height = self.measure(text)

        offset = max(0, int(offset))

        surface = pygame.Surface(
            (width + offset, height + offset),
            pygame.SRCALPHA,
        )

        if not self.available:

            return surface

        advance = self.cell_width * self.scale

        for index, character in enumerate(text):

            x = index * advance

            shadow_glyph = self._colored_glyph(character, shadow)

            if shadow_glyph is not None:

                surface.blit(
                    shadow_glyph,
                    (x + offset, offset),
                )

            glyph = self._colored_glyph(character, color)

            if glyph is not None:

                surface.blit(
                    glyph,
                    (x, 0),
                )

        return surface