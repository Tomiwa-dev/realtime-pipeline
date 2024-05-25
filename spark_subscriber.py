from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructField

spark = (SparkSession.builder.appName("kafka_consumer")
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.1")
         .getOrCreate())

sc = spark.sparkContext
sc.setLogLevel("WARN")
kafka_bootstrap_servers = "localhost:9092"
inputDF = (spark.readStream.format("kafka")
           .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
           .option("subscribe", "eth_transactions").load())

print("Kafka stream read initialized.")


inputDF_2 = inputDF.selectExpr("CAST(value AS STRING) as value")

schema = StructType([
    StructField("blockNumber", StringType(), True),
    StructField("from", StringType(), True),
    StructField("gas", StringType(), True),
    StructField("gasPrice", StringType(), True),
    StructField("to", StringType(), True),
    StructField("transactionIndex", StringType(), True),
    StructField("type", StringType(), True),
    StructField("value", StringType(), True)
])

parsedDF = inputDF_2.select(from_json(col("value"), schema).alias("parsed_value")).select("parsed_value.*")

transformDF = parsedDF.select('blockNumber', 'from', 'gas', (col('gas').cast("double")/10**18).alias('gas_eth'),
                              'gasPrice', (col('gasPrice').cast("double")/10**18).alias('gasPrice_eth'),
                              'to', 'transactionIndex', 'type', 'value',
                             (col('value').cast("double")/10**18).alias('value_eth'))

# outputDF = transformDF.selectExpr("to_json(struct(*)) AS value")
transformDF.printSchema()

query = (transformDF.selectExpr("to_json(struct(*)) AS value")
         .writeStream
         .format("kafka").option("kafka.bootstrap.servers", kafka_bootstrap_servers)
         .option("topic", "transfrom")
         .option("checkpointLocation", "./spark_checkpoint")
         .outputMode("update").option("startingOffsets", "latest")
         .start())

query.awaitTermination()

