# `Spark`
### Spark is a unified analytics engine for large-scale data processing
- Written in scala, scalable, powerful caching, real time, poly glot 
- Spark caches the data in-memory and enhance the system performance
- Spark does not have storage space and cluster resource management
- We can use kubernetes for cluster management


## `Main components`
- Spark core
- Spark SQL and shark
- Spark streaming
- MLlib
- GraphX
- Standalone scheduler

## `Architecture`

![image info](./pictures/cluster-overview.png)

#### Spark Driver
    As soon as we submit the spark job, the driver program runs the `main()` method of your application and creates DAG’s representing the data flow internally. Based on the DAG workflow, the driver requests the cluster manager to allocate the resources (workers) required for processing. Once the resources are allocated, the driver then using `spark context` sends the serialized result (code+data) to the workers to execute as Tasks and their result is captured.

#### Spark Context
    It connects to the cluster manager through the driver to acquire the executors required for processing. Then it sends the serialized result to the workers as tasks to run.


## `Concepts`
  - `RDD`:
  
     - Resilient Distributed Datasets are the group of data items that can be stored in memory on worker nodes.
     - immutable
     - With the occurrence of any error in the network, rdds can be recovered from the history of changes
   - `RDD Lineage`:
     - provides the foundation for Spark's fault tolerance by recording the sequence of transformations applied to data
  - `Directed Acyclic Graph (DAG)`: 
  
    - DAG is a graph that performs a sequence of computations on data.

   - `Persist/Cache`
        - MEMORY_ONLY
        - MEMORY_AND_DISK
        - MEMORY_ONLY_SER
        - MEMORY_AND_DISK_USER
        - DISK_ONLY
        - OFF_HEAP
   - `Global Variables` 
        - broadcast variables (readonly)
        - accumulators
  
   - `Lazy Evaluation` 
        - Spark does not begin computing the partitions until an action is called

 


## `Install Java`

  ``` bash

  sudo apt install openjdk-8-jdk
  sudo update-alternatives --config java

```
## `Install single node and config`
  ```bash
  mkdir spark-head
  mkdir spark-node
  tar -xzvf spark-3.1.2-bin-hadoop3.2.tgz
  cp -r spark-3.1.2-bin-hadoop3.2/* spark-head
  cp -r spark-3.1.2-bin-hadoop3.2/* spark-node
  rm -r spark-3.1.2-bin-hadoop3.2
  ```
## `Start Master`

  ```bash
  ./spark-head/sbin/start-master.sh --webui-port 8080

  jps

  ```

## `Start the first Worker node`

  ```bash
  ./spark-node/sbin/start-worker.sh  spark://yrezaei-pc-de:7077 --webui-port 8081 -p 9911

  jps
  ```

##
 

## `Install pyspark`
  ```bash
    pip install pyspark
  ```



## `Run`

```
   http://172.17.200.170:4040
```



## `Stop Master/Workers`

  ```bash 
    ./spark-head/sbin/stop-master.sh
  ```

  ```bash
    ./spark-node/sbin/stop-worker.sh
  ```
