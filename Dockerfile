FROM apache/airflow:1.10.10

RUN pip install upgrade pip && \
    pip install --no-cache-dir boto3

COPY ./data /opt/airflow/data