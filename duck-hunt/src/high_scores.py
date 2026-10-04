"""
Persistencia de las mejores puntuaciones.

Las puntuaciones viven en el directorio de datos del usuario (XDG), no dentro
del directorio de instalación: así una instalación en ``/usr`` —que es de solo
lectura— no impide guardar récords y una actualización del juego no los borra.

Si existe el fichero antiguo ``data/high_scores.json`` dentro del proyecto se
lee también, de modo que las partidas guardadas antes de esta versión no se
pierden.
"""

import json
import os
import sys
import tempfile

from .assets import (
    LEGACY_DATA_DIR,
    USER_DATA_DIR,
    ensure_user_data_dir,
)

from .config import (
    HIGH_SCORES_FILE,
    MAX_HIGH_SCORES,
)


class HighScores:
    """Lista ordenada de las mejores partidas."""

    def __init__(self, path=None):
        """Indica dónde se leerán y escribirán los récords."""

        self.path = (
            path
            if path is not None
            else USER_DATA_DIR / HIGH_SCORES_FILE
        )

        self.entries = []

        self._load()

    # ======================================================================
    # Carga
    # ======================================================================

    def _read_file(self, path):
        """Lee un JSON de puntuaciones devolviendo la lista, o vacía."""

        try:

            with open(path, encoding="utf-8") as handle:

                data = json.load(handle)

        except (OSError, ValueError):

            return []

        if not isinstance(data, dict):

            return []

        raw = data.get("high_scores")

        if not isinstance(raw, list):

            return []

        entries = []

        for item in raw:

            if not isinstance(item, dict):

                continue

            try:

                score = int(item.get("score", 0))

            except (TypeError, ValueError):

                continue

            entries.append(
                {
                    "score": score,
                    "round": int(item.get("round", 1) or 1),
                }
            )

        return entries

    def _load(self):
        """Carga los récords propios y, si no hay, los antiguos."""

        entries = self._read_file(self.path)

        legacy = LEGACY_DATA_DIR / HIGH_SCORES_FILE

        if not entries and legacy.exists():

            entries = self._read_file(legacy)

        self.entries = sorted(
            entries,
            key=lambda entry: entry["score"],
            reverse=True,
        )[:MAX_HIGH_SCORES]

    # ======================================================================
    # Consulta
    # ======================================================================

    @property
    def top_score(self):
        """Mejor puntuación guardada, o cero si no hay ninguna."""

        return self.entries[0]["score"] if self.entries else 0

    def qualifies(self, score):
        """Indica si una puntuación entraría en la tabla."""

        if score <= 0:

            return False

        return len(self.entries) < MAX_HIGH_SCORES or score > self.top_score

    # ======================================================================
    # Escritura
    # ======================================================================

    def add(self, score, round_number=1):
        """
        Añade una puntuación y devuelve si ha entrado en la tabla.

        Guarda en disco solo cuando la entrada cambia, para no escribir en cada
        fin de partida.
        """

        if not self.qualifies(score):

            return False

        self.entries.append(
            {
                "score": int(score),
                "round": int(round_number),
            }
        )

        self.entries.sort(
            key=lambda entry: entry["score"],
            reverse=True,
        )

        self.entries = self.entries[:MAX_HIGH_SCORES]

        self.save()

        return True

    def save(self):
        """
        Escribe el fichero de forma atómica.

        Se escribe primero en un temporal del mismo directorio y luego se
        renombra, para que un corte de luz a media escritura no deje el
        fichero corrupto.
        """

        if not ensure_user_data_dir():

            return False

        try:

            handle = tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=str(self.path.parent),
                prefix=self.path.name,
                suffix=".tmp",
                delete=False,
            )

            with handle:

                json.dump(
                    {"high_scores": self.entries},
                    handle,
                    indent=2,
                )

                handle.flush()

                os.fsync(handle.fileno())

            os.replace(
                handle.name,
                str(self.path),
            )

        except (OSError, ValueError) as error:

            print(
                f"[duck-hunt] no se pudieron guardar las puntuaciones: {error}",
                file=sys.stderr,
            )

            return False

        return True