from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import split

conf = SparkConf() \
    .setAppName("Elastic-App") \
    .set("spark.jars.packages","com.redislabs:spark-redis_2.12:3.0.0")

spark = SparkSession.builder.config(conf=conf)\
    .getOrCreate()

data = spark.readStream.format("org.apache.spark.sql.redis")\
    .option("table", "people") \
    .option("key.column", "id") \
    .option("host", 'localhost') \
    .option("port", 6380) \
    .load()
query = data\
  .writeStream\
  .format("console")\
  .start()

query.awaitTermination()
# streaming_df = spark \
#     .readStream \
#     .format("socket") \
#     .option("host", "localhost") \
#     .option("port", 9999) \
#     .load()

# processed_df = streaming_df \
#     .select(
#         split(streaming_df.value, ",")[0].alias("id"),
#         split(streaming_df.value, ",")[1].alias("name"),
#         split(streaming_df.value, ",")[2].alias("age")
#     )

# query = processed_df \
#     .writeStream \
#     .outputMode("append") \
#     .format("org.apache.spark.sql.redis") \
#     .option("table", "people") \
#     .option("key.column", "id") \
#     .option("host", 'localhost') \
#     .option("port", 6380) \
#     .start()



# query.awaitTermination()