import os


def export_stock_results(df, path):
    full_path = os.getcwd() + path
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    for symbol, group_df in df.groupby('symbol'):
        group_df.to_csv(f"{full_path}{symbol}_table.csv", index=False)
