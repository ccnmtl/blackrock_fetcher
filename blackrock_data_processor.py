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


def filter_columns(keep_columns, rows):
    """Filter CSV-style data based on a list of column names.

    Returns a list of lists.
    """
    newrows = []
    keep_indices = []

    # Find the column indices to keep.
    for i, name in enumerate(rows[0]):
        if name in keep_columns:
            keep_indices.append(i)

    for i, row in enumerate(rows):
        newrow = []
        for keep_idx in keep_indices:
            newrow.append(row[keep_idx])
        newrows.append(newrow)

    return newrows


def process_dendrometer_data(path, filename):
    fname = os.path.join(path, filename)
    rows = []
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            rows += [row]

    # Remove blank rows
    # The incoming CSV contains a few rows near the beginning that we don't
    # want.
    del rows[0]
    del rows[1]
    del rows[1]

    #
    # The incoming CSV's header row looks like this:
    #   "TIMESTAMP", "RECORD", "Battery_Volt_MIN", "ProgSig",
    #   "Red_Oak_1_AVG", "Red_Oak_1_MAX", "Red_Oak_1_MIN", "Red_Oak_1_STD",
    #   "Red_Oak_2_AVG", "Red_Oak_2_MAX", "Red_Oak_2_MIN", "Red_Oak_2_STD",
    #   "Red_Oak_3_AVG", "Red_Oak_3_MAX", "Red_Oak_3_MIN", "Red_Oak_3_STD",
    #   "Red_Oak_4_AVG", "Red_Oak_4_MAX", "Red_Oak_4_MIN", "Red_Oak_4_STD",
    #   "Red_Oak_5_AVG", "Red_Oak_5_MAX", "Red_Oak_5_MIN", "Red_Oak_5_STD"
    #
    # Here are the columns we want to filter to:
    keep_columns = [
        'TIMESTAMP', 'Red_Oak_1_AVG', 'Red_Oak_2_AVG', 'Red_Oak_3_AVG',
        'Red_Oak_4_AVG', 'Red_Oak_5_AVG'
    ]
    newrows = filter_columns(keep_columns, rows)

    for i, row in enumerate(newrows):
        newrow = newrows[i]
        if i == 0:
            newrow.append('Site AVG')
        else:
            newrow.append(calc_avg([newrow[1], newrow[2], newrow[3],
                                    newrow[4], newrow[5]]))

        if i == 0:
            newrow.append('Site STD DEV')
        else:
            newrow.append(calc_std_dev([newrow[1], newrow[2], newrow[3],
                                        newrow[4], newrow[5]]))

    outfile = os.path.join(PROCESSED_DATA_DIR, filename)
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in newrows:
            writer.writerow(row)

    print('Wrote to %s' % outfile)


def process_environmental_data(path, filename):
    fname = os.path.join(path, filename)
    rows = []
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            rows += [row]

    # Remove blank rows
    # The incoming CSV contains a few rows near the beginning that we don't
    # want.
    del rows[0]
    del rows[1]
    del rows[1]

    #
    # The incoming CSV's header row looks like this:
    # "TIMESTAMP", "RECORD", "AvgTEMP_C", "MinTEMP_C", "MaxTEMP_C",
    # "AvgRh", "MaxRh", "MinRh", "AvgVP", "AvgDewPt", "TotalPAR",
    # "AvgGSR", "AvgWspd", "AvgWdir", "StdDevWdir", "MaxWspd",
    # "TotalRain", "AvgBP", "MaxBP", "MinBp", "AvgST_10", "AvgST_100",
    # "MinBatt", "AvgCO2", "AvgOzone", "DSTEMPF", "DSDEPTH", "DSRETRIES",
    # "SoilM_5cm", "SoilM_15cm", "UVB", "UVTEMP", "UVA", "V2mV", "V2mV2",
    # "Snow1_BATT", "Snow1_PNLTMP", "CM3_up", "CM3_dn", "CG3_up",
    #  "CG3_dn", "CM_TempC", "CM3_TempK", "Net_Rs", "Net_R1", "Albedo",
    # "Up_Total", "Dn_Total", "Net_Total", "AvgPAR_Den", "MaxPAR_Den",
    # "MinPAR_Den"
    #
    # Here are the columns we want to filter to:
    keep_columns = [
        'TIMESTAMP', 'AvgTEMP_C', 'AvgVP', 'TotalRain',
        'SoilM_5cm', 'AvgPAR_Den'
    ]
    newrows = filter_columns(keep_columns, rows)

    outfile = os.path.join(PROCESSED_DATA_DIR, filename)
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in newrows:
            writer.writerow(row)

    print('Wrote to %s' % outfile)


if __name__ == '__main__':
    path = os.path.join(LOCAL_DIRECTORY_BASE, 'current')
    process_dendrometer_data(path, 'Mnt_Misery_Table20.csv')
    process_environmental_data(path, 'Lowland.csv')
