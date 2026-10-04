"""
Configuración principal de Duck Hunt.

Todas las constantes del juego viven aquí: el resto de módulos leen de este
fichero y nunca escriben números mágicos. Las reglas de ronda reproducen las
del Duck Hunt de NES: diez patos por ronda, seis aciertos para pasar, tres
disparos por pato y la velocidad subiendo con la ronda.
"""

from .assets import (
    DATA_DIR,
    FONTS_DIR,
    ICONS_DIR,
    IMAGES_DIR,
    PROJECT_ROOT,
    SOUNDS_DIR,
)


# ============================================================================
# Aplicación
# ============================================================================

APP_NAME = "Duck Hunt"

APP_VERSION = "1.0.0"

APP_ID = "com.duckhunt.Game"

APP_DESCRIPTION = "Juego clásico de caza de patos"

APP_AUTHOR = "Taller Python"


# ============================================================================
# Rutas
# ============================================================================

__all_resources__ = (
    PROJECT_ROOT,
    DATA_DIR,
    ICONS_DIR,
)

ICON_FILE = ICONS_DIR / "duck-hunt.png"

LOGO_FILE = IMAGES_DIR / "logo.png"

BACKGROUND_FILE = "background.png"

FONT_ATLAS_FILE = FONTS_DIR / "font_atlas.png"

FONT_METRICS_FILE = FONTS_DIR / "font_metrics.json"


# ============================================================================
# Ventana
# ============================================================================

WINDOW_WIDTH = 960

WINDOW_HEIGHT = 720

WINDOW_TITLE = APP_NAME

FULLSCREEN_KEY = "f11"


# ============================================================================
# Game loop
# ============================================================================

FPS = 60

# El delta time nunca avanza más que esto: si la ventana se congela o el
# proceso se pausa, la física no teletransporta patos por la pantalla.
MAX_DELTA_TIME = 0.05


# ============================================================================
# Colores
# ============================================================================

COLOR_SKY = (135, 206, 235)

COLOR_GROUND = (104, 168, 70)

COLOR_BLACK = (0, 0, 0)

COLOR_WHITE = (255, 255, 255)

COLOR_HUD_BACKGROUND = (24, 32, 48)

COLOR_HUD_SHADOW = (8, 12, 20)

COLOR_HUD_TEXT = (248, 248, 232)

COLOR_HUD_GOLD = (255, 200, 64)

COLOR_HUD_DIM = (110, 118, 132)

COLOR_MENU_BACKGROUND = (25, 45, 70)

COLOR_MENU_TITLE = (255, 220, 80)

COLOR_MENU_TEXT = (255, 255, 255)

COLOR_MENU_SELECTED = (255, 180, 50)

COLOR_PAUSE_OVERLAY = (10, 14, 24)

COLOR_GAME_OVER = (232, 84, 72)


# ============================================================================
# Mouse
# ============================================================================

HIDE_MOUSE_CURSOR = True


# ============================================================================
# Escenario
# ============================================================================

GROUND_HEIGHT = 220

HORIZON_Y = WINDOW_HEIGHT - GROUND_HEIGHT

# Los patos nacen por debajo de la hierba y entran en pantalla subiendo, así
# que el techo de vuelo es un poco más alto que el horizonte.
FLIGHT_MIN_Y = 96

FLIGHT_MAX_Y = HORIZON_Y + 40

# El matorral central tapa a los patos mientras entran y salen.
BUSH_WIDTH = 420

BUSH_HEIGHT = 150

BUSH_Y = WINDOW_HEIGHT - BUSH_HEIGHT

BUSH_X = (WINDOW_WIDTH - BUSH_WIDTH) // 2


# ============================================================================
# Pato
# ============================================================================

DUCK_WIDTH = 64

DUCK_HEIGHT = 48

# Velocidad base del pato. La dirección exacta la decide ``Duck`` al
# aparecer, con una variación por pato.
DUCK_SPEED_X = 150.0

DUCK_SPEED_Y = 105.0

# Margen respecto a los bordes del escenario.
DUCK_MARGIN_X = 12

DUCK_MARGIN_Y = 24

DUCK_ANIMATION_FPS = 8

DUCK_SPRITE_FILES = (
    "duck_flap_1.png",
    "duck_flap_2.png",
    "duck_flap_3.png",
)

DUCK_HIT_SPRITE_FILE = "duck_hit.png"

DUCK_ICON_FILE = "duck_icon.png"


# ============================================================================
# Física de la caída
# ============================================================================

# Gravedad de la caída tras el impacto, en píxeles por segundo al cuadrado.
DUCK_GRAVITY = 1150.0

# Velocidad vertical inicial al recibir el impacto: sube un poco antes de
# caer, como en el original.
DUCK_HIT_LAUNCH_SPEED = 190.0

# La caída termina cuando el pato sale por debajo de la ventana.
DUCK_FALL_OFFSCREEN_MARGIN = 60.0

# Giro máximo durante la caída, en grados.
DUCK_FALL_MAX_ANGLE = 160.0


# ============================================================================
# Punto de mira
# ============================================================================

CROSSHAIR_FILE = "crosshair.png"

CROSSHAIR_SIZE = 48

SHOT_FLASH_SIZE = 64

SHOT_FLASH_TIME = 0.09


# ============================================================================
# Juego
# ============================================================================

STARTING_SCORE = 0

DUCK_HIT_SCORE = 100

# Bonus por acertar los diez patos de una ronda.
PERFECT_ROUND_BONUS = 1000

# Bonus final: 10 puntos por cada tiro que quede sin gastar, multiplicado por
# los patos abatidos, igual que en el NES.
END_GAME_BONUS_PER_SHOT = 10

# Tiros disponibles por pato. Agotarlos sin acertar hace escapar al pato.
SHOTS_PER_DUCK = 3


# ============================================================================
# Rondas
# ============================================================================

STARTING_ROUND = 1

DUCKS_PER_ROUND = 10

DUCKS_REQUIRED_TO_PASS = 6

# Cuántos patos vuelan a la vez según la ronda, como en el original: uno
# hasta la ronda 10, dos hasta la 20 y tres a partir de ahí.
def simultaneous_ducks_for_round(round_number):
    """Número de patos simultáneos de una ronda."""

    if round_number >= 21:

        return 3

    if round_number >= 11:

        return 2

    return 1


# Cada ronda se lleva un 12% de la velocidad base, con un techo del doble.
ROUND_SPEED_MULTIPLIER = 0.12

MAX_SPEED_MULTIPLIER = 2.0

# Segundos que un pato sobrevive antes de considerarse escapado. Es una red de
# seguridad: el escape normal ocurre al salir de la pantalla.
DUCK_FLIGHT_TIME = 14.0


# ============================================================================
# Perro
# ============================================================================

DOG_IDLE_SPRITE_FILE = "dog_idle.png"

DOG_HAPPY_SPRITE_FILE = "dog_happy.png"

DOG_LAUGH_SPRITE_FILE = "dog_laugh.png"

DOG_WIDTH = 120

DOG_HEIGHT = 140

DOG_GROUND_Y = WINDOW_HEIGHT - DOG_HEIGHT - 18

# Altura del salto del perro, en píxeles sobre el suelo.
DOG_JUMP_HEIGHT = 190.0

# Duración del salto, en segundos.
DOG_JUMP_DURATION = 0.9

# Cuánto tiempo se queda el perro en la pose tras el salto.
DOG_DISPLAY_TIME = 1.6

# En la risa se queda el doble de tiempo.
DOG_LAUGH_DISPLAY_TIME = 2.6


# ============================================================================
# Tiempos
# ============================================================================

# Pausa entre el final de un pato y la aparición del siguiente.
NEXT_DUCK_DELAY = 0.6

# Distancia mínima entre dos apariciones del mismo pato.
DUCK_SPAWN_INTERVAL = 0.9

# Tiempo que dura la pantalla de fin de ronda antes de poder continuar.
ROUND_END_DELAY = 0.8


# ============================================================================
# Sonido
# ============================================================================

MASTER_VOLUME = 0.7

MUSIC_VOLUME = 0.45

SOUND_FILES = {
    "shot": "shot.wav",
    "duck_hit": "duck_hit.wav",
    "duck_flap": "duck_flap.wav",
    "dog_laugh": "dog_laugh.wav",
    "dog_bark": "dog_bark.wav",
    "round_complete": "round_complete.wav",
    "round_fail": "round_fail.wav",
    "game_over": "game_over.wav",
    "menu_select": "menu_select.wav",
    "menu_move": "menu_move.wav",
}

MUSIC_MENU_FILE = "theme.wav"

# Frecuencia de mezcla. La None deja que pygame elija la del sistema.
MIXER_FREQUENCY = 44100

MIXER_SIZE = -16

MIXER_CHANNELS = 2


# ============================================================================
# Fuente
# ============================================================================

FONT_SCALE_SMALL = 2

FONT_SCALE_MEDIUM = 3

FONT_SCALE_LARGE = 5

FONT_SCALE_HUGE = 7


# ============================================================================
# Mejores puntuaciones
# ============================================================================

HIGH_SCORES_FILE = "high_scores.json"

MAX_HIGH_SCORES = 5


# ============================================================================
# AppIndicator
# ============================================================================

INDICATOR_ID = APP_ID

INDICATOR_ICON_NAME = "duck-hunt"

INDICATOR_TOOLTIP = APP_NAME


# ============================================================================
# GNOME
# ============================================================================

DESKTOP_FILE_NAME = "com.duckhunt.Game.desktop"

DESKTOP_FILE = DATA_DIR / DESKTOP_FILE_NAME