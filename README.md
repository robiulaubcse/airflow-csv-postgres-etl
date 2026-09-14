# Airflow CSV to PostgreSQL ETL

A beginner-level production-style ETL pipeline built with
Apache Airflow, Docker, Python, and PostgreSQL.

## Architecture

CSV
 ↓
Airflow DAG
 ↓
Extract
 ↓
Transform
 ↓
Load
 ↓
PostgreSQL

## Technologies

- Apache Airflow 3.3.1
- Docker / Docker Compose
- Python
- Pandas
- PostgreSQL
- psycopg2
- python-dotenv

## Concepts Learned

- DAG
- Tasks
- PythonOperator
- Task dependencies
- XCom
- Logical date
- Catchup
- Airflow metadata database
- Docker services and containers
- Volumes / bind mounts
- Environment variables
- Production-style project structure