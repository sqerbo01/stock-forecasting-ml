import os
import sys
import csv
import pandas as pd
import yfinance as yf

def fetch_stock_data(symbol_file, output_dir, start_date="2000-01-01", end_date=None):
    """Fetch stock data using Yahoo Finance."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

    with open(symbol_file, 'r') as f:
        symbols = [line.strip() for line in f.readlines()]

    for symbol in symbols:
        try:
            print(f"Fetching {symbol} from Yahoo Finance...")
            df = yf.download(symbol, start=start_date, end=end_date)

            if df.empty:
                print(f"Warning: No data for {symbol}")
                continue

            df = df.reset_index()
            df.rename(columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Adj Close': 'adj_close',
                'Volume': 'volume'
            }, inplace=True)

            df.insert(0, 'symbol', symbol)

            output_path = os.path.join(output_dir, f"{symbol}.csv")
            df.to_csv(output_path, index=False)
            print(f"Saved {symbol} to {output_path}")

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

if __name__ == '__main__':
    fetch_stock_data(sys.argv[1], sys.argv[2])
