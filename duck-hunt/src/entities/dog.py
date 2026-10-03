"""
Entidad Dog.

Representa al perro que aparece después de cada pato.
"""

from enum import Enum, auto

import pygame

from ..config import (
    DOG_HEIGHT,
    DOG_HAPPY_SPRITE_FILE,
    DOG_IDLE_SPRITE_FILE,
    DOG_LAUGH_SPRITE_FILE,
    DOG_WIDTH,
    DOG_X,
    DOG_Y,
    IMAGES_DIR,
)


class DogState(Enum):
    """
    Estados del perro.
    """

    IDLE = auto()
    HAPPY = auto()
    LAUGH = auto()


class Dog:
    """
    Representa al perro del juego.
    """

    def __init__(self):

        self.width = DOG_WIDTH
        self.height = DOG_HEIGHT

        self.x = DOG_X
        self.y = DOG_Y

        self.state = DogState.IDLE

        self.timer = 0.0

        self.images = {}

        self._load_images()

    # ======================================================================
    # Sprites
    # ======================================================================

    def _load_images(self):

        self.images[
            DogState.IDLE
        ] = self._load_image(
            DOG_IDLE_SPRITE_FILE,
            self._create_idle_fallback,
        )

        self.images[
            DogState.HAPPY
        ] = self._load_image(
            DOG_HAPPY_SPRITE_FILE,
            self._create_happy_fallback,
        )

        self.images[
            DogState.LAUGH
        ] = self._load_image(
            DOG_LAUGH_SPRITE_FILE,
            self._create_laugh_fallback,
        )

    def _load_image(
        self,
        filename,
        fallback,
    ):

        path = (
            IMAGES_DIR
            / filename
        )

        if path.exists():

            try:

                image = pygame.image.load(
                    path
                ).convert_alpha()

                return pygame.transform.smoothscale(
                    image,
                    (
                        self.width,
                        self.height,
                    ),
                )

            except pygame.error:
                pass

        return fallback()

    # ======================================================================
    # Fallbacks
    # ======================================================================

    def _create_idle_fallback(self):

        return self._create_dog_sprite(
            (160, 110, 60)
        )

    def _create_happy_fallback(self):

        return self._create_dog_sprite(
            (180, 130, 70)
        )

    def _create_laugh_fallback(self):

        return self._create_dog_sprite(
            (130, 90, 50)
        )

    def _create_dog_sprite(
        self,
        body_color,
    ):

        surface = pygame.Surface(
            (
                self.width,
                self.height,
            ),
            pygame.SRCALPHA,
        )

        center_x = (
            self.width // 2
        )

        # Cuerpo
        pygame.draw.ellipse(
            surface,
            body_color,
            (
                center_x - 40,
                55,
                80,
                65,
            ),
        )

        # Cabeza
        pygame.draw.circle(
            surface,
            body_color,
            (
                center_x,
                45,
            ),
            35,
        )

        # Orejas
        pygame.draw.polygon(
            surface,
            body_color,
            [
                (
                    center_x - 28,
                    25,
                ),
                (
                    center_x - 45,
                    5,
                ),
                (
                    center_x - 12,
                    20,
                ),
            ],
        )

        pygame.draw.polygon(
            surface,
            body_color,
            [
                (
                    center_x + 28,
                    25,
                ),
                (
                    center_x + 45,
                    5,
                ),
                (
                    center_x + 12,
                    20,
                ),
            ],
        )

        # Ojos
        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (
                center_x - 12,
                40,
            ),
            7,
        )

        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (
                center_x + 12,
                40,
            ),
            7,
        )

        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (
                center_x - 12,
                40,
            ),
            3,
        )

        pygame.draw.circle(
            surface,
            (0, 0, 0),
            (
                center_x + 12,
                40,
            ),
            3,
        )

        # Hocico
        pygame.draw.ellipse(
            surface,
            (90, 60, 40),
            (
                center_x - 18,
                48,
                36,
                25,
            ),
        )

        # Nariz
        pygame.draw.circle(
            surface,
            (30, 20, 20),
            (
                center_x,
                55,
            ),
            7,
        )

        return surface

    # ======================================================================
    # Estado
    # ======================================================================

    def show_happy(self):

        self.state = DogState.HAPPY

        self.timer = 0.0

    def show_laugh(self):

        self.state = DogState.LAUGH

        self.timer = 0.0

    def show_idle(self):

        self.state = DogState.IDLE

        self.timer = 0.0

    # ======================================================================
    # Update
    # ======================================================================

    def update(self, delta_time):

        self.timer += delta_time

    # ======================================================================
    # Render
    # ======================================================================

    def draw(self, surface):

        image = self.images[
            self.state
        ]

        rect = image.get_rect()

        rect.x = self.x

        rect.y = self.y

        surface.blit(
            image,
            rect,
        )
