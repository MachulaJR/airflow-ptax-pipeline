from pendulum import datetime
from airflow.sdk import task, dag
from airflow.providers.postgres.hooks.postgres import PostgresHook

@dag(
    dag_id="hello_pipeline",
    schedule=None,
    start_date=datetime(2026, 11, 10, tz="America/Sao_Paulo"),
    max_consecutive_failed_dag_runs=3,
    max_active_tasks=1,
    catchup=False
)
def hello_pipeline():

    @task.python(task_id="task_one")
    def task_one():
        dados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        return dados

    @task.python(task_id="task_two")
    def task_two(dados):
        dados_two = dados
        print(f"Quantidade dados: {len(dados_two)}")
        dados_multi = [x * 2 for x in dados_two]
        print(f"Dados multiplicados x2: {dados_multi}")

    @task.python(task_id="task_three")
    def task_three():
        hook = PostgresHook(postgres_conn_id="postgres_dw")
        consulta = hook.get_records("""
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name = ANY(%(schemas)s)
            ORDER BY schema_name;
            """,
            parameters={"schemas":["bronze", "silver", "gold", "audit"]}
        )
        print(f"Schemas lsitados no banco: {consulta}")
        return [x[0] for x in consulta]

    task1 = task_one()
    task2 = task_two(task1)
    task3 = task_three()

    task1 >> task3

hello_pipeline()
