import os
import sys
import pickle
import traceback
from helpers.regression_helpers import load_dataset, addFeatures, mergeDataframes, count_missing, applyTimeLag, performRegression

def main(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    scores = {}
    files = os.listdir(input_dir)

    delta_range = range(8, 30)
    print('Delta days accounted:', max(delta_range))

    for file_name in files:
        try:
            symbol = file_name.split('.')[0]
            datasets = load_dataset(input_dir, file_name)

            for dataset in datasets:
                columns = dataset.columns
                adjclose = columns[-2]
                returns = columns[-1]
                for delta in delta_range:
                    addFeatures(dataset, adjclose, returns, delta)
                dataset = dataset.iloc[max(delta_range):, :]

            finance = mergeDataframes(datasets)

            high_value = min(365, finance.shape[0] - 1)
            lags = range(high_value, 30)

            if 'symbol' in finance.columns:
                finance.drop('symbol', axis=1, inplace=True)

            print('Dataset size:', finance.shape)
            print('Missing after merge:', count_missing(finance))

            finance = finance.interpolate(method='time').fillna(finance.mean())

            finance.columns = [col.replace('&', '_and_') for col in finance.columns]

            finance.open = finance.open.shift(-1)

            finance = applyTimeLag(finance, [high_value], delta_range)

            print('Missing after shift:', count_missing(finance))

            mean_squared_errors, r2_scores = performRegression(finance, 0.95, symbol, output_dir)

            scores[symbol] = [mean_squared_errors, r2_scores]

        except Exception as e:
            traceback.print_exc()

    with open(os.path.join(output_dir, 'scores.pickle'), 'wb') as f:
        pickle.dump(scores, f)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
