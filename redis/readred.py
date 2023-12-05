import pyspark
from pyspark.sql import SparkSession

# Import necessary libraries for Redis
import redis

# Create a Spark session
spark = SparkSession.builder \
    .appName('redis-app') \
    .getOrCreate()

# Read data from Redis
testid = spark.read.format("org.apache.spark.sql.redis") \
    .option("keys.pattern", "keyPattern:*") \
    .option("key.column", "id") \
    .option("infer.schema", "true") \
    .load()

# Function to write data to Redis
def write_to_redis(partition):
    redis_host = "localhost"  # Replace with your Redis server host
    redis_port = 6380        # Replace with your Redis server port
    redis_db = 0              # Replace with your Redis database number
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

    for row in partition:
        key = row["id"]
        # Assuming there is a column named 'value' in your DataFrame
        value = row["value"]
        redis_client.set(key, value)

# Write data to Redis using foreachPartition
testid.foreachPartition(write_to_redis)

# Stop the Spark session
spark.stop()
