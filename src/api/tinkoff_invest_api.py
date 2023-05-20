import os
import json

from tinkoff.invest import Client, MoneyValue
from tinkoff.invest.services import InstrumentsService
from dotenv import load_dotenv


def load_env_variables():
    load_dotenv(os.path.join(os.path.dirname(__file__), 'data/.env'))


def check_token():
    dotenv_path = os.path.join(os.path.dirname(__file__), 'data/.env')
    if os.path.exists(dotenv_path) and os.stat(dotenv_path).st_size != 0:
        return True
    else:
        return False


def check_main_account():
    return os.environ["MAIN_ACCOUNT"] if 'MAIN_ACCOUNT' in os.environ else None


def set_token(token: str):
    with open('data/.env', 'w') as env:
        env.write(f'INVEST_TOKEN = {token}')


def set_main_account(account_id: str):
    with open('data/.env', 'a') as env:
        env.write(f'\nMAIN_ACCOUNT = {account_id}')


def get_accounts(client):
    available_accounts = []
    for account in client.users.get_accounts().accounts:
        if account.status == 2:
            available_accounts.append((account.id, account.name))

    return available_accounts if len(available_accounts) > 0 else None


def cast_money(money: MoneyValue) -> float:
    return money.units + money.nano / 1e9


def quantity_to_float(quantity) -> float:
    if quantity.nano == 0:
        return quantity.units
    else:
        return float(str(quantity.units) + "." + str(quantity.nano)[:2])


class TInvest:
    def __init__(self):
        self.main_account_id = os.environ["MAIN_ACCOUNT"]
        self.instrument_names: json = {}

    def get_instrument_names(self, client) -> dict:
        instrument_names = {"RUB000UTSTOM": "Рубль"}

        portfolio = client.operations.get_portfolio(account_id=self.main_account_id)
        portfolio_figis = [positions.figi for positions in portfolio.positions]

        instruments: InstrumentsService = client.instruments

        for method in ["shares", "bonds", "etfs", "currencies", "futures"]:
            for item in getattr(instruments, method)().instruments:
                if item.figi in portfolio_figis:
                    instrument_names[item.figi] = item.name

        return instrument_names

    @staticmethod
    def save_instrument_names(instrument_names) -> None:
        with open('data/instrument_names.json', 'w', encoding='UTF-8') as names:
            names.write(json.dumps(instrument_names))

    def load_instrument_names(self) -> None:
        with open('data/instrument_names.json', 'r', encoding='UTF-8') as names:
            self.instrument_names = json.load(names)

    def get_account_positions(self, client):
        return client.operations.get_portfolio(account_id=self.main_account_id).positions

    def get_position_info(self, position):
        return {
            "name": self.instrument_names[position.figi],
            "current_price": quantity_to_float(position.current_price),
            "quantity": quantity_to_float(position.quantity),
            "position_cost": round(quantity_to_float(position.current_price) * quantity_to_float(position.quantity), 2),
            "cost_change": quantity_to_float(position.expected_yield),
            "cost_change_percents": round(quantity_to_float(position.expected_yield) /
                                          (quantity_to_float(position.current_price) *
                                           quantity_to_float(position.quantity)) * 100, 2)
        }

    def get_portfolio_cost(self, client):
        portfolio = client.operations.get_portfolio(account_id=self.main_account_id)  # DRY check tomorrow
        return quantity_to_float(portfolio.total_amount_portfolio), quantity_to_float(portfolio.expected_yield)


if __name__ == "__main__":
    load_env_variables()

    if not check_token():
        set_token(str(input("token: ")))
        load_env_variables()

    with Client(os.environ["INVEST_TOKEN"]) as client:
        if check_main_account() is None:
            accounts = get_accounts(client)
            for accs in accounts:
                print(accs[1])
            set_main_account(accounts[int(input("choose acc: "))][0])
            load_env_variables()

        t = TInvest()
        print(t.get_portfolio_cost(client))
        for position in t.get_account_positions(client):
            try:
                t.load_instrument_names()
                print(t.get_position_info(position))
            except Exception:
                t.save_instrument_names(t.get_instrument_names(client))
                t.load_instrument_names()
                print(t.get_position_info(position))




