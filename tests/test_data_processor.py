import unittest
from datetime import datetime
from blackrock_data_processor import (
    calc_avg, calc_std_dev, filter_columns, filter_rows,
    match_replace
)


class TestCalculations(unittest.TestCase):
    def test_calc_avg(self):
        self.assertEqual(calc_avg([1]), 1)
        self.assertEqual(calc_avg([6, 3, 2, 1]), 3)
        self.assertEqual(calc_avg([13, 23, 12, 44, 55]), 29.4)

    def test_calc_std_dev(self):
        self.assertAlmostEqual(
            calc_std_dev([1, 2, 3, 4, 5]),
            1.41421,
            places=5)
        self.assertAlmostEqual(
            calc_std_dev([13, 23, 12, 44, 55]),
            17.21162,
            places=5)


class TestFilterColumns(unittest.TestCase):
    def test_filter_columns(self):
        rows = [
            ['a', 'b', 'c', 'd'],
            [1, 5, 4, 7],
            [6, 5, 4, 2],
            [9, 5, 6, 1],
            [1, 2, 3, 4],
        ]

        newrows = filter_columns(['a', 'b', 'c', 'd'], rows)
        self.assertEqual(
            newrows, rows,
            'Should equal itself when all rows are selected.')

        newrows = filter_columns(['a', 'c'], rows)
        self.assertEqual(newrows, [
            ['a', 'c'],
            [1, 4],
            [6, 4],
            [9, 6],
            [1, 3],
        ])

        newrows = filter_columns(['c', 'd'], rows)
        self.assertEqual(newrows, [
            ['c', 'd'],
            [4, 7],
            [4, 2],
            [6, 1],
            [3, 4],
        ])

        newrows = filter_columns([], rows)
        self.assertEqual(newrows, [[], [], [], [], []])


class TestFilterRows(unittest.TestCase):
    def test_filter_rows(self):
        rows = [
            ['timestamp', 'b', 'c', 'd'],
            ['2016-06-20 11:00:00', 5, 4, 7],
            ['2016-07-15 07:03:30', 5, 4, 2],
            ['2016-08-20 13:01:00', 5, 6, 1],
            ['2016-08-21 15:00:00', 2, 3, 4],
        ]

        newrows = filter_rows(rows)
        self.assertEqual(newrows, rows)

        newrows = filter_rows(rows, start_dt=datetime(2016, 8, 20, 12, 30))
        self.assertEqual(newrows, [
            ['timestamp', 'b', 'c', 'd'],
            ['2016-08-20 13:01:00', 5, 6, 1],
            ['2016-08-21 15:00:00', 2, 3, 4],
        ])

        newrows = filter_rows(
            rows,
            start_dt=datetime(2016, 8, 20, 12, 30),
            end_dt=datetime(2016, 8, 20, 14, 30))
        self.assertEqual(newrows, [
            ['timestamp', 'b', 'c', 'd'],
            ['2016-08-20 13:01:00', 5, 6, 1],
        ])


class TestMatchReplace(unittest.TestCase):
    def test_match_replace(self):
        rows = [
            ['timestamp', 'Red_Oak_1', 'Red_Oak_2', 'Red_Oak_3'],
            ['2016-06-20 11:00:00', 5, 4, 7],
            ['2016-07-15 07:03:30', 5, 4, 2],
            ['2016-08-20 13:01:00', 5, 6, 1],
            ['2016-08-21 15:00:00', 2, 3, 4],
        ]

        newrows = match_replace(rows, 'Red_Oak', 'Red_Oak')
        self.assertEqual(newrows, rows)

        newrows = match_replace(rows, 'Red_Oak', 'White_Oak')
        self.assertEqual(newrows, [
            ['timestamp', 'White_Oak_1', 'White_Oak_2', 'White_Oak_3'],
            ['2016-06-20 11:00:00', 5, 4, 7],
            ['2016-07-15 07:03:30', 5, 4, 2],
            ['2016-08-20 13:01:00', 5, 6, 1],
            ['2016-08-21 15:00:00', 2, 3, 4],
        ])

        newrows = match_replace([], 'Red_Oak', 'White_Oak')
        self.assertEqual(newrows, [])


if __name__ == '__main__':
    unittest.main()
