import os

import psycopg2
from dotenv import load_dotenv


load_dotenv("/opt/airflow/.env")


def load_sales(df):

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO sales (
            order_id,
            order_date,
            customer,
            product,
            quantity,
            price,
            total_amount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            row["order_id"],
            row["order_date"],
            row["customer"],
            row["product"],
            row["quantity"],
            row["price"],
            row["total_amount"],
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany(insert_query, data)

    connection.commit()

    cursor.close()
    connection.close()

    print(f"Loaded rows: {len(data)}")