# -*- encoding: utf-8 -*-

import pandas as pd
from math import sqrt

def tradestats(orderbook, init_capital=3000, tradedate=None):
    """
    ## strategy performance statistics
    - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Inputs:
    #  orderbook      order history
    #  tradedate      backtest trade dates
    - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Outputs:
    #  stats          backtest performance
    - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    if not tradedate:
        raise Exception("please enter backtest trade dates list：")

    if len(orderbook) < 1:
        stats = []
    else:
        # calculate performance indicators
        num_trades = len(orderbook)/2     # total number of trades
        num_win = orderbook.loc[orderbook['pnl'] > 0].shape[0]   # total number of profitable trades
        percent_win = num_win/num_trades       # poritable trades/ total trades
        pnl_total = orderbook['pnl'].sum()     # accumulated pnl
        total_win = orderbook.loc[orderbook['pnl']>0]['pnl'].sum()    # accumulated profit
        total_loss = orderbook.loc[orderbook['pnl']<0]['pnl'].sum()   # accumulated loss
        pnl_avg = pnl_total/num_trades      # pnl for every trade

        max_win = orderbook['pnl'].max()      # maximum profit
        max_loss = orderbook['pnl'].min()     # maximum loss

        # calculate maximum drawdown
        pnl_list = orderbook.loc[orderbook['pnl'] != 0]['pnl'].tolist()
        net_value_list = [init_capital]  # suppose the initial capital is 3000
        for i in range(len(pnl_list)):
            net_value_list.append(init_capital + sum(pnl_list[:(i + 1)]))

        drawdown = [0]
        drawdown_ratio = [0]

        if len(net_value_list) > 1:
            temp_base_value = net_value_list[0]
            temp_drawdown = 0
            temp_drawdown_ratio = 0
            for i in range(1, len(net_value_list)):
                if net_value_list[i] <= net_value_list[i - 1]:
                    temp_drawdown = temp_base_value - net_value_list[i]
                    temp_drawdown_ratio = temp_drawdown / temp_base_value
                    drawdown.append(temp_drawdown)
                    drawdown_ratio.append(temp_drawdown_ratio)
                else:
                    temp_base_value = net_value_list[i]
                    temp_drawdown = 0
                    temp_drawdown_ratio = 0

        maxdrawdown = max(drawdown)
        maxdrawdown_ratio = max(drawdown_ratio)

        active_drawdown = [0]
        active_drawdown_ratio = [0]

        if len(net_value_list) > 1:
            temp_active_base_value = net_value_list[0]
            temp_minmum_value = net_value_list[0]
            temp_active_drawdown = 0
            temp_active_drawdown_ratio = 0
            for i in range(1, len(net_value_list)):
                if net_value_list[i] <= temp_active_base_value:
                    if net_value_list[i] < temp_minmum_value:
                        temp_active_drawdown = temp_active_base_value - net_value_list[i]
                        temp_active_drawdown_ratio = temp_active_drawdown / temp_active_base_value
                        temp_minmum_value = net_value_list[i]
                        active_drawdown.append(temp_active_drawdown)
                        active_drawdown_ratio.append(temp_active_drawdown_ratio)
                else:
                    temp_active_base_value = net_value_list[i]
                    temp_minmum_value = net_value_list[i]
                    temp_active_drawdown = 0
                    temp_active_drawdown_ratio = 0

        max_active_drawdown = max(active_drawdown)
        max_active_drawdown_ratio = max(active_drawdown_ratio)

        # calculte sharpe ratio
        num_days = len(tradedate)
        orderbook['date'] = orderbook['datetime'].str.split(' ',expand=True)[0]
        daypnl = []
        for i in tradedate:
            daypnl.append(orderbook.loc[orderbook['date']==i]['pnl'].sum())

        daypnl_pd = pd.DataFrame(daypnl)
        daypnl_avg = daypnl_pd.mean()
        daypnl_std = daypnl_pd.std()
        annsharp = daypnl_avg/daypnl_std*sqrt(252)     # annual sharpe ration

        # output the statistics of backtest performance

        stats = pd.DataFrame(columns=['num_trades', 'percent_win','pnl_total','total_win', 'total_loss', 'pnl_avg',
                                      'max_win', 'max_loss','maxdrawdown', 'maxdrawdown_ratio','max_active_drawdown',
                                      'max_active_drawdown_ratio','daypnl_avg','daypnl_std','annsharp'])

        stats = stats.append(pd.DataFrame({'num_trades':num_trades, 'percent_win':percent_win, 'pnl_total':pnl_total,'total_win':total_win,
                                           'total_loss':total_loss, 'pnl_avg':pnl_avg, 'max_win':max_win, 'max_loss':max_loss,
                                           'maxdrawdown':maxdrawdown, 'maxdrawdown_ratio':maxdrawdown_ratio,'max_active_drawdown':max_active_drawdown,
                                          'max_active_drawdown_ratio':max_active_drawdown_ratio,'daypnl_avg':daypnl_avg,'daypnl_std':daypnl_std,
                                           'annsharp':annsharp}), ignore_index=True)

    return stats