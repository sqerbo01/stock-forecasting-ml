import os
import sys
import numpy as np
import pandas as pd
from helpers.neural_network import NeuralNet

def run_custom_nn(df, col='adj_close', test_size=0.2):
    series = df[col].dropna().values
    X = np.arange(len(series)).reshape(-1, 1)
    y = series

    split_index = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    model = NeuralNet(num_nodes=50, learn_rate=0.001)
    model.fit(X_train, y_train, maxiter=500, SGD=True, batch=32)

    preds = model.predict(X_test, proba=False)
    preds = preds.flatten()

    mse = np.mean((preds - y_test) ** 2)
    print(f'Custom Neural Network Test MSE: {mse:.4f}')

def main(input_dir):
    files = os.listdir(input_dir)
    for file_name in files:
        file_path = os.path.join(input_dir, file_name)
        df = pd.read_csv(file_path)

        if 'adj_close' in df.columns:
            print(f"Running Custom Neural Network on {file_name}")
            run_custom_nn(df)
            break

if __name__ == '__main__':
    main(sys.argv[1])