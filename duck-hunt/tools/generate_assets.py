#!/usr/bin/env python3
"""
Generador de recursos de Duck Hunt.

Crea todos los ficheros de ``assets/`` de forma determinista, sin descargar
nada y sin depender de herramientas de diseño: las imágenes se dibujan con
Pygame, la fuente de píxeles se compone a mano y los sonidos se sintetizan con
la biblioteca estándar.

El juego usa los ficheros resultantes en tiempo de ejecución; este script solo
hace falta cuando cambian los recursos. Es idempotente: volver a ejecutarlo
regenera exactamente los mismos ficheros.

Uso::

    python tools/generate_assets.py

"""

import math
import os
import random
import struct
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pygame  # noqa: E402  (necesita ROOT en sys.path)

IMAGES_DIR = os.path.join(ROOT, "assets", "images")

FONTS_DIR = os.path.join(ROOT, "assets", "fonts")

SOUNDS_DIR = os.path.join(ROOT, "assets", "sounds")

# Las imágenes se dibujan a 4x y se reducen con smoothscale, que es lo que da
# el aspecto suave sin tener que calcular antialiasing a mano.
SUPERSAMPLE = 4

SAMPLE_RATE = 22050

SEED = 20240607


# ============================================================================
# Utilidades de color y superficies
# ============================================================================


def rgba(hex_string, alpha=255):
    """Convierte ``"#rrggbb"`` en una tupla RGBA."""

    hex_string = hex_string.lstrip("#")

    return (
        int(hex_string[0:2], 16),
        int(hex_string[2:4], 16),
        int(hex_string[4:6], 16),
        alpha,
    )


def surface_at_scale(width, height):
    """Crea una superficie ``width`` x ``height`` escalada x4."""

    return pygame.Surface(
        (width * SUPERSAMPLE, height * SUPERSAMPLE),
        pygame.SRCALPHA,
    )


def finalize(scaled, width, height):
    """Reduce una superficie escalada a su tamaño final."""

    return pygame.transform.smoothscale(scaled, (width, height))


def save_image(surface, filename):
    """Guarda una superficie en ``assets/images``."""

    name = os.fspath(filename)

    path = os.path.join(IMAGES_DIR, name)

    pygame.image.save(surface, path)

    size = os.path.getsize(path)

    print(f"  {name:24s} {surface.get_width():4d}x{surface.get_height():<4d} {size:7d} bytes")


def ellipse(surface, color, rect):
    pygame.draw.ellipse(surface, color, _scale_rect(rect))


def circle(surface, color, center, radius):
    pygame.draw.circle(
        surface,
        color,
        (
            int(center[0] * SUPERSAMPLE),
            int(center[1] * SUPERSAMPLE),
        ),
        int(radius * SUPERSAMPLE),
    )


def polygon(surface, color, points):
    pygame.draw.polygon(
        surface,
        color,
        [
            (
                int(x * SUPERSAMPLE),
                int(y * SUPERSAMPLE),
            )
            for x, y in points
        ],
    )


def rect(surface, color, bounds):
    pygame.draw.rect(surface, color, _scale_rect(bounds))


def line(surface, color, start, end, width=1):
    pygame.draw.line(
        surface,
        color,
        (
            int(start[0] * SUPERSAMPLE),
            int(start[1] * SUPERSAMPLE),
        ),
        (
            int(end[0] * SUPERSAMPLE),
            int(end[1] * SUPERSAMPLE),
        ),
        max(1, int(width * SUPERSAMPLE)),
    )


def _scale_rect(bounds):
    return pygame.Rect(
        int(bounds[0] * SUPERSAMPLE),
        int(bounds[1] * SUPERSAMPLE),
        int(bounds[2] * SUPERSAMPLE),
        int(bounds[3] * SUPERSAMPLE),
    )


# ============================================================================
# Paleta
# ============================================================================

PALETTE = {
    "sky_top": rgba("#3f8fd0"),
    "sky_bottom": rgba("#a8dcf5"),
    "sun": rgba("#fff2a8"),
    "cloud": rgba("#ffffff"),
    "cloud_shadow": rgba("#d6e9f5"),
    "hill_far": rgba("#4f9a4a"),
    "hill_near": rgba("#3f8438"),
    "ground": rgba("#5faa3c"),
    "ground_dark": rgba("#4a8a2e"),
    "ground_light": rgba("#74c04c"),
    "trunk": rgba("#6b4423"),
    "leaf": rgba("#2f7d2a"),
    "leaf_light": rgba("#3f9c33"),
    "duck_body": rgba("#3f9c33"),
    "duck_body_light": rgba("#5cbb46"),
    "duck_belly": rgba("#f4f4ec"),
    "duck_beak": rgba("#f0a828"),
    "duck_eye": rgba("#101010"),
    "duck_eye_white": rgba("#ffffff"),
    "duck_dead": rgba("#6b6b5a"),
    "dog_body": rgba("#c08040"),
    "dog_body_light": rgba("#d9a05a"),
    "dog_belly": rgba("#f0e0c0"),
    "dog_ear": rgba("#96602a"),
    "dog_nose": rgba("#201818"),
    "dog_eye": rgba("#101010"),
    "crosshair": rgba("#ffffff"),
    "crosshair_shadow": rgba("#101018"),
    "grass": rgba("#3f8438"),
    "grass_light": rgba("#57a845"),
    "grass_dark": rgba("#2c6b28"),
}


# ============================================================================
# Patos
# ============================================================================


def _draw_duck_body(surface, width, height, body_color, belly_color):
    """Silueta base del pato, mirando a la derecha."""

    ellipse(surface, body_color, (width * 0.16, height * 0.30, width * 0.56, height * 0.42))
    ellipse(surface, belly_color, (width * 0.22, height * 0.46, width * 0.44, height * 0.22))
    circle(surface, body_color, (width * 0.76, height * 0.34), height * 0.22)


def _draw_duck_beak(surface, width, height, color):
    polygon(
        surface,
        color,
        [
            (width * 0.90, height * 0.32),
            (width * 1.00, height * 0.38),
            (width * 0.90, height * 0.44),
        ],
    )


def _draw_duck_eye(surface, width, height):
    circle(surface, PALETTE["duck_eye_white"], (width * 0.79, height * 0.27), height * 0.075)
    circle(surface, PALETTE["duck_eye"], (width * 0.80, height * 0.27), height * 0.035)


def _draw_duck_foot(surface, width, height, color, x):
    line(surface, color, (width * x, height * 0.70), (width * x, height * 0.84), width=0.06)
    line(surface, color, (width * x, height * 0.84), (width * (x + 0.10), height * 0.92), width=0.05)
    line(surface, color, (width * x, height * 0.84), (width * (x - 0.08), height * 0.92), width=0.05)


def make_duck_flap(frame, width, height):
    """Genera un fotograma del aleteo. ``frame`` va de 0 a 2."""

    surface = surface_at_scale(width, height)

    _draw_duck_body(surface, width, height, PALETTE["duck_body"], PALETTE["duck_belly"])
    _draw_duck_foot(surface, width, height, PALETTE["duck_beak"], 0.30)

    # Tres posiciones de ala: arriba, en medio y abajo.
    if frame == 0:
        wing = [
            (width * 0.30, height * 0.42),
            (width * 0.44, height * 0.06),
            (width * 0.62, height * 0.40),
        ]
    elif frame == 1:
        wing = [
            (width * 0.30, height * 0.44),
            (width * 0.48, height * 0.30),
            (width * 0.66, height * 0.42),
        ]
    else:
        wing = [
            (width * 0.30, height * 0.44),
            (width * 0.44, height * 0.74),
            (width * 0.62, height * 0.42),
        ]

    polygon(surface, PALETTE["duck_body_light"], wing)

    _draw_duck_beak(surface, width, height, PALETTE["duck_beak"])
    _draw_duck_eye(surface, width, height)

    return finalize(surface, width, height)


def make_duck_hit(width, height):
    """Pato alcanzado: se desploma con las alas recogidas."""

    surface = surface_at_scale(width, height)

    ellipse(surface, PALETTE["duck_dead"], (width * 0.16, height * 0.34, width * 0.56, height * 0.36))
    ellipse(surface, PALETTE["duck_belly"], (width * 0.22, height * 0.46, width * 0.42, height * 0.20))
    circle(surface, PALETTE["duck_dead"], (width * 0.74, height * 0.38), height * 0.20)

    # Alas recogidas hacia atrás.
    polygon(
        surface,
        rgba("#585845"),
        [
            (width * 0.28, height * 0.46),
            (width * 0.06, height * 0.30),
            (width * 0.16, height * 0.56),
        ],
    )

    _draw_duck_foot(surface, width, height, PALETTE["duck_beak"], 0.34)

    # Pico abierto y ojo en forma de X, la seña clásica de pato muerto.
    polygon(
        surface,
        PALETTE["duck_beak"],
        [
            (width * 0.88, height * 0.36),
            (width * 0.99, height * 0.40),
            (width * 0.88, height * 0.48),
        ],
    )
    line(surface, PALETTE["duck_eye"], (width * 0.72, height * 0.30), (width * 0.82, height * 0.40), width=0.05)
    line(surface, PALETTE["duck_eye"], (width * 0.82, height * 0.30), (width * 0.72, height * 0.40), width=0.05)

    return finalize(surface, width, height)


def make_duck_icon(size):
    """Icono pequeño de pato para el HUD."""

    surface = surface_at_scale(size, size)

    ellipse(surface, PALETTE["duck_body"], (size * 0.12, size * 0.36, size * 0.56, size * 0.38))
    ellipse(surface, PALETTE["duck_belly"], (size * 0.18, size * 0.50, size * 0.44, size * 0.20))
    circle(surface, PALETTE["duck_body"], (size * 0.74, size * 0.38), size * 0.20)
    polygon(
        surface,
        PALETTE["duck_beak"],
        [
            (size * 0.88, size * 0.36),
            (size * 1.00, size * 0.42),
            (size * 0.88, size * 0.48),
        ],
    )
    circle(surface, PALETTE["duck_eye"], (size * 0.78, size * 0.32), size * 0.05)

    return finalize(surface, size, size)


# ============================================================================
# Perro
# ============================================================================


def make_dog(pose, width, height):
    """Perro en una de las tres poses: idle, happy o laugh."""

    surface = surface_at_scale(width, height)

    body = PALETTE["dog_body"]

    if pose == "laugh":
        body = rgba("#a86c30")

    # ------------------------------------------------------------------
    # Cuerpo y patas traseras
    # ------------------------------------------------------------------

    ellipse(surface, body, (width * 0.20, height * 0.44, width * 0.62, height * 0.34))
    ellipse(surface, PALETTE["dog_belly"], (width * 0.30, height * 0.58, width * 0.42, height * 0.20))

    rect(surface, rgba("#8a5826"), (width * 0.26, height * 0.72, width * 0.14, height * 0.14))
    rect(surface, rgba("#8a5826"), (width * 0.62, height * 0.72, width * 0.14, height * 0.14))

    # ------------------------------------------------------------------
    # Cabeza
    # ------------------------------------------------------------------

    circle(surface, body, (width * 0.50, height * 0.34), height * 0.22)

    # Orejas caídas, según la pose.
    if pose == "laugh":
        ear_left = [
            (width * 0.34, height * 0.24),
            (width * 0.22, height * 0.16),
            (width * 0.30, height * 0.38),
        ]
        ear_right = [
            (width * 0.66, height * 0.24),
            (width * 0.78, height * 0.16),
            (width * 0.70, height * 0.38),
        ]
    else:
        ear_left = [
            (width * 0.34, height * 0.22),
            (width * 0.20, height * 0.30),
            (width * 0.32, height * 0.40),
        ]
        ear_right = [
            (width * 0.66, height * 0.22),
            (width * 0.80, height * 0.30),
            (width * 0.68, height * 0.40),
        ]

    polygon(surface, PALETTE["dog_ear"], ear_left)
    polygon(surface, PALETTE["dog_ear"], ear_right)

    # ------------------------------------------------------------------
    # Cara
    # ------------------------------------------------------------------

    ellipse(surface, PALETTE["dog_belly"], (width * 0.40, height * 0.40, width * 0.20, height * 0.14))

    if pose == "laugh":
        # Boca abierta grande y ojos cerrados: la risa.
        ellipse(surface, PALETTE["dog_nose"], (width * 0.44, height * 0.42, width * 0.12, height * 0.12))
        line(surface, PALETTE["dog_eye"], (width * 0.36, height * 0.28), (width * 0.46, height * 0.34), width=0.05)
        line(surface, PALETTE["dog_eye"], (width * 0.64, height * 0.28), (width * 0.54, height * 0.34), width=0.05)
    else:
        circle(surface, PALETTE["dog_eye"], (width * 0.42, height * 0.30), height * 0.045)
        circle(surface, PALETTE["dog_eye"], (width * 0.58, height * 0.30), height * 0.045)
        circle(surface, PALETTE["dog_nose"], (width * 0.50, height * 0.44), height * 0.055)

        if pose == "happy":
            # Boca sonriente.
            line(surface, PALETTE["dog_nose"], (width * 0.42, height * 0.50), (width * 0.58, height * 0.50), width=0.045)

    # ------------------------------------------------------------------
    # Cola
    # ------------------------------------------------------------------

    if pose == "happy":
        line(surface, PALETTE["dog_ear"], (width * 0.20, height * 0.48), (width * 0.08, height * 0.26), width=0.07)
    else:
        line(surface, PALETTE["dog_ear"], (width * 0.20, height * 0.48), (width * 0.08, height * 0.44), width=0.07)

    return finalize(surface, width, height)


# ============================================================================
# Escenario
# ============================================================================


def make_background(width, height, horizon_y):
    """Cielo, colinas, línea de árboles y franja de hierba."""

    surface = surface_at_scale(width, height)

    # ------------------------------------------------------------------
    # Cielo con degradado vertical
    # ------------------------------------------------------------------

    top = PALETTE["sky_top"]

    bottom = PALETTE["sky_bottom"]

    for y in range(int(horizon_y * SUPERSAMPLE)):
        t = y / max(1, horizon_y * SUPERSAMPLE)

        color = (
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
            255,
        )
        pygame.draw.line(surface, color, (0, y), (width * SUPERSAMPLE, y))

    circle(surface, PALETTE["sun"], (width * 0.82, height * 0.16), height * 0.07)

    # ------------------------------------------------------------------
    # Nubes
    # ------------------------------------------------------------------

    for cloud_x, cloud_y, scale in (
        (0.12, 0.14, 1.0),
        (0.42, 0.22, 0.8),
        (0.68, 0.12, 1.1),
        (0.88, 0.30, 0.7),
    ):
        _draw_cloud(
            surface,
            width * cloud_x,
            height * cloud_y,
            height * 0.05 * scale,
        )

    # ------------------------------------------------------------------
    # Colinas
    # ------------------------------------------------------------------

    polygon(
        surface,
        PALETTE["hill_far"],
        [
            (0, horizon_y),
            (width * 0.18, horizon_y - height * 0.10),
            (width * 0.38, horizon_y),
            (width * 0.62, horizon_y - height * 0.13),
            (width * 0.82, horizon_y),
            (width, horizon_y - height * 0.07),
            (width, horizon_y),
        ],
    )

    polygon(
        surface,
        PALETTE["hill_near"],
        [
            (0, horizon_y),
            (width * 0.26, horizon_y - height * 0.05),
            (width * 0.55, horizon_y),
            (width * 0.78, horizon_y - height * 0.06),
            (width, horizon_y),
        ],
    )

    # ------------------------------------------------------------------
    # Árboles del fondo
    # ------------------------------------------------------------------

    for tree_x in (0.06, 0.16, 0.24, 0.84, 0.92, 0.98):
        x = width * tree_x

        rect(surface, PALETTE["trunk"], (x - width * 0.006, horizon_y - height * 0.075, width * 0.012, height * 0.075))
        circle(surface, PALETTE["leaf"], (x, horizon_y - height * 0.105), height * 0.042)
        circle(surface, PALETTE["leaf_light"], (x - width * 0.012, horizon_y - height * 0.095), height * 0.028)

    # ------------------------------------------------------------------
    # Franja de hierba
    # ------------------------------------------------------------------

    rect(
        surface,
        PALETTE["ground"],
        (0, horizon_y, width, height - horizon_y),
    )

    rect(
        surface,
        PALETTE["ground_dark"],
        (0, horizon_y, width, height * 0.02),
    )

    # Franja clara de tierra, la "calle" donde aparece el perro.
    rect(
        surface,
        PALETTE["ground_light"],
        (0, height * 0.86, width, height * 0.14),
    )

    random.seed(SEED)

    # Briznas de hierba deterministas.
    for _ in range(int(width / 6)):
        x = random.uniform(0, width)

        y = random.uniform(horizon_y + 4, height)

        length = random.uniform(4, 9)

        line(
            surface,
            PALETTE["ground_dark"],
            (x, y),
            (x + random.uniform(-3, 3), y - length),
            width=1.5,
        )

    return finalize(surface, width, height)


def _draw_cloud(surface, center_x, center_y, radius):
    """Nube de tres círculos y una base, con sombra inferior."""

    circle(surface, PALETTE["cloud_shadow"], (center_x, center_y + radius * 0.35), radius)
    circle(surface, PALETTE["cloud"], (center_x - radius * 0.9, center_y), radius * 0.8)
    circle(surface, PALETTE["cloud"], (center_x, center_y - radius * 0.4), radius)
    circle(surface, PALETTE["cloud"], (center_x + radius * 0.9, center_y), radius * 0.8)
    rect(
        surface,
        PALETTE["cloud"],
        (center_x - radius * 1.7, center_y, radius * 3.4, radius * 0.8),
    )


def make_crosshair(size):
    """Mira de líneas cruzadas con halo oscuro para leerse sobre el cielo."""

    surface = surface_at_scale(size, size)

    center = size / 2

    arm = size * 0.38

    gap = size * 0.16

    ring_radius = size * 0.16

    def cross(color, thickness):
        line(surface, color, (center, center - arm), (center, center - gap), width=thickness)
        line(surface, color, (center, center + gap), (center, center + arm), width=thickness)
        line(surface, color, (center - arm, center), (center - gap, center), width=thickness)
        line(surface, color, (center + gap, center), (center + arm, center), width=thickness)

        pygame.draw.circle(
            surface,
            color,
            (int(center * SUPERSAMPLE), int(center * SUPERSAMPLE)),
            int(ring_radius * SUPERSAMPLE),
            int(thickness * SUPERSAMPLE),
        )

    cross(PALETTE["crosshair_shadow"], size * 0.055)
    cross(PALETTE["crosshair"], size * 0.028)

    return finalize(surface, size, size)


def make_logo(width, height):
    """Título del menú: ``DUCK HUNT`` con sombra dura."""

    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    font = pygame.font.Font(None, int(height * 0.92))

    top = font.render("DUCK", True, PALETTE["duck_beak"])

    bottom = font.render("HUNT", True, PALETTE["duck_beak"])

    shadow_font = pygame.font.Font(None, int(height * 0.92))

    shadow_top = shadow_font.render("DUCK", True, rgba("#3a2408"))

    shadow_bottom = shadow_font.render("HUNT", True, rgba("#3a2408"))

    gap = int(height * 0.04)

    total_width = max(top.get_width(), bottom.get_width())

    x = (width - total_width) // 2

    y_top = int(height * 0.06)

    y_bottom = y_top + top.get_height() - gap

    surface.blit(shadow_top, (x + 4, y_top + 4))

    surface.blit(shadow_bottom, (x + 4, y_bottom + 4))

    surface.blit(top, (x, y_top))

    surface.blit(bottom, (x, y_bottom))

    # Un pato pequeño sobre el título.
    duck = make_duck_icon(int(height * 0.34))

    surface.blit(duck, ((width - duck.get_width()) // 2, int(height * 0.80)))

    return surface


# ============================================================================
# Fuente de píxeles
# ============================================================================

# Cada glifo es 5x7. Las minúsculas se reutilizan en mayúscula, así que el HUD
# y los menús pueden escribirse en mayúsculas como en el juego original.
GLYPHS = {
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": ["..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."],
    ":": [".....", "..#..", "..#..", ".....", "..#..", "..#..", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
    "<": ["...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."],
    ">": [".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."],
    "%": ["##..#", "##.#.", "..#..", ".#...", "#.##.", "#.##.", "....."],
    "*": [".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."],
    "'": ["..#..", "..#..", ".....", ".....", ".....", ".....", "....."],
    "É": ["..#..", ".###.", "#....", "####.", "#....", "#....", "#####"],
    "Ó": [".#.#.", "#####", ".....", ".###.", "#...#", "#...#", ".###."],
    "Í": ["..#..", "#####", "..#..", "..#..", "..#..", "..#..", "#####"],
    "Ñ": ["#.#.#", ".###.", ".....", "#...#", "#####", "#...#", "#...#"],
    "·": [".....", ".....", ".....", ".##..", ".##..", ".....", "....."],
}

GLYPH_WIDTH = 5

GLYPH_HEIGHT = 7

GLYPH_SPACING = 1


def make_font_atlas():
    """
    Compone el atlas de la fuente de píxeles.

    Devuelve el atlas (una columna por carácter) y guarda un JSON con la
    posición de cada glifo, que es lo que lee ``src/ui/pixel_font.py``.
    """

    characters = sorted(GLYPHS.keys())

    cell_width = GLYPH_WIDTH + GLYPH_SPACING

    cell_height = GLYPH_HEIGHT + GLYPH_SPACING

    columns = 16

    rows = int(math.ceil(len(characters) / columns))

    white = (255, 255, 255, 255)

    # Lienzo x8: cada píxel del atlas es un bloque de 8x8, luego se reduce.
    block = 8

    atlas = pygame.Surface(
        (columns * cell_width * block, rows * cell_height * block),
        pygame.SRCALPHA,
    )

    for index, character in enumerate(characters):

        column = index % columns

        row = index // columns

        rows_of_pixels = GLYPHS[character]

        for y, row_pixels in enumerate(rows_of_pixels):

            for x, pixel in enumerate(row_pixels):

                if pixel != "#":
                    continue

                pygame.draw.rect(
                    atlas,
                    white,
                    (
                        (column * cell_width + x) * block,
                        (row * cell_height + y) * block,
                        block,
                        block,
                    ),
                )

    # El atlas se escribe píxel a píxel a partir del mapa de bits original en
    # lugar de reducir el lienzo grande: así ningún borde queda suavizado.
    final = pygame.Surface((columns * cell_width, rows * cell_height), pygame.SRCALPHA)

    final.fill((255, 255, 255, 0))

    for index, character in enumerate(characters):

        column = index % columns

        row = index // columns

        rows_of_pixels = GLYPHS[character]

        for y, row_pixels in enumerate(rows_of_pixels):

            for x, pixel in enumerate(row_pixels):

                if pixel != "#":
                    continue

                final.set_at(
                    (column * cell_width + x, row * cell_height + y),
                    (255, 255, 255, 255),
                )

    pygame.image.save(final, os.path.join(FONTS_DIR, "font_atlas.png"))

    import json

    metrics = {
        "glyph_width": GLYPH_WIDTH,
        "glyph_height": GLYPH_HEIGHT,
        "cell_width": cell_width,
        "cell_height": cell_height,
        "columns": columns,
        "rows": rows,
        "glyphs": {
            character: {
                "column": index % columns,
                "row": index // columns,
            }
            for index, character in enumerate(characters)
        },
    }

    with open(os.path.join(FONTS_DIR, "font_metrics.json"), "w", encoding="utf-8") as handle:

        json.dump(metrics, handle, indent=2, ensure_ascii=False)

    atlas_size = os.path.getsize(os.path.join(FONTS_DIR, "font_atlas.png"))

    print(f"  {'font_atlas.png':24s} {final.get_width():4d}x{final.get_height():<4d} {atlas_size:7d} bytes ({len(characters)} glifos)")

    print(f"  {'font_metrics.json':24s} {'':4s}  {'':4s} {os.path.getsize(os.path.join(FONTS_DIR, 'font_metrics.json')):7d} bytes")


# ============================================================================
# Síntesis de audio
# ============================================================================


def midi_to_frequency(note):
    """Frecuencia en Hz de una nota MIDI."""

    return 440.0 * (2.0 ** ((note - 69) / 12.0))


def square_wave(phase):
    """Onda cuadrada con el mismo rango que el resto de osciladores."""

    return 1.0 if (phase % 1.0) < 0.5 else -1.0


def triangle_wave(phase):
    position = phase % 1.0

    if position < 0.5:

        return 4.0 * position - 1.0

    return 3.0 - 4.0 * position


class Track:
    """Acumula muestras float en [-1, 1] y las escribe como WAV."""

    def __init__(self, duration, sample_rate=SAMPLE_RATE):

        self.sample_rate = sample_rate

        self.count = max(1, int(duration * sample_rate))

        self.samples = [0.0] * self.count

    def add(self, start, duration, generator, gain=1.0):
        """
        Mezcla una señal desde ``start`` durante ``duration`` segundos.

        ``generator`` recibe ``(t, i)`` con el tiempo en segundos y devuelve
        el valor de la muestra.
        """

        first = int(start * self.sample_rate)

        last = min(self.count, first + int(duration * self.sample_rate))

        for index in range(max(0, first), last):

            position = index - first

            self.samples[index] += (
                generator(position / self.sample_rate, position) * gain
            )

    def envelope(self, attack=0.005, release=0.25):
        """Aplica envolvente de ataque y caída exponencial."""

        attack_samples = max(1, int(attack * self.sample_rate))

        release_start = int(self.sample_rate * release)

        for index in range(self.count):

            value = self.samples[index]

            if index < attack_samples:

                value *= index / attack_samples

            remaining = self.count - index

            if remaining < release_start:

                value *= max(0.0, remaining / max(1, release_start)) ** 1.5

            self.samples[index] = max(-1.0, min(1.0, value))

        return self

    def save(self, filename):
        """Escribe el WAV de 16 bits mono."""

        path = os.path.join(SOUNDS_DIR, filename)

        with wave.open(path, "wb") as handle:

            handle.setnchannels(1)

            handle.setsampwidth(2)

            handle.setframerate(self.sample_rate)

            frames = bytearray()

            for value in self.samples:

                frames += struct.pack("<h", int(value * 30000))

            handle.writeframes(bytes(frames))

        print(f"  {filename:24s} {self.count / self.sample_rate:5.2f}s {os.path.getsize(path):7d} bytes")


def make_shot_sound():
    """Disparo: ruido seco y barrido descendente."""

    track = Track(0.16)

    track.add(0.0, 0.16, lambda t, i: square_wave(900.0 * (2.0 ** (-6.0 * t)) * t) * math.exp(-24.0 * t), 0.55)

    track.add(0.0, 0.04, lambda t, i: (random.uniform(-1, 1)) * math.exp(-90.0 * t), 0.45)

    return track.envelope(release=0.06)


def make_duck_hit_sound():
    """Impacto: golpe grave más un graznido."""

    track = Track(0.40)

    track.add(0.0, 0.12, lambda t, i: random.uniform(-1, 1) * math.exp(-26.0 * t), 0.40)

    track.add(0.0, 0.38, lambda t, i: square_wave(midi_to_frequency(64) * (1.0 + 0.25 * math.sin(t * 40.0)) * t) * math.exp(-5.0 * t), 0.35)

    track.add(0.0, 0.30, lambda t, i: square_wave(midi_to_frequency(71) * (1.0 - 0.30 * t) * t) * math.exp(-7.0 * t), 0.22)

    return track.envelope(release=0.12)


def make_duck_flap_sound():
    """Aleteo en bucle: cuatro golpes de aire filtrados."""

    track = Track(0.50)

    for flap in range(4):

        start = flap * 0.125

        track.add(
            start,
            0.09,
            lambda t, i: _lowpass(random.uniform(-1, 1)) * math.exp(-30.0 * t),
            0.30,
        )

    return track.envelope(attack=0.002, release=0.01)


def make_dog_laugh_sound():
    """Risa del perro: seis golpes de dos formantes."""

    track = Track(1.30)

    for burst in range(6):

        start = burst * 0.21

        track.add(
            start,
            0.18,
            lambda t, i: (
                square_wave(midi_to_frequency(60) * (1.0 - 0.15 * t) * t)
                + 0.6 * square_wave(midi_to_frequency(67) * (1.0 - 0.15 * t) * t)
            )
            * math.exp(-7.0 * t),
            0.22,
        )

    return track.envelope(attack=0.004, release=0.10)


def make_dog_bark_sound():
    """Ladrido corto."""

    track = Track(0.24)

    track.add(
        0.0,
        0.20,
        lambda t, i: (
            square_wave(midi_to_frequency(52) * (1.0 - 0.35 * t) * t)
            + 0.5 * random.uniform(-1, 1)
        )
        * math.exp(-12.0 * t),
        0.32,
    )

    return track.envelope(release=0.06)


def make_round_complete_sound():
    """Jingle de ronda superada: arpegio ascendente."""

    track = Track(1.10)

    for index, note in enumerate((72, 76, 79, 84)):

        track.add(
            index * 0.16,
            0.40,
            lambda t, i, note=note: square_wave(midi_to_frequency(note) * t) * math.exp(-6.0 * t),
            0.30,
        )

    return track.envelope(release=0.20)


def make_round_fail_sound():
    """Ronda fallida: notas descendentes."""

    track = Track(0.95)

    for index, note in enumerate((67, 62, 60, 55)):

        track.add(
            index * 0.20,
            0.45,
            lambda t, i, note=note: square_wave(midi_to_frequency(note) * t) * math.exp(-5.0 * t),
            0.30,
        )

    return track.envelope(release=0.22)


def make_game_over_sound():
    """Fin de partida: melodía larga y descendente."""

    track = Track(1.80)

    for index, note in enumerate((69, 65, 62, 57)):

        track.add(
            index * 0.32,
            0.70,
            lambda t, i, note=note: square_wave(midi_to_frequency(note) * t) * math.exp(-3.5 * t),
            0.28,
        )

    track.add(
        1.30,
        0.50,
        lambda t, i: triangle_wave(midi_to_frequency(45) * t) * math.exp(-4.0 * t),
        0.30,
    )

    return track.envelope(release=0.30)


def make_menu_select_sound():
    """Blip de confirmación de menú."""

    track = Track(0.10)

    track.add(0.0, 0.09, lambda t, i: square_wave(midi_to_frequency(84) * t) * math.exp(-14.0 * t), 0.25)

    return track.envelope(attack=0.001, release=0.03)


def make_menu_move_sound():
    """Blip de movimiento en el menú, una octava más abajo."""

    track = Track(0.07)

    track.add(0.0, 0.06, lambda t, i: square_wave(midi_to_frequency(72) * t) * math.exp(-20.0 * t), 0.20)

    return track.envelope(attack=0.001, release=0.02)


def make_theme_sound():
    """
    Música del menú: melodía original de 8 compases, con bajo y charles.

    Se compone aquí para no depender de ningún fichero externo ni de música
    con derechos de terceros.
    """

    beat = 0.20  # corchea a 150 bpm

    melody = [
        (72, 2), (76, 1), (79, 1), (81, 2), (79, 2),
        (76, 2), (74, 2), (72, 4),
        (74, 2), (77, 1), (81, 1), (79, 2), (77, 2),
        (76, 4), (None, 4),
        (77, 2), (81, 2), (84, 4),
        (83, 2), (81, 2), (79, 4),
        (76, 2), (79, 2), (83, 2), (81, 2),
        (79, 4), (76, 2), (72, 2),
    ]

    melody_beats = sum(beats for _, beats in melody)

    duration = melody_beats * beat + 0.4

    track = Track(duration)

    # ------------------------------------------------------------------
    # Melodía
    # ------------------------------------------------------------------

    position = 0.0

    for note, beats in melody:

        length = beats * beat

        if note is not None:

            track.add(
                position,
                length * 0.92,
                lambda t, i, note=note: (
                    square_wave(midi_to_frequency(note) * t)
                    + 0.25 * triangle_wave(midi_to_frequency(note - 12) * t)
                )
                * math.exp(-2.4 * t),
                0.22,
            )

        position += length

    # ------------------------------------------------------------------
    # Bajo: alterna tónica y dominante en cada compás
    # ------------------------------------------------------------------

    bar_beats = melody_beats / 8

    for bar in range(8):

        for half, note in enumerate((36, 43)):

            start = (bar * bar_beats) + half * (bar_beats / 2)

            track.add(
                start,
                bar_beats / 2 * 0.9,
                lambda t, i, note=note: triangle_wave(midi_to_frequency(note) * t) * math.exp(-2.0 * t),
                0.26,
            )

    # ------------------------------------------------------------------
    # Charles en cada corchea
    # ------------------------------------------------------------------

    total_beats = int(melody_beats)

    for index in range(total_beats):

        start = index * beat

        track.add(
            start,
            0.05,
            lambda t, i: _highpass(random.uniform(-1, 1)) * math.exp(-70.0 * t),
            0.07 if index % 2 else 0.11,
        )

    # Bucle sin costura: se recorta el último silencio y se funde el final.

    _loop_seamless(track, duration)

    return track


def _lowpass(value):
    """Filtro paso bajo de un polo sobre una señal aleatoria."""

    global _LOWPASS_STATE

    _LOWPASS_STATE = _LOWPASS_STATE * 0.72 + value * 0.28

    return _LOWPASS_STATE


def _highpass(value):
    """Filtro paso alto de un polo sobre una señal aleatoria."""

    global _HIGHPASS_STATE

    _HIGHPASS_STATE = _HIGHPASS_STATE * 0.55 + value * 0.45

    return value - _HIGHPASS_STATE


_LOWPASS_STATE = 0.0

_HIGHPASS_STATE = 0.0


def _loop_seamless(track, duration):
    """
    iguala el final con el principio mezclando los últimos 120 ms, para que
    el bucle de la música no se oiga dar un salto.
    """

    fade = int(0.12 * track.sample_rate)

    fade = min(fade, track.count // 2)

    if fade <= 0:

        return

    head = track.samples[:fade]

    for index in range(fade):

        position = track.count - fade + index

        ratio = index / fade

        track.samples[position] = (
            track.samples[position] * ratio + head[index] * (1.0 - ratio)
        )


# ============================================================================
# Orquestación
# ============================================================================


def main():
    random.seed(SEED)

    for directory in (IMAGES_DIR, FONTS_DIR, SOUNDS_DIR):

        os.makedirs(directory, exist_ok=True)

    pygame.init()

    pygame.display.init()

    from src import config

    print("Generando imágenes:")

    for frame in range(3):

        save_image(make_duck_flap(frame, config.DUCK_WIDTH, config.DUCK_HEIGHT), f"duck_flap_{frame + 1}.png")

    save_image(make_duck_hit(config.DUCK_WIDTH, config.DUCK_HEIGHT), config.DUCK_HIT_SPRITE_FILE)
    save_image(make_duck_icon(32), config.DUCK_ICON_FILE)

    save_image(make_dog("idle", config.DOG_WIDTH, config.DOG_HEIGHT), config.DOG_IDLE_SPRITE_FILE)
    save_image(make_dog("happy", config.DOG_WIDTH, config.DOG_HEIGHT), config.DOG_HAPPY_SPRITE_FILE)
    save_image(make_dog("laugh", config.DOG_WIDTH, config.DOG_HEIGHT), config.DOG_LAUGH_SPRITE_FILE)

    save_image(make_background(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.HORIZON_Y), config.BACKGROUND_FILE)
    save_image(make_crosshair(config.CROSSHAIR_SIZE), config.CROSSHAIR_FILE)
    save_image(make_logo(560, 190), config.LOGO_FILE.name)

    print("Generando fuente:")

    make_font_atlas()

    print("Generando sonidos:")

    make_shot_sound().save("shot.wav")
    make_duck_hit_sound().save("duck_hit.wav")
    make_duck_flap_sound().save("duck_flap.wav")
    make_dog_laugh_sound().save("dog_laugh.wav")
    make_dog_bark_sound().save("dog_bark.wav")
    make_round_complete_sound().save("round_complete.wav")
    make_round_fail_sound().save("round_fail.wav")
    make_game_over_sound().save("game_over.wav")
    make_menu_select_sound().save("menu_select.wav")
    make_menu_move_sound().save("menu_move.wav")
    make_theme_sound().save("theme.wav")

    pygame.quit()

    print("\nRecursos generados en assets/.")

    return 0


if __name__ == "__main__":

    sys.exit(main())