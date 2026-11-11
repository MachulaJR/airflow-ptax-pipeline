from pendulum import datetime
from airflow.sdk import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

@dag(
    dag_id="teste_conexao_sql",
    schedule=None,
    start_date=datetime(2026, 11, 10, tz="America/Sao_Paulo"),
    catchup=False,
    template_searchpath=["/opt/airflow/include/sql"]
)
def teste_conexao_sql():

    select_1 = SQLExecuteQueryOperator(
            task_id="select_1",
            conn_id="postgres_dw",
            sql="""SELECT 1;"""
    )

    testar_schema = SQLExecuteQueryOperator(
            task_id="testar_schema",
            conn_id="postgres_dw",
            sql="teste/checar_schemas.sql",
            parameters={"schemas":["bronze", "silver", "gold", "audit"]}
    )

    select_1 >> testar_schema

teste_conexao_sql()
