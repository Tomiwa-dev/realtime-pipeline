from web3 import Web3
from confluent_kafka import Producer
import socket
import os
import time
import json

LAST_PROCESSED_BLOCK_FILE = 'last_processed_block.txt'
conf = {'bootstrap.servers': 'localhost:9092',
        'client.id': socket.gethostname()}

w3 = Web3(Web3.HTTPProvider('https://radial-dark-sanctuary.quiknode.pro/626969989a38ec9dbf89dec21e3e50f8f8cffc7f/'))


def current_gas_price():
    return w3.eth.gas_price / 10**9


def get_transactions(block_number):
    block = w3.eth.get_block(block_number, True)

    return block['transactions']


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def read_last_processed_block():
    if os.path.exists(LAST_PROCESSED_BLOCK_FILE):
        with open(LAST_PROCESSED_BLOCK_FILE, 'r') as file:
            content = file.read().strip()
            if content:
                return content
    return None


def write_last_processed_block(block_number):
    with open(LAST_PROCESSED_BLOCK_FILE, 'w') as file:
        file.write(str(block_number))


def block_to_process():
    last_processed_block = read_last_processed_block()
    current_block = w3.eth.get_block_number()

    if last_processed_block is not None:
        return int(last_processed_block) + 1
    else:
        return current_block


def convert_transation_to_json(txn):

    txn_dict = dict(txn)
    selected_keys = ['blockNumber', 'from', 'gas', 'gasPrice', 'to', 'transactionIndex', 'type', 'value']

    selected_dict = {key: txn_dict[key] for key in selected_keys}

    return json.dumps(selected_dict)


if __name__ == "__main__":

    if w3.is_connected():

        producer = Producer(conf)

        while True:
            block_number = block_to_process()
            current_block_number = w3.eth.get_block_number()
            if block_number <= current_block_number:
                transaction = get_transactions(block_number)

                for tx in transaction:
                    tx_json = convert_transation_to_json(tx)
                    producer.produce('eth_transactions', key="eth", value=tx_json, callback=acked)
                    producer.poll(1)

                write_last_processed_block(block_number)
                block_number += 1
            else:
                print("Most recent block processed. Waiting for next block........")
                time.sleep(1)

    else:
        print("Check your connection....")
