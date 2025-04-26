import os
import sys
import pandas as pd

def interpolate(dataframe, cols_to_interpolate):
    for col in cols_to_interpolate:
        dataframe[col] = dataframe[col].interpolate(method='spline', order=2)
    return dataframe

def main(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = os.listdir(input_dir)
    for file_name in files:
        df = pd.read_csv(os.path.join(input_dir, file_name))
        cols = ['high', 'open', 'low', 'close', 'volume', 'adj_close']
        df = interpolate(df, cols)
        df.to_csv(os.path.join(output_dir, file_name), index=False)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
