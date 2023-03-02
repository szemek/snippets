from glob import glob
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .master('local[*]') \
    .config("spark.driver.memory", "15g") \
    .appName("Python Spark SQL basic example") \
    .getOrCreate()

files = glob("**/*.parquet", recursive=True)

df = spark.read.parquet(*files)
