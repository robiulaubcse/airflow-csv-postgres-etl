import pandas as pd


def extract_sales():
    file_path = "/opt/airflow/data/sales.csv"

    df = pd.read_csv(file_path)

    print(f"Extracted rows: {len(df)}")
    print(df.head())

    return df