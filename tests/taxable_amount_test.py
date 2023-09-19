import unittest
import pandas as pd
from taxable_amount import calculate_stock_taxable_amount


class TestLongSuite(unittest.TestCase):
    def test_basic(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4'],
                'amount': [9000, -9000, 10000],
                'price': [0.21761394, 0.22319982, 0.21763141],
                'buy_or_sell': ['buy', 'sell', 'buy'],
                'total': [1958.52546, -2008.79838, 2176.3141]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)
        self.assertAlmostEqual(df.loc[1, 'Taxable_Amount'], 50.27292)
        self.assertAlmostEqual(total_tax, 50.27292)

    def test_all_trades(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4', 'RE4', 'RE4', 'RE4'],
                'amount': [9000, -9000, 10000, 11000, -5000, -5000],
                'price': [0.21761394, 0.22319982, 0.21763141, 0.1777633, 0.18793334, 0.19086441],
                'buy_or_sell': ['buy', 'sell', 'buy', 'buy', 'sell', 'sell'],
                'total': [1958.53, -2008.80, 2176.31, 1955.40, -939.67, -954.32]}

        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)

        self.assertEqual(round(df.loc[1, 'Taxable_Amount'], 2), 50.27)
        self.assertEqual(round(df.loc[4, 'Taxable_Amount'], 2), -44.07)
        self.assertEqual(round(df.loc[5, 'Taxable_Amount'], 2), -29.42)

        self.assertEqual(round(total_tax, 2), -23.22)

    def test_all_buy(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4'],
                'amount': [9000, 10000, 11000],
                'price': [0.21761394, 0.21763141, 0.1777633],
                'buy_or_sell': ['buy', 'buy', 'buy'],
                'total': [1958.53, 2176.31, 1955.4]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)
        self.assertEqual(total_tax, 0.0)

    def test_all_sell(self):
        data = {'symbol': ['RE4', 'RE4'],
                'amount': [-9000, -10000],
                'price': [0.21761394, 0.21763141],
                'buy_or_sell': ['sell', 'sell'],
                'total': [-2008.80, -2176.31]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)
        self.assertEqual(total_tax, 0.0)


class TestShortSuite(unittest.TestCase):
    def test_basic(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4'],
                'amount': [-9000, 9000, -10000],
                'price': [0.21761394, 0.22319982, 0.21763141],
                'buy_or_sell': ['sell', 'buy', 'sell'],
                'total': [-1958.52546, 2008.79838, -2176.3141]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)
        self.assertAlmostEqual(df.loc[1, 'Taxable_Amount'], -50.27292)
        self.assertAlmostEqual(total_tax, -50.27292)

    def test_short_for_profit(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4'],
                'amount': [-9000, 9000, -10000],
                'price': [0.22319982, 0.21761394, 0.21000000],
                'buy_or_sell': ['sell', 'buy', 'sell'],
                'total': [-2008.79838, 1958.52546, -2100.00000]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)

        # The taxable amount for the second trade should be negative, as we bought shares cheaper than we sold.
        self.assertAlmostEqual(df.loc[1, 'Taxable_Amount'], 50.2729199999)
        # For the third trade, since we are opening a new short position, the taxable gain should be 0
        self.assertAlmostEqual(df.loc[2, 'Taxable_Amount'], 0)
        # The total tax should be the sum of the taxable amounts for each trade.
        self.assertAlmostEqual(total_tax, 50.2729199999)

    def test_long_to_short(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4', 'RE4'],
                'amount': [9000, -9000, -10000, 5000],
                'price': [0.21761394, 0.22319982, 0.21763141, 0.22000000],
                'buy_or_sell': ['buy', 'sell', 'sell', 'buy'],
                'total': [1958.52546, -2008.79838, -2176.3141, 1100]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)

        self.assertAlmostEqual(df.loc[1, 'Taxable_Amount'], 50.27292)
        self.assertAlmostEqual(df.loc[2, 'Taxable_Amount'], 0)
        self.assertAlmostEqual(df.loc[3, 'Taxable_Amount'], -11.84295)

        self.assertAlmostEqual(total_tax, 54.11583)

    def test_short_to_long(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4', 'RE4'],
                'amount': [-9000, 9000, 10000, -5000],
                'price': [0.21761394, 0.22319982, 0.21763141, 0.22000000],
                'buy_or_sell': ['sell', 'buy', 'buy', 'sell'],
                'total': [-1958.52546, 2008.79838, 2176.3141, -1100]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)

        self.assertAlmostEqual(df.loc[1, 'Taxable_Amount'], -50.27292)
        self.assertAlmostEqual(df.loc[2, 'Taxable_Amount'], 0)
        self.assertAlmostEqual(df.loc[3, 'Taxable_Amount'], 11.84295)

        self.assertAlmostEqual(total_tax, -38.42996999)

    def test_all_trades(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4', 'RE4', 'RE4', 'RE4'],
                'amount': [-9000, 9000, -10000, -11000, 5000, 5000],
                'price': [0.21761394, 0.22319982, 0.21763141, 0.1777633, 0.18793334, 0.19086441],
                'buy_or_sell': ['sell', 'buy', 'sell', 'sell', 'buy', 'buy'],
                'total': [-1958.53, 2008.80, -2176.31, -1955.40, 939.67, 954.32]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)

        self.assertEqual(round(df.loc[1, 'Taxable_Amount'], 2), -50.27)
        self.assertEqual(round(df.loc[4, 'Taxable_Amount'], 2), 44.07)
        self.assertEqual(round(df.loc[5, 'Taxable_Amount'], 2), 29.42)
        self.assertEqual(round(total_tax, 2), 23.22)

    def test_all_sell(self):
        data = {'symbol': ['RE4', 'RE4', 'RE4'],
                'amount': [-9000, -10000, -11000],
                'price': [0.21761394, 0.21763141, 0.1777633],
                'buy_or_sell': ['sell', 'sell', 'sell'],
                'total': [-1958.53, -2176.31, -1955.4]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)
        self.assertEqual(total_tax, 0.0)

    def test_all_buy(self):
        data = {'symbol': ['RE4', 'RE4'],
                'amount': [9000, 10000],
                'price': [0.21761394, 0.21763141],
                'buy_or_sell': ['buy', 'buy'],
                'total': [2008.80, 2176.31]}
        df = pd.DataFrame(data)
        df, total_tax = calculate_stock_taxable_amount(df)
        self.assertEqual(total_tax, 0.0)


if __name__ == '__main__':
    unittest.main()
