"""
Tests de las reglas de juego.

Comprueban la parte que el jugador nota: el límite de disparos, cuándo se pasa
o se pierde una ronda, el bonus de ronda perfecta, el bonus final, cuántos
patos vuelan a la vez y la persistencia de los récords.
"""

import pytest

from src.config import (
    DUCK_HIT_SCORE,
    DUCKS_PER_ROUND,
    DUCKS_REQUIRED_TO_PASS,
    END_GAME_BONUS_PER_SHOT,
    PERFECT_ROUND_BONUS,
    SHOTS_PER_DUCK,
    WINDOW_WIDTH,
    simultaneous_ducks_for_round,
)

from src.states import GameState


# ============================================================================
# Utilidades de los tests
# ============================================================================

def run_seconds(game, seconds, on_frame=None):
    """Avanza la partida un número de segundos a 60 FPS."""

    frames = int(seconds * 60)

    for _ in range(frames):

        game.update(1 / 60)

        if on_frame is not None:

            on_frame()


def shoot_first_visible_duck(game):
    """Dispara al primer pato que esté realmente en pantalla."""

    for duck in game.flying_ducks:

        if (
            duck.rect.right > 4
            and duck.rect.left < WINDOW_WIDTH - 4
        ):

            return game.shoot(duck.rect.center)

    return False


def play_round(game, shoot=True, max_seconds=500):
    """
    Empieza una partida y juega una ronda entera.

    Con ``shoot`` a ``True`` el jugador acierta a todo; a ``False`` falla los
    tres disparos de cada pato.
    """

    game.new_game()

    def frame():
        if not shoot:

            if game.flying_ducks and game.shots_left > 0:

                game.shoot((5, 5))

            return

        shoot_first_visible_duck(game)

    run_seconds(game, max_seconds, frame)

    return game.state


# ============================================================================
# Menú
# ============================================================================


def test_game_starts_in_the_menu(game):

    assert game.state == GameState.MENU


def test_menu_wraps_around(game):
    """La selección da la vuelta en vez de quedarse en un extremo."""

    assert game.move_menu(-1) == "SALIR"

    assert game.move_menu(1) == "JUGAR"


def test_activating_jugar_starts_a_new_game(game):

    game.menu_index = 0

    game.activate_menu()

    assert game.state == GameState.PLAYING

    assert game.score == 0

    assert game.round_number == 1


def test_activating_salir_calls_the_quit_callback(surface, high_scores):
    """SALIR no cierra la ventana: avisa a la aplicación para que ella lo haga."""

    from src.game import Game

    called = []

    game = Game(
        sound=None,
        high_scores=high_scores,
        on_quit=lambda: called.append(True),
    )

    game.menu_index = 1

    game.activate_menu()

    assert called == [True]

    assert game.state == GameState.MENU


# ============================================================================
# Disparo
# ============================================================================


def test_shooting_an_empty_screen_does_not_consume_ammo(game):
    """Disparar con la pantalla despejada no gasta balas."""

    game.new_game()

    game.ducks = []

    game.shots_left = SHOTS_PER_DUCK

    assert game.shoot((100, 100)) is False

    assert game.shots_left == SHOTS_PER_DUCK


def test_a_duck_being_hit_gives_points_and_count(game):

    game.new_game()

    duck = game.flying_ducks[0]

    assert game.shoot(duck.rect.center) is True

    assert game.ducks_hit == 1

    assert game.score == DUCK_HIT_SCORE


def test_three_misses_make_the_duck_escape(game):
    """Al tercer fallo se acaban las balas y el pato se escapa."""

    game.new_game()

    assert game.shots_left == SHOTS_PER_DUCK

    game.shoot((5, 5))

    assert game.shots_left == SHOTS_PER_DUCK - 1

    assert not game.ducks_escaped

    game.shoot((5, 5))

    game.shoot((5, 5))

    assert game.shots_left == 0

    assert game.ducks_escaped == 1


def test_shooting_with_no_ammo_does_nothing(game):

    game.new_game()

    game.shots_left = 0

    duck = game.flying_ducks[0]

    assert game.shoot(duck.rect.center) is False

    assert game.ducks_hit == 0


def test_the_dog_reacts_to_a_hit(game):

    game.new_game()

    game.shoot(game.flying_ducks[0].rect.center)

    assert game.dog.visible


def test_the_dog_reacts_to_an_escape(game):

    game.new_game()

    game.shots_left = 1

    game.shoot((5, 5))

    assert game.dog.visible


# ============================================================================
# Rondas
# ============================================================================


def test_simultaneous_ducks_follow_the_original_rounds():

    assert simultaneous_ducks_for_round(1) == 1

    assert simultaneous_ducks_for_round(10) == 1

    assert simultaneous_ducks_for_round(11) == 2

    assert simultaneous_ducks_for_round(20) == 2

    assert simultaneous_ducks_for_round(21) == 3

    assert simultaneous_ducks_for_round(99) == 3


def test_the_speed_multiplier_grows_with_the_round(game):

    first = game.speed_multiplier

    game.round_number = 5

    assert game.speed_multiplier > first


def test_the_speed_multiplier_is_capped(game):

    game.round_number = 500

    assert game.speed_multiplier <= 2.0


def test_a_new_round_spawns_ten_ducks_over_time(game):

    game.new_game()

    assert game.ducks_spawned == 1

    play_round(game, shoot=True)

    assert game.ducks_spawned == DUCKS_PER_ROUND


def test_a_perfect_round_is_completed_with_a_bonus(game):

    assert play_round(game, shoot=True) == GameState.ROUND_COMPLETE

    assert game.ducks_hit == DUCKS_PER_ROUND

    assert game.last_round_bonus == PERFECT_ROUND_BONUS

    assert game.score == (
        DUCKS_PER_ROUND * DUCK_HIT_SCORE + PERFECT_ROUND_BONUS
    )


def test_missing_the_required_ducks_ends_the_game(game):

    assert play_round(game, shoot=False) == GameState.GAME_OVER

    assert game.ducks_hit < DUCKS_REQUIRED_TO_PASS


def test_the_end_bonus_counts_unused_shots(game):
    """Cada disparo que queda sin gastar suma su parte al bonus final."""

    game.new_game()

    # Se acierta a cinco patos con el primer disparo (sobran dos balas cada
    # uno) y se fallan los cinco restantes disparando las tres.
    hits_target = DUCKS_REQUIRED_TO_PASS - 1

    counter = {"hits": 0, "on_duck": 0}

    def frame():
        if not game.flying_ducks:

            counter["on_duck"] = 0

            return

        if counter["hits"] < hits_target and counter["on_duck"] == 0:

            if game.shoot(game.flying_ducks[0].rect.center):

                counter["hits"] += 1

        elif game.shots_left > 0:

            game.shoot((5, 5))

        counter["on_duck"] += 1

    run_seconds(game, 500, frame)

    assert game.state == GameState.GAME_OVER

    assert game.ducks_hit == hits_target

    # Cinco patos acertados con dos balas sin gastar cada uno.
    assert game.unused_shots == hits_target * (SHOTS_PER_DUCK - 1)

    assert game.end_bonus == (
        END_GAME_BONUS_PER_SHOT * game.unused_shots
    )

    assert game.score == (
        hits_target * DUCK_HIT_SCORE + game.end_bonus
    )


def test_failing_every_duck_gives_no_bonus(game):
    """Si se gastan las tres balas en cada pato, el bonus es cero."""

    game.new_game()

    assert play_round(game, shoot=False) == GameState.GAME_OVER

    assert game.unused_shots == 0

    assert game.end_bonus == 0


def test_a_saved_duck_becomes_gone_and_leaves_the_list(game):

    game.new_game()

    duck = game.flying_ducks[0]

    duck.hit()

    for _ in range(60 * 12):

        game.update(1 / 60)

        if duck.is_gone:

            break

    assert duck not in game.ducks


def test_the_next_round_starts_playing_again(game):

    play_round(game, shoot=True)

    game.next_round()

    assert game.state == GameState.PLAYING

    assert game.round_number == 2

    assert game.ducks_spawned == 1

    assert game.ducks_hit == 0


def test_cannot_advance_before_the_round_summary(game):
    """Tras el resumen hay una pausa breve antes de poder continuar."""

    from src.config import ROUND_END_DELAY

    game.state = GameState.ROUND_COMPLETE

    game.state_timer = 0.0

    assert game.can_continue is False

    game.state_timer = ROUND_END_DELAY

    assert game.can_continue is True


def test_going_back_to_the_menu_clears_the_round(game):

    play_round(game, shoot=True)

    game.to_menu()

    assert game.state == GameState.MENU

    assert game.ducks == []


# ============================================================================
# Puntuaciones altas
# ============================================================================


def test_high_scores_are_saved_and_sorted(high_scores):

    assert high_scores.add(1000, round_number=2)

    assert high_scores.add(5000, round_number=4)

    assert high_scores.add(3000, round_number=3)

    assert [entry["score"] for entry in high_scores.entries] == [
        5000,
        3000,
        1000,
    ]


def test_a_low_score_does_not_enter_the_table(high_scores):

    high_scores.add(5000, round_number=1)

    for _ in range(5):

        high_scores.add(4000, round_number=1)

    assert not high_scores.qualifies(10)

    assert high_scores.entries[0]["score"] == 5000


def test_the_table_keeps_at_most_five_entries(high_scores):
    """La tabla está limitada aunque se añadan muchas puntuaciones."""

    for score in range(10, 100, 10):

        high_scores.add(score, round_number=1)

    assert len(high_scores.entries) == 5

    assert high_scores.top_score == 90


def test_scores_survive_a_reload(tmp_path):

    from src.high_scores import HighScores

    path = tmp_path / "high_scores.json"

    first = HighScores(path)

    first.add(4242, round_number=6)

    assert HighScores(path).entries[0]["score"] == 4242


def test_a_corrupt_file_does_not_break_the_game(tmp_path):

    from src.high_scores import HighScores

    path = tmp_path / "high_scores.json"

    path.write_text("{ esto no es json", encoding="utf-8")

    assert HighScores(path).entries == []


def test_game_over_records_the_score(game):
    """Al perder, la puntuación entra en la tabla."""

    play_round(game, shoot=False)

    assert game.state == GameState.GAME_OVER

    # Con cero aciertos la puntuación es cero y no entra en la tabla.
    assert game.score == 0

    game.score = 1234

    assert game.high_scores.add(game.score, game.round_number)

    assert game.high_scores.top_score == 1234


# ============================================================================
# Dibujado
# ============================================================================


def test_every_state_can_be_rendered(surface, game):
    """Cada estado de la partida se dibuja sin excepciones."""

    game.render(surface)

    game.new_game()

    game.render(surface)

    game.state = GameState.ROUND_COMPLETE

    game.render(surface)

    game.state = GameState.GAME_OVER

    game.render(surface)


def test_the_background_image_is_available(game):
    """El juego usa el fondo generado y no el degradado de reserva."""

    assert game.background is not None


def test_the_crosshair_follows_the_mouse(game, pygame_module):
    """La mira se sitúa donde está el ratón."""

    expected = pygame_module.mouse.get_pos()

    game.update(1 / 60)

    assert game.crosshair.rect.center == expected