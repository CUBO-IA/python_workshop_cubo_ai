"""
Indicador de sistema (bandeja) para Duck Hunt.

Usa AyatanaAppIndicator3, que está construido sobre GTK 3. Ese binding solo
está disponible para el intérprete del sistema, no para el entorno virtual
del proyecto, así que la integración con la bandeja es opcional: sin
PyGObject el juego sigue funcionando, simplemente sin icono en la bandeja.
"""

try:

    import gi


    gi.require_version(
        "AyatanaAppIndicator3",
        "0.1",
    )

    from gi.repository import (
        AyatanaAppIndicator3,
    )

except ImportError:

    AyatanaAppIndicator3 = None


class DuckHuntIndicator:
    """
    Indicador de bandeja con las acciones de la partida.

    Si PyGObject no está disponible, todos los métodos son no-op y el juego
    sigue siendo jugable.
    """

    def __init__(
        self,
        on_show_game,
        on_pause_game,
        on_quit,
        on_mute_game=None,
    ):

        self.available = (
            AyatanaAppIndicator3 is not None
        )

        self.on_show_game = on_show_game
        self.on_pause_game = on_pause_game
        self.on_quit = on_quit
        self.on_mute_game = on_mute_game

        self.paused = False

        self.muted = False

        self.indicator = None

        if not self.available:

            return

        self.indicator = (
            AyatanaAppIndicator3.Indicator.new(
                "duck-hunt",
                "duckhunt",
                AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS,
            )
        )

        self.indicator.set_status(
            AyatanaAppIndicator3.IndicatorStatus.ACTIVE
        )

        self.indicator.set_title(
            "Duck Hunt"
        )

        self._add_menu()

    def _add_menu(self):
        """Construye el menú contextual del indicador."""

        if not self.available:

            return

        import gi

        from gi.repository import (
            Gtk,
        )

        menu = Gtk.Menu()

        show_item = Gtk.MenuItem(
            label="Mostrar juego",
        )

        show_item.connect(
            "activate",
            lambda _widget: self.on_show_game(),
        )

        menu.append(
            show_item
        )

        self.pause_item = Gtk.MenuItem(
            label="Pausar",
        )

        self.pause_item.connect(
            "activate",
            lambda _widget: self.on_pause_game(),
        )

        menu.append(
            self.pause_item
        )

        self.mute_item = Gtk.MenuItem(
            label="Silenciar",
        )

        self.mute_item.connect(
            "activate",
            lambda _widget: self._on_mute_activated(),
        )

        menu.append(
            self.mute_item
        )

        quit_item = Gtk.MenuItem(
            label="Salir",
        )

        quit_item.connect(
            "activate",
            lambda _widget: self.on_quit(),
        )

        menu.append(
            quit_item
        )

        menu.show_all()

        self.indicator.set_menu(
            menu
        )

    # =================================================================
    # Estado
    # =================================================================

    def set_paused(
        self,
        paused,
    ):

        self.paused = paused

        if not self.available:

            return

        label = ""

        if self.paused:

            label = "Pausado"

        elif self.muted:

            label = "Silenciado"

        self.indicator.set_label(
            label,
            "",
        )

        self._sync_pause_item()

    def set_muted(self, muted):
        """Refleja el estado del silencio en el menú de la bandeja."""

        self.muted = muted

        if not self.available:

            return

        label = "Activar sonido" if muted else "Silenciar"

        try:

            self.mute_item.set_label(label)

            self.mute_item.set_sensitive(not muted)

        except (AttributeError, TypeError):

            pass

        if not self.paused:

            self.indicator.set_label(
                "Silenciado" if muted else "",
                "",
            )

    def _on_mute_activated(self):
        """Callback del elemento de menú que silencia el audio."""

        if hasattr(self, "on_mute_game"):

            self.on_mute_game()

    def _sync_pause_item(self):
        """Actualiza la etiqueta del elemento de pausa."""

        if not self.available:

            return

        try:

            self.pause_item.set_label(
                "Reanudar" if self.paused else "Pausar"
            )

        except (AttributeError, TypeError):

            pass

    def show(self):

        if not self.available:

            return
