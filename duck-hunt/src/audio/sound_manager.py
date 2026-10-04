"""
Gestión de sonido de Duck Hunt.

Envuelve ``pygame.mixer`` y resuelve los tres casos que se dan en la práctica:

- Hay dispositivo de audio: se cargan y reproducen los ficheros de
  ``assets/sounds``.
- No hay mixer (una sesión sin sonido, un contenedor de pruebas): el juego
  sigue funcionando y todas las llamadas son inertes.
- Falta un fichero concreto: se avisa una sola vez y el resto del audio
  sigue sonando.
"""

import sys

import pygame

from ..assets import SOUNDS_DIR
from ..config import (
    MASTER_VOLUME,
    MIXER_CHANNELS,
    MIXER_FREQUENCY,
    MIXER_SIZE,
    MUSIC_MENU_FILE,
    MUSIC_VOLUME,
    SOUND_FILES,
)


class SoundManager:
    """
    Carga y reproducción de los sonidos del juego.

    Los efectos se cargan bajo demanda y se cachean: ``Sound`` es más caro de
    construir que de reproducir, y el juego repite los mismos diez ficheros
    miles de veces.
    """

    def __init__(self):
        """Inicializa el mixer si se puede y deja el gestor listo."""

        self.available = False

        self.muted = False

        self._sounds = {}

        self._missing_reported = set()

        self._looping = None

        self._music_name = None

        self._init_mixer()

    # ======================================================================
    # Mixer
    # ======================================================================

    def _init_mixer(self):
        """Arranca el mixer tolerando que no haya tarjeta de sonido."""

        try:

            if not pygame.mixer.get_init():

                pygame.mixer.init(
                    frequency=MIXER_FREQUENCY,
                    size=MIXER_SIZE,
                    channels=MIXER_CHANNELS,
                )

            self.available = True

            self._apply_volume()

        except pygame.error as error:

            # Sin audio no se interrumpe la partida: solo se pierde el sonido.
            self.available = False

            print(f"[duck-hunt] audio no disponible: {error}", file=sys.stderr)

    def _apply_volume(self):
        """Fija el volumen maestro actual."""

        if not self.available:

            return

        volume = 0.0 if self.muted else MASTER_VOLUME

        try:

            pygame.mixer.set_num_channels(16)

            for index in range(pygame.mixer.get_num_channels()):

                pygame.mixer.Channel(index).set_volume(volume)

        except pygame.error:

            pass

    # ======================================================================
    # Efectos
    # ======================================================================

    def _load(self, name):
        """
        Carga un efecto y lo cachea.

        Devuelve ``None`` si el mixer no está, el nombre no existe o el
        fichero falta o está corrupto.
        """

        if name in self._sounds:

            return self._sounds[name]

        if name in self._missing_reported:

            return None

        filename = SOUND_FILES.get(name)

        if not filename:

            return None

        path = SOUNDS_DIR / filename

        if not path.exists():

            self._missing_reported.add(name)

            print(
                f"[duck-hunt] falta el sonido {path}",
                file=sys.stderr,
            )

            return None

        if not self.available:

            return None

        try:

            sound = pygame.mixer.Sound(str(path))

        except pygame.error as error:

            self._missing_reported.add(name)

            print(
                f"[duck-hunt] no se pudo cargar {path}: {error}",
                file=sys.stderr,
            )

            return None

        self._sounds[name] = sound

        return sound

    def play(self, name, loops=0, volume=1.0):
        """
        Reproduce un efecto y devuelve su objeto ``Sound``, o ``None``.

        ``loops`` sigue la convención de Pygame: 0 suena una vez y -1 en
        bucle hasta que se llame a ``stop_loop``.
        """

        if self.muted:

            return None

        sound = self._load(name)

        if sound is None:

            return None

        try:

            sound.set_volume(
                max(0.0, min(1.0, volume))
            )

            sound.play(loops=loops)

        except pygame.error:

            return None

        return sound

    def stop_loop(self, name=None):
        """Detiene el efecto en bucle indicado, o todos si no se dice cuál."""

        if self._looping is None:

            return

        if name is not None and name != self._looping:

            return

        sound = self._sounds.get(self._looping)

        if sound is not None:

            try:

                sound.stop()

            except pygame.error:

                pass

        self._looping = None

    def loop(self, name, volume=1.0):
        """Arranca un efecto en bucle, sustituyendo el anterior."""

        if self._looping == name:

            return

        self.stop_loop()

        sound = self.play(name, loops=-1, volume=volume)

        if sound is not None:

            self._looping = name

    # ======================================================================
    # Música
    # ======================================================================

    def play_music(self, name=MUSIC_MENU_FILE, loops=-1, volume=MUSIC_VOLUME):
        """Carga y reproduce música en bucle."""

        if self.muted or not self.available:

            return

        if self._music_name == name and pygame.mixer.music.get_busy():

            return

        path = SOUNDS_DIR / name

        if not path.exists():

            return

        try:

            pygame.mixer.music.load(str(path))

            pygame.mixer.music.set_volume(
                0.0 if self.muted else volume
            )

            pygame.mixer.music.play(loops=loops)

            self._music_name = name

        except pygame.error:

            self._music_name = None

    def stop_music(self):
        """Detiene la música y la descarga."""

        if not self.available:

            return

        try:

            pygame.mixer.music.stop()

            pygame.mixer.music.unload()

        except pygame.error:

            pass

        self._music_name = None

    # ======================================================================
    # Silencio
    # ======================================================================

    def toggle_mute(self):
        """Alterna el silencio y devuelve el estado nuevo."""

        self.muted = not self.muted

        if not self.available:

            return self.muted

        try:

            if self.muted:

                pygame.mixer.music.set_volume(0.0)

            else:

                pygame.mixer.music.set_volume(MUSIC_VOLUME)

            for index in range(pygame.mixer.get_num_channels()):

                pygame.mixer.Channel(index).set_volume(
                    0.0 if self.muted else MASTER_VOLUME
                )

        except pygame.error:

            pass

        return self.muted

    def shutdown(self):
        """Libera el mixer antes de cerrar la aplicación."""

        self.stop_loop()

        self.stop_music()

        self._sounds.clear()

        if self.available:

            try:

                pygame.mixer.quit()

            except pygame.error:

                pass

            self.available = False