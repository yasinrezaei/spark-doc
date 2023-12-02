# Spark Document

## Install Java

  ```bash

  sudo apt install openjdk-8-jdk
  sudo update-alternatives --config java

```
## Install single node and config
  ```bash
  mkdir spark-head
  mkdir spark-node
  tar -xzvf spark-3.1.2-bin-hadoop3.2.tgz
  cp -r spark-3.1.2-bin-hadoop3.2/* spark-head
  cp -r spark-3.1.2-bin-hadoop3.2/* spark-node
  rm -r spark-3.1.2-bin-hadoop3.2
  ```
## Start `Master` 

  ```bash
  ./spark-head/sbin/start-master.sh --webui-port 8080

  ```

### Start the first  `Worker node`

  ```bash
  ./spark-node/sbin/start-worker.sh  spark://DESKTOP-HSK5ETQ.localdomain:7077 --webui-port 8081 -p 9911
  ```
  
 

## Install pyspark
  ```bash
    pip install pyspark
  ```



## Run

```
   http://172.17.200.170:4040
```



## Stop Master/Workers

  ```bash 
    ./spark-head/sbin/stop-master.sh
  ```

  ```bash
    ./spark-node/sbin/stop-worker.sh
  ```

