from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("WriteToElasticsearch").getOrCreate()
# Create a DataFrame from your data
df = spark.createDataFrame([(1, "Hello"), (2, "World")], ["id", "message"])
# Write the DataFrame to an Elasticsearch index
df.write.format("org.elasticsearch/elasticsearch-spark-30_2.12@7.17.3").save("index/type")
# Stop the SparkSession
spark.stop()
