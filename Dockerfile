FROM apache/airflow:2.2.3

COPY requirements.txt .

RUN pip3 install -r requirements.txt