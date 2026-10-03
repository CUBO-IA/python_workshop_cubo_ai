"""
Lógica principal de Duck Hunt.
"""

import pygame

from .config import (
    COLOR_GROUND,
    COLOR_SKY,
    DUCK_FLIGHT_TIME,
    DUCKS_PER_ROUND,
    DUCKS_REQUIRED_TO_PASS,
    DOG_DISPLAY_TIME,
    HORIZON_Y,
    NEXT_DUCK_DELAY,
    ROUND_SPEED_MULTIPLIER,
    STARTING_BULLETS,
    STARTING_ROUND,
    STARTING_SCORE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from .entities.duck import Duck, DuckState
from .entities.dog import Dog
from .states import GameState
from .ui.crosshair import Crosshair
from .ui.hud import HUD
from .ui.screens import ScreenRenderer


class Game:
    """
    Controla el estado completo de Duck Hunt.
    """

    def __init__(self):

        self.state = GameState.MENU

        self.score = STARTING_SCORE

        self.round_number = STARTING_ROUND

        self.bullets = STARTING_BULLETS

        self.ducks_spawned = 0

        self.ducks_hit = 0

        self.ducks_escaped = 0

        self.duck_flight_timer = 0.0

        self.next_duck_timer = 0.0

        self.dog_timer = 0.0

        self.duck = None

        self.crosshair = Crosshair()

        self.hud = HUD()

        self.dog = Dog()

        self.screens = ScreenRenderer()

    # ======================================================================
    # Nueva partida
    # ======================================================================

    def new_game(self):

        self.state = GameState.PLAYING

        self.score = STARTING_SCORE

        self.round_number = STARTING_ROUND

        self._reset_round()

    def _reset_round(self):

        self.ducks_spawned = 0

        self.ducks_hit = 0

        self.ducks_escaped = 0

        self.duck_flight_timer = 0.0

        self.next_duck_timer = 0.0

        self.dog_timer = 0.0

        self.duck = None

        self.dog.show_idle()

        self._spawn_duck()

    # ======================================================================
    # Dificultad
    # ======================================================================

    @property
    def speed_multiplier(self):

        multiplier = (
            1.0
            + (
                self.round_number - 1
            )
            * ROUND_SPEED_MULTIPLIER
        )

        return min(
            multiplier,
            2.0,
        )

    # ======================================================================
    # Crear pato
    # ======================================================================

    def _spawn_duck(self):

        if (
            self.ducks_spawned
            >= DUCKS_PER_ROUND
        ):

            return

        self.duck = Duck(
            speed_multiplier=(
                self.speed_multiplier
            )
        )

        self.ducks_spawned += 1

        self.duck_flight_timer = 0.0

        self.bullets = STARTING_BULLETS

        self.dog.show_idle()

    # ======================================================================
    # Update
    # ======================================================================

    def update(
        self,
        delta_time,
    ):

        self.crosshair.update()

        if self.state == GameState.MENU:

            return

        if (
            self.state
            == GameState.ROUND_COMPLETE
        ):

            return

        if (
            self.state
            == GameState.GAME_OVER
        ):

            return

        if self.state == GameState.PLAYING:

            self._update_playing(
                delta_time
            )

    def _update_playing(
        self,
        delta_time,
    ):

        self._update_dog(
            delta_time
        )

        self._update_duck(
            delta_time
        )

        self._update_next_duck(
            delta_time
        )

        self._check_round_end()

    # ======================================================================
    # Pato
    # ======================================================================

    def _update_duck(
        self,
        delta_time,
    ):

        if self.duck is None:
            return

        self.duck.update(
            delta_time
        )

        if self.duck.is_flying:

            self.duck_flight_timer += (
                delta_time
            )

            if (
                self.duck_flight_timer
                >= DUCK_FLIGHT_TIME
            ):

                self._duck_escaped()

        elif self.duck.is_hit:

            if self.duck.death_finished:

                self.next_duck_timer = (
                    NEXT_DUCK_DELAY
                )

    # ======================================================================
    # Perro
    # ======================================================================

    def _update_dog(
        self,
        delta_time,
    ):

        self.dog.update(
            delta_time
        )

        if self.dog_timer <= 0:

            return

        self.dog_timer -= (
            delta_time
        )

        if self.dog_timer <= 0:

            self.dog.show_idle()

    # ======================================================================
    # Siguiente pato
    # ======================================================================

    def _update_next_duck(
        self,
        delta_time,
    ):

        if self.next_duck_timer <= 0:

            return

        # No crear otro pato mientras
        # el actual todavía está cayendo.

        if (
            self.duck is not None
            and self.duck.is_hit
            and not self.duck.death_finished
        ):

            return

        self.next_duck_timer -= (
            delta_time
        )

        if self.next_duck_timer <= 0:

            self.next_duck_timer = 0

            self._spawn_duck()

    # ======================================================================
    # Disparo
    # ======================================================================

    def shoot(
        self,
        position,
    ):

        if self.state != GameState.PLAYING:

            return False

        if self.bullets <= 0:

            return False

        if self.duck is None:

            return False

        if not self.duck.is_flying:

            return False

        self.bullets -= 1

        if self.duck.rect.collidepoint(
            position
        ):

            self._duck_hit()

            return True

        # --------------------------------------------------------------
        # Fallo
        # --------------------------------------------------------------

        self._shot_missed()

        return False

    # ======================================================================
    # Impacto
    # ======================================================================

    def _duck_hit(self):

        if self.duck is None:
            return

        if not self.duck.hit():
            return

        self.score += 100

        self.ducks_hit += 1

        self.dog.show_happy()

        self.dog_timer = (
            DOG_DISPLAY_TIME
        )

        self.next_duck_timer = (
            NEXT_DUCK_DELAY
        )

    # ======================================================================
    # Fallo
    # ======================================================================

    def _shot_missed(self):

        # Si se acabaron las balas,
        # el pato puede escapar.

        if self.bullets <= 0:

            self._duck_escaped()

    # ======================================================================
    # Pato escapado
    # ======================================================================

    def _duck_escaped(self):

        if self.duck is None:
            return

        if not self.duck.escape():
            return

        self.ducks_escaped += 1

        self.dog.show_laugh()

        self.dog_timer = (
            DOG_DISPLAY_TIME
        )

        self.next_duck_timer = (
            NEXT_DUCK_DELAY
        )

    # ======================================================================
    # Final de ronda
    # ======================================================================

    def _check_round_end(self):

        if (
            self.ducks_spawned
            < DUCKS_PER_ROUND
        ):

            return

        if self.next_duck_timer > 0:

            return

        if self.duck is not None:

            if self.duck.is_flying:

                return

            if (
                self.duck.is_hit
                and not self.duck.death_finished
            ):

                return

        # --------------------------------------------------------------
        # Evaluar resultado
        # --------------------------------------------------------------

        if (
            self.ducks_hit
            >= DUCKS_REQUIRED_TO_PASS
        ):

            self.state = (
                GameState.ROUND_COMPLETE
            )

        else:

            self.state = (
                GameState.GAME_OVER
            )

    # ======================================================================
    # Siguiente ronda
    # ======================================================================

    def next_round(self):

        if self.state != GameState.ROUND_COMPLETE:

            return

        self.round_number += 1

        self.state = GameState.PLAYING

        self._reset_round()

    # ======================================================================
    # Render
    # ======================================================================

    def render(
        self,
        surface,
    ):

        if self.state == GameState.MENU:

            self.screens.draw_menu(
                surface
            )

            return

        if (
            self.state
            == GameState.ROUND_COMPLETE
        ):

            self.screens.draw_round_complete(
                surface,
                self.round_number,
                self.score,
                self.ducks_hit,
            )

            return

        if (
            self.state
            == GameState.GAME_OVER
        ):

            self.screens.draw_game_over(
                surface,
                self.score,
                self.round_number,
            )

            return

        # ==================================================================
        # Gameplay
        # ==================================================================

        self._draw_background(
            surface
        )

        if self.duck is not None:

            self.duck.draw(
                surface
            )

        # Perro sobre el escenario.
        self.dog.draw(
            surface
        )

        self.hud.draw(
            surface,
            self.score,
            self.round_number,
            self.bullets,
            self.ducks_hit,
            DUCKS_PER_ROUND,
        )

        self.crosshair.draw(
            surface
        )

    # ======================================================================
    # Background
    # ======================================================================

    def _draw_background(
        self,
        surface,
    ):

        surface.fill(
            COLOR_SKY
        )

        self._draw_clouds(
            surface
        )

        ground_rect = pygame.Rect(
            0,
            HORIZON_Y,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
            - HORIZON_Y,
        )

        pygame.draw.rect(
            surface,
            COLOR_GROUND,
            ground_rect,
        )

        pygame.draw.line(
            surface,
            (80, 130, 50),
            (
                0,
                HORIZON_Y,
            ),
            (
                WINDOW_WIDTH,
                HORIZON_Y,
            ),
            4,
        )

        self._draw_vegetation(
            surface
        )

    def _draw_clouds(
        self,
        surface,
    ):

        cloud_color = (
            245,
            250,
            255,
        )

        clouds = [
            (120, 100, 60),
            (420, 150, 50),
            (760, 90, 70),
        ]

        for x, y, size in clouds:

            pygame.draw.circle(
                surface,
                cloud_color,
                (
                    x,
                    y,
                ),
                size // 2,
            )

            pygame.draw.circle(
                surface,
                cloud_color,
                (
                    x + size // 2,
                    y - 10,
                ),
                size // 2,
            )

            pygame.draw.circle(
                surface,
                cloud_color,
                (
                    x + size,
                    y,
                ),
                size // 2,
            )

            pygame.draw.rect(
                surface,
                cloud_color,
                (
                    x - size // 2,
                    y,
                    size * 2,
                    size // 2,
                ),
            )

    def _draw_vegetation(
        self,
        surface,
    ):

        tree_color = (
            35,
            120,
            45,
        )

        dark_tree_color = (
            25,
            90,
            35,
        )

        positions = [
            (80, HORIZON_Y),
            (180, HORIZON_Y),
            (780, HORIZON_Y),
            (870, HORIZON_Y),
        ]

        for x, y in positions:

            pygame.draw.rect(
                surface,
                (100, 65, 30),
                (
                    x - 8,
                    y - 80,
                    16,
                    80,
                ),
            )

            pygame.draw.circle(
                surface,
                dark_tree_color,
                (
                    x,
                    y - 90,
                ),
                35,
            )

            pygame.draw.circle(
                surface,
                tree_color,
                (
                    x - 20,
                    y - 70,
                ),
                30,
            )

            pygame.draw.circle(
                surface,
                tree_color,
                (
                    x + 20,
                    y - 70,
                ),
                30,
            )
