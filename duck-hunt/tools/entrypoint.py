#!/usr/bin/env python3
"""
Punto de entrada del binario congelado.

``run.py`` incluye una lógica que relanza el juego con el intérprete del
entorno virtual cuando pygame no se puede importar. Eso tiene sentido
desarrollando en el repositorio, pero no dentro del paquete: aquí pygame va
siempre incluido. Este script es el que empaqueta PyInstaller, y es
deliberadamente mínimo.

Admite un argumento:

``--self-test``
    Arranca todo el juego, ejecuta unos fotogramas y sale. Sirve para
    comprobar que el binario funciona sin abrir una ventana, que es lo que
    hace ``scripts/build.sh test``.
"""

import os
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT not in sys.path:

    sys.path.insert(0, ROOT)


SELF_TEST_FLAG = "--self-test"

# Fotogramas que se simulan en el modo de comprobación.
SELF_TEST_FRAMES = 120


def self_test():
    """
    Arranca el juego en headless y lo actualiza unos fotogramas.

    Devuelve 0 si todo va bien. No dibuja en pantalla: con el vídeo en modo
    ``dummy`` la superficie existe pero no se muestra nada.
    """

    import pygame

    from src.config import (
        WINDOW_HEIGHT,
        WINDOW_WIDTH,
    )

    from src.game import Game
    from src.sprites import load_image

    pygame.init()

    pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    # Los recursos vienen empaquetados dentro del ejecutable: comprobarlos es
    # justo lo que este modo tiene que demostrar.
    missing = []

    for filename in (
        "background.png",
        "duck_flap_1.png",
        "duck_hit.png",
        "dog_idle.png",
        "crosshair.png",
    ):

        if load_image(filename) is None:

            missing.append(filename)

    if missing:

        print(
            f"Recursos que no se pudieron cargar: {', '.join(missing)}",
            file=sys.stderr,
        )

        pygame.quit()

        return 1

    surface = pygame.Surface(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    game = Game()

    game.render(surface)

    game.new_game()

    for _ in range(SELF_TEST_FRAMES):

        game.update(1 / 60)

        game.render(surface)

    print(
        f"duck-hunt {game.round_number}: {game.ducks_spawned} pato(s), "
        f"{len(game.ducks)} en pantalla, estado {game.state.name}"
    )

    pygame.quit()

    return 0


def main():
    """Arranca la aplicación y propaga su código de salida."""

    arguments = sys.argv[1:]

    if SELF_TEST_FLAG in arguments:

        return self_test()

    if arguments:

        print(f"Opción desconocida: {arguments[0]}", file=sys.stderr)

        return 2

    from src.app import Application

    application = Application()

    application.run()

    return 0


if __name__ == "__main__":

    sys.exit(main())