"""
Tests de la entidad pato.

Se comprueba lo que de verdad define al pato: que vuela en línea recta, que
rebota en los límites, que escapa al salir de la pantalla, que solo puede
abatirse mientras vuela y que al recibir el impacto cae con gravedad.
"""

import pytest

from src.config import (
    DUCK_GRAVITY,
    DUCK_HIT_LAUNCH_SPEED,
    FLIGHT_MAX_Y,
    FLIGHT_MIN_Y,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)

from src.entities.duck import Duck, DuckState


# ============================================================================
# Estado inicial
# ============================================================================


def test_duck_starts_flying(duck):

    assert duck.is_flying

    assert duck.state == DuckState.FLYING

    assert not duck.is_hit

    assert not duck.is_escaped


def test_duck_from_left_enters_moving_right(duck):

    assert duck.side == -1

    assert duck.x < 0

    assert duck.vx > 0


def test_duck_from_right_enters_moving_left(surface):

    duck = Duck(
        speed_multiplier=1.0,
        side=1,
    )

    assert duck.x > WINDOW_WIDTH

    assert duck.vx < 0


def test_duck_does_not_escape_on_the_first_frame(surface):
    """
    El umbral de escape tiene que quedar más allá del punto de entrada.

    Si no, un pato que nace en el borde derecho se contaría como escapado en
    su primer fotograma y la ronda nunca podría completarse.
    """

    for side in (-1, 1):

        duck = Duck(
            speed_multiplier=1.0,
            side=side,
        )

        duck.update(1 / 60)

        assert duck.is_flying


# ============================================================================
# Vuelo
# ============================================================================


def test_duck_moves_in_a_straight_line(duck):

    start = (duck.x, duck.y)

    for _ in range(60):

        duck.update(1 / 60)

    moved_x = duck.x - start[0]

    moved_y = duck.y - start[1]

    # Tras un segundo, un segundo de velocidad.
    assert moved_x == pytest.approx(duck.speed_x, rel=0.05)

    assert abs(moved_y) == pytest.approx(duck.speed_y, rel=0.05)


def test_duck_bounces_off_the_ceiling(duck):

    duck.y = FLIGHT_MIN_Y + 1

    duck.vy = -abs(duck.vy)

    for _ in range(30):

        duck.update(1 / 60)

    assert duck.y >= FLIGHT_MIN_Y

    assert duck.vy > 0


def test_duck_never_leaves_the_flight_ceiling(duck):
    """Con many rebotes el pato sigue dentro del área de vuelo."""

    duck.y = FLIGHT_MIN_Y + 1

    duck.vy = -abs(duck.vy)

    for _ in range(600):

        duck.update(1 / 60)

        assert duck.y <= FLIGHT_MAX_Y

        assert duck.y >= FLIGHT_MIN_Y


def test_duck_escapes_when_leaving_the_screen(duck):

    for _ in range(60 * 30):

        duck.update(1 / 60)

        if duck.is_escaped:

            break

    assert duck.is_escaped

    assert duck.x > WINDOW_WIDTH or duck.x < 0


def test_expire_marks_a_stuck_duck_as_escaped(duck):

    duck.flight_time = 99.0

    assert duck.expire(14.0)

    assert duck.is_escaped


def test_expire_ignores_a_duck_that_is_not_flying(duck):

    duck.hit()

    assert not duck.expire(14.0)

    assert duck.is_hit


# ============================================================================
# Colisión
# ============================================================================


def test_duck_is_hit_at_its_centre(duck):

    duck.x = WINDOW_WIDTH / 2

    duck.y = 300

    duck._sync_rect()

    assert duck.collides_with(duck.rect.center)


def test_duck_is_not_hit_far_from_its_body(duck):

    duck.x = WINDOW_WIDTH / 2

    duck.y = 300

    duck._sync_rect()

    assert not duck.collides_with((0, 0))


def test_a_dead_duck_cannot_be_hit_again(duck):

    duck.hit()

    assert not duck.collides_with(duck.rect.center)


# ============================================================================
# Impacto y caída
# ============================================================================


def test_hit_switches_the_state(duck):

    assert duck.hit()

    assert duck.is_hit

    assert duck.state == DuckState.HIT


def test_hit_cannot_be_applied_twice(duck):

    assert duck.hit()

    assert not duck.hit()


def test_hit_launches_the_duck_upwards(duck):
    """El retroceso del tiro manda al pato hacia arriba antes de caer."""

    duck.hit()

    assert duck.vy < 0

    assert duck.vy == pytest.approx(-DUCK_HIT_LAUNCH_SPEED)


def test_falling_duck_accelerates_downwards(duck):

    duck.hit()

    velocities = []

    for _ in range(90):

        duck.update(1 / 60)

        if duck.is_gone:

            break

        velocities.append(duck.vy)

    # La velocidad vertical solo crece: eso es la gravedad.
    assert all(
        later > earlier
        for earlier, later in zip(velocities, velocities[1:])
    )

    # Y además sigue la fórmula v = v0 + g·t fotograma a fotograma.
    steps = len(velocities)

    assert velocities[-1] == pytest.approx(
        -DUCK_HIT_LAUNCH_SPEED
        + DUCK_GRAVITY * steps / 60,
        rel=1e-6,
    )


def test_falling_duck_rotates(duck):

    duck.hit()

    for _ in range(60):

        duck.update(1 / 60)

    assert duck.angle < 0


def test_falling_duck_disappears_off_screen(duck):

    duck.hit()

    for _ in range(60 * 10):

        duck.update(1 / 60)

        if duck.is_gone:

            break

    assert duck.is_gone

    assert duck.y > WINDOW_HEIGHT


# ============================================================================
# Animación
# ============================================================================


def test_animation_advances_through_the_frames(surface):
    """Con los tres sprites generados, el aleteo va cambiando de fotograma."""

    duck = Duck(speed_multiplier=1.0, side=-1)

    assert len(duck.frames) == 3

    initial = duck.frame_index

    for _ in range(60):

        duck.update(1 / 60)

    assert duck.frame_index != initial


def test_hit_image_is_available(surface):

    duck = Duck(speed_multiplier=1.0, side=-1)

    assert duck.hit_image is not None


def test_draw_does_not_crash(surface, duck):
    """Dibujar en cualquiera de los estados no debe levantar excepciones."""

    duck.draw(surface)

    duck.hit()

    for _ in range(30):

        duck.update(1 / 60)

        duck.draw(surface)

    duck.escape()

    duck.draw(surface)