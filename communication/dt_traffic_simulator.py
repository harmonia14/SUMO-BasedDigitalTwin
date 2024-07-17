#!/usr/bin/env python3.11

from kafka import KafkaProducer
from dt_config_constants import (
    BROKER_EP, ENTERPRISE_EP, ENCODING, SUMO_CMD,
    SIMULATION_DURATION, KAFKA_VERSION
)
from dt_kafka_topic_manager import sendCamData, sendProbeData, sendTollData, sendInductionLoopData, initTopics
from dt_sensor_data_generator import SUMO_HOME_TOOLS, getTimeStamp
from datetime import date, datetime
import dt_file_io_utils as file
import traci, time, logging

# Configure logging
logging.basicConfig(filename='dt_traffic_simulator.log', 
                    level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

SUMO_HOME_TOOLS()  # checks for SUMO dependency

comp = 'gzip'
print("Starting producers...")
print("Connecting to cluster at:", BROKER_EP)

induction_loop_producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION, compression_type=comp)

print("Starting enterprise producers...")
toll_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)
camera_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)
probe_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)

print("Connected to enterprise cluster at:", ENTERPRISE_EP)

date = date.today()
initTopics()

print("Waiting to start simulation...")
traci.start(SUMO_CMD)
print("Simulation started...")

start_t = time.time()
t = 0

while t < SIMULATION_DURATION:
    traci.simulationStep()
    vehIDs = traci.vehicle.getIDList()
    t = traci.simulation.getTime()
    timestamp = getTimeStamp(date, t)

    if t % 1 == 0:
        sendProbeData(vehIDs, probe_producer, timestamp, "probe_vehicles")
        sendCamData(vehIDs, camera_producer, timestamp, "motorway_cameras")
        sendTollData(vehIDs, toll_producer, timestamp, "toll_bridge_cameras")
        sendInductionLoopData(vehIDs, induction_loop_producer, timestamp, "inductive_loops")

end_time = datetime.now()
real_duration_s = time.time() - start_t
print('Simulation finished at', end_time)
print('Total sim time in seconds: ', real_duration_s)
file.writeTestInfoToFile(end_time, real_duration_s, SIMULATION_DURATION, BROKER_EP, ENTERPRISE_EP)

traci.close()
print("Simulation ended. SUMO closed.")