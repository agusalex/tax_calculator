import pandas as pd


def adjust_price(row):
    """
    Adjusts the price based on the asset class.
    For stocks (STK), it simply adjusts the price by the FX rate to base.
    For options (OPT), it also considers the multiplier in the adjustment.
    """
    if row['AssetClass'] == 'STK':
        return row['TradePrice'] * row['FXRateToBase']
    elif row['AssetClass'] == 'OPT':
        return (row['TradePrice'] * row.get('Multiplier', 1)) * row['FXRateToBase']
    else:
        return None


def filter_convert(df):
    stocks_or_options = df[
        (df['LevelOfDetail'] == 'EXECUTION') & ((df['AssetClass'] == 'STK') | (df['AssetClass'] == 'OPT'))].copy()
    currency_conversions = df[(df['LevelOfDetail'] == 'EXECUTION') & (df['AssetClass'] == 'CASH')].copy()

    # Calculate the new 'price' column
    stocks_or_options['Symbol'] = stocks_or_options['Symbol'].str.replace(' +', '-', regex=True)
    stocks_or_options['price'] = stocks_or_options.apply(adjust_price, axis=1)
    currency_conversions['price'] = currency_conversions['TradePrice']
    implicit_conversions_aux = []
    # Loop through the stocks_or_options DataFrame
    for index, row in stocks_or_options.iterrows():
        if row['CurrencyPrimary'] != 'EUR':
            # Create an entry for implicit currency conversion
            implicit_conversion = {
                'Quantity': row['Quantity'] * row['TradePrice'],
                'AssetClass': row['AssetClass'],
                'price': row['FXRateToBase'],
                'Symbol': "EUR." + row['CurrencyPrimary'],
                'SettleDateTarget': row['SettleDateTarget'],
                'Buy/Sell': row['Buy/Sell'],
                'TradeID': row['TradeID']
            }
            implicit_conversions_aux.append(implicit_conversion)
    implicit_conversions = pd.DataFrame(implicit_conversions_aux)
    currency_conversions = pd.concat([currency_conversions])

    # Call your transformToStandard function (assuming you've defined this elsewhere)
    return stocks_or_options, currency_conversions, implicit_conversions


def transform_to_standard(trades):
    df_selected = trades[['Symbol', 'AssetClass', 'Quantity', 'price', 'Buy/Sell', 'SettleDateTarget', 'TradeID']]
    # Select and rename the columns
    df_renamed = df_selected.rename(columns={
        'Symbol': 'symbol',
        'Quantity': 'amount',
        'price': 'price',
        'Buy/Sell': 'buy_or_sell',
        'SettleDateTarget': 'date',
        'TradeID': 'id',
        'AssetClass': 'asset_class'
    })
    # Export the new DataFrame to a CSV file
    return df_renamed
