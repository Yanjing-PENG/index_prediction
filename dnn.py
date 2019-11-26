# -*- encoding: utf-8 -*-

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam
from data_preprocess import normalization

import numpy as np
import matplotlib.pyplot as plt

TRAINING_DATA = './data/training_data.csv'
VALIDATION_DATA = './data/validation_data.csv'

train_data = np.genfromtxt(TRAINING_DATA, skip_header=1, dtype=float, delimiter=',')
np.random.shuffle(train_data)
validation_data = np.genfromtxt(VALIDATION_DATA, skip_header=1, dtype=float, delimiter=',')

x_train = train_data[:, :-1]
x_train = normalization(x_train)
y_train = keras.utils.to_categorical(train_data[:, -1].astype(np.int64).reshape(-1, 1), num_classes=3)

x_test = validation_data[:, :-1]
x_test = normalization(x_test)
y_test = keras.utils.to_categorical(validation_data[:, -1].astype(np.int64).reshape(-1, 1), num_classes=3)


model = Sequential()

model.add(Dense(500, activation='relu', input_dim=x_train.shape[1]))
model.add(Dropout(0.5))
model.add(Dense(200, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(40, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(3, activation='softmax'))

sgd = SGD(learning_rate=0.001, decay=9, momentum=0, nesterov=False)
adam = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)

model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=['accuracy'])

print(model.summary())

history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=2000, verbose=2, batch_size=100)

plt.figure(figsize=[12, 4])
plt.subplot(121)
plt.plot(history.epoch, history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')

plt.subplot(122)
plt.plot(history.epoch, history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper right')
plt.show()

model.save('dnn_model.h5')

