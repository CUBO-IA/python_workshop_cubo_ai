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

from .gnome_app import (
    GnomeApplication,
)

from .indicator import (
    DuckHuntIndicator,
)

from .states import (
    GameState,
)


class Application:
    """
    Aplicación principal.

    Pygame:
        controla el juego.

    GNOME:
        controla la integración de escritorio.

    AppIndicator:
        controla el indicador de sistema.
    """

    def __init__(self):

        # ==================================================================
        # Pygame
        # ==================================================================

        pygame.init()

        self.screen = (
            pygame.display.set_mode(
                (
                    WINDOW_WIDTH,
                    WINDOW_HEIGHT,
                )
            )
        )

        pygame.display.set_caption(
            WINDOW_TITLE
        )

        self.clock = pygame.time.Clock()

        self.running = False

        self.visible = True

        self.paused = False

        # ==================================================================
        # Juego
        # ==================================================================

        self.game = Game()

        # ==================================================================
        # AppIndicator
        # ==================================================================

        self.indicator = (
            DuckHuntIndicator(
                on_show_game=(
                    self.show_window
                ),
                on_pause_game=(
                    self.toggle_pause
                ),
                on_quit=(
                    self.quit
                ),
            )
        )

        # ==================================================================
        # GNOME
        # ==================================================================

        self.gnome = (
            GnomeApplication(
                self
            )
        )

        # ==================================================================
        # Mouse
        # ==================================================================

        if HIDE_MOUSE_CURSOR:

            pygame.mouse.set_visible(
                False
            )

    # ======================================================================
    # Ventana
    # ======================================================================

    def show_window(self):

        self.visible = True

        pygame.display.set_mode(
            (
                WINDOW_WIDTH,
                WINDOW_HEIGHT,
            )
        )

        pygame.display.set_caption(
            WINDOW_TITLE
        )

        pygame.event.post(
            pygame.event.Event(
                pygame.USEREVENT
            )
        )

    def hide_window(self):

        self.visible = False

        pygame.display.iconify()

    # ======================================================================
    # Pausa
    # ======================================================================

    def toggle_pause(self):

        self.paused = (
            not self.paused
        )

        self.indicator.set_paused(
            self.paused
        )

    # ======================================================================
    # Eventos
    # ======================================================================

    def process_events(self):

        for event in pygame.event.get():

            # --------------------------------------------------------------
            # Cerrar ventana
            # --------------------------------------------------------------

            if (
                event.type
                == pygame.QUIT
            ):

                # No cerramos inmediatamente.
                #
                # La aplicación sigue disponible
                # mediante el AppIndicator.

                self.hide_window()

                continue

            # --------------------------------------------------------------
            # Mouse
            # --------------------------------------------------------------

            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
            ):

                if (
                    event.button == 1
                    and not self.paused
                ):

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

        # --------------------------------------------------------------
        # Pausa global
        # --------------------------------------------------------------

        if event.key == pygame.K_F10:

            self.toggle_pause()

            return

        # --------------------------------------------------------------
        # Si está pausado
        # --------------------------------------------------------------

        if self.paused:

            if event.key == pygame.K_ESCAPE:

                self.show_window()

            return

        # --------------------------------------------------------------
        # Estado del juego
        # --------------------------------------------------------------

        state = self.game.state

        # ==================================================================
        # MENU
        # ==================================================================

        if state == GameState.MENU:

            if event.key == pygame.K_RETURN:

                self.game.new_game()

            elif event.key == pygame.K_ESCAPE:

                self.hide_window()

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

        if self.paused:

            return

        if not self.visible:

            return

        self.game.update(
            delta_time
        )

    # ======================================================================
    # Render
    # ======================================================================

    def render(self):

        if not self.visible:

            return

        self.game.render(
            self.screen
        )

        pygame.display.flip()

    # ======================================================================
    # Salir
    # ======================================================================

    def quit(self):

        self.running = False

    # ======================================================================
    # Game loop
    # ======================================================================

    def run(self):

        self.running = True

        self.indicator.show()

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
