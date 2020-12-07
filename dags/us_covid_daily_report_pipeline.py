# Import Airflow specific modules
from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.http_sensor import HttpSensor
from airflow.hooks import S3_hook

# Import Python specific modules
from datetime import datetime 
import os

# Set up connection to enable local files to be uploaded to S3
def upload_file_to_S3_with_hook(filename, key, bucket_name):
    """
    Helper function to load a given file to an S3 bucket.

    :param str filename: full path of file (including file extension) to be uploaded to S3
    :param str key: filename to be inserted into the target S3 bucket
    "param str bucket_name: name of S3 bucket 
    """
    hook = S3_hook.S3Hook('s3_connection')
    hook.load_file(filename, key, bucket_name)

# Initiate our dag definition
dag = DAG(
    dag_id="us_covid_daily_report_pipeline",
    start_date=datetime(2020, 12, 1),
    schedule_interval="@daily"
)

# Check if Covid api has data for a given date
is_covid_api_available = HttpSensor(
    task_id="is_covid_api_available",
    method="GET",
    http_conn_id="covid_api",
    endpoint="v1/us/{{ ds_nodash }}.json",
    response_check=lambda response: "date" in response.text,
    poke_interval=5,
    timeout=20
)

# Download Covid US states data for a given date
fetch_covid_us_data = BashOperator(
    task_id="fetch_covid_us_data",
    bash_command="curl -o /opt/airflow/data/{{ ds_nodash }}.json \
        --request GET \
	    --url https://api.covidtracking.com/v1/us/{{ ds_nodash }}.json",
    dag=dag
)

# Upload Covid data to S3 using a helper function
upload_file_to_s3 = PythonOperator(
    task_id="upload_file_to_s3",
    python_callable=upload_file_to_S3_with_hook,
    op_kwargs={
        "filename": "./data/{{ ds_nodash }}.json",
        "key": "{{ ds_nodash }}.json",
        "bucket_name": "datasets-jduran9987"
    },
    dag=dag
)

# Setting our dependencies
is_covid_api_available >> fetch_covid_us_data >> upload_file_to_s3