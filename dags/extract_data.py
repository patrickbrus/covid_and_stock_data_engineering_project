# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago
import utils

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Patrick Brus',
    'start_date': days_ago(0),
    'email': ['brus.patrick63@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

# define the DAG
dag = DAG(
    dag_id='extract-data-dag',
    default_args=default_args,
    description='DAG to extract the data from the different sources and put them to AWS S3',
    schedule_interval=timedelta(minutes=1),
)

# define the tasks
extract_stock_data = PythonOperator(
    dag=dag,
    task_id="extract_stock_data",
    python_callable=utils.extract_and_load_stock_data,
)

# define the tasks
extract_covid_data = PythonOperator(
    dag=dag,
    task_id="extract_covid_data",
    python_callable=utils.extract_and_load_covid_data,
)

# define the tasks
extract_weather_data = PythonOperator(
    dag=dag,
    task_id="extract_weather_data",
    python_callable=utils.extract_and_load_weather_data,
)

end_of_data_pipeline = DummyOperator(task_id="end_of_data_pipeline", dag=dag)


# create tree
extract_stock_data >> extract_covid_data >> extract_weather_data >> end_of_data_pipeline


