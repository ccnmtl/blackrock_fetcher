import csv
import os.path

try:
    from local_settings import PROCESSED_DATA_DIR
except ImportError:
    from example_settings import PROCESSED_DATA_DIR


def process_dendrometer_data(path, filename):
    fname = os.path.join(path, filename)
    rows = []
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows += [row]

    # Remove blank rows
    del rows[0]
    del rows[1]
    del rows[1]

    # Remove columns that we don't want
    for row in rows:
        del row[0]
        del row[0]
        del row[0]
        del row[0]
        del row[1]
        del row[1]
        del row[1]
        del row[2]
        del row[2]
        del row[2]
        del row[3]
        del row[3]
        del row[3]
        del row[4]
        del row[4]
        del row[5]
        del row[5]
        del row[5]

    outfile = os.path.join(PROCESSED_DATA_DIR, filename)
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)

    print('Wrote to {}'.format(outfile))
