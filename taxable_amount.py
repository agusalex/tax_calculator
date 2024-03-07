import pandas as pd


def calculate_stock_taxable_amount(df):
    # Initialize variables
    symbol_to_accumulated_securities = {}
    symbol_to_avg_moving_price = {}
    taxable_gain_total = 0.0
    # Read CSV into a DataFrame
    # Initialize new columns for the DataFrame
    df['Accumulated_Securities'] = 0
    df['Avg_Moving_Price'] = 0.0
    df['Taxable_Amount'] = 0.0
    # Loop through each row in the DataFrame
    for i, row in df.iterrows():
        symbol = row['symbol']
        amount = row['amount']
        price = row['price']
        sell_or_buy = row['buy_or_sell']

        # Initialize if symbol not encountered before
        if symbol not in symbol_to_accumulated_securities:
            symbol_to_accumulated_securities[symbol] = 0
            symbol_to_avg_moving_price[symbol] = 0.0

        previous_amount = symbol_to_accumulated_securities[symbol]
        previous_avg_moving_price = symbol_to_avg_moving_price[symbol]

        buy = "buy"
        # When closing a short
        if previous_amount + amount == 0 and sell_or_buy.lower() == "buy":
            buy = "sell"
        # When shorting
        elif previous_amount + amount < 0:
            buy = "sell"

        # Update accumulated amount and average moving price based on whether it's a 'buy' or 'sell' operation
        if sell_or_buy.lower() == buy:
            new_total_amount = previous_amount + amount
            new_avg_moving_price = (previous_avg_moving_price * previous_amount + amount * price) / (
                    previous_amount + amount)
            print(new_avg_moving_price)
        else:  # 'sell'
            new_total_amount = previous_amount + amount
            new_avg_moving_price = previous_avg_moving_price
            taxable_gain = -(price - previous_avg_moving_price) * amount
            taxable_gain_total += taxable_gain
            df.at[i, 'Taxable_Amount'] = taxable_gain

        print(
            f"Symbol: {symbol}, Price: {price}, Units: {amount}, Taxable Amount: {round(df.at[i, 'Taxable_Amount'], 2)}, Avg"
            f"Moving Price: {round(new_avg_moving_price, 4)}")
        # Update DataFrame and dictionaries for future rows
        df.at[i, 'Accumulated_Securities'] = new_total_amount
        df.at[i, 'Avg_Moving_Price'] = new_avg_moving_price
        symbol_to_accumulated_securities[symbol] = new_total_amount
        symbol_to_avg_moving_price[symbol] = new_avg_moving_price

    return df, taxable_gain_total


def calculate_currency_impact(df):
    currency_impacts = []
    currency_map = {}  # Store the cumulative total and amounts for calculating MAP

    for i, row in df.iterrows():
        currency = row['symbol'].split('.')[1]
        exchange_rate = row['price']
        transaction_amount = row['amount']
        transaction_id = row['id']

        # Initialize currency in map if not present
        if currency not in currency_map:
            currency_map[currency] = {'total_value': 0, 'total_amount': 0}

        # Calculate the impact based on MAP if available
        previous_map = currency_map[currency]['total_value'] / max(1, currency_map[currency]['total_amount'])
        impact = 0
        if transaction_amount != 0:  # Avoid division by zero
            if row['buy_or_sell'].upper() == 'BUY':
                # For buys, impact is negative as it represents a cost
                impact = -(abs(transaction_amount) * exchange_rate - abs(transaction_amount) * previous_map)
            else:
                # For sells, impact is positive as it represents a gain
                impact = abs(transaction_amount) * exchange_rate - abs(transaction_amount) * previous_map

        # Update the currency map with new total values and amounts for MAP calculation
        new_total_amount = currency_map[currency]['total_amount'] + abs(transaction_amount)
        new_total_value = currency_map[currency]['total_value'] + abs(transaction_amount) * exchange_rate
        currency_map[currency]['total_amount'] = new_total_amount
        currency_map[currency]['total_value'] = new_total_value

        # Record the transaction impact along with updated MAP
        new_map = new_total_value / max(1, new_total_amount)  # Avoid division by zero
        currency_impacts.append({
            'TransactionID': transaction_id,
            'Currency': currency,
            'Impact': impact,
            'MovingAveragePrice': new_map,
        })

    return pd.DataFrame(currency_impacts)