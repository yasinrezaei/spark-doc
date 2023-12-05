from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import split

conf = SparkConf() \
    .setAppName("Elastic-App") \
    .set("spark.jars.packages","org.elasticsearch:elasticsearch-spark-30_2.12:8.11.1")\
    .set("spark.sql.streaming.checkpointLocation", "checkpoint")
spark = SparkSession.builder.config(conf=conf)\
    .config("spark.es.nodes", "localhost") \
    .config("spark.es.port", 9200) \
    .config("spark.es.nodes.wan.only", "true") \
    .config("es.spark.sql.streaming.sink.log.enabled","false")\
    .getOrCreate()

streaming_df = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

processed_df = streaming_df \
    .select(
        split(streaming_df.value, ",")[0].alias("id"),
        split(streaming_df.value, ",")[1].alias("name")
    )

query = processed_df \
    .writeStream \
    .outputMode("append") \
    .format("org.apache.spark.sql.redis") \
    .option("table", "output") \
    .start()


query.awaitTermination()