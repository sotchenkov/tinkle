import api.abstract
from ui.view import TinkleUI
from ui.auth import TinkleAuth
from api import abstract

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


def letsstart():
    if api.abstract.check_environment() == "NoToken":
        tinkle = TinkleAuth()
    else:
        tinkle_auth = TinkleUI()

    Gtk.main()


def start_ui():
    tinkle_auth = TinkleUI()
    Gtk.main()


if __name__ == '__main__':
    # threading.Thread(target=letsstart).start()
    letsstart()
# ToDo: Добавить сюда потоки
