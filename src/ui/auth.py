import threading
import cairo
import gi
import sys

import api.abstract, api.tinkoff_invest_api

from ui.view import TinkleUI

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

from ui import animations
from ui.static.ui_colors import *


class TinkleAuth(Gtk.Window):

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

        self.image = Gtk.Image()

        self.image.set_from_file("./ui/static/logo100.png")

        self.entry = Gtk.Entry()
        self.entry.set_width_chars(20)
        self.entry.set_size_request(-1, 40)
        self.fixed.put(self.entry, 130, 370)

        self.fixed.put(self.image, 200, 180)

        self.entry.set_placeholder_text("token")

        self.add(self.overlay)
        self.overlay.add_overlay(self.draw_area)
        self.overlay.add_overlay(self.fixed)

        self.draw_area.connect("draw", self.draw_background)
        self.entry.connect("activate", self.on_entry_activated)
        self.connect("delete-event", Gtk.main_quit)

        self.create_empty_buttons()
        # self.show_arrow_button("ssss")

        self.no_accs = ""
        self.accounts = []
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

    def text(self, cr):
        self.show_text(cr, MAIN_TEXT_COLOR, 24, "bold", (205, 320), "TINKLE")
        self.show_text(cr, SECONDARY_TEXT_COLOR, 16, "bold", (115, 470), self.no_accs)

    def create_empty_buttons(self):
        self.portfolio_name_1 = Gtk.ToggleButton(label='')
        portfolio_name_1_context = self.portfolio_name_1.get_style_context()
        self.portfolio_name_1.connect("clicked", self.button_name_1_clicked)
        portfolio_name_1_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        portfolio_name_1_context.add_class("portfolio_name_button")
        self.fixed.put(self.portfolio_name_1, 200, 440)

        self.portfolio_name_2 = Gtk.ToggleButton(label='')
        self.portfolio_name_2.connect("clicked", self.button_name_2_clicked)
        portfolio_name_2_context = self.portfolio_name_2.get_style_context()
        portfolio_name_2_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        portfolio_name_2_context.add_class("portfolio_name_button")
        self.fixed.put(self.portfolio_name_2, 200, 500)

        self.portfolio_name_3 = Gtk.ToggleButton(label='')
        self.portfolio_name_3.connect("clicked", self.button_name_3_clicked)
        portfolio_name_3_context = self.portfolio_name_3.get_style_context()
        portfolio_name_3_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        portfolio_name_3_context.add_class("portfolio_name_button")
        self.fixed.put(self.portfolio_name_3, 200, 560)

        self.portfolio_name_4 = Gtk.ToggleButton(label='')
        self.portfolio_name_4.connect("clicked", self.button_name_4_clicked)
        portfolio_name_4_context = self.portfolio_name_4.get_style_context()
        portfolio_name_4_context.add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        portfolio_name_4_context.add_class("portfolio_name_button")
        self.fixed.put(self.portfolio_name_4, 200, 620)

    def button_name_1_clicked(self, *kwargs):
        api.tinkoff_invest_api.set_main_account(self.accounts[0][0])
        self.destroy()
        t = TinkleUI()
        Gtk.main()

    def button_name_2_clicked(self, *kwargs):
        api.tinkoff_invest_api.set_main_account(self.accounts[1][0])
        self.destroy()
        t = TinkleUI()
        Gtk.main()

    def button_name_3_clicked(self, *kwargs):
        api.tinkoff_invest_api.set_main_account(self.accounts[2][0])
        self.destroy()
        t = TinkleUI()
        Gtk.main()

    def button_name_4_clicked(self, *kwargs):
        api.tinkoff_invest_api.set_main_account(self.accounts[3][0])
        self.destroy()
        t = TinkleUI()
        Gtk.main()

    def on_entry_activated(self, entry):
        api.tinkoff_invest_api.set_token(entry.get_text())
        self.accounts = api.abstract.get_accountss()
        if self.accounts is None:
            self.no_accs = "У вас нет доступных аккаунтов"
        try:
            self.portfolio_name_1.set_label(self.accounts[0][1])
            self.portfolio_name_2.set_label(self.accounts[1][1])
            self.portfolio_name_3.set_label(self.accounts[2][1])
            self.portfolio_name_4.set_label(self.accounts[3][1])
        except:
            pass

    def draw_background(self, widget, cr):
        self.painter(cr, BG_DARK_COLOR, True, 0, 0, list(self.get_size())[0] - 10, list(self.get_size())[1])
        self.painter(cr, BLOCKS_DARK_COLOR, False, 20, 20, 450, 670)

        self.text(cr)
