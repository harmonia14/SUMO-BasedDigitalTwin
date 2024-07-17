#!/usr/bin/env python3

import logging
import time
from kafka import KafkaConsumer, KafkaProducer
from dt_config_constants import DECODING, BROKER_EP, ENTERPRISE_EP, ENCODING, TOPIC_LOOKUP, KAFKA_VERSION
from dt_kafka_topic_manager import getPartition
from multiprocessing import Process


# Configure logging
logging.basicConfig(filename='dt_enterprise_data_forwarder.log', 
                    level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def consume(producerEP, consumerEP, topic):
    producer = KafkaProducer(bootstrap_servers=producerEP, value_serializer=ENCODING, compression_type='gzip')
    consumer = KafkaConsumer(bootstrap_servers=consumerEP, value_deserializer=DECODING, api_version=KAFKA_VERSION)
    consumer.subscribe(topics=topic)
    logging.info(f"Consumer for topics {topic} is running...")

    try:
        for msg in consumer:
            # Send the message to the appropriate physical topic
            producer.send(TOPIC_LOOKUP[msg.topic], msg.value, partition=getPartition(msg))
            logging.info(f"Message consumed from topic {msg.topic}, partition {msg.partition}, and sent to {TOPIC_LOOKUP[msg.topic]}")
    except Exception as e:
        logging.error(f"Error consuming messages from topics {topic}: {e}")
    finally:
        consumer.close()
        logging.info(f"Consumer for topics {topic} has stopped.")

if __name__ == '__main__':
    logging.info("Starting consumers...")

    topics_list = [
        ["enterprise_motorway_cameras"],
        ["enterprise_toll_bridge_cameras"],
        ["enterprise_probe_vehicles"]
    ]

    processes = [Process(target=consume, args=(BROKER_EP, ENTERPRISE_EP, topics)) for topics in topics_list]

    for process in processes:
        process.start()

    for process in processes:
        process.join()