from trading import *

import numpy as np

class ContraStrat(Strategy):
    """
    Implementation of the contrarian trading strategy where buy/sell  decisions are made
    based on how far price has moved from a certain anchor point.  If the target security
    falls enough you buy, while if it goes sufficently high you sell.  Thus, you adjust
    your position contrary to the price movement.
    """
    def __init__(self):
        self.n = 50
        self.lagged_prices = []
        self.spread = 0.0005
        self.unit = 5


    def buy(self, **data):
        spot_price = data.get('spot_price')
        if len(self.lagged_prices) < self.n:
            self.lagged_prices.append(spot_price)
            return 0
        print(self.lagged_prices)
        avg = np.mean(map(int, self.lagged_prices))
        price_move = spot_price - avg

        thres = spot_price * (fee_pc + self.spread)


        if price_move > thres: return self.unit


    def sell(self, **data):
        spot_price = data.get('spot_price')
        if len(self.lagged_prices) < self.n:
            self.lagged_prices.append(spot_price)
            return 0
        avg = np.mean(self.lagged_prices)
        price_move = spot_price - avg

        thres = spot_price * (fee_pc + self.spread)

        if price_move < -thres: return -self.unit

class BasicLSTMStrat(Strategy):
    """
    A trading strategy that works using a very basic LSTM to inform trading decisions.
    This network was trained on only a few lagged spot prices to predict future spot
    prices.
    """
    pass