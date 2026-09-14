from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from src.sales.extract import extract_sales
from src.sales.transform import transform_sales
from src.sales.load import load_sales


def extract_task():
    return extract_sales()


def transform_task(**context):
    df = context["ti"].xcom_pull(
        task_ids="extract"
    )

    return transform_sales(df)


def load_task(**context):
    df = context["ti"].xcom_pull(
        task_ids="transform"
    )

    load_sales(df)


with DAG(
    dag_id="csv_to_postgres_production",
    start_date=datetime(2026, 9, 14),
    schedule=None,
    catchup=False,
    description="Production-style CSV to PostgreSQL ETL pipeline",
    tags=["etl", "postgres", "sales"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_task,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_task,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_task,
    )

    extract >> transform >> load