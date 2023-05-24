import api.abstract
from ui.view import TinkleUI
from ui.auth import TinkleAuth
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


def start():
    if api.abstract.check_environment() == "NoToken":
        tinkle = TinkleAuth()
    elif api.abstract.check_environment() == "NoAccount":
        api.abstract.logout()
        tinkle = TinkleAuth()
    else:
        tinkle_auth = TinkleUI()

    Gtk.main()


if __name__ == '__main__':
    start()
