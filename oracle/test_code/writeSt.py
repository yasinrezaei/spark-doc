from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType


# Initialize Spark Session
spark = SparkSession.builder\
    .appName('netcat-to-oracle-app')\
    .getOrCreate()
# spark.sparkContext.addFile('/home/yasinrezaei/Desktop/spark-doc/jars/ojdbc8.jar')
# Read from Netcat
# df = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()

# Write to Oracle DB
# query = df.writeStream.format("jdbc")\
#     .option("url", "jdbc:oracle:thin:@//localhost:49161/xe")\
#     .option("dbtable", "yasin.customer")\
#     .option("user", "yasin")\
#     .option("password", "12345")\
#     .start()

# Define the schema for the sample data
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("username", StringType(), True)
])

# Create sample data
data = [(5, "amir"), (2, "akbar"), (3, "jafar")]

# Create a DataFrame from the sample data
df = spark.createDataFrame(data, schema=schema)

# Write the sample data to Oracle DB
df.write.format("jdbc") \
    .option("url", "jdbc:oracle:thin:@//localhost:49161/xe") \
    .option("dbtable", "yasin.customer") \
    .option("user", "yasin") \
    .option("password", "12345") \
    .option("isolationLevel", "READ_COMMITTED") \
    .mode("append") \
    .save()




df=spark.read.format("jdbc") \
    .option("url", "jdbc:oracle:thin:@//localhost:49161/xe") \
    .option("dbtable", "yasin.customer") \
    .option("user", "yasin") \
    .option("password", "12345")\
    .load()
df.show()
