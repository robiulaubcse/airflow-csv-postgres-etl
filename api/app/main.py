import os

import psycopg2
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.get("/sales")
def get_sales():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            order_id,
            order_date,
            customer,
            product,
            quantity,
            price,
            total_amount
        FROM sales
        ORDER BY order_id;
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    sales = []

    for row in rows:
        sales.append({
            "order_id": row[0],
            "order_date": row[1],
            "customer": row[2],
            "product": row[3],
            "quantity": row[4],
            "price": float(row[5]),
            "total_amount": float(row[6]),
        })

    return sales