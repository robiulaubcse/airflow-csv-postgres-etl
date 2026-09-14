def transform_sales(df):
    df = df.copy()

    df["total_amount"] = df["quantity"] * df["price"]

    print(f"Transformed rows: {len(df)}")
    print(df.head())

    return df