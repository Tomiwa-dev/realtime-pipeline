# Realtime Ethereum Transaction Pipeline
This repository contains a realtime analytics pipeline that processes Ethereum blockchain transactions. The pipeline reads transactions from an Ethereum node, publishes them to a Kafka topic, processes and transforms them using Spark Streaming, stores the results in Clickhouse, and visualizes the data using Superset.
## Getting Started

### Tools Used
* Clickhouse

* Superset

* Spark Streaming

* Kafka

### Overview
1. Data Ingestion: A Python script reads Ethereum blockchain transactions and writes them to a Kafka topic named eth_transactions. 

2. Data Processing: A Spark Streaming job reads from the eth_transactions topic, transforms the data by converting values from wei to eth for specific columns (gasPrice, gas, value), and writes the transformed data to a new Kafka topic named transformed.

3. Data Storage: A table is created in Clickhouse to read the transaction queue. A materialized view is used to query the transaction queue and write to a table named transaction.

4. Data Visualization: Superset connects to the Clickhouse instance and reads the transaction table for visualization and analysis.

### Running the Project

1. Clone the repository 

    `git clone <repository_url>`
    
    `cd <repository_directory>`

2. Set up environment variables

   * create a `.env` file with the Ethereum node endpoint

3. Start the services
   To set up clickhouse 

    `docker-compose up -d`

4. Run the Ethereum data ingestion script

    `python readEthereumData.py`

5. Run the Spark subscriber script
Create a kafka topic called transform to write the transformed transactions to.


      kafka-topics --list --bootstrap-server localhost:9092`


      `kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transform`


      `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.1 spark_subscriber.py`

6. Access Superset 

   Open your browser and go to http://localhost:8088
   Log in with the credentials:
   Username: admin
   Password: admin
   Connect to Clickhouse and create dashboards and charts based on the transaction table.


