import csv
import os.path

try:
    from local_settings import PROCESSED_DATA_DIR, LOCAL_DIRECTORY_BASE
except ImportError:
    from example_settings import PROCESSED_DATA_DIR, LOCAL_DIRECTORY_BASE


def process_dendrometer_data(path, filename):
    fname = os.path.join(path, filename)
    rows = []
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            rows += [row]

    # Remove blank rows
    del rows[0]
    del rows[1]
    del rows[1]

    for i, row in enumerate(rows):
        # Remove columns that we don't want
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
        del row[4]
        del row[5]
        del row[5]
        del row[6]
        del row[6]
        del row[6]

        # Calculate site average
        if i == 0:
            row.append('Site AVG')
        else:
            avg = (row[1] + row[2] + row[3] + row[4] + row[5]) / 5
            row.append(avg)

    outfile = os.path.join(PROCESSED_DATA_DIR, filename)
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in rows:
            writer.writerow(row)

    print('Wrote to {}'.format(outfile))


if __name__ == '__main__':
    path = os.path.join(LOCAL_DIRECTORY_BASE, 'current')
    process_dendrometer_data(path, 'Mnt_Misery_Table20.csv')
