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

# Py4JJavaError: An error occurred while calling o31.showString.
# ...
# Caused by: org.apache.spark.SparkUpgradeException: You may get a different result due to the upgrading to Spark >= 3.0:
# reading dates before 1582-10-15 or timestamps before 1900-01-01T00:00:00Z
# from Parquet files can be ambiguous, as the files may be written by
# Spark 2.x or legacy versions of Hive, which uses a legacy hybrid calendar
# that is different from Spark 3.0+'s Proleptic Gregorian calendar.
# See more details in SPARK-31404. You can set the SQL config "spark.sql.parquet.datetimeRebaseModeInRead" or
# the datasource option "datetimeRebaseMode" to "LEGACY" to rebase the datetime values
# w.r.t. the calendar difference during reading. To read the datetime values
# as it is, set the SQL config "spark.sql.parquet.datetimeRebaseModeInRead" or the datasource option "datetimeRebaseMode"
# to "CORRECTED".


from glob import glob
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .master('local[*]') \
    .config("spark.driver.memory", "15g") \
    .config("spark.sql.parquet.int96RebaseModeInRead", "CORRECTED") \
    .config("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED") \
    .config("spark.sql.parquet.datetimeRebaseModeInRead", "CORRECTED") \
    .config("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED") \
    .appName("Python Spark SQL basic example") \
    .getOrCreate()

files = glob("**/*.parquet", recursive=True)

df = spark.read.parquet(*files)
