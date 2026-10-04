"""
Aplicación principal de Duck Hunt.

Se ocupa de la ventana, del bucle de juego, del teclado y del ratón. Las reglas
viven en ``Game``; aquí solo se traduce lo que hace el usuario a llamadas.

El juego no termina al cerrar la ventana: se minimiza a la bandeja del
sistema y sigue vivo. Para salir de verdad hay que usar el menú del
indicador, elegir SALIR o cerrar el juego desde la bandeja.
"""

import sys

import pygame

from .audio.sound_manager import SoundManager

from .config import (
    COLOR_PAUSE_OVERLAY,
    FPS,
    HIDE_MOUSE_CURSOR,
    MAX_DELTA_TIME,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)

from .game import Game

from .gnome_app import GnomeApplication

from .indicator import DuckHuntIndicator

from .states import GameState

from .ui.fonts import huge_font


class Application:
    """Aplicación principal: ventana, entrada y bucle de juego."""

    def __init__(self):
        """
        Prepara Pygame, la partida y la integración de escritorio.

        Ninguna de las dos integraciones de GNOME es obligatoria: si PyGObject
        no está, el juego arranca igualmente, solo sin icono en la bandeja.
        """

        pygame.init()

        self._apply_window_icon()

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        pygame.display.set_caption(WINDOW_TITLE)

        self.clock = pygame.time.Clock()

        self.running = False

        self.visible = True

        self.paused = False

        self.fullscreen = False

        # El usuario puede poner la pausa desde el teclado (F10) o desde la
        # bandeja; se distingue para no interferir con los atajos globales.
        self._user_paused = False

        # ==================================================================
        # Audio
        # ==================================================================

        self.sound = SoundManager()

        # ==================================================================
        # Juego
        # ==================================================================

        self.game = Game(
            sound=self.sound,
            on_quit=self.quit,
        )

        self.pause_font = huge_font()

        # ==================================================================
        # Escritorio
        # ==================================================================

        self.indicator = DuckHuntIndicator(
            on_show_game=self.show_window,
            on_pause_game=self.toggle_pause,
            on_quit=self.quit,
            on_mute_game=self.toggle_mute,
        )

        self.gnome = GnomeApplication(self)

        # ==================================================================
        # Ratón
        # ==================================================================

        if HIDE_MOUSE_CURSOR:

            pygame.mouse.set_visible(False)

    # ======================================================================
    # Ventana
    # ======================================================================

    def _apply_window_icon(self):
        """Pone el icono de la ventana, si el fichero está disponible."""

        from .config import ICON_FILE

        try:

            if ICON_FILE.exists():

                pygame.display.set_icon(
                    pygame.image.load(str(ICON_FILE))
                )

        except pygame.error:

            pass

    def show_window(self):
        """Trae la ventana al frente."""

        self.visible = True

        self._set_mode()

        pygame.display.set_caption(WINDOW_TITLE)

        # Despierta el bucle: el reloj se mide desde el fotograma anterior.
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))

    def hide_window(self):
        """Minimiza la ventana sin terminar el proceso."""

        self.visible = False

        pygame.display.iconify()

    def toggle_fullscreen(self):
        """Alterna pantalla completa."""

        self.fullscreen = not self.fullscreen

        if self.fullscreen:

            self.screen = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN,
            )

            return

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
        )

    def _set_mode(self):
        """Vuelve a crear la ventana en el modo que toca."""

        if self.fullscreen:

            self.screen = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN,
            )

            return

        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
        )

    # ======================================================================
    # Pausa
    # ======================================================================

    def toggle_pause(self):
        """Pone o quita la pausa y refleja el estado en la bandeja."""

        self.paused = not self.paused

        self._user_paused = self.paused

        self.indicator.set_paused(self.paused)

        return self.paused

    def toggle_mute(self):
        """Silencia o reactiva el audio y refleja el estado en la bandeja."""

        muted = self.sound.toggle_mute()

        self.indicator.set_muted(muted)

        return muted

    # ======================================================================
    # Eventos
    # ======================================================================

    def process_events(self):
        """Lee y despacha todos los eventos pendientes."""

        for event in pygame.event.get():

            # --------------------------------------------------------------
            # Despertar del minimization
            # --------------------------------------------------------------

            if event.type == pygame.USEREVENT:

                continue

            # --------------------------------------------------------------
            # Cerrar ventana
            # --------------------------------------------------------------

            if event.type == pygame.QUIT:

                self.hide_window()

                continue

            # --------------------------------------------------------------
            # Ratón
            # --------------------------------------------------------------

            if event.type == pygame.MOUSEBUTTONDOWN:

                if (
                    event.button == 1
                    and not self.paused
                ):

                    self.game.shoot(event.pos)

                continue

            # --------------------------------------------------------------
            # Teclado
            # --------------------------------------------------------------

            if event.type != pygame.KEYDOWN:

                continue

            self._process_keyboard(event)

    # ======================================================================
    # Teclado
    # ======================================================================

    def _process_keyboard(self, event):
        """Traduce una tecla en una acción, según el estado actual."""

        # --------------------------------------------------------------
        # Teclas globales
        # --------------------------------------------------------------

        if event.key == pygame.K_F10:

            self.toggle_pause()

            return

        if event.key == pygame.K_m:

            self.toggle_mute()

            return

        if event.key == pygame.K_F11:

            self.toggle_fullscreen()

            return

        # --------------------------------------------------------------
        # Pausa
        # --------------------------------------------------------------

        if self.paused:

            if event.key in (pygame.K_ESCAPE, pygame.K_p):

                self.toggle_pause()

            return

        state = self.game.state

        # --------------------------------------------------------------
        # Menú
        # --------------------------------------------------------------

        if state == GameState.MENU:

            if event.key == pygame.K_UP:

                self.game.move_menu(-1)

            elif event.key == pygame.K_DOWN:

                self.game.move_menu(1)

            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:

                self.game.activate_menu()

            elif event.key == pygame.K_ESCAPE:

                self.hide_window()

            return

        # --------------------------------------------------------------
        # Fin de ronda
        # --------------------------------------------------------------

        if state == GameState.ROUND_COMPLETE:

            if event.key == pygame.K_RETURN:

                if self.game.can_continue:

                    self.game.next_round()

            elif event.key == pygame.K_ESCAPE:

                self.game.to_menu()

            return

        # --------------------------------------------------------------
        # Game over
        # --------------------------------------------------------------

        if state == GameState.GAME_OVER:

            if event.key == pygame.K_RETURN:

                if self.game.can_continue:

                    self.game.new_game()

            elif event.key == pygame.K_ESCAPE:

                self.game.to_menu()

            return

        # --------------------------------------------------------------
        # Jugando
        # --------------------------------------------------------------

        if state == GameState.PLAYING:

            if event.key == pygame.K_ESCAPE:

                self.game.to_menu()

    # ======================================================================
    # Bucle
    # ======================================================================

    def update(self, delta_time):
        """Avanza la partida, salvo que esté en pausa o minimizada."""

        if self.paused or not self.visible:

            return

        self.game.update(delta_time)

    def render(self):
        """Dibuja un fotograma."""

        if not self.visible:

            return

        self.game.render(self.screen)

        if self.paused:

            self._draw_pause_overlay()

        pygame.display.flip()

    def _draw_pause_overlay(self):
        """Capa semitransparente con el cartel de pausa."""

        overlay = pygame.Surface(
            self.screen.get_size(),
            pygame.SRCALPHA,
        )

        overlay.fill((*COLOR_PAUSE_OVERLAY, 170))

        text = self.pause_font.render_shadowed(
            "PAUSA",
            (255, 220, 120),
            (20, 20, 30),
        )

        overlay.blit(
            text,
            text.get_rect(
                center=(
                    self.screen.get_width() // 2,
                    self.screen.get_height() // 2,
                )
            ),
        )

        hint = self.pause_font.render(
            "F10 O ESC PARA SEGUIR",
            (200, 210, 225),
        )

        overlay.blit(
            hint,
            hint.get_rect(
                center=(
                    self.screen.get_width() // 2,
                    self.screen.get_height() // 2 + 60,
                )
            ),
        )

        self.screen.blit(overlay, (0, 0))

    def quit(self):
        """Pide el cierre de la aplicación."""

        self.running = False

    def run(self):
        """Arranca el bucle principal hasta que alguien cierre el juego."""

        self.running = True

        self.indicator.show()

        try:

            while self.running:

                self.process_events()

                delta_time = (
                    self.clock.tick(FPS) / 1000.0
                )

                self.update(
                    min(
                        delta_time,
                        MAX_DELTA_TIME,
                    )
                )

                self.render()

        except KeyboardInterrupt:

            pass

        finally:

            self.shutdown()

    def shutdown(self):
        """Cierra Pygame y el mixer sin dejar sonido colgando."""

        self.sound.shutdown()

        pygame.quit()