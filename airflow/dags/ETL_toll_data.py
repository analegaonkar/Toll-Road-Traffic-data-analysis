#sudo mkdir -p /home/project/airflow/dags/finalassignment/staging
#sudo chown -R 100999 /home/project/airflow/dags/finalassignment
#sudo chmod -R g+rw /home/project/airflow/dags/finalassignment  
#sudo chown -R 100999 /home/project/airflow/dags/finalassignment/staging
#sudo chmod -R g+rw /home/project/airflow/dags/finalassignment/staging
#cd /home/project/airflow/dags/finalassignment/staging
#wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz
#cd staging/
#airflow dags list-import-errors

# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

# defining DAG arguments
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'AN',
    'start_date': days_ago(0),
    'email': ['an@dummy.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the first task
unzip_data = BashOperator(
    task_id = 'unzip_data',
    bash_command = 'tar -xvzf /home/project/airflow/dags/finalassignment/tolldata.tgz -C /home/project/airflow/dags/finalassignment',
    dag = dag,
)

# define the second task - should extract the fields Rowid, Timestamp, Anonymized Vehicle number, and Vehicle type
extract_data_from_csv = BashOperator(
    task_id = 'extract_data_from_csv',
    bash_command = 'cut -d"," -f1,2,3,4 /home/project/airflow/dags/finalassignment/vehicle-data.csv > /home/project/airflow/dags/finalassignment/staging/csv_data.csv',
    dag = dag,
)

# define the third task - should extract the fields Number of axles, Tollplaza id, and Tollplaza code
extract_data_from_tsv = BashOperator(
    task_id = 'extract_data_from_tsv',
    bash_command = 'cut -f5,6,7 /home/project/airflow/dags/finalassignment/tollplaza-data.tsv | tr -s "[:blank:]" "," | tr -d "\\r" > /home/project/airflow/dags/finalassignment/staging/tsv_data.csv',
    dag = dag,
)

# define the fourth task - should extract the fields Type of Payment code, and Vehicle Code f
extract_data_from_fixed_width = BashOperator(
    task_id = 'extract_data_from_fixed_width',
    bash_command = 'cat /home/project/airflow/dags/finalassignment/payment-data.txt | tr -s "[:space:]" | cut -d " " -f11,12 | tr -s "[:blank:]" "," > /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv',
    dag = dag,
)


# define the fifth task
consolidate_data = BashOperator(
    task_id = 'consolidate_data',
    bash_command = 'paste -d "," /home/project/airflow/dags/finalassignment/staging/csv_data.csv /home/project/airflow/dags/finalassignment/staging/tsv_data.csv /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv > /home/project/airflow/dags/finalassignment/staging/extracted_data.csv',
    dag = dag,
)

# define the sixth task - convert vehicle type (4th column) from lower to upper case
transform_data = BashOperator(
    task_id = 'transform_data',
    bash_command = 'sed "s/[^,]*/\\U&/4" /home/project/airflow/dags/finalassignment/staging/extracted_data.csv > /home/project/airflow/dags/finalassignment/staging/transformed_data.csv',
    dag = dag,
)

# task pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data