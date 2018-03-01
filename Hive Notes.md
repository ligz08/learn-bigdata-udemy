# Hive Theory
Hive is based on **Hadoop** and **MapReduce**.

Hive is good at:  
- OLAP

Hive is bad at:  
- Small data set
- Online transaction processing (OLTP)
Real-time queries
- Row level entry (like modifying a row)

Hive data model:
![hive model](https://s3.amazonaws.com/files.dezyre.com/hadoop_page1.0/slides/hive/hive_intro/Hive_Introduction_Sllides-page-018-min.jpg)

**Metadata**: data about the database itself.

# Hive Client
- `hive`: interactive shell  
- `hive -e ‘SELECT * FROM tbl;’` -- run single query from terminal
- `hive -f path_to_file.sql` -- run a sql script file


# Hive Admin Commands
- `show databases;`
- `show tables;`
- `desc [formatted] table_name;` -- describe a table
- `show partitions table_name;` -- show partition details of a table


# HiveQL
### [Create table](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-CreateTable)
```sql
CREATE TABLE IF NOT EXISTS tbl_name
COMMENT ‘...’
PARTITION BY ...
ROW FORMAT DELIMITED FIELDS TERMINATED BY ‘,’
STORED AS TEXTFILE
LOCATION ‘hdfs:///path/file’
TBLPROPERTIES (...);
```

### Load data
```sql
LOAD DATA [LOCAL] INPATH ‘path’ OVERWRITE INTO TABLE table_name;
```

# Managed vs. External table
Managed tables (default option when creating a table) are managed within Hive.

External tables are pointers to data files, and the data files may be shared with other programs.  

When dropping a managed table, both metadata and the underlying data file are deleted. When dropping an external table, the data file still exists.


# Hive Best Practise
### Hive Ingestion (txt→ORC)
ORC files are faster for machine reading
```sql
CREATE TABLE table1(col1 type1, col2 type2)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ‘,’ STORED AS TEXTFILE;

LOAD DATA INPATH ‘hdfs:///path/to/file’;

CREATE TABLE table2(col1 type1, col2 type2) ROW FORMAT DELIMITED FIELDS TERMINATED BY ‘,’ STORED AS RCFILE;

INSERT OVERWRITE TABLE table2 SELECT * FROM table1;
```
### Traditional DB → Hive: Sqoop
### Use Partitions


# ORC and Compressing
```sql
CREATE TABLE table1(col1 type1, col2 type2)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ‘,’ 
STORED AS ORC TBLPROPERTIES(‘orc.compress’=’ZLIB’);
```


# Hive Interview FAQ
- Managed (internal) vs. external table?

- OLTP vs. OLAP? Which is Hive suitable for?  
A: OLAP. Hive is suitable for processing big batches of data.

- What is metastore in Hive?  
A: It records info about Hive databases, eg. databases, tables, schema, columns, column dtypes, file locations associated with tables…

- Why we need Hive?  
A: Query data stored on HDFS in a SQL fashion, view files as relational tables.

- How to check HDFS location of table?  
A: `desc formatted table_name`

- How to check partitions of a table?  
A: `show partitions table_name;`

- What’s the significance of `IF EXISTS`/`IF NOT EXISTS`?  
A: Avoid reporting error and terminating scripts.

- When you point a partition to a new dir, what happens to the data?  
A: Hive will look for data in the new dir, if there’s no file, the partition will have no data.

- When loading data into Hive, how do you specify loading from HDFS vs. local FS?  
A: `LOAD DATA LOCAL INPATH ‘path’`