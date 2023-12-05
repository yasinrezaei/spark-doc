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

# df = spark.createDataFrame([(1, "yasin"), (2, "amir")], ["id", "name"])
# # Write the DataFrame to an Elasticsearch index
# df.write.format("org.elasticsearch.spark.sql")\
#     .option("es.nodes", "http://localhost:9200")\
#     .save("spark")


# q ="""{
#   "query" : {
#         "match_all" : {}
#     }
# }"""

# spark_df = spark.read.format("org.elasticsearch.spark.sql").option("es.query", q).load("spark")
# spark_df.show()



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

# # Display the Stream in Console
# query = processed_df \
#     .writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()


query = processed_df \
    .writeStream \
    .outputMode("append") \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", "spark") \
    .start()

# Keep the process running
query.awaitTermination()