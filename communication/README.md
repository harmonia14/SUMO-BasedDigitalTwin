# Communication Architecture for Transportation Digital Twin

This folder contains the communication component of the Transportation Digital Twin project, based on the work by Conor Fennell but with significant modifications.

## Overview

This component simulates the communication architecture for a transportation digital twin, focusing on data streaming from various traffic sensors to a digital twin system using Apache Kafka.

## Dependencies

- SUMO (Simulation of Urban MObility): A microscopic traffic simulator
- Docker and Docker Compose: For running Kafka brokers
- Python 3.x
- Apache Kafka

## Configuration

The main configuration file is `dt_config_constants.py`. This file contains important settings such as:

- Kafka broker endpoints
- Simulation parameters
- Sensor configurations

## Key Components

1. `dt_traffic_simulator.py`: Simulates traffic and generates sensor data
2. `dt_data_consumer.py`: Consumes data from Kafka topics
3. `dt_enterprise_data_forwarder.py`: Forwards data between Kafka clusters
4. `dt_kafka_topic_manager.py`: Manages Kafka topics and partitions
5. `dt_sensor_data_generator.py`: Generates simulated sensor data

## Running the Simulation

1. Start the Kafka brokers: ./run_docker_compose.sh
2. Run the traffic simulator: ./dt_traffic_simulator.py
3. In separate terminals, run the data consumer and enterprise data forwarder: ./dt_data_consumer.py (one terminal) & ./dt_enterprise_data_forwarder.py (the other terminal)
4. To stop the Kafka brokers after simulation: ./down_docker_compose.sh

## Data Flow

1. The traffic simulator generates sensor data
2. Data is published to specific Kafka topics
3. The data consumer reads from these topics
4. The enterprise data forwarder moves data between Kafka clusters as needed

## Output

Consumed data is written to the `consumed_topics` directory, organized by topic and partition.

## Notes

- This project simulates various sensor types including inductive loops, cameras, and vehicle probes
- The simulation is based on a model of the M50 motorway in Dublin
- Kafka topics and partitions are used to organize data by sensor type and location
