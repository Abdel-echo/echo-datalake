#!/bin/bash

# Define the Docker container name
CONTAINER_NAME="spark_master"

# Define the path to the Spark submit command inside the container
SPARK_SUBMIT="/opt/bitnami/spark/bin/spark-submit"

# Define the master
MASTER="local[2]"

# Define the JAR files
JARS="/opt/bitnami/spark/jars/aws-java-sdk-s3-1.12.772.jar /
/opt/bitnami/spark/jars/hadoop-aws-3.2.3.jar /
/opt/bitnami/spark/jars/aws-java-sdk-1.12.772.jar /
/opt/bitnami/spark/jars/hadoop-client-3.2.3.jar /
/opt/bitnami/spark/jars/aws-java-sdk-bundle-1.12.772.jar
"
# Define the Python script to run
SCRIPT="data_processing_spark.py"

# Run the Spark submit command inside the Docker container
docker exec -it $CONTAINER_NAME $SPARK_SUBMIT --master $MASTER --jars $JARS $SCRIPT
