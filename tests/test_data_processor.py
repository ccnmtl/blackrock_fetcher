import unittest
from blackrock_data_processor import calc_avg, calc_std_dev


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


if __name__ == '__main__':
    unittest.main()
