"""
Command line tool to launch and manage bots.
"""

from test_strats import *
from exchanges import *
from time import sleep
from test_strats import *

# trading parameters
start_act_val = 10**6
symbol = "ETH"


print('*'*50)
print('Welcome to PyTrade!\n')
print('Beginning trading now...\n')
eth_bot = CoinbaseBot(symbol)
eth_bot.add_port(ContraStrat, start_act_val)
eth_bot.add_port(BasicLSTMStrat, start_act_val)

while True:
    eth_bot.timestep()
    sleep(60)