# Digital Twin Simulation

This folder contains the core simulation files for the Transportation Digital Twin project.

## Files

1. `dt_core_simulator.py`: Main simulation runner
2. `dt_sensor_data_processor.py`: Processes sensor data and updates the simulation
3. `dt_simulation_config.py`: Configuration settings for the simulation

## File Descriptions

### dt_core_simulator.py

This is the main entry point for running the digital twin simulation. It:
- Sets up a Kafka consumer to receive sensor data
- Initializes and runs the SUMO traffic simulation
- Processes incoming data and updates the simulation state
- Handles simulation timing and termination conditions

Key features:
- Uses TraCI to interact with SUMO
- Implements a data queue system to handle out-of-order data
- Logs simulation progress and errors

### dt_sensor_data_processor.py

This file contains functions for processing and validating sensor data. It:
- Validates incoming sensor data
- Updates or adds vehicles to the simulation based on sensor data
- Handles different types of sensors (induction loops, cameras, probes, toll bridges)
- Manages a set of active vehicles in the simulation

Key features:
- Data validation for different sensor types
- Vehicle management (adding, updating, removing)
- Conversion utilities for speed and distance calculations

### dt_simulation_config.py

This file contains all the configuration parameters for the simulation, including:
- SUMO configuration (binary path, configuration files, command-line options)
- Kafka configuration (broker details, topics)
- Simulation parameters (max time, thresholds)
- Sensor configurations (cameras, toll bridges, induction loops)

## Running the Simulation

To run the simulation:

1. Ensure all dependencies are installed (SUMO, TraCI, Kafka-Python)
2. Set up your Kafka broker and topics as specified in `dt_simulation_config.py`
3. Run the simulation with: ./dt_core_simulator.py

## Notes

- The simulation is designed to work with a specific SUMO network (M50 motorway in Dublin)
- Sensor data is expected to come from Kafka topics in a specific format
- Logging is configured to output to `dt_core_simulator.log`
- Make sure to adjust the configuration in `dt_simulation_config.py` to match your specific setup and requirements

For more detailed information about each component, refer to the comments within each file.
