import argparse
import pandas as pd
from ibkr_converter import filter_convert, transform_to_standard
from taxable_amount import calculate_stock_taxable_amount, calculate_currency_impact
from reports import export_per_symbol, export_singlefile


def main(args):
    input_csv = args.input_csv
    df = pd.read_csv(input_csv)

    filtered_stocks, filtered_currency_conversions, filtered_implicit_conversions = filter_convert(df)

    stocks = transform_to_standard(filtered_stocks)
    explicit_conversions = transform_to_standard(filtered_currency_conversions)
    implicit_conversions = transform_to_standard(filtered_implicit_conversions)

    stocks_report, taxable_gain_total = calculate_stock_taxable_amount(stocks)

    combined_conversions = pd.concat([explicit_conversions, implicit_conversions], ignore_index=True)

    currency_impact = calculate_currency_impact(combined_conversions)

    print(f"Total Taxable Gain: {round(taxable_gain_total, 2)}")

    currency_reports = pd.concat([explicit_conversions, implicit_conversions])

    export_per_symbol(stocks_report, '/output/')
    export_singlefile(stocks_report, '/output/', 'trades')
    export_singlefile(currency_reports, '/output/', 'explicit_conversions')
    export_singlefile(implicit_conversions, '/output/', 'implicit_conversions')
    export_singlefile(currency_impact, '/output/', 'currency_impact')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some financial data.')
    parser.add_argument('--input_csv', type=str, default='ibkr_input.csv', help='Input CSV file name')

    args = parser.parse_args()
    main(args)