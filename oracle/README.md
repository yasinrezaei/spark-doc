## `Run Oracle`
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

## `Pyspark`
```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType


# Initialize Spark Session
spark = SparkSession.builder\
    .appName('netcat-to-oracle-app')\
    .getOrCreate()
```
## `Write data with spark to oracle`
```python
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

```
## `Read data with spark from oracle`
```python
df=spark.read.format("jdbc") \
    .option("url", "jdbc:oracle:thin:@//localhost:49161/xe") \
    .option("dbtable", "yasin.customer") \
    .option("user", "yasin") \
    .option("password", "12345")\
    .load()
df.show()
```



## `Write Stream with spark To Oracle`
#### oracle does not support write stream but we can simulate write stream with `normal write and forEachBatch option`

```python
# Read streaming data from socket
df_stream = spark.readStream\
    .format("socket")\
    .option("host", "localhost")\
    .option("port", 9999)\
    .load()

split_cols = split(df_stream['value'], ',')
df_stream = df_stream.withColumn('id', split_cols.getItem(0).cast(IntegerType())) \
                     .withColumn('username', split_cols.getItem(1).cast(StringType()))

# Select only the split columns for further processing
df_stream = df_stream.select('id', 'username')

# Write output of each micro-batch to Oracle DB
query = df_stream.writeStream\
    .foreachBatch(write_to_oracle)\
    .start()

query.awaitTermination()

```
#### if we want to send `update or upsert` query we should `sql_statement_maker` function and for each batch that we receive from socket we can call this customized query.

```python
class oracle_db:
    def __init__(self,host,port,sid,user_name,password):
        self.host=host
        self.port=port
        self.sid=sid
        self.user_name=user_name
        self.password=password
    
    def execute(self,sql_statement,rows):
        import cx_Oracle
        dsn_tns = cx_Oracle.makedsn(self.host,self.port,self.sid)
        conn = cx_Oracle.connect(user=self.user_name, password=self.password, dsn=dsn_tns)
        c = conn.cursor()

        c.executemany(sql_statement,rows)
        conn.commit()
        conn.close()


def string_manipulation(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

class sql_statement_maker:

    def __init__(self):
        pass

    def upsert(self,df,table_name: str,list_of_keys: list):
        
        columns=list(df)

        sql_statement="MERGE INTO {} USING DUAL ON (".format(table_name)

        if len(list_of_keys)==1:
            sql_statement+="{item}=:{item}".format(item=list_of_keys[0])
        elif len(list_of_keys)==0:
            print("please input key columns in list_of_keys varaible!")
        else:
            i=0
            for item in list_of_keys:
                
                if i==0:
                    sql_statement+="{item}=:{item}".format(item=item)
                else:
                    sql_statement+=" AND {item}=:{item}".format(item=item)
                i+=1
        sql_statement+=""")
        WHEN NOT MATCHED THEN INSERT(
        """
        str_values=""
        for item in columns:
            sql_statement+="{},".format(item)
            str_values+=":{},".format(item)

        sql_statement=string_manipulation(sql_statement,',')
        str_values=string_manipulation(str_values,',')
        sql_statement+=") VALUES ("+str_values+") WHEN MATCHED THEN UPDATE SET"

        value_columns = [item for item in columns if item not in list_of_keys]

        for item in value_columns:
            sql_statement+=" {item}=:{item},".format(item=item)


        sql_statement=string_manipulation(sql_statement,',')

        return sql_statement

    def insert(self,df,table_name: str):
        
        columns=list(df)
        sql_statement="INSERT INTO {} (".format(table_name)
        str_values=""
        for item in columns:
            sql_statement+="{},".format(item)
            str_values+=":{},".format(item)

        sql_statement=string_manipulation(sql_statement,',')
        str_values=string_manipulation(str_values,',')
        sql_statement+=") VALUES ("+str_values+") "
        sql_statement=string_manipulation(sql_statement,',')

        return sql_statement


def SaveToOracle(df,epoch_id):
    try:
        print("***********Start*************")
        pandasDF = df.toPandas()
        rows= pandasDF.to_dict(orient='records')
        
        table_name=config.table_name
        list_of_keys=config.list_of_keys


        sql_statement_maker_obj=sql_statement_maker()
        sql_statement=sql_statement_maker_obj.upsert(pandasDF,table_name,list_of_keys)

        host=config.host
        port=config.port
        user_name=config.user_name
        password=config.password
        sid=config.sid
        oracle_db_obj=oracle_db(host,port,sid,user_name,password)
        oracle_db_obj.execute(sql_statement,rows)

        pass
    except Exception as e:
        response = e.__str__()
        print(response)
        
        



streamingQuery = (df.writeStream
  .outputMode("append")
  .foreachBatch(SaveToOracle)
  .start()
  .awaitTermination()
                 )


```





