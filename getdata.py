# -*- encoding: utf-8 -*-

import pandas as pd
from configue import BACKTEST_PERIOD

def getData():

    data = pd.read_csv('./data/original_data.csv')
    del data['thscode']
    data['date'] = data['time'].str.split(' ', expand=True)[0]
    data['year'] = data['date'].str.split('-', expand=True)[0]

    backtest_data = data.loc[(data['year'] >= BACKTEST_PERIOD[0]) & (data['year'] <= BACKTEST_PERIOD[-1])]
    backtest_data = dict(list(backtest_data.groupby('date')))

    return backtest_data

if __name__ == '__main__':

    data = getData()
    print(data)