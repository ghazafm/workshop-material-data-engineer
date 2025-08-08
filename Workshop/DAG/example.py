import io
from datetime import datetime

import pandas as pd
import requests

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, task

default_args = {
    "owner": "ghaza",
    "retries": 5,
    "retry_delay": 60,
}


@dag(
    dag_id="example_dag",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    default_args=default_args,
    catchup=False,
)
def example_dag():
    @task
    def get_data() -> pd.DataFrame:
        response = requests.get("http://api.fauzanghaza.com/unknown")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df

    @task.virtualenv(
        requirements=["pandas"],
        system_site_packages=False,
        python_version="3.12",
    )
    def transform_data(df: pd.DataFrame):
        df.dropna()
        print(df.head())

    @task
    def contoh_postgres():
        hook = PostgresHook(postgres_conn_id="postgres_workshop")
        conn = hook.get_conn()
        cursor = conn.cursor()
        print(cursor.execute("SELECT * FROM weather_data LIMIT 5;"))
        cursor.close()
        conn.close()

    extract = get_data()
    transform = transform_data(extract)
    get_db = contoh_postgres()

    extract >> transform >> get_db


example_dag()
