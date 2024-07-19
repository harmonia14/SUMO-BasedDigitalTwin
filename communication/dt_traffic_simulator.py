#!/usr/bin/env python3.11

import traci
import time
import logging
from kafka import KafkaProducer
from dt_config_constants import (
    SUMO_CMD, BROKER_EP, ENTERPRISE_EP, KAFKA_VERSION, ENCODING,
    SIMULATION_START_TIME, SIMULATION_END_TIME
)
from dt_kafka_topic_manager import sendProbeData, sendCamData, sendTollData, sendInductionLoopData, initTopics

# Configure logging
logging.basicConfig(filename='dt_traffic_simulator.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_data(vehIDs, allow_new_vehicles):
    sendProbeData(vehIDs, probe_producer, "probe_vehicles", allow_new_vehicles)
    sendCamData(vehIDs, camera_producer, "motorway_cameras", allow_new_vehicles)
    sendTollData(vehIDs, toll_producer, "toll_bridge_cameras", allow_new_vehicles)
    sendInductionLoopData(vehIDs, induction_loop_producer, "inductive_loops", allow_new_vehicles)

print("Starting producers...")
print("Connecting to cluster at:", BROKER_EP)

# Define Kafka producers
induction_loop_producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION, compression_type='gzip')
toll_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)
camera_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)
probe_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)

print("Connected to enterprise cluster at:", ENTERPRISE_EP)

initTopics()

print("Starting simulation...")
traci.start(SUMO_CMD)

sim_start_real_time = time.time()
adding_vehicles = True
existing_vehicles = set()
last_log_time = 0

while True:
    current_sim_time = traci.simulation.getTime()
    
    if current_sim_time >= SIMULATION_END_TIME and adding_vehicles:
        adding_vehicles = False
        print(f"Reached SIMULATION_END_TIME. Stopping addition of new vehicles.")
        existing_vehicles = set(traci.vehicle.getIDList())
    
    vehIDs = traci.vehicle.getIDList()
    
    if adding_vehicles:
        vehIDs = traci.vehicle.getIDList()
        send_data(vehIDs, True)

    else:
        # Only process existing vehicles
        vehIDs = list(existing_vehicles.intersection(set(traci.vehicle.getIDList())))
        if vehIDs:
            send_data(vehIDs, False)
        existing_vehicles = set(vehIDs)
    
    # Log every second of simulation time
    if current_sim_time - last_log_time >= 1:
        logging.info(f"Simulation time: {current_sim_time:.2f}, Vehicle count: {len(vehIDs)}")
        last_log_time = current_sim_time
    
    traci.simulationStep()
    
    if not adding_vehicles and len(existing_vehicles) == 0:
        print("All existing vehicles have completed their routes. Ending simulation.")
        break


sim_end_real_time = time.time()
real_duration_s = sim_end_real_time - sim_start_real_time

print(f'Simulation finished. Simulated time: {traci.simulation.getTime() - SIMULATION_START_TIME:.2f} seconds')
print(f'Real-time duration: {real_duration_s:.2f} seconds')

traci.close()
print("Simulation ended. SUMO closed.")

# Close Kafka producers
induction_loop_producer.close()
toll_producer.close()
camera_producer.close()
probe_producer.close()