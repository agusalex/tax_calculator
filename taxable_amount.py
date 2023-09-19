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
