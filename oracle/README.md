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
CREATE USER new_user IDENTIFIED BY password;
GRANT CONNECT, RESOURCE TO new_user;
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




