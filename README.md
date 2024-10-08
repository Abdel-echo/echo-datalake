## Table of contents
- [Table of contents](#table-of-contents)
- [Project Overview](#project-overview)
- [Project Requirements](#project-requirements)
- [Project Structure](#project-structure)
- [High Level Architecture](#high-level-architecture)
- [:ship: Containers](#ship-containers)
- [Step-by-Step](#step-by-step)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Setup environment](#2-setup-environment)
  - [3. Airflow: Create user for UI](#3-airflow-create-user-for-ui)
- [Stack](#stack)
- [References](#references)

## Project Overview

This project is a proof of concept (PoC) for a data lake designed for the Echo project. 
It aims to showcase a potential data lake infrastructure to host and compute large amounts of data, mainly composed of audio files.

In this project, we delivered the following functionalities:

1. An extract audio files from local storage to a landing zone, which represents the repository of raw data (in our case, .wav or .mp3 files)
2. An ETL that takes the raw format and ingests it with some transformation into Parquet tables in the bronze zone 
3. Airflow for orchestrating and scheduling the pipelines
4. Apache Spark app for data transformation and ingestion
5. MinIO S3-compatible storage to persist our data in the data lake
6. Jupyter Notebooks to run SQL queries on data lake data (this solution is not optimal; a dedicated serving layer like Hive, Dremio, or Presto would be better)
7. All services are running with Docker Compose and Docker Desktop

## Project Requirements

This project was develop and tested using the following environment.


| Item           | Version                   |
|----------------|---------------------------|
| MacOs          | `14.6.1`                  |
| Docker         | `20.10.17, build 100c701` |
| Docker Compose | `2.10.2`                  |
| Pycharm        | `2022.2.2 (Community)`    |
| Python         | `3.9.16`                  |
| OpenJDK        | `openjdk-11-jdk`          |
| Git            | `2.39.3`                  |


## Project Structure
 

The echo-datalake-poc project is currently structured with the following specifications.

| Path                | Description                                                                          |
|---------------------|------------------------------------------------------------------------------------------|
| .                   | `dags, jars_dependecies, notebooks, scripts, spark-app, dockerfils, docker-compose.yaml`|
| dags                | `dags files`                                                                         |
| data                | `source dataset for demo`                                                            |
| jars_dependencies   | `jars dependenceies`                                                    |
| scripts             | `scripts to run`                                                                  |
| notebooks           | `jupyter notebooks`                                                             |
| docker-compose.yaml | `docker-compose file defining the services tto run`                   |
| Dockerfile.airflow  | `docker file for airflow`                                              |
| Dockerfile.spark    | `docker file for spark`                                                  |
| Dockerfile.jupyter  | `doccker file for jupyter`                                             |
| requirements.txt    | `requirements to install`                                                |
| Readme.md           | `this readme`                                                                   |

##  High Level Architecture

  
![](./imgs/arch_overview.png "arch_overview")


## :ship: Containers

* **airflow-webserver**: Airflow v2.7.0 (Webserver & Scheduler)
    * image: airflow:2.7.0-python3.9 
    * port: 8080 
  
* **postgres**: Postgres database (Airflow metadata and our pipeline)
    * image: postgres:14-0
    * port: 5432

* **spark-master**: Spark Master
    * image: bitnami/spark:3.2.3
    * port: 8085,

* **spark-worker**: Spark workers
    * image: bitnami/spark:3.2.3

*  **MinIO**: Object storage

   - image: bitnami/minio:latest

*  **createbuckets**: Object storage

   - image: bitnami/mc:latest

*  **jupyter-spark**: Spark Jupyter notebook

   - image: bitnami/spark:3.2.3
    
## Step-by-Step

### 1. Clone the Repository

`git clone https://github.com/Abdel-echo/echo-datalake-poc.git`

### 3. Download depedencies
download the following dependencies ant put them in jars_dependencies dir

- aws-java-sdk-s3-1.12.772.jar
- hadoop-aws-3.2.3.jar
- aws-java-sdk-1.12.772.jar
- hadoop-client-3.2.3.jar
- aws-java-sdk-bundle-1.12.772.jar

### 2. Setup environment

```
cd echo-datalake-poc
docker-compose up -d
```
> **NOTE**: Before **RUNNING docker-compose up -d** command check entrypoints.sh file :

airflow users create \ \
    --username admin \ \
    --firstname admin \ \
    --lastname admin \ \
    --role Admin \ \
    --email admin@example.com \ \
    --password admin

### 3. Airflow: Create user for UI
To access Airflow UI is required to create a new user account, so in our case, we are going to create an fictional user with an Admin role attached.
Modify the scripts/entrypoints.sh script to set up your airflow credentials

> **NOTE**: please confirm that Airflow is up and running, it can be checked by accessing the URL [http://localhost:8080](http://localhost:8080). Have in mind that in the first execution it may take 2 to 3 minutes :

![](./imgs/airflow.png "airflow_ui")

## Stack

| Application    | URL                                            | Credentials                                           |
|----------------|------------------------------------------------|-------------------------------------------------------|
| Airflow        | [http://localhost:8080](http://localhost:8080) | ``` User: admin``` <br> ``` Pass: admin```            |         |
| MinIO          | [http://localhost:9001](http://localhost:9001) | ``` User: MINIOADMIN``` <br> ``` Pass: MINIOAADMIN``` |           |
| Jupyter        | [http://127.0.0.1:8888](http://127.0.0.1:8888) | ``` check jupyter container to get url token```       |           |
| Spark (Master) | [http://localhost:8085](http://localhost:8085) |                                                       |         |

## Snapshots


### 1. airflow ui

![](./imgs/airflow.png "airflow_ui")

### 2. Spark_jupyter 

![](./imgs/jupyter_ui.png "jupyter_ui")

### 3. Minio ui

![](./imgs/minio_ui.png "minio_ui")

### 4. spark ui

![](./imgs/spark_ui.png "spark_ui")

## To DO:

> Add support to automatically detecting spark master url ("spark://172.24.0.3:7077") and fead it to spark-submit in data_ingestion.py/transform_task  
> because spark master url changes every time we reset docker-compose.yaml services. 
> In production, it won't be needed because spark master url will have static address or defined over dns 