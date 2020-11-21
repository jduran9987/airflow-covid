from airflow import DAG 
from airflow.operators.bash_operator import BashOperator 

from datetime import datetime 
import os

dag = DAG(
    dag_id="us_covid_daily_report_pipeline",
    start_date=datetime(2020, 11, 15),
    schedule_interval="@daily"
)

fetch_covid_us_data = BashOperator(
    task_id="fetch_covid_us_data",
    bash_command="curl -o /opt/airflow/data/{{ ds_nodash }}.json \
        --request GET \
	    --url https://api.covidtracking.com/v1/us/{{ ds_nodash }}.json",
    dag=dag
)
