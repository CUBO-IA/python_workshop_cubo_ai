"""
Carga de sprites.

Todo lo que el juego dibuja desde ficheros pasa por aquí, para tener un solo
sitio donde se decide cómo se escala una imagen, qué se hace con el color de
fondo transparente de los PNG exportados y qué ocurre si el fichero no está.
"""

import pygame

from .assets import IMAGES_DIR


def load_image(filename, size=None):
    """
    Carga un PNG de ``assets/images``.

    Devuelve una superficie con alfa, escalada a ``size`` si se indica. Si el
    fichero no existe o está corrupto devuelve ``None``, para que quien llama
    pueda decidir qué hacer en lugar de recibir una excepción.
    """

    path = IMAGES_DIR / filename

    if not path.exists():

        return None

    try:

        image = pygame.image.load(str(path)).convert_alpha()

    except pygame.error:

        return None

    if size is not None:

        image = pygame.transform.smoothscale(
            image,
            size,
        )

    return image


def load_frames(filenames, size=None):
    """
    Carga una lista de PNG como fotogramas de animación.

    Se omiten los que falten. Si no queda ninguno devuelve una lista vacía, que
    quien llama detecta con un ``if not frames``.
    """

    frames = []

    for filename in filenames:

        image = load_image(filename, size)

        if image is not None:

            frames.append(image)

    return frames


def flip_horizontal(image):
    """Devuelve la imagen reflejada horizontalmente."""

    return pygame.transform.flip(
        image,
        True,
        False,
    )


def colorize(image, color, keep_alpha=True):
    """
    Sustituye el color de una imagen por otro conservando su silueta.

    Sirve para teñir un mismo sprite de verde a rojo sin tener dos ficheros.
    """

    tinted = image.copy()

    tinted.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

    if not keep_alpha:

        tinted.set_alpha(None)

    return tinted


def draw_rotated(surface, image, center, angle):
    """
    Blitea ``image`` rotada alrededor de ``center``.

    Se usa en la caída del pato, donde la rotación cambia en cada fotograma.
    """

    rotated = pygame.transform.rotate(image, angle)

    rect = rotated.get_rect(center=center)

    surface.blit(rotated, rect)