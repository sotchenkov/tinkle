import threading
import os
# import concurrent.futures
import ui.view
from ui.view import TinkleUI
from api import tinkoff_invest_api

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


def call_repeatedly(interval, func, *args):
    stopped = threading.Event()

    def loop():
        while not stopped.wait(interval):  # the first call is in `interval` secs
            func(*args)

    threading.Thread(target=loop).start()
    return stopped.set


def main():
    # threads = threading.Thread(target=get_contents())
    t = threading.Timer(3.0, get_contents)
    # t = threading.Thread(target=start)
    # t.daemon = True
    t.start()
    # threads.start()


def start():
    from ui.view import TinkleUI


def get_contents():
    tinkoff_invest_api.load_env_variables()

    if not tinkoff_invest_api.check_token():
        tinkoff_invest_api.set_token(str(input("token: ")))
        tinkoff_invest_api.load_env_variables()

    with tinkoff_invest_api.Client(os.environ["INVEST_TOKEN"]) as client:
        if tinkoff_invest_api.check_main_account() is None:
            accounts = tinkoff_invest_api.get_accounts(client)
            for accs in accounts:
                print(accs[1])
            tinkoff_invest_api.set_main_account(accounts[int(input("choose acc: "))][0])
            tinkoff_invest_api.load_env_variables()

        t = tinkoff_invest_api.TInvest()
        print(t.get_portfolio_cost(client))
        return t.get_portfolio_cost(client)
        # for position in t.get_account_positions(client):
        #     try:
        #         t.load_instrument_names()
        #         print(t.get_position_info(position))
        #     except Exception:
        #         t.save_instrument_names(t.get_instrument_names(client))
        #         t.load_instrument_names()
        #         print(t.get_position_info(position))


def letsstart():
    # th = threading.Thread(target=call_repeatedly, args=(3, get_contents)).start()
    tinkle = TinkleUI()
    Gtk.main()
    # tinkle.cost = th


if __name__ == '__main__':
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future = executor.submit(get_contents)
    #     return_value = future.result()
    #     print(return_value)

    threading.Thread(target=letsstart).start()
    # threading.Thread(target=call_repeatedly, args=(3, get_contents)).start()

    # call_repeatedly(2, get_contents)

    # call_repeatedly(3, tinkle.update_cost(get_contents()))

# ToDo: Добавить сюда потоки
