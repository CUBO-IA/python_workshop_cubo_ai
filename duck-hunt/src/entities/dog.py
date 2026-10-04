"""
Entidad Dog.

El perro es el que da el veredicto de cada pato: salta por encima de la hierba
al abatirlo y se ríe cuando se le escapa. El salto es una parábola calculada a
partir de la duración configurada, así que el arco no depende de la tasa de
fotogramas.
"""

from enum import Enum, auto

from ..config import (
    DOG_DISPLAY_TIME,
    DOG_HAPPY_SPRITE_FILE,
    DOG_HEIGHT,
    DOG_IDLE_SPRITE_FILE,
    DOG_JUMP_DURATION,
    DOG_JUMP_HEIGHT,
    DOG_LAUGH_DISPLAY_TIME,
    DOG_LAUGH_SPRITE_FILE,
    DOG_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)

from ..sprites import (
    load_image,
)


class DogState(Enum):
    """Estados del perro."""

    HIDDEN = auto()

    JUMPING = auto()

    HAPPY = auto()

    LAUGH = auto()

    IDLE = auto()


class Dog:
    """Representa al perro del juego."""

    def __init__(self):
        self.width = DOG_WIDTH

        self.height = DOG_HEIGHT

        self.x = (WINDOW_WIDTH - self.width) // 2

        # Altura a la que el perro se apoya, sobre la hierba.
        self.ground_y = WINDOW_HEIGHT - self.height - 18

        self.y = float(self.ground_y)

        self.state = DogState.HIDDEN

        self.timer = 0.0

        # Fase del salto, de 0 a 1.
        self.jump_phase = 0.0

        self._pose_for_jump = DogState.HAPPY

        self._load_images()

    # ======================================================================
    # Sprites
    # ======================================================================

    def _load_images(self):
        """Carga los tres sprites, tolerando que falte alguno."""

        self.images = {
            DogState.IDLE: load_image(
                DOG_IDLE_SPRITE_FILE,
                (self.width, self.height),
            ),
            DogState.HAPPY: load_image(
                DOG_HAPPY_SPRITE_FILE,
                (self.width, self.height),
            ),
            DogState.LAUGH: load_image(
                DOG_LAUGH_SPRITE_FILE,
                (self.width, self.height),
            ),
        }

    # ======================================================================
    # Estado
    # ======================================================================

    @property
    def visible(self):
        """Indica si el perro debe dibujarse ahora mismo."""

        return self.state != DogState.HIDDEN

    @property
    def height_above_ground(self):
        """Altura actual del salto, en píxeles sobre el suelo."""

        return self.ground_y - self.y

    def show_happy(self):
        """El perro salta sobre la hierba para celebrar un pato abatido."""

        self._start_jump(DogState.HAPPY)

    def show_laugh(self):
        """El perro se ríe de un pato que se le escapó."""

        self._start_jump(DogState.LAUGH)

    def show_idle(self):
        """El perro vuelve a su pose de reposo y se queda quieto."""

        self.state = DogState.IDLE

        self.timer = 0.0

        self.y = float(self.ground_y)

    def hide(self):
        """El perro desaparece de la pantalla."""

        self.state = DogState.HIDDEN

        self.timer = 0.0

    def _start_jump(self, pose):
        """
        Lanza el salto con la pose indicada.

        Si el perro ya estaba en pantalla, el nuevo salto lo reinicia: en el
        juego original el perro reacciona al instante a cada pato.
        """

        self._pose_for_jump = pose

        self.state = DogState.JUMPING

        self.jump_phase = 0.0

        self.timer = 0.0

    # ======================================================================
    # Update
    # ======================================================================

    def update(self, delta_time):
        """Avanza el salto o cuenta atrás de la pose."""

        self.timer += delta_time

        if self.state == DogState.JUMPING:

            self._update_jump(delta_time)

            return

        if self.state in (DogState.HAPPY, DogState.LAUGH):

            if self.timer >= self._display_time():

                self.hide()

    def _display_time(self):
        """Cuánto tiempo se mantiene la pose tras aterrizar."""

        if self.state == DogState.LAUGH:

            return DOG_LAUGH_DISPLAY_TIME

        return DOG_DISPLAY_TIME

    def _update_jump(self, delta_time):
        """
        Calcula la altura del salto.

        La parábola sale de la fase normalizada del salto, de modo que el arco
        es idéntico a 30 o a 144 FPS.
        """

        self.jump_phase += delta_time / DOG_JUMP_DURATION

        if self.jump_phase >= 1.0:

            self.jump_phase = 1.0

            self.state = self._pose_for_jump

            self.timer = 0.0

            self.y = float(self.ground_y)

            return

        # 4·t·(1−t) vale 0 en los extremos y 1 en la mitad: es la parábola
        # más barata que da un arco limpio.
        arc = 4.0 * self.jump_phase * (1.0 - self.jump_phase)

        self.y = self.ground_y - (DOG_JUMP_HEIGHT * arc)

    # ======================================================================
    # Render
    # ======================================================================

    def draw(self, surface):
        """Dibuja el perro si está visible y hay sprite para su estado."""

        if not self.visible:

            return

        image = self.images.get(self.state)

        if image is None and self.state == DogState.JUMPING:

            image = self.images.get(self._pose_for_jump)

        if image is None:

            return

        surface.blit(
            image,
            image.get_rect(
                topleft=(
                    int(self.x),
                    int(self.y),
                )
            ),
        )