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
    def buy(self, **data):
        """
        Decides whether to buy assst based on provided data.

        Returns:
            The number of assets to buy, or 0 for no buys.
        """
        raise NotImplementedError()

    def sell(self, **data):
        """
        Decides whether to sell asset based on provided data.
        Returns:
            The number of assets to buy, or 0 for no sells.
        """
        raise NotImplementedError()

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
        self.last_sp = 0
        self.title = "t, spot_price, cash, pos, fees"

        with open(logfile, 'w+') as f:
            f.write(self.title)
            f.close()

    def __str__(self):
        return f'{self.t}, {self.last_sp}, {self.cash}, {self.position}, {self.fees}'

    def trade(self, sp, order_num):
        """
        Execute trade based off of order. Negative order_num means sell
        Args:
            order_num: float of coins to be exchanged in transaction
        """
        # flip sign to reflect cash flow movement based on buying versus selling
        # fee is paid separately from order
        subtotal = sp * order_num
        fee = abs(subtotal) * fee_pc
        self.cash -= subtotal
        self.cash -= fee

        # adjust position to reflect transaction
        self.position += order_num

        # keep tracks of fees paid
        self.fees += fee

    def timestep(self, data):
        """
        Execute strategy for one time step.
        Args:
            data: dictionary of current market conditions
        """
        self.t += 1

        data["cash"] = self.cash
        data["position"] = self.position

        buy_num = self.strat.buy(**data)
        sell_num = self.strat.sell(**data)

        sp = data["spot_price"] = float(data["spot_price"])
        self.last_sp = sp

        self.trade(sp, buy_num - sell_num)

        self._log(**data)

    def toggle_trading(self):
        """
        Switches portfolio between active and non-active for trading.
        """
        raise NotImplementedError()

    def _log(self, **data):
        if not self.logfile:
            raise FileNotFoundError()

        with open(self.logfile, 'w+') as f:
            f.write(self.__str__())
            f.close()

class Bot(object):
    """
    Manages several portfolios and presents information about them.
    """

    def __init__(self, logfile='test.csv'):
        self.portfolios = []
        self.logfile = logfile
        self.t = 0

    def summary(self):
        """
        Prints information about each portfolio in the bot.
        """
        for i, p in enumerate(self.portfolios):
            print(f'\t\t\t {p.title}')
            print(f'Portfolio {i}: {p}')

    def timestep(self):
        data = self._data_pull()

        # only considered a timestep if data is received
        if not data:
            return None

        self.t += 1
        for p in self.portfolios:
            p.timestep(data)
        self._log()
        print('*'*50 + '\n')
        self.summary()

    def add_port(self, strat, start_cash, logfile=None):
        if not logfile:
            logfile = f'portfolio_{len(self.portfolios)+1}.csv'
        self.portfolios.append(Portfolio(strat, start_cash, logfile))

    def _log(self, **data):
        pass

    def _data_pull(self):
        """
        Pulls data from the exchange API.
        Returns:
            Dictionary of price/currency data from exchange.
        """
        raise NotImplementedError("Bot data pull function")