import datetime

from airflow.sdk import dag, task

default_args = {
    "owner": "ghaza",
    "retries": 5,
    "retry_delay": 60,
}


@dag(
    dag_id="decorative_base",
    default_args=default_args,
    start_date=datetime(2025, 7, 27, 2, 0, 0),
    schedule="@daily",
    description="our first DAG that i write",
    catchup=False,
)
def decorative_base():
    @task.bash
    def first_task():
        return "echo hello world, this is the first task"

    @task
    def say_hello(name: str):
        print(f"Hello, world, My name is {name}")

    def my_name():
        return "Ghaza"

    first = first_task()
    name = my_name()
    hello = say_hello(name)  # name akan otomatis dieksekusi sebelum hello

    first >> hello
