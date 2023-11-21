import pandas as pd
import argparse

import tensorflow as tf
import os
import pandas as pd
import numpy as np
import pickle

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import InputLayer, LSTM, Dense
from sklearn.metrics import mean_squared_error as mse
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint

extra_info=True

#We input the number of regions we are going to focus on
num_regions=8
#We choose the parameters for our model
window_size=10
num_train = 300
num_train2 = num_train+300
num_val = 150
#num:test would be the last 20% of the year, to comply with the task
num_test = 300

#We will use this function later to predict to plot the predictions alongside the labels
def plot_predictions1(model, X, y, start=0, end=100):
  predictions = model.predict(X).flatten()
  df = pd.DataFrame(data={'Predictions':predictions, 'Actuals':y})
  plt.plot(df['Predictions'][start:end])
  plt.plot(df['Actuals'][start:end])
  return df, mse(y, predictions)

def df_to_X_y(df, window_size=window_size):
    df_as_np = df.to_numpy()
    X = []
    y = []
    for i in range(len(df_as_np) - window_size):
        #We take every column except the last one, because its values are the labels
        row = [r[0:-1] for r in df_as_np[i:i+window_size]]
        X.append(row)
        label = df_as_np[i+window_size][-1]
        y.append(label)
    return np.array(X), np.array(y)


def load_data(file_path):
    # TODO: Load processed data from CSV file
    data_csv = './data/your_train.csv'
    #Leemos el archivo, indicando que la primera columna son datos de fecha y hora
    #le decimos que use esos timestamps como indice
    df = pd.read_csv(data_csv, parse_dates=[0], index_col=0)
    return df

def split_data(df):
    # TODO: Split data into training and validation sets (the test set is already provided in data/test_data.csv)
    df_to_X_y(df, window_size=window_size)
    X, y = df_to_X_y(df)
    if extra_info:
        X.shape, y.shape
    #X_train and y_train have a size of "num_train"
    X_train, y_train = X[:num_train], y[:num_train]
    #X_val and y_val have a size of "num_val"
    X_val, y_val = X[num_train:(num_train+num_val)], y[num_train:(num_train+num_val)]
    #X_test and y_test have a size of "num_test"
    X_test, y_test = X[(num_train+num_val):(num_train+num_val+num_test)], y[num_train:(num_train+num_test)]
    if extra_info:
        X_train.shape, y_train.shape, X_val.shape, y_val.shape, X_test.shape, y_test.shape
    return X_train, X_val, y_train, y_val

def train_model(X_train, y_train, X_val, y_val):
    # TODO: Initialize your model and train it
    #We create our model, adding the necessary layers

    model1 = Sequential()
    model1.add(InputLayer((window_size, 51)))
    model1.add(LSTM(100))
    model1.add(Dense(8, 'relu'))
    model1.add(Dense(1, 'linear'))
    if extra_info:
        model1.summary()
    cp4 = ModelCheckpoint('./models/model_checkpoint/', save_best_only=True)
    model1.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.0002), metrics=[RootMeanSquaredError()])
    model1.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=12, callbacks=[cp4])
    return model1

def save_model(model1, model_path):
    # TODO: Save your trained model
    model1.save('./models/saved_model_folder')
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Model training script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/your_train.csv', 
        help='Path to the processed data file to train the model'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models', 
        help='Path to save the trained model'
    )
    return parser.parse_args()

def main(input_file, model_file):
    df = load_data(input_file)
    X_train, X_val, y_train, y_val = split_data(df)
    model = train_model(X_train, y_train, X_val, y_val)
    save_model(model, model_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file)