from trading import *

from coinbase.wallet.client import Client
from secret import api_key, api_secret

import json

client = Client(api_key, api_secret)

class CoinbaseBot(Bot):
    """
    Bot to interact with coinbase and manage portfolios on that exchange.
    """
    def __init__(self, logfile="coinbasebot_log.csv", currency="ETH"):
        Bot.__init__(self, logfile)
        self.currency_pair = f'{currency}-USD'

    def _data_pull(self):
        """
        Pulls data from the exchange API.
        Returns:
            Dictionary of price/currency data from exchange.
        """
        # could probably handle this error better
        # perhaps by catching a Connection Error
        # # right now this is sloppy
        try:
            res = client.get_spot_price(currency_pair=self.currency_pair)
            data = json.loads(str(res))
            return {"spot_price":(data['amount']), }
        except:
            pass
