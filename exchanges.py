from trading import *

from coinbase.wallet.client import Client
from secret import api_key, api_secret

import json

client = Client(api_key, api_secret)

class CoinbaseBot(Bot):
    """Bot to interact with coinbase and manage portfolios on that exchange."""
    def __init__(self, currency):
        self.currency_pair = f'{currency}-USD'

    def _data_pull(self):
        res = client.get_spot_price(currency_pair=self.currency_pair)
        data = json.loads(str(res))
        return {"spot_price":(data['amount']), }
