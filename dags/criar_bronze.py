from pendulum import datetime
from airflow.sdk import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

@dag(
    dag_id="criar_bronze",
    schedule=None,
    start_date=datetime(2026, 11, 10, tz="America/Sao_Paulo"),
    catchup=False,
    template_searchpath=["/opt/airflow/include/sql"]
)
def criar_bronze():
    SQLExecuteQueryOperator(
            task_id="criar_ptax_raw",
            conn_id="postgres_dw",
            sql="bronze/create_ptax_raw.sql"
    )

criar_bronze()
