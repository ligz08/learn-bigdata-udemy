# Spark SQL and DataFrame

## Spark Theory
![Spark Stack](https://dhenschen.files.wordpress.com/2015/06/spark-2015-vision.jpg)  
- RDD = resilient distributed data 
- DataFrame = RDD with schema

### Spark SQL  
Spark SQL is awesome because:
- *Integrated* : seamlessly mix SQL with Python/Java/Scala/R...
- *Uniform Data Access* : provides a common way to access data from Hive, JSON, ...  
- *100% Hive Compatibility* : 
- *Standard Connectivity* : connect through JDBC/ODBC, so that many BI/BA tools can work with it

## `sapark-shell` -- Spark Interactive Shell with Scala  
- Run: `spark-sell`  
- Query: `sqlContext.sql('Hive QL')` *note: no `;` at the end of HQL string  




## PySpark 
### Interactive Shell  
`pyspark` -- a python interactive shell to run Spark

### `pyspark.SQLContext` example

A `pyspark` `SQLContext` example for processing text file:  (using Spark version 1)  
Assume the text file looks like this:
```text
John, 21
Mary, 20
...
```
The  Python script:
```python
from pyspark.sql import SQLContext, Row
sqlContext = SQLContext(sc)
```
Note that `sc` is a Spark Context object that Spark should have created for you before this script is executed.  
The SQLContext object is a wrapper around the Spark Context.
```python
lines = sc.textFile('path/to/your/file.csv')
parts = lines.map(lambda line: line.split(','))
rows = parts.map(lambda part: Row(name=part[0], age=int(part[1])))

tableSchema = sqlContext.inferSchema(rows)
tableSchema.registerTempTable('people')
```
Here we read a text file with `sc.textFile()`, and parse it by splitting each line with `,`. 
Then register the parsed info as a temporary table with `.registerTempTable()`. 
A temporary table only exists when you run this script. 
During that time you can run SQL queries as if that temp table is in your database.  
Say we want to find teenagers whose age are between 13 and 19:
```python
teenagers = sqlContext.sql('SELECT name FROM people WHERE age>=13 AND age<=19')
```
Query results (such as `teenager` here) are stored as RDD objects. All normal RDD operation can apply.
```python
teenNames = teenagers.map(lambda p: 'Name: ' + p.name)
for teenName in teenNames.collect(): 
    print(teenName)
```
Here [`.collect()`](https://spark.apache.org/docs/2.2.0/api/python/pyspark.html#pyspark.RDD.collect) method returns a list of rows/elements in an RDD object.


### `pyspark.HiveContext` example
Basic steps:  
- create a `HiveContext` instance
- do all that good stuff you can do with Hive QL, wrapped in the `.sql()` method (refer to: [Hive notes](Hive%20Notes.md))
```python
from pyspark.sql import HiveContext
hiveCtx = HiveContext(sc)

hiveCtx.sql("""
    CREATE TABLE IF NOT EXISTS src (key INT, value STRING)
""")
hiveCtx.sql("""
    LOAD DATA LOCAL PATH 'path/to/your/file.txt' OVERWRITE INTO TABLE src
""")

results = hiveCtx.sql('SELECT * FROM src LIMIT 10').collect()
```


### DataFrame
A Spark DataFrame is a distributed collection of `Row` objects.  
DataFrame offers a unified interface to read/write data from/to a variety of formats.

A `read` example:
```python
df = sqlContext.read \
        .format('json') \
        .option('sampleRatio', '0.1') \
        .load('/home/michael/data.json')
```
A `write` example:
```python
df.write \
    .format('parquet')
    .mode('append')
    .partionBy('year')
    .saveAsTable('table_name')
```
Useful DF methods:
- [`df.printSchema()`](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame.printSchema) -- print schema with some style
- [`df.collect()`](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame.collect) -- return a list of rows to Python
- [`df.show()`](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame.show) -- print what's in the df on screen (don't use on big df)
- [`df.registerTempTable('table_name')`](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame.registerTempTable)  -- register df as a table, so you can refer to the `table_name  ` in later HQL queries.
- [`df.saveAsTable()`](http://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrameWriter.saveAsTable) -- save the df content as a table in Hive