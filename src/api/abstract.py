import time
from api.tinkoff_invest_api import *
import os


def check_environment():
    try:
        load_env_variables()
        with Client(os.environ["INVEST_TOKEN"]) as client:
            if check_main_account() is None:
                return "NoAccount"
    except:
        return "NoToken"


def logout():
    os.remove('./api/data/.env')


def get_accountss():
    check_environment()
    with Client(os.environ["INVEST_TOKEN"]) as client:
        return get_accountsss(client)


def portfolio_cost():
    check_environment()
    with Client(os.environ["INVEST_TOKEN"]) as client:
        return TInvest().get_portfolio_cost(client)


def _most_profitable(instruments):
    return sorted(instruments, key=lambda x: x['cost_change_percents'], reverse=True)


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

        return _most_profitable(pos)
