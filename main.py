import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class Window(Gtk.Window):

    def __init__(self):
        super().__init__(title="aaaaa")

        # Set window properties
        self.set_default_size(500, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)
        # self.set_skip_pager_hint(True)
        # self.set_modal(True)
        self.set_app_paintable(True)

        # Connect signals
        self.connect("delete-event", Gtk.main_quit)

        # Set opacity
        # self.set_opacity(0.4)
        self.set_visual(Gdk.Screen.get_default().get_rgba_visual())

        self.draw_area = Gtk.DrawingArea()
        self.draw_area.connect("draw", self.on_draw)
        self.add(self.draw_area)

        # self.connect("draw", self.on_draw)
        self.show_all()
        self.move(1660, 35)

        # set window transparent
        # self.set_app_paintable(True)
        # self.set_visual(self.get_rgba_visual())
        # self.connect("draw", self.transparent_bckg)

    def on_draw(self, widget, cr):
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(0, 0, 0.5, 0.5)
        cr.set_operator(cairo.OPERATOR_DEST_OVER)
        cr.paint()

    def transparent_bckg(self, widget, cr):
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        return False


win = Window()
Gtk.main()
