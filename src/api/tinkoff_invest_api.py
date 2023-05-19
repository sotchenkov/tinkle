import os

from tinkoff.invest import Client, MoneyValue


def check_token():
    return True if os.environ['INVEST_TOKEN'] else False


def set_token(token: str):
    os.environ["INVEST_TOKEN"] = token


def set_main_account(account_id: str):
    os.environ["MAIN_ACCOUNT_ID"] = account_id


class TInvest:
    def __init__(self):
        self.token = os.environ["INVEST_TOKEN"]
        self.client = Client(self.token)

    def get_accounts(self):
        available_accounts = []
        with self.client as client:
            accounts = client.users.get_accounts()
            for account in accounts.accounts:
                if account.status == 2:
                    available_accounts.append((account.id, account.name))

            return available_accounts if len(available_accounts) > 0 else None


if __name__ == "__main__":
    if check_token():
        t = TInvest()
        for accs in t.get_accounts():
            print(accs[1])
    else:
        pass
