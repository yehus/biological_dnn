from keras.models import Sequential
from keras.optimizers import Adadelta, RMSprop, SGD
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout, Activation
import numpy as np
from scipy.stats.stats import pearsonr
from keras.regularizers import *
from keras.callbacks import ModelCheckpoint
from keras.constraints import maxnorm




def build_model(datasize=36):
    # datasize = DATASIZE
    W_maxnorm = 3
    DROPOUT = 0.5  #{{choice([0.3, 0.5, 0.7])}}

    model = Sequential()
    model.add(Conv2D(32, (4, 3), border_mode='same', input_shape=(datasize, 4, 1), activation='relu')) # , W_constraint=maxnorm(W_maxnorm)))
    model.add(MaxPool2D(pool_size=(1, 5), strides=(1, 5),padding='same'))
    model.add(Conv2D(64, (4, 3), border_mode='same',
                     activation='relu'))  # , W_constraint=maxnorm(W_maxnorm)))
    model.add(MaxPool2D(pool_size=(1, 5), strides=(1, 3), padding='same'))
    model.add(Conv2D(64, (4, 5), border_mode='same',
                     activation='relu'))  # , W_constraint=maxnorm(W_maxnorm)))
    model.add(MaxPool2D(pool_size=(1, 5), strides=(1, 3), padding='same'))
    # model.add(Convolution2D(256, 1, 5, border_mode='same', activation='relu', W_constraint=maxnorm(W_maxnorm)))
    # model.add(MaxPooling2D(pool_size=(1, 5), strides=(1, 3)))
    # model.add(Convolution2D(512, 1, 5, border_mode='same', activation='relu', W_constraint=maxnorm(W_maxnorm)))
    # model.add(MaxPooling2D(pool_size=(1, 5), strides=(1, 3)))
    model.add(Flatten())

    model.add(Dense(32, activation='relu'))
    model.add(Dropout(DROPOUT))
    # model.add(Dense(10, activation='relu'))
    # model.add(Dense(64, activation='relu'))
    # model.add(Dropout(DROPOUT))
    model.add(Dense(2, activation='sigmoid'))
    # model.add(Activation('softmax'))

    myoptimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-06)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model



def train(model, X_train, Y_train):
    # data_code = 'DATACODE'
    # topdir = 'TOPDIR'
    # model_arch = 'MODEL_ARCH'
    model.fit(X_train, Y_train, batch_size=64, epochs=3, validation_split=0.1)
    return model



def save_network(model):
    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")

    model.save('entire_model.h5')


def load_model(model):
    model.load_weights('model.h5')
    return model


def predict(model, X_test):
    # model = build_model()
    return model.predict(X_test)