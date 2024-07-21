# dt_sensor_data_processor.py

import traci
import logging
import math
import time
from datetime import datetime, timedelta
import sumolib
from dt_simulation_config import *
from collections import defaultdict
future_data = defaultdict(list)

# At the top of the file, after imports
vehicles_added = set()

# Load the network once at the module level
net = sumolib.net.readNet(SUMO_NET_FILE)


def validate_sensor_data(data_dic):
    valid_sensor_types = {'induction_loop', 'camera', 'probe', 'toll_bridge'}
    
    if 'sensor_type' not in data_dic:
        logging.error(f"Missing sensor_type in data: {data_dic}")
        return False
    
    if data_dic['sensor_type'] not in valid_sensor_types:
        logging.error(f"Invalid sensor_type: {data_dic['sensor_type']}")
        return False
    
    required_fields = {'vehicle_id', 'speed', 'route_id'}
    missing_fields = required_fields - set(data_dic.keys())
    
    if missing_fields:
        logging.error(f"Missing required fields for {data_dic['sensor_type']}: {missing_fields}")
        return False
    
    logging.info(f"Received valid data from {data_dic['sensor_type']} sensor: Vehicle ID {data_dic['vehicle_id']}")
    return True

def log_time_info(current_sumo_time, simulation_start_time, simulation_start_sumo_time):
    current_real_time = time.time()
    elapsed_real_time = current_real_time - simulation_start_time
    elapsed_sumo_time = current_sumo_time - simulation_start_sumo_time
    
    real_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sumo_datetime = (datetime.fromtimestamp(simulation_start_time) + timedelta(seconds=elapsed_sumo_time)).strftime("%Y-%m-%d %H:%M:%S")
    
    speed_factor = elapsed_sumo_time / elapsed_real_time if elapsed_real_time > 0 else 0
    
    logging.info(f"Real time: {real_datetime}, "
                 f"Simulation time: {sumo_datetime}, "
                 f"Elapsed real time: {timedelta(seconds=int(elapsed_real_time))}, "
                 f"Elapsed SUMO time: {timedelta(seconds=int(elapsed_sumo_time))}, "
                 f"Speed factor: {speed_factor:.2f}x")


def process_sensor_data(data_dic):
    try:
        if validate_sensor_data(data_dic):
            timestamp = float(data_dic['timestamp'])
            current_time = traci.simulation.getTime()
            
            if timestamp <= current_time:
                update_or_add_vehicle(data_dic)
            else:
                future_data[timestamp].append(data_dic)
                logging.info(f"Data for time {timestamp} stored for future processing")
        else:
            logging.warning(f"Skipping invalid sensor data: {data_dic}")
    except Exception as e:
        logging.error(f"Error processing {data_dic.get('sensor_type', 'unknown')} data: {e}")

def update_or_add_vehicle(data_dic):
    veh_id = data_dic['vehicle_id']
    speed = float(data_dic['speed'])
    route_id = data_dic['route_id']
    sensor_type = data_dic['sensor_type']

    try:
        if veh_id not in vehicles_added:
            if route_id not in traci.route.getIDList():
                logging.error(f"Route {route_id} does not exist. Skipping vehicle {veh_id}")
                return
            traci.vehicle.add(veh_id, route_id)
            vehicles_added.add(veh_id)
            logging.info(f"Added new vehicle {veh_id} (reported by {sensor_type} sensor)")
        
        if veh_id in traci.vehicle.getIDList():
            traci.vehicle.setSpeed(veh_id, kphToMps(speed))
            
            if traci.vehicle.getRouteID(veh_id) != route_id:
                traci.vehicle.setRoute(veh_id, [route_id])
            logging.info(f"Updated vehicle {veh_id} (reported by {sensor_type} sensor)")
        else:
            logging.warning(f"Vehicle {veh_id} not found in simulation, but is in vehicles_added set. It may have finished its route.")
    
    except traci.exceptions.TraCIException as e:
            logging.error(f"TraCI error for vehicle {veh_id} (reported by {sensor_type} sensor): {e}")
    except Exception as e:
        logging.error(f"Error updating/adding vehicle {veh_id} (reported by {sensor_type} sensor): {e}")

def kphToMps(speed):
    return speed * 1000 / 3600

def mpsToKph(speed):
    return speed * 3600 / 1000

def calcDistance(point1, point2):
    """
    Calculate the Euclidean distance between two points in 2D space.
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def save_simulation_data():
    data = {
        'time': traci.simulation.getTime(),
        'vehicle_count': len(traci.vehicle.getIDList()),
        'arrived_count': traci.simulation.getArrivedNumber()
    }
    with open(f"simulation_data_{int(traci.simulation.getTime())}.json", "w") as f:
        json.dump(data, f)
    logging.info(f"Simulation data saved at time {traci.simulation.getTime()}")

def clean_up_finished_vehicles():
    global vehicles_added
    current_vehicles = set(traci.vehicle.getIDList())
    finished_vehicles = vehicles_added - current_vehicles
    for veh_id in finished_vehicles:
        if veh_id not in traci.simulation.getArrivedIDList():
            logging.warning(f"Vehicle {veh_id} not in simulation but not marked as arrived. Keeping in vehicles_added.")
        else:
            vehicles_added.remove(veh_id)
            logging.info(f"Removed finished vehicle {veh_id} from tracking")
    