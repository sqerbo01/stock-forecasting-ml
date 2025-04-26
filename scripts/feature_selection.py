import os
import sys
import pandas as pd
import numpy as np
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import StratifiedKFold

def feature_selection(input_dir):
    files = os.listdir(input_dir)
    for file_name in files:
        df = pd.read_csv(os.path.join(input_dir, file_name))
        
        if 'adj_close' not in df.columns:
            continue
        
        y = df['adj_close']
        X = df.drop(columns=['symbol', 'date', 'adj_close'], errors='ignore')

        estimator = LinearRegression()
        selector = RFECV(estimator, step=1, cv=StratifiedKFold(n_splits=2, shuffle=True))

        selector = selector.fit(X, y)

        print(f"Selected features for {file_name}: {list(X.columns[selector.support_])}")

if __name__ == '__main__':
    feature_selection(sys.argv[1])
