from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime
import urllib.request
import json


def get_sales_from_api():
    url = "http://fastapi:8000/sales"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    print(f"Received {len(data)} sales records")

    return data


def show_sales_data(**context):
    sales = context["ti"].xcom_pull(
        task_ids="get_sales_from_api"
    )

    print("Sales data received from XCom:")
    print(json.dumps(sales, indent=2))


with DAG(
    dag_id="api_to_xcom",
    start_date=datetime(2026, 9, 15),
    schedule=None,
    catchup=False,
    tags=["api", "xcom", "fastapi"],
) as dag:

    get_sales = PythonOperator(
        task_id="get_sales_from_api",
        python_callable=get_sales_from_api,
    )

    show_sales = PythonOperator(
        task_id="show_sales_data",
        python_callable=show_sales_data,
    )

    get_sales >> show_sales