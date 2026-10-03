"""
Aplicación principal de Duck Hunt.
"""

import pygame

from .config import (
    FPS,
    HIDE_MOUSE_CURSOR,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)
from .game import Game
from .states import GameState


class Application:
    """
    Clase principal de la aplicación.
    """

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (
                WINDOW_WIDTH,
                WINDOW_HEIGHT,
            )
        )

        pygame.display.set_caption(
            WINDOW_TITLE
        )

        self.clock = pygame.time.Clock()

        self.running = False

        self.game = Game()

        if HIDE_MOUSE_CURSOR:

            pygame.mouse.set_visible(
                False
            )

    # ======================================================================
    # Eventos
    # ======================================================================

    def process_events(self):

        for event in pygame.event.get():

            # --------------------------------------------------------------
            # Cerrar ventana
            # --------------------------------------------------------------

            if event.type == pygame.QUIT:

                self.running = False

                continue

            # --------------------------------------------------------------
            # Mouse
            # --------------------------------------------------------------

            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
            ):

                if event.button == 1:

                    self.game.shoot(
                        event.pos
                    )

                continue

            # --------------------------------------------------------------
            # Teclado
            # --------------------------------------------------------------

            if (
                event.type
                != pygame.KEYDOWN
            ):

                continue

            self._process_keyboard(
                event
            )

    # ======================================================================
    # Keyboard
    # ======================================================================

    def _process_keyboard(
        self,
        event,
    ):

        state = self.game.state

        # ==================================================================
        # MENU
        # ==================================================================

        if state == GameState.MENU:

            if event.key == pygame.K_RETURN:

                self.game.new_game()

            elif event.key == pygame.K_ESCAPE:

                self.running = False

            return

        # ==================================================================
        # ROUND COMPLETE
        # ==================================================================

        if (
            state
            == GameState.ROUND_COMPLETE
        ):

            if event.key == pygame.K_RETURN:

                self.game.next_round()

            elif event.key == pygame.K_ESCAPE:

                self.game.state = (
                    GameState.MENU
                )

            return

        # ==================================================================
        # GAME OVER
        # ==================================================================

        if state == GameState.GAME_OVER:

            if event.key == pygame.K_RETURN:

                self.game.new_game()

            elif event.key == pygame.K_ESCAPE:

                self.game.state = (
                    GameState.MENU
                )

            return

        # ==================================================================
        # PLAYING
        # ==================================================================

        if state == GameState.PLAYING:

            if event.key == pygame.K_ESCAPE:

                self.game.state = (
                    GameState.MENU
                )

    # ======================================================================
    # Update
    # ======================================================================

    def update(
        self,
        delta_time,
    ):

        self.game.update(
            delta_time
        )

    # ======================================================================
    # Render
    # ======================================================================

    def render(self):

        self.game.render(
            self.screen
        )

        pygame.display.flip()

    # ======================================================================
    # Game loop
    # ======================================================================

    def run(self):

        self.running = True

        try:

            while self.running:

                self.process_events()

                delta_time = (
                    self.clock.tick(FPS)
                    / 1000.0
                )

                delta_time = min(
                    delta_time,
                    0.1,
                )

                self.update(
                    delta_time
                )

                self.render()

        finally:

            self.shutdown()

    # ======================================================================
    # Shutdown
    # ======================================================================

    def shutdown(self):

        pygame.quit()
