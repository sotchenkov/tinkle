import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

COST = "29 596,24 ₽"
CHANGE = "–395,2 ₽ · 1,45%"


class Window(Gtk.Window):

    def __init__(self):
        super().__init__(title="tinkle")

        # Свойства окна
        self.set_default_size(500, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)
        # self.set_skip_pager_hint(True)
        # self.set_modal(True)
        self.set_app_paintable(True)

        # Подключение сигналов
        self.connect("delete-event", Gtk.main_quit)

        # Прозрачность
        # self.set_opacity(0.4)
        self.set_visual(Gdk.Screen.get_default().get_rgba_visual())

        self.draw_area = Gtk.DrawingArea()
        self.draw_area.connect("draw", self.on_draw)
        self.add(self.draw_area)

        screen = self.get_screen()
        mon_geom = screen.get_display().get_primary_monitor().get_geometry()
        screen_size = [mon_geom.width - mon_geom.x, mon_geom.height - mon_geom.y]

        self.move(screen_size[0] - 500, 35)
        self.show_all()

    def on_draw(self, widget, cr):
        # cr.set_operator(cairo.OPERATOR_SOURCE)
        # cr.set_source_rgba(0, 0, 0.5, 0.5)
        # cr.set_operator(cairo.OPERATOR_DEST_OVER)
        # cr.paint()

        # заливка цветом фона
        # cr.set_operator(cairo.OPERATOR_SOURCE)
        # cr.set_source_rgba(0, 0, 0.5, 0.5)
        # cr.set_operator(cairo.OPERATOR_DEST_OVER)
        # cr.fill()

        # размеры холста
        WIDTH, HEIGHT = 500, 700

        # координаты прямоугольника и радиус скругления углов
        x, y, width, height, radius = 0, 0, 490, 700, 25

        # настройка цвета обводки и заливки прямоугольника
        # cr.set_source_rgb(100, 100, 100)
        cr.set_source_rgba(0, 0, 0.5, 0.5)
        # cr.set_line_width(5)

        # скругление углов прямоугольника
        cr.move_to(x + radius, y)
        cr.arc(x + width - radius, y + radius, radius, -90 * (3.14 / 180), 0 * (3.14 / 180))
        cr.arc(x + width - radius, y + height - radius, radius, 0 * (3.14 / 180), 90 * (3.14 / 180))
        cr.arc(x + radius, y + height - radius, radius, 90 * (3.14 / 180), 180 * (3.14 / 180))
        cr.arc(x + radius, y + radius, radius, 180 * (3.14 / 180), 270 * (3.14 / 180))
        cr.close_path()

        # отрисовка прямоугольника
        cr.fill()

        self.draw_cost_background(cr)

    def draw_cost_background(self, cr):
        # координаты прямоугольника и радиус скругления углов
        x, y, width, height, radius = 20, 20, 450, 125, 25

        # настройка цвета обводки и заливки прямоугольника
        cr.set_source_rgba(0, 0, 0.5, 0.9)
        # cr.set_source_rgba(0, 0, 0.5, 0.5)
        # cr.set_line_width(5)

        # скругление углов прямоугольника
        cr.move_to(x + radius, y)
        cr.arc(x + width - radius, y + radius, radius, -90 * (3.14 / 180), 0 * (3.14 / 180))
        cr.arc(x + width - radius, y + height - radius, radius, 0 * (3.14 / 180), 90 * (3.14 / 180))
        cr.arc(x + radius, y + height - radius, radius, 90 * (3.14 / 180), 180 * (3.14 / 180))
        cr.arc(x + radius, y + radius, radius, 180 * (3.14 / 180), 270 * (3.14 / 180))
        cr.close_path()

        # отрисовка прямоугольника
        cr.fill()

        cr.set_source_rgba(0.9, 0.9, 0.9, 0.9)
        cr.select_font_face("San Francisco", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(28)
        cr.move_to(45, 75)
        cr.show_text(COST)

        cr.fill()

        self.draw_stocks_background(cr)

    def draw_stocks_background(self, cr):
        # координаты прямоугольника и радиус скругления углов
        x, y, width, height, radius = 20, 155, 450, 525, 25

        # настройка цвета обводки и заливки прямоугольника
        # cr.set_source_rgb(100, 100, 100)
        cr.set_source_rgba(0, 0, 0.5, 0.9)
        # cr.set_line_width(5)

        # скругление углов прямоугольника
        cr.move_to(x + radius, y)
        cr.arc(x + width - radius, y + radius, radius, -90 * (3.14 / 180), 0 * (3.14 / 180))
        cr.arc(x + width - radius, y + height - radius, radius, 0 * (3.14 / 180), 90 * (3.14 / 180))
        cr.arc(x + radius, y + height - radius, radius, 90 * (3.14 / 180), 180 * (3.14 / 180))
        cr.arc(x + radius, y + radius, radius, 180 * (3.14 / 180), 270 * (3.14 / 180))
        cr.close_path()

        # отрисовка прямоугольника
        cr.fill()

        self.draw_cost_change(cr)

    def draw_cost_change(self, cr):
        # координаты прямоугольника и радиус скругления углов
        x, y, width, height, radius = 45, 90, 186, 25, 10

        # настройка цвета обводки и заливки прямоугольника
        # cr.set_source_rgb(100, 100, 100)
        cr.set_source_rgba(0.9, 0, 0, 0.4)
        # cr.set_line_width(5)

        # скругление углов прямоугольника
        cr.move_to(x + radius, y)
        cr.arc(x + width - radius, y + radius, radius, -90 * (3.14 / 180), 0 * (3.14 / 180))
        cr.arc(x + width - radius, y + height - radius, radius, 0 * (3.14 / 180), 90 * (3.14 / 180))
        cr.arc(x + radius, y + height - radius, radius, 90 * (3.14 / 180), 180 * (3.14 / 180))
        cr.arc(x + radius, y + radius, radius, 180 * (3.14 / 180), 270 * (3.14 / 180))
        cr.close_path()

        # отрисовка прямоугольника
        cr.fill()

        cr.set_source_rgba(0.8, 0, 0, 0.9)
        cr.select_font_face("San Francisco", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(16)
        cr.move_to(63, 108)
        cr.show_text(CHANGE)

        cr.fill()

        cr.set_source_rgba(0.9, 0.9, 0.9, 0.5)
        cr.select_font_face("San Francisco", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(16)
        cr.move_to(240, 107)
        cr.show_text("за всё время")

        cr.fill()

        cr.set_source_rgba(0.9, 0.9, 0.9, 0.5)
        cr.select_font_face("San Francisco", cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(32)
        cr.move_to(425, 75)
        cr.show_text("$")

        cr.fill()


win = Window()
Gtk.main()
