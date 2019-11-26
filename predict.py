import keras
from keras.models import load_model
from data_preprocess import normalization

import numpy as np

TRAINING_DATA = './data/training_data.csv'
VALIDATION_DATA = './data/validation_data.csv'
train_data = np.genfromtxt(TRAINING_DATA, skip_header=1, dtype=float, delimiter=',')
validation_data = np.genfromtxt(VALIDATION_DATA, skip_header=1, dtype=float, delimiter=',')

x_train = train_data[:, :-1]
x_train = normalization(x_train)
y_train = keras.utils.to_categorical(train_data[:, -1].astype(np.int64).reshape(-1, 1), num_classes=3)
x_validation = validation_data[:, :-1]
x_validation = normalization(x_validation)
y_validation = keras.utils.to_categorical(validation_data[:, -1].astype(np.int64).reshape(-1, 1), num_classes=3)

model = load_model('dnn_model.h5')
y_predict_train = model.predict(x_train)
y_predict_validation = model.predict(x_validation)
model.predict(x_validation[0].reshape(1, 60))
