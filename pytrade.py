"""
dsiadsbihfsabhifdsbasfi
"""

from secret import api_key, api_secret

from coinbase.wallet.client import Client
from time import sleep

import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd

client = Client(api_key, api_secret)

# environment setup
t = 1
start_val = 10 ** 6
act = {'dol': start_val, 'eth': 0, 'net': 0}
unit = 100
last = 0
fee_pc = 0.0025

log_file = "log2.csv"

# run params
thres = 0.1
spread = 0.0001
tdelta = 100

prices = []

# initial purchase
res = client.get_spot_price(currency_pair='ETH-USD')
data = json.loads(str(res))
curr_price = float(data['amount'])
prices.append(curr_price)
coin_num = unit * 5
order_amount = curr_price * coin_num
order_tot = order_amount * (1 + fee_pc)
act['dol'] -= order_tot
act['eth'] += coin_num

file = open(log_file, "w+")
file.write("t,spot_price,act_dol,act_eth,net_worth,profit,threshold,target_price,price_gap\n")
file.close()

while True:
    try:
        res = client.get_spot_price(currency_pair='ETH-USD')
        data = json.loads(str(res))

        curr_price = float(data['amount'])
        prices.append(curr_price)
        coin_num = unit
        order_amount = curr_price * coin_num
        order_tot = order_amount * (1 + fee_pc)

        thres = curr_price * (fee_pc + spread)

        if t < tdelta:
            target_price = curr_price
        else:
            target_price = np.average(prices[t - tdelta:t])

        # buy
        if target_price - thres > curr_price and act['dol'] > order_tot:
            act['dol'] -= order_tot
            act['eth'] += coin_num

        # sell
        if target_price + 5 * thres < curr_price and act['eth'] > coin_num:
            act['dol'] += order_amount * (1 - fee_pc)
            act['eth'] -= coin_num

        # update total net worth
        act['net'] = act['dol'] + act['eth'] * curr_price
        print(f'timestep: {t}, spot price: ${curr_price:,.2f}, account: ${act}')
        print(f'threshold: ${thres:,.2f}')
        print(f'target price: ${target_price:,.2f}')
        print(f'price gap: ${curr_price-target_price:,.2f}')
        print(
            f"Profit: ${float(act['net'])-start_val:,.2f}, {(float(act['net'])-start_val)/start_val:,.2f}%")
        print('*' * 50)

        # log data in csv file
        file = open(log_file, 'a')
        file.write(
            f"{t},{curr_price:,.2f},{act['dol']},{act['eth']},{act['net']},{float(act['net'])-start_val},{thres},{target_price},{curr_price-target_price}\n")
        file.close()

        last = curr_price
        t += 1
    except Exception as e:
        print(f"Exception {e} encountered.")
    sleep(30)