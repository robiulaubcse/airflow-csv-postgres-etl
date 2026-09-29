import os

import psycopg2
from dotenv import load_dotenv


load_dotenv("/opt/airflow/.env")


def get_warehouse_connection():
    return psycopg2.connect(
        host=os.getenv("WAREHOUSE_DB_HOST"),
        port=os.getenv("WAREHOUSE_DB_PORT"),
        dbname=os.getenv("WAREHOUSE_DB_NAME"),
        user=os.getenv("WAREHOUSE_DB_USER"),
        password=os.getenv("WAREHOUSE_DB_PASSWORD"),
    )

def insert_cart(cursor, cart):
    cursor.execute(
        """
        INSERT INTO warehouse.carts (
            cart_id,
            user_id,
            total,
            discounted_total,
            total_products,
            total_quantity
        )
        VALUES (
            %s, %s, %s, %s, %s, %s
        )
        """,
        (
            cart["cart_id"],
            cart["user_id"],
            cart["total"],
            cart["discounted_total"],
            cart["total_products"],
            cart["total_quantity"],
        ),
    )

def insert_cart_item(cursor, item):
    cursor.execute(
        """
        INSERT INTO warehouse.cart_items (
            cart_id,
            product_id,
            title,
            price,
            quantity,
            total,
            discount_percentage,
            discounted_total,
            thumbnail
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        """,
        (
            item["cart_id"],
            item["product_id"],
            item["title"],
            item["price"],
            item["quantity"],
            item["total"],
            item["discount_percentage"],
            item["discounted_total"],
            item["thumbnail"],
        ),
    )


def load_batch(transformed_batch):
    conn = get_warehouse_connection()
    cur = conn.cursor()

    try:
        for record in transformed_batch:
            insert_cart(cur, record["cart"])

            for item in record["items"]:
                insert_cart_item(cur, item)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()