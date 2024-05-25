CREATE TABLE default.transactions_queue
(
    blockNumber      String,
    from             String,
    gas              String,
    gas_eth          Float64,
    gasPrice         String,
    gasPrice_eth     Float64,
    to               String,
    transactionIndex String,
    type             String,
    value            String,
    value_eth        Float64
)
    engine = Kafka('kafka:29092', 'transfrom', 'foo', 'JSONEachRow')
        SETTINGS kafka_thread_per_consumer = 0, kafka_num_consumers = 1;

CREATE TABLE default.transactions
(
    blockNumber      String,
    from             String,
    gas              String,
    gas_eth          Float64,
    gasPrice         String,
    gasPrice_eth     Float64,
    to               String,
    transactionIndex String,
    type             String,
    value            String,
    value_eth        Float64
)
    engine = MergeTable()
ORDER BY (blockNumber);

CREATE MATERIALIZED VIEW default.transactions_consumer
            TO default.transactions
            (
             `blockNumber` String,
             `from` String,
             `gas` String,
             `gas_eth` Float64,
             `gasPrice` String,
             `gasPrice_eth` Float64,
             `to` String,
             `transactionIndex` String,
             `type` String,
             `value` String,
             `value_eth` Float64
                )
AS
SELECT *
FROM default.transactions_queue;