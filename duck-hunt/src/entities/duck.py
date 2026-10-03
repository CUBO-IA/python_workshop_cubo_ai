"""
Entidad Duck.

Representa el pato que vuela y puede ser alcanzado.
"""

from enum import Enum, auto

import pygame

from ..config import (
    COLOR_BLACK,
    DUCK_ANIMATION_FPS,
    DUCK_DEATH_TIME,
    DUCK_HEIGHT,
    DUCK_HIT_SPRITE_FILE,
    DUCK_MAX_X,
    DUCK_MAX_Y,
    DUCK_MIN_X,
    DUCK_MIN_Y,
    DUCK_SPRITE_FILES,
    DUCK_SPEED_X,
    DUCK_SPEED_Y,
    DUCK_START_X,
    DUCK_START_Y,
    DUCK_WIDTH,
    IMAGES_DIR,
)


class DuckState(Enum):
    """
    Estados internos del pato.
    """

    FLYING = auto()
    HIT = auto()
    ESCAPED = auto()


class Duck:
    """
    Representa un pato dentro del juego.
    """

    def __init__(
        self,
        speed_multiplier=1.0,
    ):

        # ==================================================================
        # Dimensiones
        # ==================================================================

        self.width = DUCK_WIDTH
        self.height = DUCK_HEIGHT

        # ==================================================================
        # Posición
        # ==================================================================

        self.x = float(DUCK_START_X)
        self.y = float(DUCK_START_Y)

        # ==================================================================
        # Dirección
        # ==================================================================

        self.direction_x = 1
        self.direction_y = 1

        # ==================================================================
        # Velocidad
        # ==================================================================

        self.speed_x = (
            DUCK_SPEED_X
            * speed_multiplier
        )

        self.speed_y = (
            DUCK_SPEED_Y
            * speed_multiplier
        )

        # ==================================================================
        # Colisión
        # ==================================================================

        self.rect = pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height,
        )

        # ==================================================================
        # Estado
        # ==================================================================

        self.state = DuckState.FLYING

        self.death_timer = 0.0

        # ==================================================================
        # Animación
        # ==================================================================

        self.animation_frames = []

        self.animation_index = 0

        self.animation_timer = 0.0

        self.hit_image = None

        self._load_sprites()

    # ======================================================================
    # Propiedades
    # ======================================================================

    @property
    def is_flying(self):
        return self.state == DuckState.FLYING

    @property
    def is_hit(self):
        return self.state == DuckState.HIT

    @property
    def is_escaped(self):
        return self.state == DuckState.ESCAPED

    @property
    def death_finished(self):
        return (
            self.state == DuckState.HIT
            and self.death_timer
            >= DUCK_DEATH_TIME
        )

    # ======================================================================
    # Sprites
    # ======================================================================

    def _load_sprites(self):

        self.animation_frames.clear()

        for filename in DUCK_SPRITE_FILES:

            path = IMAGES_DIR / filename

            if not path.exists():
                continue

            try:

                image = pygame.image.load(
                    path
                ).convert_alpha()

                image = pygame.transform.smoothscale(
                    image,
                    (
                        self.width,
                        self.height,
                    ),
                )

                self.animation_frames.append(
                    image
                )

            except pygame.error:

                continue

        if not self.animation_frames:

            self.animation_frames.append(
                self._create_fallback_sprite()
            )

        hit_path = (
            IMAGES_DIR
            / DUCK_HIT_SPRITE_FILE
        )

        if hit_path.exists():

            try:

                self.hit_image = (
                    pygame.image.load(
                        hit_path
                    ).convert_alpha()
                )

                self.hit_image = (
                    pygame.transform.smoothscale(
                        self.hit_image,
                        (
                            self.width,
                            self.height,
                        ),
                    )
                )

            except pygame.error:

                self.hit_image = None

    def _create_fallback_sprite(self):

        surface = pygame.Surface(
            (
                self.width,
                self.height,
            ),
            pygame.SRCALPHA,
        )

        center_x = self.width // 2
        center_y = self.height // 2

        # Cuerpo
        pygame.draw.ellipse(
            surface,
            (40, 100, 190),
            (
                center_x - 22,
                center_y - 8,
                40,
                24,
            ),
        )

        # Cabeza
        pygame.draw.circle(
            surface,
            (40, 100, 190),
            (
                center_x + 18,
                center_y - 12,
            ),
            13,
        )

        # Pico
        pygame.draw.polygon(
            surface,
            (240, 170, 30),
            [
                (
                    center_x + 28,
                    center_y - 13,
                ),
                (
                    center_x + 42,
                    center_y - 7,
                ),
                (
                    center_x + 28,
                    center_y - 2,
                ),
            ],
        )

        # Ojo
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (
                center_x + 22,
                center_y - 16,
            ),
            4,
        )

        pygame.draw.circle(
            surface,
            COLOR_BLACK,
            (
                center_x + 22,
                center_y - 16,
            ),
            2,
        )

        # Ala
        pygame.draw.ellipse(
            surface,
            (25, 75, 150),
            (
                center_x - 15,
                center_y - 4,
                25,
                14,
            ),
        )

        return surface

    # ======================================================================
    # Update
    # ======================================================================

    def update(self, delta_time):

        if self.state == DuckState.FLYING:

            self._update_position(
                delta_time
            )

            self._update_animation(
                delta_time
            )

        elif self.state == DuckState.HIT:

            self._update_death(
                delta_time
            )

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def _update_position(
        self,
        delta_time,
    ):

        self.x += (
            self.speed_x
            * self.direction_x
            * delta_time
        )

        self.y += (
            self.speed_y
            * self.direction_y
            * delta_time
        )

        self._check_boundaries()

    def _check_boundaries(self):

        if self.x <= DUCK_MIN_X:

            self.x = DUCK_MIN_X

            self.direction_x = 1

        elif self.x >= DUCK_MAX_X:

            self.x = DUCK_MAX_X

            self.direction_x = -1

        if self.y <= DUCK_MIN_Y:

            self.y = DUCK_MIN_Y

            self.direction_y = 1

        elif self.y >= DUCK_MAX_Y:

            self.y = DUCK_MAX_Y

            self.direction_y = -1

    # ======================================================================
    # Animación de vuelo
    # ======================================================================

    def _update_animation(
        self,
        delta_time,
    ):

        if len(self.animation_frames) <= 1:
            return

        frame_duration = (
            1.0
            / DUCK_ANIMATION_FPS
        )

        self.animation_timer += delta_time

        while (
            self.animation_timer
            >= frame_duration
        ):

            self.animation_timer -= (
                frame_duration
            )

            self.animation_index += 1

            if (
                self.animation_index
                >= len(
                    self.animation_frames
                )
            ):

                self.animation_index = 0

    # ======================================================================
    # Animación de muerte
    # ======================================================================

    def _update_death(
        self,
        delta_time,
    ):

        self.death_timer += delta_time

        # El pato cae.
        self.y += 260.0 * delta_time

        # Girar ligeramente durante la caída.
        self.direction_y = 1

    # ======================================================================
    # Impacto
    # ======================================================================

    def hit(self):

        if self.state != DuckState.FLYING:
            return False

        self.state = DuckState.HIT

        self.death_timer = 0.0

        return True

    # ======================================================================
    # Escape
    # ======================================================================

    def escape(self):

        if self.state != DuckState.FLYING:
            return False

        self.state = DuckState.ESCAPED

        return True

    # ======================================================================
    # Render
    # ======================================================================

    def draw(self, surface):

        if self.state == DuckState.ESCAPED:
            return

        if (
            self.state == DuckState.HIT
            and self.hit_image is not None
        ):

            image = self.hit_image

        else:

            image = self.animation_frames[
                self.animation_index
            ]

        if (
            self.direction_x < 0
            and self.state == DuckState.FLYING
        ):

            image = pygame.transform.flip(
                image,
                True,
                False,
            )

        # Girar el pato durante la caída.
        if self.state == DuckState.HIT:

            progress = min(
                self.death_timer
                / DUCK_DEATH_TIME,
                1.0,
            )

            angle = -90 * progress

            image = pygame.transform.rotate(
                image,
                angle,
            )

        draw_rect = image.get_rect(
            center=self.rect.center
        )

        surface.blit(
            image,
            draw_rect,
        )
