import hashlib
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf

from IPython import embed

spark = SparkSession \
    .builder \
    .master('local[*]') \
    .config("spark.driver.memory", "15g") \
    .appName("Python Spark SQL basic example") \
    .getOrCreate()

data = """
[
    {
        "data": {
            "firstname": "John",
            "lastname": "Kowalski",
            "address": {
                "city": "Warsaw",
                "street": "Hoza"
            }
        }
    },
    {
        "data": {
            "firstname": "Elizabeth",
            "lastname": "Kirk",
            "address": {
                "city": "New York",
                "street": "5th Avenue"
            }
        }
    }
]
"""

df = spark.read.json(spark.sparkContext.parallelize([data]))


def hash_column(value):
    return hashlib.pbkdf2_hmac("sha256", str(value).encode(), "salt".encode(), 1).hex()

hash_column_udf = udf(hash_column, StringType())

df.withColumn("data", df["data"].withField("address.city", hash_column_udf("data.address.city"))).show(truncate=False)
