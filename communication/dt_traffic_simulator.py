#!/usr/bin/env python3.11

import traci
from dt_config_constants import SUMO_CMD, BROKER_EP, ENTERPRISE_EP, ENCODING, KAFKA_VERSION
from dt_kafka_topic_manager import sendCamData, sendProbeData, sendTollData, sendInductionLoopData, initTopics, KafkaProducer
from dt_sensor_data_generator import SUMO_HOME_TOOLS
import time
import logging

# Configure logging
logging.basicConfig(filename='dt_traffic_simulator.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

SUMO_HOME_TOOLS()  # checks for SUMO dependency

SIMULATION_START_TIME = 79200  # 22:00:00
SIMULATION_END_TIME = 79500    # 22:05:00

print("Starting producers...")
print("Connecting to cluster at:", BROKER_EP)

induction_loop_producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION, compression_type='gzip')
toll_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)
camera_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)
probe_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)

print("Connected to enterprise cluster at:", ENTERPRISE_EP)

initTopics()

print("Starting simulation...")
traci.start(SUMO_CMD)

sim_start_real_time = time.time()

while traci.simulation.getTime() < SIMULATION_END_TIME:
    current_sim_time = traci.simulation.getTime()
    
    # Send data at every simulation step (0.01s)
    vehIDs = traci.vehicle.getIDList()
    sendProbeData(vehIDs, probe_producer, "probe_vehicles")
    sendCamData(vehIDs, camera_producer, "motorway_cameras")
    sendTollData(vehIDs, toll_producer, "toll_bridge_cameras")
    sendInductionLoopData(vehIDs, induction_loop_producer, "inductive_loops")
    
    # Log every second of simulation time
    if int(current_sim_time * 100) % 100 == 0:
        logging.info(f"Simulation time: {current_sim_time:.2f}, Vehicle count: {len(vehIDs)}")
    
    traci.simulationStep()

sim_end_real_time = time.time()
real_duration_s = sim_end_real_time - sim_start_real_time

print(f'Simulation finished. Simulated time: {SIMULATION_END_TIME - SIMULATION_START_TIME} seconds')
print(f'Real-time duration: {real_duration_s:.2f} seconds')

traci.close()
print("Simulation ended. SUMO closed.")

# You can use dt_file_io_utils here if needed to write additional information