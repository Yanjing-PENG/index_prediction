# -*- encoding:utf-8 -*-

from getdata import getData
from signaltrade import signaltrade
from tradestats import tradestats
from plot import plot_net_value
from configue import M, T
import pandas as pd

# set the display parameters for pandas DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# set some basic parameters
init_capital = 3000
quantity = 1
fee_rate = 0.0001

# do the backtest
data_1m = getData()
signaltrade_result = signaltrade(data_1m, 0.003, M, T, quantity, fee_rate)
orderbook = signaltrade_result[1]
tradedate = signaltrade_result[2]
# get detailed backtest performance
stats = tradestats(orderbook, init_capital, tradedate)


# save backtest performance into excel file
writer = pd.ExcelWriter('backtest_result.xlsx')
stats.to_excel(writer, 'stats', index=False)
orderbook.to_excel(writer, 'orderbook', index=False)

writer.save()

# plot the net value figure
start_time = signaltrade_result[0][tradedate[0]].loc[0, 'time']
plot_net_value(orderbook, start_time, init_capital)

# print out the backtest performance
print('-------------------------------------------------------------------------------')
print(stats)
print('-------------------------------------------------------------------------------')
