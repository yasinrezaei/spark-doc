## `Run`
```bash
docker pull elasticsearch:8.11.0
```
```bash
    docker run -d --name elasticsearch --net somenetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:8.11.0
```

## `Config For elastic`
```python
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

```

## `Write to elastic`
```python
df = spark.createDataFrame([(1, "yasin"), (2, "amir")], ["id", "name"])

df.write.format("org.elasticsearch.spark.sql")\
    .option("es.nodes", "http://localhost:9200")\
    .save("spark")
```

## `Read from elastic`
```python
q ="""{
  "query" : {
        "match_all" : {}
    }
}"""

spark_df = spark.read.format("org.elasticsearch.spark.sql").option("es.query", q).load("spark")
spark_df.show()
```

## `Write Stream to elastic`
```python
# get stream from socket nc
streaming_df = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()
# splir data
processed_df = streaming_df \
    .select(
        split(streaming_df.value, ",")[0].alias("id"),
        split(streaming_df.value, ",")[1].alias("name")
    )
# write stream
query = processed_df \
    .writeStream \
    .outputMode("append") \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", "spark") \
    .start()


query.awaitTermination()

```


## `Read Stream From elastic` + see this issue [here](https://github.com/elastic/elasticsearch-hadoop/issues/1227)
![image info](./pictures/el.png)