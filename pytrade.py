"""
dsiadsbihfsabhifdsbasfi
"""

from secret import api_key, api_secret

from coinbase.wallet.client import Client
from time import sleep
import argparse

import json
import numpy as np
import datetime as dt
import pdb

client = Client(api_key, api_secret)

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--currency", required=True,
                help="currency being traded with usd")
ap.add_argument("-s", "--spread", required=True,
                help="min. goal per transaction")
ap.add_argument("-r", "--risk", required=True,
                help="maximum pc tolerance for crypto position")
ap.add_argument("-a", "--avg", required=True,
                help="averaging period")
ap.add_argument("-u", "--unit", required=True,
                help="unit of crypto currency for each transaction")
ap.add_argument("-l", "--log", required=False,
                help="name of log file")

args = vars(ap.parse_args())

# run params
currency = args["currency"]
spread = float(args["spread"])
risk_tol = float(args["risk"])
tdelta = int(args["avg"])
unit = int(args["unit"])
if args["log"] is not None:
    log_file = args["log"]
else:
    log_file = f"log_{currency}.csv"
currency_pair=f'{currency}-USD'

# environment setup
t = 1
start_val = 10 ** 6
act = {'dol': start_val, currency: 0, 'net': 0
      , 'fees': 0, 'spent': 0, 'gains': 0, 'profit': 0}
last = 0
fee_pc = 0.0025
day = dt.datetime.now()

prices = []

# initial purchase
res = client.get_spot_price(currency_pair=currency_pair)
data = json.loads(str(res))
spot_price = float(data['amount'])
prices.append(spot_price)
coin_num = unit * 5
order_amount = spot_price * coin_num
fee = order_amount * fee_pc
order_tot = order_amount + fee
act['dol'] -= order_tot
act[currency] += coin_num
act['net'] = act['dol'] + act[currency] * spot_price
act['fees'] += fee
act['spent'] += order_amount

file = open(log_file, "w+")
file.write(f"t,spot_price,act_dol,act_{currency},net_worth,profit,threshold,target_price,"
           f"price_gap,fees,spent,gains,profit\n")
file.close()

#pdb.set_trace()

while True:
    try:
        today = dt.datetime.now()

        # liquidate all assets at midnight
        if today.date() == day.date():
            res = client.get_spot_price(currency_pair=currency_pair)
            data = json.loads(str(res))

            spot_price = float(data['amount'])
            prices.append(spot_price)
            coin_num = unit
            order_amount = spot_price * coin_num
            fee = order_amount * fee_pc
            order_tot = order_amount + fee

            thres = spot_price * (fee_pc + spread)

            if t < tdelta:
                target_price = spot_price
            else:
                target_price = np.average(prices[t - tdelta:t])

            # buy
            if target_price - thres > spot_price and act['dol'] > order_tot and (order_amount + act[
                currency] * spot_price) / act['net'] < risk_tol:
                act['dol'] -= order_tot
                act[currency] += coin_num
                act['fees'] += fee
                act['spent'] += order_amount


            # sell
            if target_price + thres < spot_price and act[currency] > coin_num:
                act['dol'] += order_amount *(1 - fee_pc)
                act['fees'] += order_amount * fee_pc
                act[currency] -= coin_num
                act['gains'] += order_amount

            # update total net worth
            act['net'] = act['dol'] + act[currency] * spot_price
            act['profit'] = act['gains'] - act['fees']

            print(f'Currently trading: {currency}...')
            print(f'timestep: {t}, spot price: ${spot_price:,.2f}, account: ${act}')
            print(f'threshold: ${thres:,.2f}')
            print(f'target price: ${target_price:,.2f}')
            print(f'spot-target: ${spot_price-target_price:,.2f}')
            print(f"Unrealized gains: ${float(act['net'])-start_val:,.2f},"
                f"{(float(act['net'])-start_val)/start_val:,.2f}%")
            print(f"EBITDA: {act['profit']}")
            print('*' * 50)

            # log data in csv file
            file = open(log_file, 'a')
            file.write(
                f"{t},{spot_price:,.2f},{act['dol']},{act[currency]},{act['net']},"
                f"{float(act['net'])-start_val},{thres},{target_price},{spot_price-target_price},"
                f"{act['fees']},{act['spent']},{act['gains']},{act['profit']}\n"
            )
            file.close()

            last = spot_price
            t += 1
        else:
            day = today
            coin_num = act['eth']
            order_amount = spot_price * coin_num
            act['dol'] += order_amount * (1 - fee_pc)
            act[currency] -= coin_num
    except OSError as e:
        print(f"Exception {e} encountered.")
    sleep(30)