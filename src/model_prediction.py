import pandas as pd
import argparse

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, LSTM, Dense
from sklearn.metrics import mean_squared_error as mse
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint

#We input the number of regions we are going to focus on
num_regions=8
#We choose the parameters for our model
window_size=10
num_train = 300
num_train2 = num_train+300
num_val = 150
#num:test would be the last 20% of the year, to comply with the task
num_test = 300

def load_data(file_path):
    # TODO: Load test data from CSV file
        data_csv = '../data/processed_data.csv'
    #Leemos el archivo, indicando que la primera columna son datos de fecha y hora
    #le decimos que use esos timestamps como indice
    df = pd.read_csv(data_csv, parse_dates=[0], index_col=0)
    return df

def load_model(model_path):
    # TODO: Load the trained model
    return model

def make_predictions(df, model):
    # TODO: Use the model to make predictions on the test data
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
    #Make predictions
    predictions = model.predict(X_test, y_test)
    return predictions

def save_predictions(predictions, predictions_file):
    # TODO: Save predictions to a JSON file
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Prediction script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file', 
        type=str, 
        default='data/test_data.csv', 
        help='Path to the test data file to make predictions'
    )
    parser.add_argument(
        '--model_file', 
        type=str, 
        default='models/model.pkl',
        help='Path to the trained model file'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='predictions/predictions.json', 
        help='Path to save the predictions'
    )
    return parser.parse_args()

def main(input_file, model_file, output_file):
    df = load_data(input_file)
    model = load_model(model_file)
    predictions = make_predictions(df, model)
    save_predictions(predictions, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.model_file, args.output_file)
