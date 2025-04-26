# scripts/fetch_data.py

import os
import csv
from ychartspy.client import YChartsClient

def convert(timestamp):
    """Convert timestamp from ms to date string."""
    import datetime
    return datetime.datetime.fromtimestamp(int(timestamp) / 1e3).strftime('%Y-%m-%d')

def fetch_stock_data(symbol_file, parameter_file, output_dir):
    """Fetch stock data using YCharts API."""
    with open(parameter_file, 'r') as f:
        parameters = [line.strip() for line in f.readlines()]

    client = YChartsClient()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(symbol_file, 'r') as f:
        for symbol_row in csv.reader(f):
            symbol = symbol_row[0].strip()
            data = {}

            for param in parameters:
                try:
                    rows = client.get_security_metric(symbol, param, start_date="01/01/1900")
                    for ts, value in rows:
                        date = convert(ts)
                        if date not in data:
                            data[date] = {"symbol": symbol, "date": date}
                        data[date][param] = value
                except Exception as e:
                    print(f"Error fetching {param} for {symbol}: {e}")

            # Save data
            output_path = os.path.join(output_dir, f"{symbol}.csv")
            if data:
                df = pd.DataFrame(list(data.values()))
                df.to_csv(output_path, index=False)
                print(f"Saved {symbol} to {output_path}")

if __name__ == '__main__':
    import sys
    fetch_stock_data(sys.argv[1], sys.argv[2], sys.argv[3])
