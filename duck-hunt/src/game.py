"""
Lógica principal de Duck Hunt.

Aquí viven las reglas, tal y como en el juego original:

- Diez patos por ronda y hay que abatir seis para pasar.
- Cada pato aparece con tres disparos; si se gastan sin acertar, escapa.
- A partir de la ronda 11 vuelan dos patos a la vez, y desde la 21, tres.
- Abatir los diez da bonus de ronda perfecta.
- Al terminar la partida se suma un bonus por cada disparo sin usar.

Este módulo no sabe nada de SDL: solo actualiza el estado y dibuja sobre la
superficie que le pasan.
"""

import pygame

from .config import (
    BACKGROUND_FILE,
    COLOR_GROUND,
    COLOR_SKY,
    DUCK_FLIGHT_TIME,
    DUCK_HIT_SCORE,
    DUCKS_PER_ROUND,
    DUCKS_REQUIRED_TO_PASS,
    END_GAME_BONUS_PER_SHOT,
    FLIGHT_MAX_Y,
    FLIGHT_MIN_Y,
    HORIZON_Y,
    NEXT_DUCK_DELAY,
    PERFECT_ROUND_BONUS,
    ROUND_END_DELAY,
    ROUND_SPEED_MULTIPLIER,
    SHOTS_PER_DUCK,
    STARTING_ROUND,
    STARTING_SCORE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    simultaneous_ducks_for_round,
)

from .entities.bullet import ShotFlash

from .entities.duck import Duck, DuckState

from .entities.dog import Dog

from .entities.grass import Grass

from .high_scores import HighScores

from .sprites import load_image

from .states import GameState

from .ui.crosshair import Crosshair

from .ui.hud import HUD

from .ui.screens import ScreenRenderer


MENU_OPTIONS = (
    "JUGAR",
    "SALIR",
)


class Game:
    """Controla el estado completo de Duck Hunt."""

    def __init__(
        self,
        sound=None,
        high_scores=None,
        on_quit=None,
    ):
        """
        Crea la partida en el menú.

        ``sound`` es un ``SoundManager`` y puede ser ``None``, lo que resulta
        útil en las pruebas. ``on_quit`` se invoca al elegir SALIR en el menú,
        porque el juego no cierra la ventana por su cuenta.
        """

        self.state = GameState.MENU

        self.sound = sound

        self.on_quit = on_quit

        self.high_scores = (
            high_scores
            if high_scores is not None
            else HighScores()
        )

        # ==================================================================
        # Marcador
        # ==================================================================

        self.score = STARTING_SCORE

        self.round_number = STARTING_ROUND

        self.shots_left = SHOTS_PER_DUCK

        self.ducks_spawned = 0

        self.ducks_hit = 0

        self.ducks_escaped = 0

        # Disparos que quedaron sin usar al cerrar cada pato. Suman el bonus
        # final de partida.
        self.unused_shots = 0

        self.last_round_bonus = 0

        self.end_bonus = 0

        # ==================================================================
        # Tiempos
        # ==================================================================

        self.spawn_timer = 0.0

        self.state_timer = 0.0

        # ==================================================================
        # Entidades
        # ==================================================================

        self.ducks = []

        self.crosshair = Crosshair()

        self.hud = HUD()

        self.dog = Dog()

        self.grass = Grass()

        self.flash = ShotFlash()

        self.screens = ScreenRenderer()

        self.menu_index = 0

        self.background = load_image(
            BACKGROUND_FILE,
            (WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        self.duck_flap_playing = False

    # ======================================================================
    # Dificultad
    # ======================================================================

    @property
    def speed_multiplier(self):
        """Factor de velocidad de los patos en la ronda actual."""

        multiplier = 1.0 + (
            self.round_number - 1
        ) * ROUND_SPEED_MULTIPLIER

        return min(
            multiplier,
            2.0,
        )

    @property
    def simultaneous_limit(self):
        """Cuántos patos pueden volar a la vez en la ronda actual."""

        return simultaneous_ducks_for_round(self.round_number)

    @property
    def flying_ducks(self):
        """Patos que están en pantalla y pueden ser alcanzados."""

        return [
            duck
            for duck in self.ducks
            if duck.is_flying
        ]

    # ======================================================================
    # Ciclo de partida
    # ======================================================================

    def new_game(self):
        """Empieza una partida desde cero."""

        self.score = STARTING_SCORE

        self.round_number = STARTING_ROUND

        self._reset_round()

        self.state = GameState.PLAYING

        self._play_music_if_ready()

    def _reset_round(self):
        """Prepara los contadores y suelta el primer pato."""

        self.ducks_spawned = 0

        self.ducks_hit = 0

        self.ducks_escaped = 0

        self.unused_shots = 0

        self.last_round_bonus = 0

        self.end_bonus = 0

        self.ducks = []

        self.spawn_timer = 0.0

        self.state_timer = 0.0

        self.shots_left = SHOTS_PER_DUCK

        self.dog.hide()

        self._spawn_duck()

    def next_round(self):
        """Avanza a la ronda siguiente."""

        if self.state != GameState.ROUND_COMPLETE:

            return

        self.round_number += 1

        self._reset_round()

        self.state = GameState.PLAYING

    def to_menu(self):
        """Vuelve al menú abandoning la partida."""

        self.state = GameState.MENU

        self.menu_index = 0

        self.ducks = []

        self.dog.hide()

        self._stop_flap()

        self._play_music()

    # ======================================================================
    # Menú
    # ======================================================================

    def move_menu(self, delta):
        """Mueve la selección del menú y devuelve la opción elegida."""

        count = len(MENU_OPTIONS)

        self.menu_index = (
            self.menu_index + delta
        ) % count

        self._play("menu_move")

        return MENU_OPTIONS[self.menu_index]

    def activate_menu(self):
        """Ejecuta la opción seleccionada: jugar o salir."""

        option = MENU_OPTIONS[self.menu_index]

        self._play("menu_select")

        if option == "JUGAR":

            self.new_game()

        elif callable(self.on_quit):

            self.on_quit()

        return option

    # ======================================================================
    # Audio
    # ======================================================================

    def _play(self, name, loops=0, volume=1.0):
        """Atajo que reproduce un efecto si hay gestor de sonido."""

        if self.sound is not None:

            return self.sound.play(
                name,
                loops=loops,
                volume=volume,
            )

        return None

    def _play_music(self):
        """Arranca la música del menú."""

        if self.sound is not None:

            self.sound.play_music()

    def _play_music_if_ready(self):
        """La música del menú sigue sonando durante la partida."""

        self._play_music()  # noqa: WPS430

    def _start_flap(self):
        """Enciende el bucle de aleteo si hay algún pato en vuelo."""

        if self.duck_flap_playing or self.sound is None:

            return

        self.sound.loop("duck_flap", volume=0.35)

        self.duck_flap_playing = True

    def _stop_flap(self):
        """Apaga el bucle de aleteo."""

        if not self.duck_flap_playing or self.sound is None:

            return

        self.sound.stop_loop("duck_flap")

        self.duck_flap_playing = False

    # ======================================================================
    # Update
    # ======================================================================

    def update(self, delta_time):
        """Avanza la partida un paso de tiempo."""

        self.crosshair.update()

        self.flash.update(delta_time)

        if self.state == GameState.PLAYING:

            self._update_playing(delta_time)

            return

        if self.state in (
            GameState.ROUND_COMPLETE,
            GameState.GAME_OVER,
        ):

            self.state_timer += delta_time

    def _update_playing(self, delta_time):
        """Actualiza todo lo que ocurre durante la partida."""

        self._update_spawning(delta_time)

        self._update_ducks(delta_time)

        self.dog.update(delta_time)

        self._sync_flap_audio()

        self._check_round_end()

    def _update_spawning(self, delta_time):
        """Mete patos nuevos respetando el límite simultáneo de la ronda."""

        if self.spawn_timer > 0:

            self.spawn_timer -= delta_time

            return

        if self.ducks_spawned >= DUCKS_PER_ROUND:

            return

        if len(self.ducks) >= self.simultaneous_limit:

            return

        self._spawn_duck()

    def _update_ducks(self, delta_time):
        """
        Avanza cada pato, contabiliza los que escapan y retira los que ya no
        ocupan la pantalla.

        Los patos alcanzados siguen en la lista mientras caen, porque se ven;
        los escapados se retiran en cuanto salen de la pantalla.
        """

        survivors = []

        for duck in self.ducks:

            duck.update(delta_time)

            duck.expire(DUCK_FLIGHT_TIME)

            if duck.is_escaped and not duck.resolved:

                duck.resolved = True

                self._resolve_duck(duck, escaped=True)

            if duck.is_escaped or duck.is_gone:

                continue

            survivors.append(duck)

        self.ducks = survivors

    def _sync_flap_audio(self):
        """Mantiene el sonido de aleteo en consonancia con los patos en vuelo."""

        if self.flying_ducks:

            self._start_flap()

        else:

            self._stop_flap()

    # ======================================================================
    # Patos
    # ======================================================================

    def _spawn_duck(self):
        """Crea un pato nuevo y le asigna sus tres disparos."""

        duck = Duck(
            speed_multiplier=self.speed_multiplier,
        )

        self.ducks.append(duck)

        self.ducks_spawned += 1

        # Cada pato entra con la munición llena: es lo que evita que un pato
        # fallado arrastre al siguiente.
        self.shots_left = SHOTS_PER_DUCK

        self.spawn_timer = NEXT_DUCK_DELAY

    def _resolve_duck(self, duck, escaped):
        """
        Cierra la participación de un pato.

        Suma los disparos sin gastar al bonus final y pide al perro la
        reacción correspondiente.
        """

        self.unused_shots += self.shots_left

        if escaped:

            self.ducks_escaped += 1

            self.dog.show_laugh()

            self._play("dog_laugh")

        else:

            self.ducks_hit += 1

            self.score += DUCK_HIT_SCORE

            self.dog.show_happy()

            self._play("dog_bark")

        duck.resolved = True

    # ======================================================================
    # Disparo
    # ======================================================================

    def shoot(self, position):
        """
        Dispara en ``position``.

        Devuelve ``True`` si el tiro ha abatido a un pato y ``False`` en el
        resto de casos, incluidos los disparos que no cuentan.
        """

        if self.state != GameState.PLAYING:

            return False

        self.flash.trigger(position)

        flying = self.flying_ducks

        if not flying:

            # Con la pantalla despejada no se gasta munición: así el jugador
            # no pierde tiros por disparar mientras espera.
            self._play("shot", volume=0.5)

            return False

        if self.shots_left <= 0:

            return False

        self.shots_left -= 1

        self._play("shot")

        for duck in flying:

            if duck.collides_with(position):

                duck.hit()

                self._resolve_duck(duck, escaped=False)

                self._play("duck_hit")

                return True

        # Fallo: si ya no quedan balas, escapan todos los que queden.
        if self.shots_left <= 0:

            for duck in list(flying):

                duck.escape()

                self._resolve_duck(duck, escaped=True)

        return False

    # ======================================================================
    # Fin de ronda
    # ======================================================================

    def _check_round_end(self):
        """Evalúa si la ronda ha terminado y decide si se gana o se pierde."""

        if self.state != GameState.PLAYING:

            return

        if self.ducks_spawned < DUCKS_PER_ROUND:

            return

        # Quedan patos en juego, vivos o cayendo: la ronda no ha terminado.
        if self.flying_ducks or self.ducks:

            return

        self._finish_round()

    def _finish_round(self):
        """Cierra la ronda, calcula el bonus y cambia de estado."""

        self._stop_flap()

        self.dog.hide()

        if (
            self.ducks_hit
            >= DUCKS_REQUIRED_TO_PASS
        ):

            if self.ducks_hit >= DUCKS_PER_ROUND:

                self.last_round_bonus = PERFECT_ROUND_BONUS

            else:

                self.last_round_bonus = 0

            self.score += self.last_round_bonus

            self.state = GameState.ROUND_COMPLETE

            self._play("round_complete")

            return

        self.end_bonus = (
            END_GAME_BONUS_PER_SHOT
            * self.unused_shots
        )

        self.score += self.end_bonus

        self.state = GameState.GAME_OVER

        self._play("game_over")

        self.high_scores.add(
            self.score,
            self.round_number,
        )

    @property
    def can_continue(self):
        """Indica si ya se puede avanzar con Enter tras el resumen."""

        return (
            self.state
            in (
                GameState.ROUND_COMPLETE,
                GameState.GAME_OVER,
            )
            and self.state_timer >= ROUND_END_DELAY
        )

    # ======================================================================
    # Render
    # ======================================================================

    def render(self, surface):
        """Dibuja el estado actual en ``surface``."""

        if self.state == GameState.MENU:

            self.screens.draw_menu(
                surface,
                self.menu_index,
                self.high_scores.entries,
            )

            self.crosshair.draw(surface)

            return

        if self.state == GameState.ROUND_COMPLETE:

            self.screens.draw_round_complete(
                surface,
                self.round_number,
                self.score,
                self.ducks_hit,
                self.last_round_bonus,
            )

            self.crosshair.draw(surface)

            return

        if self.state == GameState.GAME_OVER:

            self.screens.draw_game_over(
                surface,
                self.score,
                self.round_number,
                self.end_bonus,
                self.high_scores.entries,
            )

            self.crosshair.draw(surface)

            return

        self._draw_playing(surface)

    def _draw_playing(self, surface):
        """Dibuja la escena de juego."""

        self._draw_background(surface)

        # Los patos van antes del matorral: así pasan por detrás.
        for duck in self.ducks:

            duck.draw(surface)

        self.grass.draw(surface)

        self.dog.draw(surface)

        self.hud.draw(
            surface,
            self.round_number,
            self.score,
            self.shots_left,
            DUCKS_PER_ROUND - self.ducks_spawned,
        )

        self.crosshair.draw(surface)

        self.flash.draw(surface)

    def _draw_background(self, surface):
        """
        Dibuja el escenario.

        Usa la imagen generada cuando está disponible y, si no, cae en un
        degradado simple para que el juego siga siendo jugable.
        """

        if self.background is not None:

            surface.blit(
                self.background,
                (0, 0),
            )

            return

        surface.fill(COLOR_SKY)

        pygame.draw.rect(
            surface,
            COLOR_GROUND,
            (0, HORIZON_Y, WINDOW_WIDTH, WINDOW_HEIGHT - HORIZON_Y),
        )

    # ======================================================================
    # Límites del escenario
    # ======================================================================

    @property
    def flight_area(self):
        """Rectángulo de vuelo, usado por los tests y las depuraciones."""

        return pygame.Rect(
            0,
            FLIGHT_MIN_Y,
            WINDOW_WIDTH,
            FLIGHT_MAX_Y - FLIGHT_MIN_Y,
        )