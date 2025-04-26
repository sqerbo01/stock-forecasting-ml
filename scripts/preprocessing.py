import os
import sys
import csv
import math

def roundup(var):
    return float(format(var, '.6f'))

def preprocess_file(input_path, output_path):
    with open(input_path, 'r') as textfile:
        reader = list(csv.reader(textfile))
        header = reader[0]
        data = reader[1:]

        new_data = []
        prev = 0.0
        avg = 0.0
        num_moving_avg = 50
        volatile_avg = 0.0
        num_volatile = 10
        curr_volatility = 0.0

        for count, row in enumerate(reversed(data)):
            if count == 0:
                row.append(prev)
            else:
                diff = roundup(float(row[7]) - float(prev))
                row.append(diff)

            if count < num_moving_avg:
                avg = roundup((count * avg + float(row[7])) / (count + 1))
            else:
                avg = roundup((num_moving_avg * avg + float(row[7]) - float(data[count - num_moving_avg][7])) / num_moving_avg)

            if count < num_volatile:
                volatile_avg = roundup((count * volatile_avg + float(row[7])) / (count + 1))
            else:
                volatile_avg = roundup((num_volatile * volatile_avg + float(row[7]) - float(data[count - num_volatile][7])) / num_volatile)

            if count:
                loop_count = min(count, num_volatile)
                for i in range(loop_count):
                    curr_volatility += math.pow((float(row[7]) - volatile_avg), 2)
                curr_volatility = roundup(math.sqrt(curr_volatility / loop_count))

            row.append(avg)
            row.append(curr_volatility)
            prev = float(row[7])
            curr_volatility = 0.0
            new_data.append(row)

    new_data.insert(0, header + ['prev_day_diff', '50_day_moving_avg', '10_day_volatility'])

    with open(output_path, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(new_data)

def main(input_dir, output_dir):
    files = os.listdir(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in files:
        preprocess_file(os.path.join(input_dir, file_name), os.path.join(output_dir, file_name))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
