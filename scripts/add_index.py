import os
import sys
import csv

def add_index(input_dir, sp500_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(sp500_file, 'r') as f:
        sp500_data = list(csv.reader(f))
        sp500_dict = {row[0]: row[1:] for row in sp500_data[1:]}  # skip header

    for file_name in os.listdir(input_dir):
        with open(os.path.join(input_dir, file_name), 'r') as f_in:
            data = list(csv.reader(f_in))
            header = data[0] + ['sp500_open', 'sp500_high', 'sp500_low', 'sp500_close', 'sp500_volume', 'sp500_adj_close']
            new_data = [header]

            for row in data[1:]:
                date = row[1]
                sp500_row = sp500_dict.get(date, [''] * 6)
                new_data.append(row + sp500_row)

        with open(os.path.join(output_dir, file_name), 'w', newline='') as f_out:
            writer = csv.writer(f_out)
            writer.writerows(new_data)

if __name__ == '__main__':
    add_index(sys.argv[1], sys.argv[2], sys.argv[3])
