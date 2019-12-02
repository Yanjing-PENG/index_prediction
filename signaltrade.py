# -*- encoding: utf-8 -*-

from addorder import addorder
import pandas as pd
import numpy as np
import keras
from keras.models import load_model
from data_preprocess import normalization

model = load_model('dnn_model.h5')

def signaltrade(data_1m, loss_ratio, M, T, quantity=1, fee_rate=0.0001):
    """
    ## basing on signals and the strategy to do the backtest simulation
    - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Inputs:
    #  data_1m        candlesticks data of 1 minute resolution
    #  quantity       security quantity for each trade
    #  fee_rate       commission fee rate
    - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Outputs:
    #  data_1m        data with trade signals
    #  orderbook      order history
    """
    # initialize order book and backtest tradedate
    orderbook = pd.DataFrame(columns=['datetime','price','quantity','fee','pnl','type'])
    tradedate = list(data_1m.keys())[140: 280]

    # loops based on date
    for i in tradedate:
        # get the i-th date's data
        data_1m_i = data_1m[i]
        data_1m_i['order'] = 0
        data_1m_i.reset_index(inplace=True, drop=True)
        signal = []

        # loops basing on time
        index = data_1m_i.index.tolist()
        tem = list(range(M-1, index[-1], T))

        for j in range(len(tem)):
            # get trade signals
            x = np.array(data_1m_i['close'][tem[j]-59: tem[j]+1].to_list())
            x = x.reshape(1, M)
            x = normalization(x)
            p = model.predict(x)
            signal.append(np.argmax(p))
            c = data_1m_i.loc[tem[j], 'close']

            # excute trades
            if j < (len(tem)-1) and data_1m_i['order'].sum() == 0:
                if signal[-1] == 1:   # open long position
                    orderbook = addorder(orderbook, [data_1m_i.loc[tem[j], 'time'], c, quantity, fee_rate], 'long')
                    data_1m_i.loc[tem[j], 'order'] = 1
                    threshold_price = c * (1 - loss_ratio)

                if signal[-1] == 2:   # open short position
                    orderbook = addorder(orderbook, [data_1m_i.loc[tem[j], 'time'], c, -quantity, fee_rate], 'short')
                    data_1m_i.loc[tem[j], 'order'] = -1
                    threshold_price = c * (1 + loss_ratio)

            if data_1m_i['order'].sum() == 1 and signal[-1] != 1:   # close long position
                orderbook = addorder(orderbook, [data_1m_i.loc[tem[j], 'time'], c, -quantity, fee_rate], 'close long')
                data_1m_i.loc[tem[j], 'order'] = -1
                if j < (len(tem)-1) and signal[-1] == 2:   # open short position
                    orderbook = addorder(orderbook, [data_1m_i.loc[tem[j], 'time'], c, -quantity, fee_rate], 'short')
                    data_1m_i.loc[tem[j], 'order'] = -2
                    threshold_price = c * (1 + loss_ratio)

            if data_1m_i['order'].sum() == -1 and signal[-1] != 2:  # close short position
                orderbook = addorder(orderbook, [data_1m_i.loc[tem[j], 'time'], c, quantity, fee_rate], 'close short')
                data_1m_i.loc[tem[j], 'order'] = 1
                if j < (len(tem)-1) and signal[-1] == 1:   # open long position
                    orderbook = addorder(orderbook, [data_1m_i.loc[tem[j], 'time'], c, quantity, fee_rate], 'long')
                    data_1m_i.loc[tem[j], 'order'] = 2
                    threshold_price = c * (1 - loss_ratio)

            if data_1m_i['order'].sum() == 1:
                if j < (len(tem)-1):
                    for k in range(tem[j], tem[j+1]):
                        if data_1m_i.loc[k, 'close'] <= threshold_price:      # long position stop loss
                            orderbook = addorder(orderbook, [data_1m_i.loc[k, 'time'], data_1m_i.loc[k, 'close'], -quantity, fee_rate],
                                                 'stop loss close long')
                            data_1m_i.loc[tem[j], 'order'] = -1
                            break
                else:
                    for k in range(tem[j], index[-1]):
                        if data_1m_i.loc[k, 'close'] <= threshold_price:      # long position stop loss
                            orderbook = addorder(orderbook, [data_1m_i.loc[k, 'time'], data_1m_i.loc[k, 'close'], -quantity, fee_rate],
                                                 'stop loss close long')
                            data_1m_i.loc[tem[j], 'order'] = -1
                            break

            if data_1m_i['order'].sum() == -1:
                if j < (len(tem)-1):
                    for k in range(tem[j], tem[j+1]):
                        if data_1m_i.loc[k, 'close'] >= threshold_price:      # short position stop loss
                            orderbook = addorder(orderbook, [data_1m_i.loc[k, 'time'], data_1m_i.loc[k, 'close'], quantity, fee_rate],
                                                 'stop loss close short')
                            data_1m_i.loc[k, 'order'] = 1
                            break
                else:
                    for k in range(tem[j], index[-1]):
                        if data_1m_i.loc[k, 'close'] >= threshold_price:      # short position stop loss
                            orderbook = addorder(orderbook, [data_1m_i.loc[k, 'time'], data_1m_i.loc[k, 'close'], quantity, fee_rate],
                                                 'stop loss close short')
                            data_1m_i.loc[k, 'order'] = 1
                            break


        if data_1m_i['order'].sum() == 1:      # close long position befor the end time of market
            orderbook = addorder(orderbook, [data_1m_i.loc[index[-2], 'time'], data_1m_i.loc[index[-2], 'close'], -quantity, fee_rate], 'end of marketc, close long')
            data_1m_i.loc[index[-2], 'order'] = -1

        if data_1m_i['order'].sum() == -1:     # close short position befor the end time of market
            orderbook = addorder(orderbook, [data_1m_i.loc[index[-2], 'time'], data_1m_i.loc[index[-2], 'close'], quantity, fee_rate], 'end of market, close short')
            data_1m_i.loc[index[-2], 'order'] = 1

    return [data_1m, orderbook, tradedate]
