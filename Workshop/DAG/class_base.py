from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    "owner": "ghaza",
    "retries": 5,
    "retry_delay": timedelta(seconds=60),
}


def my_name(name: str):
    return name


def hello_world(**context):
    ti = context["ti"]
    name = ti.xcom_pull(task_ids="my_name")
    print(f"Hello, world, My name is {name}")


with DAG(
    dag_id="class_base",
    default_args=default_args,
    start_date=datetime(2025, 7, 27, 2, 0, 0),
    schedule="@daily",
    description="our first DAG that i write",
    catchup=False,
) as dag:
    first_task = BashOperator(
        task_id="first_task",
        bash_command="echo hello world, this is the first task",
    )

    hello = PythonOperator(
        task_id="say_hello",
        python_callable=hello_world,
    )

    name = PythonOperator(
        task_id="my_name",
        python_callable=my_name,
        op_kwargs={"name": "Fauzan Ghaza"},
    )

    first_task >> name >> hello  # menentukan urutan eksekusi
