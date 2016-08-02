import csv
import math
import os.path

try:
    from local_settings import PROCESSED_DATA_DIR, LOCAL_DIRECTORY_BASE
except ImportError:
    from example_settings import PROCESSED_DATA_DIR, LOCAL_DIRECTORY_BASE


def calc_avg(a):
    """Returns the average of the given list of numbers."""
    return sum(a) / float(len(a))


def calc_std_dev(a):
    """Returns the standard deviation of the given list of numbers."""
    mean = calc_avg(a)
    distances = []
    for e in a:
        distances.append(abs(e - mean) ** 2)
    return math.sqrt(sum(distances) / float(len(distances)))


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

        if i == 0:
            row.append('Site AVG')
        else:
            row.append(calc_avg([row[1], row[2], row[3], row[4], row[5]]))

        if i == 0:
            row.append('Site STD DEV')
        else:
            row.append(calc_std_dev([row[1], row[2], row[3], row[4], row[5]]))

    outfile = os.path.join(PROCESSED_DATA_DIR, filename)
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in rows:
            writer.writerow(row)

    print('Wrote to {}'.format(outfile))


if __name__ == '__main__':
    path = os.path.join(LOCAL_DIRECTORY_BASE, 'current')
    process_dendrometer_data(path, 'Mnt_Misery_Table20.csv')
