## `Run`
```bash
docker pull oracleinanutshell/oracle-xe-11g
docker run -d -p 49161:1521 oracleinanutshell/oracle-xe-11g
```

## `Connection`

    hostname: localhost
    port: 49161
    sid: xe
    username: system
    password: oracle

## `Commands`
```bash
docker exec -it < CONTAINER_ID > bash
sqlplus sys as sysdba
````
```sql
CREATE USER yasin IDENTIFIED BY 12345;
GRANT CONNECT, RESOURCE TO yasin;
```
```bash
sqlplus new_user/password
```

```sql
CREATE TABLE customer(
	id NUMBER PRIMARY KEY,
    username VARCHAR2(100)
)
INSERT INTO CUSTOMER (id,username) values(1,'yasin');
SELECT * FROM customer;
```
## `Config`
```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType


spark = SparkSession.builder\
    .appName('netcat-to-oracle-app')\
    .getOrCreate()

```

## `Write to oracle`
```python
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

```

## `Read From Oracle`
```python

df=spark.read.format("jdbc") \
    .option("url", "jdbc:oracle:thin:@//localhost:49161/xe") \
    .option("dbtable", "yasin.customer") \
    .option("user", "yasin") \
    .option("password", "12345")\
    .load()
df.show()

```



