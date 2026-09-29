import os
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from datetime import datetime, timezone
import json

load_dotenv("/opt/airflow/.env")


def get_staging_connection():
    return psycopg2.connect(
        host=os.getenv("API_DB_HOST"),
        port=os.getenv("API_DB_PORT"),
        dbname=os.getenv("API_DB_NAME"),
        user=os.getenv("API_DB_USER"),
        password=os.getenv("API_DB_PASSWORD"),
    )


def generate_batch_id():
    return str(uuid.uuid4())


def insert_cart(cursor, cart, batch_id):
    cursor.execute(
        """
        INSERT INTO staging.carts_raw (
            batch_id,
            cart_id,
            user_id,
            total,
            discounted_total,
            total_products,
            total_quantity,
            products_json,
            extracted_at
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        """,
        (
            batch_id,
            cart["id"],
            cart["userId"],
            cart["total"],
            cart["discountedTotal"],
            cart["totalProducts"],
            cart["totalQuantity"],
            json.dumps(cart["products"]),
            datetime.now(timezone.utc),
        ),
    )



def extract_to_staging():
    from src.carts.extract import fetch_all_carts

    carts = fetch_all_carts()
    batch_id = generate_batch_id()

    conn = get_staging_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        for cart in carts:
            insert_cart(cur, cart, batch_id)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()

    return {
        "batch_id": batch_id,
        "rows_extracted": len(carts),
    }