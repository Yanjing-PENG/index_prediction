# -*- encoding:utf-8 -*-

import pandas as pd
import plotly.offline as pltoff
import plotly.graph_objs as go

def plot_net_value(orderbook, start_time, start_net_value):
    """
    ## plot the net value figure
    - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Inputs:
    # orderbook:    order history
    - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    data = orderbook.loc[orderbook['pnl'] != 0][['datetime','pnl']]
    data['net_value'] = 0

    pnl = pd.DataFrame(columns=data.columns)
    pnl = pnl.append({'datetime':start_time,'pnl':0,'net_value':start_net_value}, ignore_index=True)
    pnl = pnl.append(data, ignore_index=True)

    for i in range(1, len(pnl), 1):
        pnl.iloc[i, 2] = pnl.iloc[i-1, 2] + pnl.iloc[i, 1]

    trace0 = go.Scatter(
        x=['_' + str(i) for i in pnl['datetime'].tolist()],
        y=[i / start_net_value for i in pnl['net_value'].tolist()])
    data = [trace0]
    layout = go.Layout(showlegend=True, xaxis={'title': 'backtest_time'}, yaxis={'title': 'net_value'})
    fig = go.Figure(data, layout)
    pltoff.plot(fig, filename='net_value.html')
