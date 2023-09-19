import argparse
import pandas as pd
from ibkr_converter import filter_convert, transform_to_standard
from taxable_amount import calculate_stock_taxable_amount
from reports import export_stock_results


def main(args):
    input_csv = args.input_csv
    df = pd.read_csv(input_csv)

    filtered_stocks, filtered_currency_conversions, filtered_implicit_conversions = filter_convert(df)

    stocks = transform_to_standard(filtered_stocks)
    currency_conversions = transform_to_standard(filtered_currency_conversions)
    implicit_conversions = transform_to_standard(filtered_implicit_conversions)

    stocks_report, taxable_gain_total = calculate_stock_taxable_amount(stocks)

    print(f"Total Taxable Gain: {round(taxable_gain_total, 2)}")

    currency_reports = pd.concat([currency_conversions, implicit_conversions])

    export_stock_results(stocks_report,'/output/')
    export_stock_results(currency_reports,'/output/explicit/')
    export_stock_results(implicit_conversions, '/output/implicit/')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some financial data.')
    parser.add_argument('--input_csv', type=str, default='ibkr_input.csv', help='Input CSV file name')

    args = parser.parse_args()
    main(args)