import os
import sys
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

def run_svm(file_dataframe, test_size=0.2):
    file_dataframe['new_col'] = pd.to_datetime(file_dataframe['date']).apply(lambda dt: 10000 * dt.year + 1000 * dt.month + dt.day)

    X = file_dataframe[['open']]
    y = file_dataframe['new_col']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    svr_model = SVR(kernel='linear', C=1e3)
    svr_model.fit(X_train, y_train)

    score = svr_model.score(X_test, y_test)
    print('SVM Model Score:', score)

    return score

def main(input_dir):
    files = os.listdir(input_dir)

    for file_name in files:
        file_path = os.path.join(input_dir, file_name)
        file_dataframe = pd.read_csv(file_path)

        print(f"Running SVM on {file_name}")
        run_svm(file_dataframe)

        break  # Just run on first file for now

if __name__ == '__main__':
    main(sys.argv[1])
