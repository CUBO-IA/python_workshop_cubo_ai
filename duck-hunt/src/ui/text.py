"""
Ayudas de dibujo de texto.

El HUD y las pantallas repiten las mismas operaciones: escribir una línea,
centrarla, alinearla a un borde. Aquí viven todas juntas para que el estilo
(sombra dura, colores) sea el mismo en cada sitio.
"""

from .fonts import (
    large_font,
    medium_font,
    small_font,
)


def draw_text(
    surface,
    text,
    position,
    color,
    font=None,
    shadow=None,
):
    """
    Escribe ``text`` con el píxel alineado a la izquierda y arriba.

    Devuelve la superficie dibujada, por si quien llama quiere medirla.
    """

    if font is None:

        font = medium_font()

    if shadow is not None:

        image = font.render_shadowed(
            text,
            color,
            shadow,
        )

    else:

        image = font.render(text, color)

    surface.blit(image, position)

    return image


def draw_text_centered(
    surface,
    text,
    center_y,
    color,
    font=None,
    shadow=(8, 12, 20),
):
    """Escribe ``text`` centrado horizontalmente y a la altura ``center_y``."""

    if font is None:

        font = medium_font()

    image = font.render_shadowed(text, color, shadow)

    rect = image.get_rect(
        center=(
            surface.get_width() // 2,
            int(center_y),
        )
    )

    surface.blit(image, rect)

    return image


def draw_text_right(
    surface,
    text,
    right_x,
    center_y,
    color,
    font=None,
    shadow=None,
):
    """Escribe ``text`` terminado en ``right_x`` y centrado en ``center_y``."""

    if font is None:

        font = small_font()

    image = font.render(text, color)

    rect = image.get_rect()

    rect.right = int(right_x)

    rect.centery = int(center_y)

    if shadow is not None:

        behind = font.render(text, shadow)

        behind_rect = behind.get_rect()

        behind_rect.right = int(right_x)

        behind_rect.centery = int(center_y)

        surface.blit(behind, behind_rect)

    surface.blit(image, rect)

    return image


def draw_panel(surface, bounds, color):
    """Pinta el fondo translúcido de un panel de menú."""

    panel = surface.subsurface(bounds).copy()

    panel.fill(color)

    return panel