import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def prepare_sequences(series, n_steps):
    X, y = [], []
    for i in range(len(series) - n_steps):
        seq_x, seq_y = series[i:i + n_steps], series[i + n_steps]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

def run_lstm(df, col='adj_close', n_steps=10, test_size=0.2):
    series = df[col].dropna().values
    X, y = prepare_sequences(series, n_steps)

    split_index = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    model = create_lstm_model((n_steps, 1))
    model.fit(X_train, y_train, epochs=20, verbose=0)

    loss = model.evaluate(X_test, y_test)
    print(f'LSTM Test Loss (MSE): {loss}')

def main(input_dir):
    files = os.listdir(input_dir)
    for file_name in files:
        file_path = os.path.join(input_dir, file_name)
        df = pd.read_csv(file_path)

        if 'adj_close' in df.columns:
            print(f"Running LSTM on {file_name}")
            run_lstm(df)
            break  # Just first file for testing

if __name__ == '__main__':
    main(sys.argv[1])
