import cairo
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib

from src.ui import animations

COST = "10 292 596,24 ₽"
CHANGE = "–395,2 ₽ · 1,45%"


class TinleUI(Gtk.Window):

    def __init__(self):
        super().__init__(title="tinkle")

        # Свойства окна
        self.set_default_size(500, 710)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)
        self.set_app_paintable(True)

        # Подключение сигналов
        self.connect("delete-event", Gtk.main_quit)

        # Прозрачность
        self.set_visual(Gdk.Screen.get_default().get_rgba_visual())

        self.draw_area = Gtk.DrawingArea()
        self.draw_area.connect("draw", self.draw_background)

        # Create a label
        label = Gtk.Label()

        # Create an EventBox and add the label to it
        event_box = Gtk.EventBox()

        event_box.add(label)

        self.button = Gtk.ToggleButton(label="^")
        self.button.set_size_request(100, 50)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./ui/static/css/style.css")

        # Apply the CSS style to the button
        context = self.button.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context.add_class("transparent_button")
        fixed = Gtk.Fixed()
        fixed.put(self.button, 385, 87)
        self.button.connect("clicked", self.on_click_me_clicked, fixed)

        button1 = Gtk.ToggleButton(label="⚙")
        button1.set_size_request(100, 50)

        # Apply the CSS style to the button
        context1 = button1.get_style_context()
        context1.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context1.add_class("settings_btn")
        fixed.put(button1, 385, 40)
        button1.connect("clicked", self.on_click_settings_btn, fixed)

        # Create an overlay and add the drawing area and label to it
        self.overlay = Gtk.Overlay()
        self.add(self.overlay)
        self.overlay.add_overlay(self.draw_area)
        self.overlay.add_overlay(fixed)

        screen = self.get_screen()
        mon_geom = screen.get_display().get_primary_monitor().get_geometry()
        screen_size = [mon_geom.width - mon_geom.x, mon_geom.height - mon_geom.y]

        self.move(screen_size[0] - 500, 35)
        self.show_all()

        animations.app_start_animation(self)

    def painter(self, cr: cairo.Context, rgba: tuple, clear: bool, x: int, y: int, width: int, height: int,
                radius=25) -> None:
        if clear:
            cr.set_operator(cairo.OPERATOR_CLEAR)
            cr.paint()
            cr.set_operator(cairo.OPERATOR_OVER)

        cr.set_source_rgba(*rgba)

        # скругление углов прямоугольника
        cr.move_to(x + radius, y)
        cr.arc(x + width - radius, y + radius, radius, -90 * (3.14 / 180), 0 * (3.14 / 180))
        cr.arc(x + width - radius, y + height - radius, radius, 0 * (3.14 / 180), 90 * (3.14 / 180))
        cr.arc(x + radius, y + height - radius, radius, 90 * (3.14 / 180), 180 * (3.14 / 180))
        cr.arc(x + radius, y + radius, radius, 180 * (3.14 / 180), 270 * (3.14 / 180))
        cr.close_path()

        # отрисовка прямоугольника
        cr.fill()
        self.queue_draw()

    def show_text(self, cr: cairo.Context, rgba: tuple, size: int, coordinates: tuple, text: str) -> None:
        cr.select_font_face("San Francisco", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_source_rgba(*rgba)
        cr.set_font_size(size)
        cr.move_to(*coordinates)
        cr.show_text(text)

    def draw_background(self, widget, cr):
        self.painter(cr, (0, 0, 0.5, 0.5), True, 0, 0, list(self.get_size())[0] - 10, list(self.get_size())[1])
        self.painter(cr, (0, 0, 0.5, 0.9), False, 20, 20, 450, 125)
        self.painter(cr, (0, 0, 0.5, 0.9), False, 20, 165, 450, 525)
        self.painter(cr, (0.9, 0, 0, 0.4), False, 45, 90, 168, 25, 10)

        self.draw_text(cr)

    def draw_text(self, cr):
        self.show_text(cr, (0.9, 0.9, 0.9, 0.9), 28, (45, 75), COST)
        self.show_text(cr, (.8, 0, 0, 0.9), 16, (63, 108), CHANGE)
        self.show_text(cr, (0.9, 0.9, 0.9, 0.5), 16, (240, 107), "за всё время")

    def on_click_settings_btn(self, button, *kwargs):
        if button.get_active():
            self.current_size = list(self.get_size())[1]

            animations.settings_icon_rotate_left_animation(self, button)

            self.draw_area.connect("draw", self.draw_settings_menu_background)

            if list(self.get_size())[1] == 165:
                animations.show_settings_if_minimized_window_animation(self)

        else:
            if list(self.get_size())[1] == 710 and self.current_size == 165:
                animations.hide_settings_if_minimized_window_animation(self)

            self.button.show()

            animations.settings_icon_rotate_right_animation(self, button)

            self.draw_area.connect("draw", self.draw_background)
            self.queue_draw()

    def draw_settings_menu_background(self, widget, cr):
        self.painter(cr, (0.1, 0.1, 0.1, 0.97), False, 20, 20, list(self.get_size())[0] - 50,
                     list(self.get_size())[1] - 40)

    def on_click_me_clicked(self, button, fixed):
        if list(self.get_size())[1] == 710:
            if button.get_active():
                animations.arrow_button_rotate_down_animation(self, button, fixed)
                self.draw_area.connect("draw", self.draw_background)

        else:
            if list(self.get_size())[1] == 165:
                animations.arrow_button_rotate_up_animation(self, button, fixed)


win = TinleUI()
Gtk.main()
