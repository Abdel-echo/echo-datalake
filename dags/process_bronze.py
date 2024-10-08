from airflow.operators.bash import BashOperator
import librosa, os, glob
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Define airflow dag
default_args = {
    'owner': 'echo_datalake',
    'start_date': datetime(2023, 7, 15, 00)
}


with DAG('Process_Bronze',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:

    start_task = BashOperator(
        task_id='start_pipeline',
        bash_command='echo "Starting the pipeline..."'
    )

    etl_task = BashOperator(
        task_id='bddAudioSource_spark',
        bash_command='spark-submit --master  spark://172.20.0.6:7077 --jars "/opt/bitnami/spark/jars/hadoop-aws-3.2.3.jar,/opt/bitnami/spark/jars/hadoop-client-3.2.3.jar,/opt/bitnami/spark/jars/aws-java-sdk-bundle-1.12.772.jar,/opt/bitnami/spark/jars/aws-java-sdk-s3-1.12.772.jar,/opt/bitnami/spark/jars/aws-java-sdk-1.12.772.jar" /opt/airflow/spark_app/spark/bddAudioSource_spark.py',
    )

    end_task = BashOperator(
        task_id='end_pipeline',
        bash_command='echo "Pipeline finished."'
    )
    # transform_task = SparkSubmitOperator(
    #     application='/opt/airflow/spark_app/data_processing_spark.py',
    #     conn_id='spark',
    #     task_id='spark_submit_task'
    # )
    # transform_task = BashOperator(
    #     task_id='load_data_to_bronze_table',
    #     bash_command='python  /opt/airflow/spark_app/data_processing_spark.py',
    # )

    start_task >> etl_task >> end_task
