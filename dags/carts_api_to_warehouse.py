from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from psycopg2.extras import RealDictCursor

from src.carts.staging import (
    extract_to_staging,
    get_staging_connection,
)
from src.carts.transform import transform_batch
from src.carts.warehouse import load_batch

def extract_task():
    result = extract_to_staging()

    print(f"Batch ID: {result['batch_id']}")
    print(f"Rows extracted: {result['rows_extracted']}")

    return result

def transform_task(**context):
    batch_id = context["ti"].xcom_pull(
        task_ids="extract_to_staging"
    )["batch_id"]

    conn = get_staging_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute(
            """
            SELECT
                cart_id,
                user_id,
                total,
                discounted_total,
                total_products,
                total_quantity,
                products_json
            FROM staging.carts_raw
            WHERE batch_id = %s
            ORDER BY cart_id
            """,
            (batch_id,),
        )

        rows = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    transformed = transform_batch(rows)

    print(f"Batch ID: {batch_id}")
    print(f"Staging rows: {len(rows)}")
    print(f"Transformed carts: {len(transformed)}")
    print(
        f"Transformed items: "
        f"{sum(len(x['items']) for x in transformed)}"
    )

    return {
        "batch_id": batch_id,
        "rows_transformed": len(transformed),
        "items_transformed": sum(
            len(x["items"])
            for x in transformed
        ),
    }


def load_task(**context):
    batch_id = context["ti"].xcom_pull(
        task_ids="extract_to_staging"
    )["batch_id"]

    conn = get_staging_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute(
            """
            SELECT
                cart_id,
                user_id,
                total,
                discounted_total,
                total_products,
                total_quantity,
                products_json
            FROM staging.carts_raw
            WHERE batch_id = %s
            ORDER BY cart_id
            """,
            (batch_id,),
        )

        rows = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    transformed = transform_batch(rows)

    load_batch(transformed)

    print(f"Batch ID: {batch_id}")
    print(f"Carts loaded: {len(transformed)}")
    print(
        f"Items loaded: "
        f"{sum(len(x['items']) for x in transformed)}"
    )




with DAG(
    dag_id="carts_api_to_warehouse",
    start_date=datetime(2026, 9, 28),
    schedule=None,
    catchup=False,
    tags=["carts", "etl", "warehouse"],
) as dag:

    extract = PythonOperator(
        task_id="extract_to_staging",
        python_callable=extract_task,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_task,
    )

    load = PythonOperator(
        task_id="load_to_warehouse",
        python_callable=load_task,
    )

    extract >> transform >> load