from pendulum import datetime
from pathlib import Path
import json

from airflow.sdk import dag, task, Variable, get_current_context, BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.timetables.interval import CronDataIntervalTimetable

from ptax.client import buscar_cotacao
from ptax.storage import salvar_json, ler_json

SQL_UPSERT = Path("/opt/airflow/include/sql/bronze/upsert_ptax_raw.sql")

@dag(
    dag_id="bronze_ptax_ingest",
    schedule=CronDataIntervalTimetable("@daily", timezone="America/Sao_Paulo"),
    start_date=datetime(2026, 11, 1, tz="America/Sao_Paulo"),
    catchup=False,
    max_active_runs=1,
    tags=["bronze", "ptax"]
)
def bronze_ptax_ingest():

    @task.python(task_id="extrair")
    def extrair() -> dict:
        context = get_current_context()

        inicio = context["data_interval_start"]
        if inicio is None:
            raise ValueError("Nao possui data_interval_start")
        data = inicio.in_timezone("America/Sao_Paulo").date()

        base_path = Variable.get("bronze_base_path")
        conexao = BaseHook.get_connection("http_bcb_ptax")
        base_url = f"https://{conexao.host}"

        moeda = "USD"
        dados = buscar_cotacao(moeda, data, base_url)
        caminho = salvar_json(dados, base_path, moeda, data)

        return {"moeda": moeda, "data_ref": data.isoformat(), "arquivo": caminho,
                "qtd_registros" : len(dados["value"]), "source_url" : base_url}

    @task.python(task_id="carregar")
    def carregar(meta: dict) -> dict:
        context = get_current_context()
        dados = ler_json(meta["arquivo"])
        sql = SQL_UPSERT.read_text(encoding="utf-8")
        parametros = {
            "moeda": meta["moeda"],
            "data_ref": meta["data_ref"],
            "payload": json.dumps(dados, ensure_ascii=False),
            "qtd_registros": meta["qtd_registros"],
            "source_url": meta["source_url"],
            "arquivo_origem": meta["arquivo"],
            "run_id": context["run_id"],
        }
        hook = PostgresHook(postgres_conn_id="postgres_dw")
        hook.run(sql, parameters=parametros, autocommit=True)

        return {"moeda": meta["moeda"], "data_ref": meta["data_ref"]}
        
    carregar(extrair())

bronze_ptax_ingest()