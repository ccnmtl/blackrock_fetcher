import csv
import os.path

try:
    from local_settings import PROCESSED_DATA_DIR
except ImportError:
    from example_settings import PROCESSED_DATA_DIR


def process(fname):
    rows = []
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        for row in reader:
            rows += [row]

    # Remove blank rows
    del rows[0]
    del rows[1]
    del rows[1]

    outfile = os.path.join(PROCESSED_DATA_DIR, 'processed_data.csv')
    print(outfile)
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)
