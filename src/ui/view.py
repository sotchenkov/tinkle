import threading
import cairo
import gi

import api.abstract

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

from ui import animations
from ui.static.ui_colors import *


def which_color_bg(num) -> ():
    return TEXT_BG_RED_COLOR if num < 0 else TEXT_BG_GREEN_COLOR


def which_color_text(num) -> ():
    return TEXT_RED_COLOR if num < 0 else TEXT_GREEN_COLOR


def pretty_str_from_float(float_num) -> str:
    return '{0:,}'.format(float_num).replace(',', ' ').replace('.', ',')


def change_cost_bg_size(change_num):
    return change_num * 10 + 28


def check_frame(num, window_size):
    if num + 60 < window_size - 200:
        return num + 60, 106
    else:
        return 50, 135


def call_repeatedly(interval, func, *args):
    stopped = threading.Event()

    def loop():
        while not stopped.wait(interval):  # the first call is in `interval` secs
            func(*args)

    threading.Thread(target=loop).start()
    return stopped.set


class TinkleUI(Gtk.Window):

    def __init__(self):
        super().__init__(title="tinkle")
        mon_geom = self.get_screen().get_display().get_primary_monitor().get_geometry()
        self.screen_size = [mon_geom.width - mon_geom.x, mon_geom.height - mon_geom.y]

        self.set_default_size(500, 710)
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)  # widget features
        self.set_app_paintable(True)
        self.set_visual(Gdk.Screen.get_default().get_rgba_visual())  # transparent
        self.move(self.screen_size[0] - 500, 35)

        self.draw_area, self.css_provider, self.fixed, self.overlay = Gtk.DrawingArea(), Gtk.CssProvider(), \
            Gtk.Fixed(), Gtk.Overlay()

        self.css_provider.load_from_path("./ui/static/css/style.css")  # style for buttons

        self.image = Gtk.Image()

        self.add(self.overlay)
        self.overlay.add_overlay(self.draw_area)
        self.overlay.add_overlay(self.fixed)

        self.draw_area.connect("draw", self.draw_background)
        self.connect("delete-event", Gtk.main_quit)

        self.show_arrow_button()
        self.show_settings_button()
        self.show_position_change_buttons()
        self.show_logout_button()
        self.show_instruments_preloader()

        self.cost = 0.0
        self.change = 0.0
        self.change_precents = 0.0
        self.change_len = 0
        self.instruments = [[] * 5]

        self.update_portfolio_cost()
        call_repeatedly(3, self.update_portfolio_cost)
        self.loading = threading.Thread(target=self.instruments_checker).start()
        animations.app_start_animation(self)
        self.show_all()

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

    def show_text(self, cr: cairo.Context, rgba: tuple, size: int, font_weight: str, coordinates: tuple,
                  text: str) -> None:
        if font_weight == "normal":
            cr.select_font_face("San Francisco", cairo.FONT_SLANT_NORMAL,
                                cairo.FONT_WEIGHT_NORMAL)
        else:
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

    def show_position_change_buttons(self):
        self.move_left_up_button = Gtk.ToggleButton(label="▢")
        self.move_left_up_button.set_size_request(100, 50)
        settings_button_context = self.move_left_up_button.get_style_context()
        settings_button_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        settings_button_context.add_class("change_position_button")
        self.move_left_up_button.connect("clicked", self.move_left_up)

        self.move_right_down_button = Gtk.ToggleButton(label="▢")
        self.move_right_down_button.set_size_request(100, 50)
        settings_button_context = self.move_right_down_button.get_style_context()
        settings_button_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        settings_button_context.add_class("change_position_button")
        self.move_right_down_button.connect("clicked", self.move_right_down)

        self.move_right_up_button = Gtk.ToggleButton(label="▢")
        self.move_right_up_button.set_size_request(100, 50)
        settings_button_context = self.move_right_up_button.get_style_context()
        settings_button_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        settings_button_context.add_class("change_position_button")
        self.move_right_up_button.connect("clicked", self.move_right_up)

        self.move_left_down_button = Gtk.ToggleButton(label="▢")
        self.move_left_down_button.set_size_request(100, 50)
        settings_button_context = self.move_left_down_button.get_style_context()
        settings_button_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        settings_button_context.add_class("change_position_button")
        self.move_left_down_button.connect("clicked", self.move_left_down)

    def move_left_up(self, *kwargs):
        self.move(10, 35)

    def move_right_down(self, *kwargs):
        self.move(self.screen_size[0] - 500, self.screen_size[1] - 717)

    def move_right_up(self, *kwargs):
        self.move(self.screen_size[0] - 500, 35)

    def move_left_down(self, *kwargs):
        self.move(10, self.screen_size[1] - 717)

    def show_logout_button(self):
        self.loguot_button = Gtk.ToggleButton(label="logout")
        self.loguot_button.set_size_request(100, 50)
        settings_button_context = self.loguot_button.get_style_context()
        settings_button_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        settings_button_context.add_class("portfolio_name_button")
        self.loguot_button.connect("clicked", self.logout_clicked)

    def logout_clicked(self, *kwargs):
        from ui.auth import TinkleAuth
        self.destroy()
        t = TinkleAuth()
        Gtk.main()
        api.abstract.logout()

    def show_instruments_preloader(self):
        pixbufanim = GdkPixbuf.PixbufAnimation.new_from_file("./ui/static/loader.gif")
        self.image.set_from_animation(pixbufanim)
        self.fixed.put(self.image, 230, 380)

    def draw_background(self, widget, cr):
        self.painter(cr, BG_DARK_COLOR, True, 0, 0, list(self.get_size())[0] - 10, list(self.get_size())[1])
        self.painter(cr, BLOCKS_DARK_COLOR, False, 20, 20, 450, 125)
        self.painter(cr, BLOCKS_DARK_COLOR, False, 20, 165, 450, 525)
        self.painter(cr, which_color_bg(self.change), False, 45, 90, change_cost_bg_size(self.change_len), 25, 10)
        # 168

        self.draw_text(cr)

    def draw_text(self, cr):
        self.show_text(cr, MAIN_TEXT_COLOR, 28, "bold", (45, 75), pretty_str_from_float(self.cost) + ROUBLE)
        self.show_text(cr, which_color_text(self.change), 16, "bold", (63, 108),
                       pretty_str_from_float(self.change) + NORMAL_DOT + pretty_str_from_float(
                           self.change_precents) + "%")
        self.change_len = len(pretty_str_from_float(self.change) + NORMAL_DOT + pretty_str_from_float(
            self.change_precents) + "%")
        self.show_text(cr, SECONDARY_TEXT_COLOR, 16, "bold",
                       check_frame(change_cost_bg_size(self.change_len), self.get_size()[0]), "за всё время")

        instr_len = len(self.instruments[0])
        for i in range(instr_len):
            self.show_text(cr, MAIN_TEXT_COLOR, 20, "bold", (45, 210 + i * 85), self.instruments[i]["name"])
            cost_ints = pretty_str_from_float(self.instruments[i]["position_cost"]) + ROUBLE
            self.show_text(cr, MAIN_TEXT_COLOR, 20, "normal", (-cr.text_extents(cost_ints).width + 460, 210 + i * 85),
                           cost_ints)
            self.show_text(cr, SECONDARY_TEXT_COLOR, 16, "normal", (45, 235 + i * 85),
                           str(self.instruments[i]["quantity"]) + " шт." + BOLD_DOT + pretty_str_from_float(
                               self.instruments[i]["current_price"]) + ROUBLE)
            change = pretty_str_from_float(
                self.instruments[i]["cost_change"]) + ROUBLE + NORMAL_DOT + pretty_str_from_float(
                (self.instruments[i]["cost_change_percents"])) + "%"
            self.show_text(cr, which_color_text(self.instruments[i]["cost_change"]), 16, "normal",
                           (-cr.text_extents(change).width + 450, 235 + i * 85), change)

    def on_click_settings_btn(self, button, *kwargs):
        if button.get_active():
            self.current_size = list(self.get_size())[1]

            animations.settings_icon_rotate_left_animation(button)

            self.arrow_button.hide()

            self.fixed.put(self.move_right_down_button, 240, 330)
            self.fixed.put(self.move_left_up_button, 160, 260)
            self.fixed.put(self.move_right_up_button, 240, 260)
            self.fixed.put(self.move_left_down_button, 160, 330)
            self.move_left_up_button.show()
            self.move_right_down_button.show()
            self.move_right_up_button.show()
            self.move_left_down_button.show()

            self.fixed.put(self.loguot_button, 200, 610)
            self.loguot_button.show()

            self.draw_area.connect("draw", self.draw_settings_menu_background)

            if list(self.get_size())[1] == 165:
                animations.show_settings_if_minimized_window_animation(self)

        else:
            if list(self.get_size())[1] == 710 and self.current_size == 165:
                animations.hide_settings_if_minimized_window_animation(self)

            self.arrow_button.show()
            self.fixed.remove(self.move_left_up_button)
            self.fixed.remove(self.move_right_down_button)
            self.fixed.remove(self.move_left_down_button)
            self.fixed.remove(self.move_right_up_button)
            self.fixed.remove(self.loguot_button)

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

    def update_portfolio_cost(self):
        content = api.abstract.portfolio_cost()
        self.cost = content[0]
        self.change = content[1]
        self.change_precents = content[2]

    def update_instruments_cost(self):
        self.instruments = api.abstract.instruments_cost()

    def instruments_checker(self):
        l = api.abstract.instruments_cost()
        while len(l) == 0:
            pass
        self.update_instruments_cost()
        call_repeatedly(3, self.update_instruments_cost)

        self.image.hide()
