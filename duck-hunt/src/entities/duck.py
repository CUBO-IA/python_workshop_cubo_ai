"""
Entidad Duck.

Un pato aparece fuera de la pantalla, cruza el cielo en diagonal y escapa al
salir por un lateral. Al recibir un impacto cambia a un plano distinto: deja de
volar, sube un instante por el retroceso del tiro y cae con gravedad girando
hasta desaparecer por abajo.
"""

import random

from enum import Enum, auto

import pygame

from ..config import (
    DUCK_ANIMATION_FPS,
    DUCK_FALL_MAX_ANGLE,
    DUCK_FALL_OFFSCREEN_MARGIN,
    DUCK_GRAVITY,
    DUCK_HIT_LAUNCH_SPEED,
    DUCK_HIT_SPRITE_FILE,
    DUCK_HEIGHT,
    DUCK_MARGIN_X,
    DUCK_MARGIN_Y,
    MAX_SPEED_MULTIPLIER,
    DUCK_SPEED_X,
    DUCK_SPEED_Y,
    DUCK_SPRITE_FILES,
    DUCK_WIDTH,
    FLIGHT_MAX_Y,
    FLIGHT_MIN_Y,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)

from ..sprites import (
    draw_rotated,
    flip_horizontal,
    load_frames,
    load_image,
)


class DuckState(Enum):
    """Estados internos del pato."""

    FLYING = auto()

    HIT = auto()

    ESCAPED = auto()

    GONE = auto()


class Duck:
    """Representa un pato dentro del juego."""

    def __init__(
        self,
        speed_multiplier=1.0,
        side=None,
        rng=None,
    ):
        """
        Crea un pato y decide por dónde entra.

        ``side`` fuerza la entrada por la izquierda (``-1``) o la derecha
        (``1``). Si no se indica se elige al azar, que es lo que quiere el
        juego salvo en los tests.
        """

        self.rng = rng or random

        multiplier = min(
            max(0.1, float(speed_multiplier)),
            MAX_SPEED_MULTIPLIER,
        )

        # ==================================================================
        # Entrada
        # ==================================================================

        self.side = (
            side
            if side is not None
            else self.rng.choice((-1, 1))
        )

        # Cada pato varía un poco su velocidad y su altura de entrada, para
        # que dos patos seguidos no se parezcan.
        variation = self.rng.uniform(0.88, 1.12)

        self.speed_x = DUCK_SPEED_X * multiplier * variation

        self.speed_y = DUCK_SPEED_Y * multiplier * variation

        if self.side < 0:

            self.x = -float(DUCK_WIDTH)

            self.vx = abs(self.speed_x)

        else:

            self.x = float(WINDOW_WIDTH + DUCK_WIDTH)

            self.vx = -abs(self.speed_x)

        self.y = float(
            self.rng.uniform(
                FLIGHT_MAX_Y - 140,
                FLIGHT_MAX_Y - 20,
            )
        )

        self.vy = -abs(self.speed_y)

        # ==================================================================
        # Tamaño y colisión
        # ==================================================================

        self.width = DUCK_WIDTH

        self.height = DUCK_HEIGHT

        # La caja de impacto es algo menor que el dibujo: los patos del NES
        # tienen una zona muerta generosa y el jugador debe poder acertar.
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # ==================================================================
        # Estado
        # ==================================================================

        self.state = DuckState.FLYING

        # El juego marca aquí que ya ha contabilizado este pato, para no
        # sumar dos veces sus disparos sin gastar.
        self.resolved = False

        self.flight_time = 0.0

        self.fall_time = 0.0

        self.angle = 0.0

        # ==================================================================
        # Animación
        # ==================================================================

        self.frames = load_frames(
            DUCK_SPRITE_FILES,
            (self.width, self.height),
        )

        self.hit_image = load_image(
            DUCK_HIT_SPRITE_FILE,
            (self.width, self.height),
        )

        self.frame_index = 0

        self.frame_timer = 0.0

        self._flipped_cache = {}

        self._sync_rect()

    # ======================================================================
    # Propiedades
    # ======================================================================

    @property
    def is_flying(self):
        """Indica si el pato sigue volando y por tanto puede ser alcanzado."""

        return self.state == DuckState.FLYING

    @property
    def is_hit(self):
        """Indica si el pato ya fue alcanzado y está cayendo."""

        return self.state == DuckState.HIT

    @property
    def is_escaped(self):
        """Indica si el pato ha salido de la pantalla."""

        return self.state == DuckState.ESCAPED

    @property
    def is_gone(self):
        """Indica si el pato ya no ocupa la partida y se puede retirar."""

        return self.state == DuckState.GONE

    @property
    def depth_scale(self):
        """
        Factor de escala según la altura, para dar sensación de profundidad.

        Va del 90% en lo alto a 100% cerca del suelo.
        """

        span = max(1.0, FLIGHT_MAX_Y - FLIGHT_MIN_Y)

        position = (self.y - FLIGHT_MIN_Y) / span

        return 0.90 + 0.10 * max(0.0, min(1.0, position))

    @property
    def facing_right(self):
        """``True`` si el pato mira hacia la derecha."""

        return self.vx > 0

    # ======================================================================
    # Movimiento
    # ======================================================================

    def update(self, delta_time):
        """Avanza el pato según su estado actual."""

        if self.state == DuckState.FLYING:

            self._update_flight(delta_time)

        elif self.state == DuckState.HIT:

            self._update_fall(delta_time)

        self._sync_rect()

    def _update_flight(self, delta_time):
        """Vuelo en línea recta con rebote en los bordes."""

        self.flight_time += delta_time

        self.x += self.vx * delta_time

        self.y += self.vy * delta_time

        self._bounce()

        self._update_animation(delta_time)

        # Escape al salir por un lateral, que es como termina el vuelo en el
        # juego original. El umbral es simétrico y queda más allá del punto de
        # entrada, para que un pato recién nacido no cuente como escapado.
        if (
            self.x > WINDOW_WIDTH + self.width + DUCK_MARGIN_X
            or self.x < -self.width - DUCK_MARGIN_X
        ):

            self.state = DuckState.ESCAPED

    def _bounce(self):
        """
        Rebota contra el techo y el suelo del área de vuelo.

        En los laterales no rebota: el pato sale de la pantalla y cuenta como
        escapado, que es como termina el vuelo en el juego original. Si
        rebotara también en los lados se quedaría atrapado yendo y viniendo
        hasta que lo rescatara el temporizador de seguridad.
        """

        if self.y <= FLIGHT_MIN_Y:

            self.y = FLIGHT_MIN_Y

            self.vy = abs(self.vy)

        elif self.y >= FLIGHT_MAX_Y:

            self.y = FLIGHT_MAX_Y

            self.vy = -abs(self.vy)

    def _update_animation(self, delta_time):
        """Avanza el aleteo a ``DUCK_ANIMATION_FPS``."""

        if len(self.frames) <= 1:

            return

        frame_duration = 1.0 / DUCK_ANIMATION_FPS

        self.frame_timer += delta_time

        while self.frame_timer >= frame_duration:

            self.frame_timer -= frame_duration

            self.frame_index = (
                self.frame_index + 1
            ) % len(self.frames)

    # ======================================================================
    # Caída
    # ======================================================================

    def _update_fall(self, delta_time):
        """Caída con gravedad y giro progresivo."""

        self.fall_time += delta_time

        self.vy += DUCK_GRAVITY * delta_time

        self.y += self.vy * delta_time

        progress = min(1.0, self.fall_time / 0.8)

        self.angle = -DUCK_FALL_MAX_ANGLE * progress

        if self.y > WINDOW_HEIGHT + DUCK_FALL_OFFSCREEN_MARGIN:

            self.state = DuckState.GONE

    # ======================================================================
    # Colisión
    # ======================================================================

    def _sync_rect(self):
        """Recalcula la caja de impacto a partir de la posición."""

        scale = self.depth_scale

        width = int(self.width * scale)

        height = int(self.height * scale)

        self.rect.width = width

        self.rect.height = height

        self.rect.centerx = int(self.x)

        self.rect.centery = int(self.y)

    def collides_with(self, point):
        """Indica si ``point`` cae dentro de la zona abatible del pato."""

        if not self.is_flying:

            return False

        # Se encoge un poco la caja: apuntar a la punta del ala debe fallar.
        return self.rect.inflate(-8, -10).collidepoint(point)

    # ======================================================================
    # Eventos
    # ======================================================================

    def hit(self):
        """
        Marca el pato como alcanzado.

        Devuelve ``False`` si ya estaba muerto o escapado, de modo que un
        segundo impacto sobre el mismo pato no cuente dos veces.
        """

        if not self.is_flying:

            return False

        self.state = DuckState.HIT

        self.vy = -DUCK_HIT_LAUNCH_SPEED

        self.vx *= 0.25

        self.fall_time = 0.0

        self.angle = 0.0

        return True

    def escape(self):
        """Marca el pato como escapado si aún estaba volando."""

        if not self.is_flying:

            return False

        self.state = DuckState.ESCAPED

        return True

    def expire(self, max_flight_time):
        """
        Red de seguridad: si un pato lleva demasiado tiempo volando sin salir,
        se da por escapado. Evita que una ronda se atasque.
        """

        if (
            self.state == DuckState.FLYING
            and self.flight_time >= max_flight_time
        ):

            self.state = DuckState.ESCAPED

            return True

        return False

    # ======================================================================
    # Render
    # ======================================================================

    def _flipped(self, image):
        """Devuelve la versión reflejada de una imagen, cacheada."""

        key = id(image)

        cached = self._flipped_cache.get(key)

        if cached is None:

            cached = flip_horizontal(image)

            self._flipped_cache[key] = cached

        return cached

    def _current_image(self):
        """Elige el fotograma que corresponde al estado actual."""

        if self.state == DuckState.HIT and self.hit_image is not None:

            return self.hit_image

        if not self.frames:

            return None

        return self.frames[self.frame_index]

    def draw(self, surface):
        """Dibuja el pato, salvo si ya no está en juego."""

        if self.state in (DuckState.ESCAPED, DuckState.GONE):

            return

        image = self._current_image()

        if image is None:

            return

        scale = self.depth_scale

        target = (
            max(1, int(self.width * scale)),
            max(1, int(self.height * scale)),
        )

        if image.get_size() != target:

            image = pygame.transform.scale(image, target)

        if not self.facing_right:

            image = self._flipped(image)

        if self.state == DuckState.HIT:

            draw_rotated(
                surface,
                image,
                self.rect.center,
                self.angle,
            )

            return

        surface.blit(
            image,
            image.get_rect(center=self.rect.center),
        )