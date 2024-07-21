#!/usr/bin/env python

import logging
from kafka import KafkaConsumer
import traci
from dt_simulation_config import *
from dt_sensor_data_processor import *
from collections import defaultdict

# Configure logging
logging.basicConfig(filename='dt_core_simulator.log', 
                    level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def run_simulation():
    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BROKER_ENDPOINT,
        value_deserializer=KAFKA_DECODING,
        consumer_timeout_ms=1000,
        api_version=KAFKA_VERSION
    )
    
    consumer.subscribe(topics=KAFKA_TOPICS)
    
    no_data_count = 0
    max_no_data_count = 50
    simulation_started = False
    data_queue = []
    future_data = defaultdict(list)

    try:
        traci.start(SUMO_CMD)
        logging.info("TraCI connection established. Waiting for initial data...")

        while True:
            new_data_received = False
            records = consumer.poll(100)
            
            if records:
                # no_data_count = 0
                # if not simulation_started:
                #     simulation_started = True
                #     logging.info("Received initial data. Starting simulation.")
                new_data_received = True
                for key, value in records.items():
                    for message in value:
                        data = message.value
                        if isinstance(data, dict) and 'timestamp' in data:
                            try:
                                timestamp = float(data['timestamp'])
                                data_queue.append((timestamp, data))
                            except ValueError:
                                logging.error(f"Invalid timestamp in data: {data}")
                        else:
                            logging.error(f"Unexpected data format: {data}")
                    
                    if not simulation_started:
                        simulation_started = True
                        logging.info("Received initial data. Starting simulation.")
            
            if simulation_started:
                current_time = traci.simulation.getTime()
                
                # Process data from queue and future data
                data_processed = False
                # Sort the data_queue based on timestamp
                data_queue.sort(key=lambda x: x[0])
                while data_queue and data_queue[0][0] <= current_time:
                    _, data = data_queue.pop(0)
                    process_sensor_data(data)
                    data_processed = True

                for timestamp, data_list in list(future_data.items()):
                    if timestamp <= current_time:
                        for data in data_list:
                            process_sensor_data(data)
                            data_processed = True
                        del future_data[timestamp]

                if data_processed:
                    no_data_count = 0
                    last_processed_time = current_time
                elif not new_data_received:
                    no_data_count += 1

                traci.simulationStep()

                # Log the current state after each simulation step
                logging.info(f"Current state - Simulation time: {current_time}, "
                             f"No data count: {no_data_count}, "
                             f"Vehicle count: {traci.vehicle.getIDCount()}, "
                             f"Data queue size: {len(data_queue)}, "
                             f"Future data size: {sum(len(v) for v in future_data.values())}")
            
            if no_data_count > max_no_data_count and traci.vehicle.getIDCount() == 0 and not data_queue:
                logging.info("No more data and all vehicles have completed. Ending simulation.")
                break

    except traci.exceptions.FatalTraCIError as e:
        logging.error(f"FatalTraCIError: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
    finally:
        traci.close()
        logging.info("Simulation ended and connection to SUMO closed.")

if __name__ == "__main__":
    logging.info("Starting Digital Twin Core Simulator")
    try:
        run_simulation()
    except Exception as e:
        logging.exception(f"Error in simulation: {e}")
    logging.info("Digital Twin Core Simulator finished")