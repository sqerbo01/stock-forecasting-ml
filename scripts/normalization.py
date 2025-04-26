import pandas as pd
import os
import sys
from sklearn.preprocessing import MinMaxScaler

def normalize_file(input_path, output_path, cols_to_normalize):
    df = pd.read_csv(input_path)
    scaler = MinMaxScaler()

    df[cols_to_normalize] = scaler.fit_transform(df[cols_to_normalize])
    df.to_csv(output_path, index=False)

def main(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = os.listdir(input_dir)
    for file_name in files:
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)
        cols = ['high', 'open', 'low', 'close', 'volume', 'adj_close']
        normalize_file(input_path, output_path, cols)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
