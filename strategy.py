"""
A module that flehses out the strategy class which can control when
a trading algorithm decides to buy/sell assets.
"""

class Strategy(object):
    """
    A class to determine when to buy, sell assets.
    """
    def __init__(self):
        pass

    def buy_asset(self, sp):
        """
        Decides whether to buy asset.
        :param sp: spot price.
        :return:
        """
        pass

    def sell_asset(self, sp):
        pass