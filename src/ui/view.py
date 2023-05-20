import cairo
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib

from ui import animations
from ui.static.ui_colors import *

COST = 10292596
CHANGE = 3444.23
PERSENTS = "10.1%"


def which_color_bg(num) -> ():
    return TEXT_BG_RED_COLOR if num < 0 else TEXT_BG_GREEN_COLOR


def which_color_text(num) -> ():
    return TEXT_RED_COLOR if num < 0 else TEXT_GREEN_COLOR


def pretty_str_from_float(float_num) -> str:
    return '{0:,}'.format(float_num).replace(',', ' ').replace('.', ',')


def change_cost_bg_size(change_num):
    return len(str(change_num)) * 11 + 110


def check_frame(num, window_size):
    return change_cost_bg_size(num) + 70, 105


class TinkleUI(Gtk.Window):

    def __init__(self):
        super().__init__(title="tinkle")

        mon_geom = self.get_screen().get_display().get_primary_monitor().get_geometry()
        screen_size = [mon_geom.width - mon_geom.x, mon_geom.height - mon_geom.y]

        self.set_default_size(500, 710)
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)  # widget features
        self.set_app_paintable(True)
        self.set_visual(Gdk.Screen.get_default().get_rgba_visual())  # transparent
        self.move(screen_size[0] - 500, 35)

        self.draw_area, self.css_provider, self.fixed, self.overlay = Gtk.DrawingArea(), Gtk.CssProvider(), \
            Gtk.Fixed(), Gtk.Overlay()

        self.css_provider.load_from_path("./ui/static/css/style.css")  # style for buttons

        self.add(self.overlay)
        self.overlay.add_overlay(self.draw_area)
        self.overlay.add_overlay(self.fixed)

        self.draw_area.connect("draw", self.draw_background)
        self.connect("delete-event", Gtk.main_quit)

        self.show_arrow_button()
        self.show_settings_button()

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

        cr.fill()
        self.queue_draw()

    def show_text(self, cr: cairo.Context, rgba: tuple, size: int, coordinates: tuple, text: str) -> None:
        cr.select_font_face("San Francisco", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_source_rgba(*rgba)
        cr.set_font_size(size)
        cr.move_to(*coordinates)
        cr.show_text(str(text))

    def show_arrow_button(self):
        self.arrow_button = Gtk.ToggleButton(label="^")
        self.arrow_button.set_size_request(100, 50)

        arrow_button_context = self.arrow_button.get_style_context()
        arrow_button_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        arrow_button_context.add_class("transparent_button")

        self.fixed.put(self.arrow_button, 385, 87)

        self.arrow_button.connect("clicked", self.on_click_me_clicked, self.fixed)

    def show_settings_button(self):
        settings_button = Gtk.ToggleButton(label="⚙")
        settings_button.set_size_request(100, 50)

        settings_button_context = settings_button.get_style_context()
        settings_button_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        settings_button_context.add_class("settings_btn")

        self.fixed.put(settings_button, 385, 40)

        settings_button.connect("clicked", self.on_click_settings_btn, self.fixed)

    def draw_background(self, widget, cr):
        self.painter(cr, BG_DARK_COLOR, True, 0, 0, list(self.get_size())[0] - 10, list(self.get_size())[1])
        self.painter(cr, BLOCKS_DARK_COLOR, False, 20, 20, 450, 125)
        self.painter(cr, BLOCKS_DARK_COLOR, False, 20, 165, 450, 525)
        self.painter(cr, which_color_bg(CHANGE), False, 45, 90, change_cost_bg_size(CHANGE), 25, 10)
        # 168
        self.draw_text(cr)

    def draw_text(self, cr):
        self.show_text(cr, MAIN_TEXT_COLOR, 28, (45, 75), pretty_str_from_float(COST) + ROUBLE)
        self.show_text(cr, which_color_text(CHANGE), 16, (63, 108), pretty_str_from_float(CHANGE) + DOT + PERSENTS)
        self.show_text(cr, SECONDARY_TEXT_COLOR, 16, check_frame(CHANGE, self.get_size()), "за всё время")

    def on_click_settings_btn(self, button, *kwargs):
        if button.get_active():
            self.current_size = list(self.get_size())[1]
            self.arrow_button.hide()

            animations.settings_icon_rotate_left_animation(button)

            self.draw_area.connect("draw", self.draw_settings_menu_background)

            if list(self.get_size())[1] == 165:
                animations.show_settings_if_minimized_window_animation(self)

        else:
            if list(self.get_size())[1] == 710 and self.current_size == 165:
                animations.hide_settings_if_minimized_window_animation(self)

            self.arrow_button.show()

            animations.settings_icon_rotate_right_animation(button)

            self.draw_area.connect("draw", self.draw_background)
            self.queue_draw()

    def draw_settings_menu_background(self, widget, cr):
        self.painter(cr, SETTINGS_BG_COLOR, False, 20, 20, list(self.get_size())[0] - 50,
                     list(self.get_size())[1] - 40)

    def on_click_me_clicked(self, button, fixed):
        if list(self.get_size())[1] == 710:
            if button.get_active():
                animations.arrow_button_rotate_down_animation(self, button, fixed)
                self.draw_area.connect("draw", self.draw_background)

        else:
            if list(self.get_size())[1] == 165:
                animations.arrow_button_rotate_up_animation(self, button, fixed)


win = TinkleUI()
Gtk.main()
