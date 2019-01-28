from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'execution_date': datetime.today(),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=2),
}
dag = DAG(
    'dag_test', default_args=default_args )

t2 = BashOperator(
    task_id = 'get_data',
    bash_command = 'cd ~/ && wget http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data',
    retries = 3,
    dag = dag)

t3 = BashOperator(
    task_id = 'run_regression',
    bash_command = "python ~/regress.py",
    retries = 3,
    dag = dag
    )

t4 = BashOperator(
    task_id = 'print_results',
    bash_command = "cat ~/results.csv",
    retries = 3,
    dag = dag
    )

t3.set_upstream(t2)
t4.set_upstream(t3)

#t2.set_downstream(t3)
#t3.set_downstream(t4)
