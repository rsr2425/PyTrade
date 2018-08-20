"""
A module that fleshes out the strategy class which can control when
a trading algorithm decides to buy/sell assets.

This file also specifies certain parameters for trading, such as the fee percentage per
transaction.
"""

fee_pc = 0.0000

class Strategy(object):
    """
    Determines when to buy/sell assets.  Base class all actual strategy classes should
    inherit from.
    """
    def buy(self, data):
        """
        Decides whether to buy assst based on provided data.

        Returns:
            The number of assets to buy, or 0 for no buys.
        """
        pass

    def sell(self, data):
        """
        Decides whether to sell asset based on provided data.
        Returns:
            The number of assets to buy, or 0 for no sells.
        """
        pass

class Portfolio(object):
    """
    Tracks the details of a portfolio, such as cash and positions. Each portfolio
    only has one strategy object.

    Portfolio object should be passed a strategy object when created.
    """
    def __init__(self, strategy, start_cash, logfile):
        self.strat = strategy
        self.cash = start_cash
        self.logfile = logfile
        self.position = 0
        self.t = 0
        self.active = True # not used right now
        self.fees = 0

    def __str__(self):
        raise NotImplementedError()


    def trade(self, sp, order_num):
        """
        Execute trade based off of order. Negative order_num means sell
        Args:
            order_num: float of coins to be exchanged in transaction

        Returns:

        """
        # flip sign to reflect cash flow movement based on buying versus selling
        # fee is paid separately from order
        subtotal = sp * order_num
        fee = abs(subtotal) * fee_pc
        self.cash -= subtotal
        self.cash -= fee

        # adjust position to reflect transaction
        self.position += order_num

    def timestep(self, data):
        """
        Execute strategy for one time step.
        Args:
            data: dictionary of current market conditions
        """
        self.t += 1

        data["cash"] = self.cash
        data["position"] = self.position

        buy_num = self.strat.buy(data)
        sell_num = self.strat.sell(data)

        sp = data["spot_price"]

        self.trade(sp, buy_num - sell_num)

        self._log()

    def toggle_trading(self):
        """
        Switches portfolio between active and non-active for trading.
        """
        raise NotImplementedError

    def _log(self):
        raise NotImplementedError()

class Bot(object):
    """
    Manages several portfolios and presents information about them.
    """

    def __init__(self, logfile='test.csv'):
        self.portfolios = []
        self.logfile = logfile

    def summary(self):
        """
        Prints information about each portfolio in the bot.
        """
        for i, p in enumerate(self.portfolios): print(p)

    def timestep(self):
        data = self._data_pull()
        for p in self.portfolios:
            p.timestep(data)
        self._log(self)

    def add_port(self, strat, start_cash):
        self.portfolios.append(Portfolio(strat, start_cash))

    def _log(self):
        raise NotImplementedError("Bot log function")

    def _data_pull(self):
        raise NotImplementedError("Bot data pull function")