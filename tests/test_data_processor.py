import unittest
from blackrock_data_processor import (
    calc_avg, calc_std_dev, filter_columns
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


if __name__ == '__main__':
    unittest.main()
