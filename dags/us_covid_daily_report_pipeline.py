from airflow import DAG 
from airflow.operators.bash_operator import BashOperator 

from datetime import datetime 

dag = DAG(
    dag_id="us_covid_dialy_report_pipeline",
    start_date=datetime(2020, 11, 1),
    schedule_interval=@daily
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command="curl -o data/{{ execution_date.date }}.json \
        --request GET \
	    --url 'https://covid-19-data.p.rapidapi.com/country/code?code=us' \
	    --header 'x-rapidapi-host: covid-19-data.p.rapidapi.com' \
	    --header 'x-rapidapi-key: 69505f59d0msh0a2d90cc6614786p15b75fjsn0e5e633a73b7'"
    dag=dag
)