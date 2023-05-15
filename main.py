import cairo
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GLib

COST = "10 292 596,24 ₽"
CHANGE = "–395,2 ₽ · 1,45%"


class Window(Gtk.Window):

    def __init__(self):
        super().__init__(title="tinkle")

        # Свойства окна
        self.set_default_size(500, 710)
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

        # Create a label
        label = Gtk.Label()

        # Create an EventBox and add the label to it
        event_box = Gtk.EventBox()

        # event_box.set_size_request(50, 70)
        event_box.add(label)

        ########BUTTON1#######
        self.button = Gtk.ToggleButton(label="^")
        self.button.set_size_request(100, 50)

        # button.get_child().set_angle(180)
        # Load the CSS file
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style.css")

        # Apply the CSS style to the button
        context = self.button.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context.add_class("transparent_button")
        fixed = Gtk.Fixed()
        fixed.put(self.button, 385, 87)
        self.button.connect("clicked", self.on_click_me_clicked, fixed)
        ###############

        ########BUTTON2#######
        button1 = Gtk.ToggleButton(label="⚙")
        button1.set_size_request(100, 50)
        # button.get_child().set_angle(180)
        # Load the CSS file
        # css_provider = Gtk.CssProvider()
        # css_provider.load_from_path("style.css")

        # Apply the CSS style to the button
        context1 = button1.get_style_context()
        context1.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context1.add_class("settings_btn")
        # fixed1 = Gtk.Fixed()
        fixed.put(button1, 385, 40)
        button1.connect("clicked", self.on_click_settings_btn, fixed)

        # Create an overlay and add the drawing area and label to it
        self.overlay = Gtk.Overlay()
        self.add(self.overlay)
        self.overlay.add_overlay(self.draw_area)
        self.overlay.add_overlay(fixed)
        # overlay.add_overlay(fixed1)

        screen = self.get_screen()
        mon_geom = screen.get_display().get_primary_monitor().get_geometry()
        screen_size = [mon_geom.width - mon_geom.x, mon_geom.height - mon_geom.y]

        self.move(screen_size[0] - 500, 35)
        self.show_all()
        self.lunch_animation()

    def on_click_settings_btn(self, button, fixed, *kwargs):
        if button.get_active():
            self.current_size = list(self.get_size())[1]
            self.button.hide()

            # button.set_label("⚙")
            current_angle = 0
            duration = 300  # Duration of the animation in milliseconds
            steps = 40
            step_time = duration // steps

            # fixed.move(button, 415, 80)
            def update_draw(step):
                if step < steps:
                    angle = current_angle + (180 - current_angle) * (step + 1) // steps
                    button.get_child().set_angle(angle)
                    GLib.timeout_add(step_time, update_draw, step + 1)

            update_draw(0)
            self.draw_area.connect("draw", self.draw_settings_menu_background)
            self.draw_settings_menu_animation()
            # Add any additional actions or visual changes here

            if list(self.get_size())[1] == 165:

                current_width, current_height = self.get_size()
                target_width, target_height = current_width, current_height + 545
                duration = 400  # Duration of the animation in milliseconds
                steps = 40
                step_time = duration // steps

                def update_size(step):
                    if step < steps:
                        width = current_width + (target_width - current_width) * (step + 1) // steps
                        height = current_height + (target_height - current_height) * (step + 1) // steps
                        self.resize(width, height)
                        GLib.timeout_add(step_time, update_size, step + 1)

                print("2")
                update_size(0)
        else:
            print("imcolling")
            if list(self.get_size())[1] == 710 and self.current_size == 165:
                current_width, current_height = self.get_size()
                target_width, target_height = current_width, current_height - 545
                duration = 400  # Duration of the animation in milliseconds
                steps = 40
                step_time = duration // steps

                def update_size(step):
                    if step < steps:
                        width = current_width + (target_width - current_width) * (step + 1) // steps
                        height = current_height + (target_height - current_height) * (step + 1) // steps
                        self.resize(width, height)
                        GLib.timeout_add(step_time, update_size, step + 1)

                print("1")
                update_size(0)
                # self.clear()
                # self.draw_area.connect("draw", self.on_draw)
            self.button.show()

            current_angle = 0
            duration = 300  # Duration of the animation in milliseconds
            steps = 40
            step_time = duration // steps

            # fixed.move(button, 415, 80)
            def update_draw(step):
                if step < steps:
                    angle = current_angle + (-180 + current_angle) * (step + 1) // steps
                    button.get_child().set_angle(angle)
                    GLib.timeout_add(step_time, update_draw, step + 1)

            update_draw(0)
            self.draw_area.connect("draw", self.on_draw)
            self.queue_draw()

    def draw_settings_menu_background(self, widget, cr):
        # cr.set_operator(cairo.OPERATOR_CLEAR)
        # cr.paint()
        # cr.set_operator(cairo.OPERATOR_OVER)
        # координаты прямоугольника и радиус скругления углов

        x, y, width, height, radius = 20, 20, list(self.get_size())[0]-50, list(self.get_size())[1]-40, 25
        cr.set_source_rgba(0.1, 0.1, 0.1, 0.97)

        # настройка цвета обводки и заливки прямоугольника

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

    def draw_settings_menu_animation(self):
        pass

        # current_width, current_height = 0, 0
        # target_width, target_height = self.get_size()
        # duration = 400  # Duration of the animation in milliseconds
        # steps = 40
        # step_time = duration // steps
        #
        # def update_size(step):
        #     if step < steps:
        #         width = current_width + (target_width - current_width) * (step + 1) // steps
        #         height = current_height + (target_height - current_height) * (step + 1) // steps
        #         self.resize(width, height)
        #         GLib.timeout_add(step_time, update_size, step + 1)
        #
        # print("2")
        # update_size(0)

    def on_click_me_clicked(self, button, fixed, *kwargs):
        if list(self.get_size())[1] == 710:
            if button.get_active():
                # self.resize(500, 500)
                button.set_label("^")
                button.get_child().set_angle(180)
                fixed.move(button, 385, 72)
                # fixed.put(button, 385, 87)

                current_width, current_height = self.get_size()
                target_width, target_height = current_width, current_height - 545
                duration = 400  # Duration of the animation in milliseconds
                steps = 40
                step_time = duration // steps

                def update_size(step):
                    if step < steps:
                        width = current_width + (target_width - current_width) * (step + 1) // steps
                        height = current_height + (target_height - current_height) * (step + 1) // steps
                        self.resize(width, height)
                        GLib.timeout_add(step_time, update_size, step + 1)

                print("1")
                update_size(0)
                # self.clear()
                self.draw_area.connect("draw", self.on_draw)

            # Add any additional actions or visual changes here
        else:
            if list(self.get_size())[1] == 165:
                button.set_label("^")
                fixed.move(button, 385, 87)

                current_width, current_height = self.get_size()
                target_width, target_height = current_width, current_height + 545
                duration = 400  # Duration of the animation in milliseconds
                steps = 40
                step_time = duration // steps

                def update_size(step):
                    if step < steps:
                        width = current_width + (target_width - current_width) * (step + 1) // steps
                        height = current_height + (target_height - current_height) * (step + 1) // steps
                        self.resize(width, height)
                        GLib.timeout_add(step_time, update_size, step + 1)

                print("2")
                update_size(0)

    def on_draw(self, widget, cr):
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        # координаты прямоугольника и радиус скругления углов
        x, y, width, height, radius = 0, 0, list(self.get_size())[0] - 10, list(self.get_size())[1], 25

        # x, y, width, height, radius = 0, 0, 490, 165, 25
        # print(list(self.get_size())[0])

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
        self.queue_draw()

    def lunch_animation(self):
        current_width, current_height = 0, 0
        target_width, target_height = self.get_size()
        duration = 250  # Duration of the animation in milliseconds
        steps = 60
        step_time = duration // steps

        def update_size(step):
            if step < steps:
                width = current_width + (target_width - current_width) * (step + 1) // steps
                height = current_height + (target_height - current_height) * (step + 1) // steps
                self.resize(width, height)
                GLib.timeout_add(step_time, update_size, step + 1)

        print("2")
        update_size(0)

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
        x, y, width, height, radius = 20, 165, 450, 525, 25

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

        cr.fill()

        # отрисовка прямоугольника
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

        # cr.set_source_rgba(0.9, 0.9, 0.9, 0.5)
        # cr.select_font_face("San Francisco", cairo.FONT_SLANT_NORMAL,
        #                     cairo.FONT_WEIGHT_BOLD)
        # cr.set_font_size(32)
        # cr.move_to(425, 75)
        # cr.show_text("⚙")
        #
        # cr.fill()


win = Window()
Gtk.main()
