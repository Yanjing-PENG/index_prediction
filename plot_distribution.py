# -*- encoding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from configue import TRAIN_PERIOD
from configue import T

data = pd.read_csv('./data/original_data.csv')

del data['thscode']
data['date'] = data['time'].str.split(' ', expand=True)[0]
data['year'] = data['date'].str.split('-', expand=True)[0]

data = data.loc[(data['year'] >= TRAIN_PERIOD[0]) & (data['year'] <= TRAIN_PERIOD[-1])]
data = dict(list(data.groupby('date')))

change = []
for i in data.keys():
    tem = data[i]
    tem.reset_index(drop=True, inplace=True)
    for j in range(tem.shape[0] - T):
        change.append(tem['close'][j+T] - tem['close'][j])
        # if tem['close'][j+T] - tem['close'][j] > 200 or tem['close'][j+T] - tem['close'][j] < -200:
        #     print(i, tem['time'][j], tem['close'][j], tem['close'][j+T])

plt.hist(change, bins='auto', density=1, range=(-100, 100), alpha=0.6)
plt.xlabel('price changes over %d minutes' % T)
plt.ylabel('frequency')
plt.title('frequency distribution histogram')
plt.savefig('changes distribution')

change = pd.Series(change)
print(change.describe())
