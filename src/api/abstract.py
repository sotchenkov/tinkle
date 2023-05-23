import time

from api.tinkoff_invest_api import *
import os


def check_environment():
    load_env_variables()

    if not check_token():
        return "NoToken"
        # set_token(str(input("token: ")))
        # load_env_variables()

    with Client(os.environ["INVEST_TOKEN"]) as client:
        if check_main_account() is None:
            return "NoAccount"
            # accounts = get_accounts(client)
            # for accs in accounts:
            #     print(accs[1])
            # set_main_account(accounts[int(input("choose acc: "))][0])
            # load_env_variables()


def portfolio_cost():
    check_environment()
    with Client(os.environ["INVEST_TOKEN"]) as client:
        return TInvest().get_portfolio_cost(client)


def _most_profitable(instruments):
    pass


def instruments_cost():
    check_environment()
    with Client(os.environ["INVEST_TOKEN"]) as client:
        t = TInvest()
        pos = []
        for position in t.get_account_positions(client):
            try:
                t.load_instrument_names()
                pos.append(t.get_position_info(position))
            except Exception:
                t.save_instrument_names(t.get_instrument_names(client))
                t.load_instrument_names()
                print(t.get_position_info(position))

        if len(pos) == 0:
            return "NoInstruments"
        return pos


# ToDO: Добавить расчёт топ-5 самых доходных
