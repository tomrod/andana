from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.today(),
    'execution_date': datetime.today(),
    'email': ['narrative.wrangler@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=2),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}
dag = DAG(
    'seashells', default_args=default_args )

# t1 = BashOperator(
#    task_id = 'set_path',
#    bash_command = 'cd /home/brute/Dropbox/Writing/Blog/andana/assets/misc/',
#    dag = dag
#    )

t2 = BashOperator(
    task_id = 'get_data',
    bash_command = 'cd /home/brute/Dropbox/Writing/Blog/andana/assets/misc && wget http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data',
    retries = 3,
    dag = dag)

# t1.set_downstream(t2)
# t2.set_upstream(t1)
