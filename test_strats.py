from trading import *

class ContraStrat(Strategy):
    """
    Implementation of the contrarian trading strategy where buy/sell  decisions are made
    based on how far price has moved from a certain anchor point.  If the target security
    falls enough you buy, while if it goes sufficently high you sell.  Thus, you adjust
    your position contrary to the price movement.
    """
    def __init__(self):
        pass

    def buy(self, **data):
        pass

    def sell(self, **data):
        pass

    def calc_anchor(self, **data):
        pass

class BasicLSTMStrat(Strategy):
    pass