from minio import Minio
from pyspark.sql import SparkSession

def initialize_spark_session(app_name, access_key, secret_key):
    """
    Initialize the Spark Session with provided configurations.

    :param app_name: Name of the spark application.
    :param access_key: Access key for S3.
    :param secret_key: Secret key for S3.
    :return: Spark session object or None if there's an error.
    """
    try:
        spark = SparkSession \
            .builder \
            .appName(app_name) \
            .config("spark.hadoop.fs.s3a.access.key", access_key) \
            .config("spark.hadoop.fs.s3a.secret.key", secret_key) \
            .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
            .config("spark.hadoop.fs.s3a.path.style.access", "true") \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")
        logger.info('Spark session initialized successfully')
        return spark

    except Exception as e:
        logger.error(f"Spark session initialization failed. Error: {e}")
        return None


def initialise_minio_connection(access_key, secret_key):
    # Initialize MinIO client
    minio_client = Minio(
        "minio:9000",
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )
    return minio_client


def get_raw_data(spark, path):
    name = "h01_1"
    audio_path = f"{path}/{name}.wav"
    # Load audio file using librosa
    print("audio_path = ", audio_path)
    audio_data_list = []
    for filename in os.listdir(path):
        if filename.endswith(".wav"):
            audio_data, sample_rate = librosa.load(f"{path}/{filename}", sr=16000)
            audio_data_list.append((filename, sample_rate, audio_data.tolist()))

    # Define schema for the DataFrame
    schema = StructType([
        StructField("file_name", StringType(), False),
        StructField("sample_rate", IntegerType(), False),
        StructField("audio_data", ArrayType(FloatType()), False)
    ])

    # Create a DataFrame
    df = spark.createDataFrame(audio_data_list, schema)

    # Write the DataFrame to a Delta table
    # print(f"s3://{bronze_bucket}/audio/audio_table")
    # df.write.format("parquet").mode("overwrite").save(f"s3a://{bronze_bucket}/audio/{name}")
    logging.info("reading data successful !")
    return df


def write_data(df, bucket, path):
    try:
        df.write.format("parquet").mode("overwrite").save(f"s3a://{bucket}/{path}")
        logging.info("write data to bucket successfully!")
    except Exception as e:
        logger.warning(f"Failed to write data to path {path}, Error: {e}")