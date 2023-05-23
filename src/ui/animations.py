from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import time


def resize_animation_master(window, current_width, current_height, target_width, target_height, duration, steps):
    step_time = duration // steps

    def update_size(step):
        if step < steps:
            width = current_width + (target_width - current_width) * (step + 1) // steps
            height = current_height + (target_height - current_height) * (step + 1) // steps
            window.resize(width, height)
            GLib.timeout_add(step_time, update_size, step + 1)

    update_size(0)


def rotate_animation_master(button, direction: str, current_angle, duration, steps):
    step_time = duration // steps

    def rotate(step):
        if step < steps:
            angle = current_angle + ((180 if direction == "left" else -180) - current_angle) * (step + 1) // steps
            button.get_child().set_angle(angle)
            GLib.timeout_add(step_time, rotate, step + 1)

    rotate(0)


def app_start_animation(window):
    resize_animation_master(window, 0, 0, list(window.get_size())[0], list(window.get_size())[1], 250, 60)


def settings_icon_rotate_left_animation(button):
    rotate_animation_master(button, "left", 0, 300, 40)


def settings_icon_rotate_right_animation(button):
    rotate_animation_master(button, "right", 0, 300, 40)


def show_settings_if_minimized_window_animation(window):
    resize_animation_master(window, list(window.get_size())[0], list(window.get_size())[1], list(window.get_size())[0],
                            list(window.get_size())[1] + 545, 400, 40)


def hide_settings_if_minimized_window_animation(window):
    resize_animation_master(window, list(window.get_size())[0], list(window.get_size())[1], list(window.get_size())[0],
                            list(window.get_size())[1] - 545, 400, 40)


def arrow_button_rotate_up_animation(window, button, fixed):
    button.set_label("^")
    fixed.move(button, 385, 87)

    resize_animation_master(window, list(window.get_size())[0], list(window.get_size())[1], list(window.get_size())[0],
                            list(window.get_size())[1] + 545, 400, 40)


def arrow_button_rotate_down_animation(window, button, fixed):
    button.set_label("^")
    button.get_child().set_angle(180)
    fixed.move(button, 385, 72)

    resize_animation_master(window, list(window.get_size())[0], list(window.get_size())[1], list(window.get_size())[0],
                            list(window.get_size())[1] - 545, 400, 40)



