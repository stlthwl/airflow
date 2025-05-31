from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime, timedelta
import json

default_args = {
    'owner': 'admin',
    'start_date': datetime(2024, 5, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=0),
    'max_retry_delay': timedelta(minutes=0),
    'depends_on_past': False,
    'catchup': False,
}

def check_response(response):
    from airflow.exceptions import AirflowException
    if response.status_code != 200:
        raise AirflowException(f"Request failed with code {response.status_code}: {response.text}")
    return True

with DAG(
    'test_dag',
    default_args=default_args,
    schedule_interval='*/15 * * * *',
    catchup=False,
    tags=['http', 'telegram'],
) as dag:

    check_endpoint_available = HttpSensor(
        task_id='check_endpoint_available',
        http_conn_id=None,
        endpoint='https://90.156.154.231:3001/api/v1/sendMessageTelegram',
        method='POST',
        request_params={},
        response_check=lambda response: True,
        extra_options={"verify": False},
        poke_interval=5,
        timeout=20
    )

    send_telegram_message = SimpleHttpOperator(
        task_id='send_telegram_message',
        http_conn_id=None,
        endpoint='https://90.156.154.231:3001/api/v1/sendMessageTelegram',
        method='POST',
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        data=json.dumps({
            "userTechId": 1080079179,
            "textMessage": "test airflow"
        }),
        extra_options={
            "verify": False
        },
        response_check=check_response,
        log_response=True,
        retries=0,
    )

    check_endpoint_available >> test_dag

# from airflow import DAG
# from airflow.providers.http.operators.http import SimpleHttpOperator
# from datetime import datetime, timedelta
# import json
#
# default_args = {
#     'owner': 'admin',
#     'start_date': datetime(2024, 5, 1),
#     'retries': 0,
#     'retry_delay': timedelta(minutes=0),
#     'max_retry_delay': timedelta(minutes=0),
#     'depends_on_past': False,
#     'catchup': False,
# }
#
# with DAG(
#     'test_dag',
#     default_args=default_args,
#     schedule_interval='*/15 * * * *',
#     catchup=False,
#     tags=['http', 'telegram'],
# ) as dag:
#
#     send_telegram_message = SimpleHttpOperator(
#         task_id='send_telegram_message',
#         http_conn_id=None,  # Можно создать HTTP connection в Airflow для этого URL
#         endpoint='https://90.156.154.231:3001/api/v1/sendMessageTelegram',
#         method='POST',
#         headers={
#             "Content-Type": "application/json",
#             "Accept": "application/json"
#         },
#         data=json.dumps({
#             "userTechId": 1080079179,
#             "textMessage": "test airflow"
#         }),
#         extra_options={
#             "verify": False  # Отключаем проверку SSL (не рекомендуется для production)
#         },
#         log_response=True,
#         retries=0,
#     )
#
#     send_telegram_message