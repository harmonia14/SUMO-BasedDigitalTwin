#!/usr/bin/env python3

import logging
import time
from kafka import KafkaConsumer
from dt_config_constants import DECODING, BROKER_EP, KAFKA_VERSION, TOPICS
import dt_file_io_utils as file
from multiprocessing import Process


# Configure logging
logging.basicConfig(filename='dt_data_consumer.log', 
                    level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def consume(broker_ep, topics):
    """
    Consume messages from Kafka topics and write them to a file.

    Args:
        broker_ep (str): Bootstrap server for Kafka consumer.
        topics (list): List of topics to subscribe to.
    """
    consumer = KafkaConsumer(
        bootstrap_servers=broker_ep,
        value_deserializer=DECODING,
        api_version=KAFKA_VERSION
    )
    consumer.subscribe(topics=topics)
    logging.info(f"Consumer for topics {topics} is running...")

    try:
        for msg in consumer:
            # Used for latency calculations
            # latency = (time.time() - float(msg.value['sent_timestamp'])) * 1000    
            # file.writeLatencyToFile(msg.topic, latency)
            file.writeMessageToFile(msg.partition, msg.topic, msg.value)
            logging.info(f"Message consumed from topic {msg.topic}, partition {msg.partition}")
    except Exception as e:
        logging.error(f"Error consuming messages from topics {topics}: {e}")
    finally:
        consumer.close()
        logging.info(f"Consumer for topics {topics} has stopped.")

if __name__ == '__main__':
    logging.info("Starting consumers...")

    topics_list = [
        ["inductive_loops"],
        ["probe_vehicles"],
        ["motorway_cameras"],
        ["toll_bridge_cameras"]
    ]

    processes = [Process(target=consume, args=(BROKER_EP, topics)) for topics in topics_list]

    for process in processes:
        process.start()

    for process in processes:
        process.join()