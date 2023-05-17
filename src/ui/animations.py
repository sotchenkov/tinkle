from gi.repository import Gtk, Gdk, GLib


def app_start_animation(window):
    current_width, current_height = 0, 0
    target_width, target_height = window.get_size()
    duration = 250  # Duration of the animation in milliseconds
    steps = 60
    step_time = duration // steps

    def update_size(step):
        if step < steps:
            width = current_width + (target_width - current_width) * (step + 1) // steps
            height = current_height + (target_height - current_height) * (step + 1) // steps
            window.resize(width, height)
            GLib.timeout_add(step_time, update_size, step + 1)

    update_size(0)


def settings_icon_rotate_left_animation(window, button):
    window.button.hide()

    current_angle = 0
    duration = 300  # Duration of the animation in milliseconds
    steps = 40
    step_time = duration // steps

    def update_draw(step):
        if step < steps:
            angle = current_angle + (180 - current_angle) * (step + 1) // steps
            button.get_child().set_angle(angle)
            GLib.timeout_add(step_time, update_draw, step + 1)

    update_draw(0)


def settings_icon_rotate_right_animation(window, button):
    current_angle = 0
    duration = 300  # Duration of the animation in milliseconds
    steps = 40
    step_time = duration // steps

    def update_draw(step):
        if step < steps:
            angle = current_angle + (-180 + current_angle) * (step + 1) // steps
            button.get_child().set_angle(angle)
            GLib.timeout_add(step_time, update_draw, step + 1)

    update_draw(0)


def show_settings_if_minimized_window_animation(window):
    current_width, current_height = window.get_size()
    target_width, target_height = current_width, current_height + 545
    duration = 400  # Duration of the animation in milliseconds
    steps = 40
    step_time = duration // steps

    def update_size(step):
        if step < steps:
            width = current_width + (target_width - current_width) * (step + 1) // steps
            height = current_height + (target_height - current_height) * (step + 1) // steps
            window.resize(width, height)
            GLib.timeout_add(step_time, update_size, step + 1)

    update_size(0)


def hide_settings_if_minimized_window_animation(window):
    current_width, current_height = window.get_size()
    target_width, target_height = current_width, current_height - 545
    duration = 400  # Duration of the animation in milliseconds
    steps = 40
    step_time = duration // steps

    def update_size(step):
        if step < steps:
            width = current_width + (target_width - current_width) * (step + 1) // steps
            height = current_height + (target_height - current_height) * (step + 1) // steps
            window.resize(width, height)
            GLib.timeout_add(step_time, update_size, step + 1)

    update_size(0)


def arrow_button_rotate_up_animation(window, button, fixed):
    button.set_label("^")
    fixed.move(button, 385, 87)

    current_width, current_height = window.get_size()
    target_width, target_height = current_width, current_height + 545
    duration = 400  # Duration of the animation in milliseconds
    steps = 40
    step_time = duration // steps

    def update_size(step):
        if step < steps:
            width = current_width + (target_width - current_width) * (step + 1) // steps
            height = current_height + (target_height - current_height) * (step + 1) // steps
            window.resize(width, height)
            GLib.timeout_add(step_time, update_size, step + 1)

    update_size(0)


def arrow_button_rotate_down_animation(window, button, fixed):
    button.set_label("^")
    button.get_child().set_angle(180)
    fixed.move(button, 385, 72)

    current_width, current_height = window.get_size()
    target_width, target_height = current_width, current_height - 545
    duration = 400  # Duration of the animation in milliseconds
    steps = 40
    step_time = duration // steps

    def update_size(step):
        if step < steps:
            width = current_width + (target_width - current_width) * (step + 1) // steps
            height = current_height + (target_height - current_height) * (step + 1) // steps
            window.resize(width, height)
            GLib.timeout_add(step_time, update_size, step + 1)

    update_size(0)
