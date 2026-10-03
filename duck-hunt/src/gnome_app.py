"""
Integración de Duck Hunt con GNOME.

Este módulo conecta el juego Pygame con el ciclo de vida
de una aplicación de escritorio.
"""

try:

    import gi


    gi.require_version(
        "Gtk",
        "3.0",
    )

    from gi.repository import (
        Gtk,
    )

except ImportError:

    # PyGObject solo está disponible para el intérprete del sistema, no
    # para el entorno virtual del proyecto (que es el que tiene pygame).
    # Sin él el juego sigue funcionando, solo se pierde la integración
    # con el ciclo de vida de GTK.

    gi = None

    Gtk = None


class GnomeApplication:
    """
    Adaptador para la integración con GNOME.
    """

    def __init__(
        self,
        game_app,
    ):

        self.available = (
            Gtk is not None
        )

        self.game_app = game_app

        self.gtk_app = None

        self.window = None

    # ======================================================================
    # Inicialización
    # ======================================================================

    def create_application(
        self,
    ):

        if not self.available:

            return None

        self.gtk_app = Gtk.Application(
            application_id=(
                "com.duckhunt.Game"
            ),
        )

        self.gtk_app.connect(
            "activate",
            self._on_activate,
        )

        return self.gtk_app

    # ======================================================================
    # Activación
    # ======================================================================

    def _on_activate(
        self,
        application,
    ):

        self.show_game()

    # ======================================================================
    # Mostrar juego
    # ======================================================================

    def show_game(self):

        if self.game_app is None:

            return

        self.game_app.show_window()

    # ======================================================================
    # Ocultar juego
    # ======================================================================

    def hide_game(self):

        if self.game_app is None:

            return

        self.game_app.hide_window()

    # ======================================================================
    # Ejecutar
    # ======================================================================

    def run(
        self,
        argv=None,
    ):

        if not self.available:

            return 0

        if self.gtk_app is None:

            self.create_application()

        return self.gtk_app.run(
            argv
        )

    # ======================================================================
    # Salir
    # ======================================================================

    def quit(self):

        if self.gtk_app is not None:

            self.gtk_app.quit()
