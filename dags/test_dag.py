from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'admin',
    'start_date': datetime(2024, 5, 1),
    'retries': 0,  # Не пытаться перезапускать в этой итерации
    'retry_delay': timedelta(minutes=0),  # Не ждать перед retry (т.к. retries=0)
    'max_retry_delay': timedelta(minutes=0),  # Максимальная задержка перед retry
    'depends_on_past': False,  # Не зависеть от прошлых запусков
    'catchup': False,  # Не запускать пропущенные интервалы
}

with DAG(
    'test_http_dag',
    default_args=default_args,
    schedule_interval='*/15 * * * *',  # Каждые 15 минут (без перезапуска при ошибке)
    catchup=False,
    tags=['http'],
) as dag:

    http_task = SimpleHttpOperator(
        task_id='call_local_api',
        http_conn_id=None,
        endpoint='http://host.docker.internal:8000/email',
        method='POST',
        headers={"Content-Type": "application/json"},
        log_response=True,
        retries=0,  # Отключаем retry для этой задачи (если DAG retries=0, можно не дублировать)
    )

    http_task

# from airflow import DAG
# from airflow.providers.http.operators.http import SimpleHttpOperator
# from datetime import datetime, timedelta
#
# default_args = {
#     'owner': 'admin',
#     'start_date': datetime(2025, 5, 6),
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }
#
# with DAG(
#     'test_dag',
#     default_args=default_args,
#     schedule_interval='*/15 * * * *',
#     catchup=False,
#     tags=['api'],
# ) as dag:
#     http_task = SimpleHttpOperator(
#         task_id='http_request',
#         http_conn_id=None,
#         endpoint='http://host.docker.internal:8000/test_airflow',  # Полный URL
#         method='POST',
#         log_response=True,
#     )