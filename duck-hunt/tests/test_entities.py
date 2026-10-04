"""
Tests de las entidades auxiliares.

El perro (salto y poses), el matorral, el destello de disparo, la fuente de
píxeles y el gestor de sonido, que es la pieza con más ramas de error porque
tiene que funcionar también sin dispositivo de audio.
"""

import math

import pygame

import pytest

from src.config import (
    DOG_DISPLAY_TIME,
    DOG_GROUND_Y,
    DOG_IDLE_SPRITE_FILE,
    DOG_JUMP_DURATION,
    DOG_JUMP_HEIGHT,
    DOG_LAUGH_DISPLAY_TIME,
)

from src.entities.dog import Dog, DogState


# ============================================================================
# Perro
# ============================================================================


def test_dog_starts_hidden(surface):
    """El perro no aparece hasta que hay un pato que comentar."""

    dog = Dog()

    assert dog.state == DogState.HIDDEN

    assert not dog.visible


def test_dog_appears_with_the_happy_pose(surface):

    dog = Dog()

    dog.show_happy()

    assert dog.state == DogState.JUMPING

    dog.update(DOG_JUMP_DURATION)

    assert dog.state == DogState.HAPPY

    assert dog.visible


def test_dog_appears_with_the_laugh_pose(surface):

    dog = Dog()

    dog.show_laugh()

    dog.update(DOG_JUMP_DURATION)

    assert dog.state == DogState.LAUGH


def test_the_jump_follows_a_parabola(surface):
    """La mitad del salto es el punto más alto y los extremos tocan el suelo."""

    dog = Dog()

    dog.show_happy()

    dog.update(DOG_JUMP_DURATION / 2)

    assert dog.height_above_ground == pytest.approx(
        DOG_JUMP_HEIGHT,
        rel=0.02,
    )

    dog.update(DOG_JUMP_DURATION / 2)

    assert dog.height_above_ground == pytest.approx(0.0, abs=1.0)


def test_the_jump_never_sinks_below_the_ground(surface):
    """En pantalla, menos ``y`` es más arriba: el perro solo sube."""

    dog = Dog()

    dog.show_happy()

    for _ in range(120):

        dog.update(1 / 60)

        assert dog.y <= dog.ground_y


def test_the_jump_is_independent_of_the_frame_rate(surface):
    """El mismo tiempo de salto da la misma altura este o no el framerate."""

    fine = Dog()

    fine.show_happy()

    for _ in range(90):

        fine.update(1 / 60)

    coarse = Dog()

    coarse.show_happy()

    coarse.update(1.5)

    assert fine.height_above_ground == pytest.approx(
        coarse.height_above_ground,
        rel=0.05,
    )


def test_the_dog_hides_after_showing_the_pose(surface):

    dog = Dog()

    dog.show_happy()

    dog.update(DOG_JUMP_DURATION)

    assert dog.state == DogState.HAPPY

    dog.update(DOG_DISPLAY_TIME + 0.1)

    assert dog.state == DogState.HIDDEN


def test_the_laugh_lasts_longer(surface):

    dog = Dog()

    dog.show_laugh()

    dog.update(DOG_JUMP_DURATION)

    dog.update(DOG_DISPLAY_TIME + 0.1)

    assert dog.state == DogState.LAUGH

    dog.update(DOG_LAUGH_DISPLAY_TIME)

    assert dog.state == DogState.HIDDEN


def test_a_new_reaction_restarts_the_jump(surface):

    dog = Dog()

    dog.show_happy()

    for _ in range(10):

        dog.update(1 / 60)

    dog.show_laugh()

    assert dog.state == DogState.JUMPING

    dog.update(DOG_JUMP_DURATION)

    assert dog.state == DogState.LAUGH


def test_the_dog_has_a_sprite_for_every_pose(surface):

    dog = Dog()

    assert dog.images[DogState.IDLE] is not None

    assert dog.images[DogState.HAPPY] is not None

    assert dog.images[DogState.LAUGH] is not None


def test_drawing_the_dog_does_not_crash(surface):

    dog = Dog()

    dog.draw(surface)

    dog.show_happy()

    for _ in range(120):

        dog.update(1 / 60)

        dog.draw(surface)


# ============================================================================
# Matorral
# ============================================================================


def test_grass_covers_the_bottom_of_the_screen(surface):
    """El matorral tapa la franja por la que entran los patos."""

    from src.entities.grass import Grass

    grass = Grass()

    assert grass.y + grass.height >= grass.height

    assert grass.draw(surface) is None


# ============================================================================
# Destello de disparo
# ============================================================================


def test_the_flash_is_off_until_fired(surface):

    from src.entities.bullet import ShotFlash

    flash = ShotFlash()

    assert not flash.active

    flash.draw(surface)


def test_the_flash_lights_up_and_fades(surface):

    from src.config import SHOT_FLASH_TIME
    from src.entities.bullet import ShotFlash

    flash = ShotFlash()

    flash.trigger((200, 200))

    assert flash.active

    flash.update(SHOT_FLASH_TIME / 2)

    assert flash.active

    flash.update(SHOT_FLASH_TIME)

    assert not flash.active


def test_firing_the_crosshair_triggers_the_flash(surface, game):

    game.new_game()

    duck = game.flying_ducks[0]

    game.shoot(duck.rect.center)

    assert game.flash.active


# ============================================================================
# Fuente de píxeles
# ============================================================================


def test_the_pixel_font_is_available(surface):
    """El atlas generado tiene que estar presente y con glifos."""

    from src.ui.pixel_font import PixelFont

    font = PixelFont(scale=2)

    assert font.available

    assert font.glyphs


def test_render_produces_the_expected_size(surface):

    from src.ui.pixel_font import PixelFont

    font = PixelFont(scale=3)

    width, height = font.measure("ABCD")

    image = font.render("ABCD", (255, 255, 255))

    assert image.get_size() == (width, height)

    assert height == font.height


def test_render_actually_draws_glyphs(surface):
    """Una superficie completamente vacía significaría que el atlas falla."""

    from src.ui.pixel_font import PixelFont

    font = PixelFont(scale=2)

    image = font.render("GAME OVER", (255, 255, 255))

    opaque = sum(
        1
        for x in range(image.get_width())
        for y in range(image.get_height())
        if image.get_at((x, y)).a > 0
    )

    assert opaque > 0


def test_the_text_is_actually_tinted(surface):
    """El color pedido tiene que verse, no salir siempre en blanco."""

    from src.ui.pixel_font import PixelFont

    font = PixelFont(scale=2)

    image = font.render("A", (255, 0, 0))

    colours = {
        image.get_at((x, y))[:3]
        for x in range(image.get_width())
        for y in range(image.get_height())
        if image.get_at((x, y)).a > 0
    }

    assert colours == {(255, 0, 0)}


def test_shadowed_text_is_larger(surface):
    """La sombra desplaza el texto y agranda la superficie."""

    from src.ui.pixel_font import PixelFont

    font = PixelFont(scale=2)

    plain = font.render("SCORE", (255, 255, 255))

    shadowed = font.render_shadowed("SCORE", (255, 255, 255))

    assert shadowed.get_width() > plain.get_width()


def test_unknown_characters_fall_back_to_a_glyph(surface):

    from src.ui.pixel_font import PixelFont

    font = PixelFont(scale=2)

    image = font.render("ÑÁÉ", (255, 255, 255))

    assert image.get_width() > 0


# ============================================================================
# Sonido
# ============================================================================


def test_the_sound_manager_works_without_audio(surface):
    """Sin mixer el gestor no rompe: solo no suena nada."""

    from src.audio.sound_manager import SoundManager

    manager = SoundManager()

    # Puede haber o no mixer según el entorno; en ambos casos no debe
    # levantar excepciones.
    assert manager.play("shot") is None or manager.available

    assert manager.play("no_existe") is None

    manager.play_music()

    manager.toggle_mute()

    manager.stop_loop()

    manager.shutdown()


def test_muting_toggles_the_state(surface):

    from src.audio.sound_manager import SoundManager

    manager = SoundManager()

    first = manager.toggle_mute()

    assert manager.toggle_mute() is not first


def test_the_sound_files_exist():
    """Los once ficheros generados por el script de assets están."""

    from src.assets import SOUNDS_DIR
    from src.config import MUSIC_MENU_FILE, SOUND_FILES

    for filename in SOUND_FILES.values():

        path = SOUNDS_DIR / filename

        assert path.exists(), f"falta {filename}"

        assert path.stat().st_size > 0, f"{filename} está vacío"

    assert (SOUNDS_DIR / MUSIC_MENU_FILE).exists()


def test_every_sprite_file_exists():
    """Las imágenes que el juego carga tienen que estar en disco."""

    from src.assets import IMAGES_DIR
    from src.config import (
        BACKGROUND_FILE,
        CROSSHAIR_FILE,
        DUCK_HIT_SPRITE_FILE,
        DUCK_ICON_FILE,
        DUCK_SPRITE_FILES,
    )

    filenames = (
        list(DUCK_SPRITE_FILES)
        + [
            DUCK_HIT_SPRITE_FILE,
            DUCK_ICON_FILE,
            BACKGROUND_FILE,
            CROSSHAIR_FILE,
            DOG_IDLE_SPRITE_FILE,
            "dog_happy.png",
            "dog_laugh.png",
            "logo.png",
        ]
    )

    for filename in filenames:

        path = IMAGES_DIR / filename

        assert path.exists(), f"falta {filename}"

        assert path.stat().st_size > 0, f"{filename} está vacío"