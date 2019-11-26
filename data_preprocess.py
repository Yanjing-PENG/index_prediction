# -*- encoding: utf-8 -*-

import pandas as pd
import csv
from configue import TRAIN_PERIOD
from configue import VALIDATION_PERIOD
from configue import T
from configue import UP_THRESHOLD
from configue import DOWN_THRESHOLD

def generate_dataset(original_data, t, up_threshold, down_threshold, file_name):

    file = open('./data/' + file_name + '.csv', 'w', encoding='utf-8')
    writer = csv.writer(file, delimiter=',')

    column_names = []
    for i in range(59):
        column_names.append('x_-' + str(59 - i))
    column_names.append('x_0')
    column_names.append('y')
    writer.writerow(column_names)

    if file_name == 'training_data':
        for i in original_data.keys():
            tem = original_data[i]
            tem.reset_index(drop=True, inplace=True)
            for j in range(59, tem.shape[0] - T):
                instance = tem['close'][(j-59): (j+1)]
                instance = instance.to_list()
                if tem['close'][j+T] - tem['close'][j] >= up_threshold:
                    instance.append(1)
                    writer.writerow(instance)
                    writer.writerow(instance)
                elif tem['close'][j+T] - tem['close'][j] <= down_threshold:
                    instance.append(-1)
                    writer.writerow(instance)
                    writer.writerow(instance)
                else:
                    instance.append(0)
                    writer.writerow(instance)

    else:
        for i in original_data.keys():
            tem = original_data[i]
            tem.reset_index(drop=True, inplace=True)
            for j in range(59, tem.shape[0] - T):
                instance = tem['close'][(j - 59): (j + 1)]
                instance = instance.to_list()
                if tem['close'][j+T] - tem['close'][j] >= up_threshold:
                    instance.append(1)
                elif tem['close'][j+T] - tem['close'][j] <= down_threshold:
                    instance.append(-1)
                else:
                    instance.append(0)
                writer.writerow(instance)

    file.close()

def normalization(data):
    for i in range(len(data)):
        u = data[i].mean()
        std = data[i].std()
        data[i] = (data[i] - u) / std
    return data


if __name__ == '__main__':

    data = pd.read_csv('./data/original_data.csv')
    del data['thscode']
    data['date'] = data['time'].str.split(' ', expand=True)[0]
    data['year'] = data['date'].str.split('-', expand=True)[0]

    training_data = data.loc[(data['year'] >= TRAIN_PERIOD[0]) & (data['year'] <= TRAIN_PERIOD[-1])]
    training_data = dict(list(training_data.groupby('date')))

    validation_data = data.loc[(data['year'] >= VALIDATION_PERIOD[0]) & (data['year'] <= VALIDATION_PERIOD[-1])]
    validation_data = dict(list(validation_data.groupby('date')))

    generate_dataset(training_data, T, UP_THRESHOLD, DOWN_THRESHOLD, 'training_data')
    generate_dataset(validation_data, T, UP_THRESHOLD, DOWN_THRESHOLD, 'validation_data')