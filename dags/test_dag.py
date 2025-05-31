from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
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

with DAG(
    'test_dag',
    default_args=default_args,
    schedule_interval='*/15 * * * *',
    catchup=False,
    tags=['http', 'telegram'],
) as dag:

    send_telegram_message = SimpleHttpOperator(
        task_id='send_telegram_message',
        http_conn_id=None,  # Можно создать HTTP connection в Airflow для этого URL
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
            "verify": False  # Отключаем проверку SSL (не рекомендуется для production)
        },
        log_response=True,
        retries=0,
    )

    send_telegram_message