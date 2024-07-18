import os, sys, traci, datetime, random, math
import numpy as np
from dt_config_constants import CAMERA_LOOKUP, TOLL_BRIDGE, autonomousVehicles, LOOPS, LOOP_COORDINATES


def addDistanceNoise(p1, p2):
    d = calcDistance(p1, p2)
    return random.uniform(0.95 * d, 1.05 * d)

def addGeoDistanceNoise(coordinates):
    lon = coordinates[0]
    lat = coordinates[1]
    r = 10 / 111300  # converts 10 meters into degrees
    w = r * math.sqrt(random.uniform(0, 1))
    t = 2 * math.pi * (random.uniform(0, 1))
    x = w * math.cos(t)
    lon_e = x / math.cos(lat)
    lat_e = w * math.sin(t)
    return lon + lon_e, lat + lat_e


def mpsToKph(speed):
    return (speed * 3600) / 1000

def addSpeedNoise(speed):
    return random.uniform(0.95 * speed, 1.05 * speed)

def SUMO_HOME_TOOLS():
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
        print("SUMO_HOME environment variable present!")
    else:
        print("please declare environment variable 'SUMO_HOME'")
        sys.exit("please declare environment variable 'SUMO_HOME'")

def getVehicleLocationGeo(vehID):
    x, y = traci.vehicle.getPosition(vehID)
    lon, lat = traci.simulation.convertGeo(x, y)
    return (lon, lat)

def calcDistance(p1, p2):
    return traci.simulation.getDistance2D(x1=float(p1[0]), y1=float(p1[1]), x2=float(p2[0]), y2=float(p2[1]), isGeo=False)

def getDirection(vehID, sensor):
    edge = str(traci.vehicle.getRoadID(vehID))
    for i in sensor["northEdges"].split(","):
        if i in edge:
            return 'N'
    for i in sensor["southEdges"].split(","):
        if i in edge:
            return 'S'
    return 'Unknown'

def get_loop_direction(loop_id):
    if 'Northbound' in loop_id:
        return 'N'
    elif 'Southbound' in loop_id:
        return 'S'
    elif 'Eastbound' in loop_id:
        return 'E'
    elif 'Westbound' in loop_id:
        return 'W'
    else:
        return 'Unknown'

def getVehiclesInView(vehicleIDs, sensor, r, dir):
    lon, lat = sensor["coordinates"].split(",")
    x, y = traci.simulation.convertGeo(float(lat), float(lon), fromGeo=True)
    p1 = [x, y]
    vehicles = []
    for vehID in vehicleIDs:
        x, y = traci.vehicle.getPosition(vehID)
        p2 = [x, y]
        if (dir == 'N' and p2[1] > p1[1]) or (dir == 'S' and p2[1] < p1[1]):
            if calcDistance(p1, p2) < r and getDirection(vehID, sensor):
                vehicles.append(vehID)
    return vehicles

def getCamVehicleIDs(camera_id, vehicleIDs):
    return getVehiclesInView(vehicleIDs, CAMERA_LOOKUP[camera_id], 150, camera_id[4])

def getInductionLoopVehicleIDs(loop_id, vehicleIDs):
    loopVehicles = traci.inductionloop.getLastStepVehicleIDs(loop_id)
    return [vehID for vehID in loopVehicles if vehID in vehicleIDs]

def getProbeVehicleIDs(vehicleIDs):
    return [vehID for vehID in vehicleIDs if traci.vehicle.getTypeID(vehID) in autonomousVehicles]

def getTollVehicleIDs(vehicleIDs, p1):
    return getVehiclesInViewToll(vehicleIDs, 100, p1)

def getVehiclesInViewToll(vehicleIDs, r, p1):
    vehicles = []
    for vehID in vehicleIDs:
        x, y = traci.vehicle.getPosition(vehID)
        p2 = [x, y]
        if calcDistance(p1, p2) < r and getDirection(vehID, TOLL_BRIDGE):
            vehicles.append(vehID)
    return vehicles

def create_unified_data(sensor_type, **kwargs):
    data = {
        'sensor_type': sensor_type,
        'sensor_id': kwargs.get('sensor_id', ''),
        'timestamp': f'{traci.simulation.getTime():.2f}',  # Format to 2 decimal places # Use SUMO simulation time
        'vehicle_id': kwargs.get('vehicle_id', ''),
        'lane_id': kwargs.get('lane_id', ''),
        'lane_index': kwargs.get('lane_index', ''),
        'direction': kwargs.get('direction', ''),
        'speed': kwargs.get('speed', ''),
        'location': kwargs.get('location', ''),
        'distance': kwargs.get('distance', ''),
        'lane_position': kwargs.get('lane_position', ''),
        'vehicle_type': kwargs.get('vehicle_type', ''),
        'vehicle_class': kwargs.get('vehicle_class', ''),
        'route_id': kwargs.get('route_id', ''),  # Add this line
    }
    return {k: v for k, v in data.items() if v != ''}  # Remove empty fields

def getLoopData(loop_id):
    vehicle_data = traci.inductionloop.getVehicleData(loop_id)
    loop_position = traci.inductionloop.getPosition(loop_id)
    
    # Get loop's geo-coordinates
    loop_prefix = loop_id.split('-')[0]  # Extract the prefix (e.g., 'NRA_000000001503_Northbound')
    
    # Find the closest matching prefix in LOOP_COORDINATES
    matching_prefix = next((key for key in LOOP_COORDINATES.keys() if key in loop_prefix), None)
    
    if matching_prefix is None:
        print(f"Warning: No matching coordinates found for loop {loop_id}")
        return []  # Return an empty list if no matching coordinates are found
    
    loop_lon, loop_lat = LOOP_COORDINATES[matching_prefix]
    loop_x, loop_y = traci.simulation.convertGeo(loop_lat, loop_lon, fromGeo=True)
    
    data_list = []
    for veh_id, veh_length, entry_time, exit_time, vType in vehicle_data:
        if exit_time < 0:  # Vehicle is still on the loop
            veh_x, veh_y = traci.vehicle.getPosition(veh_id)
            distance = math.sqrt((loop_x - veh_x)**2 + (loop_y - veh_y)**2)
            lane_position = traci.vehicle.getLanePosition(veh_id)
            speed = traci.vehicle.getSpeed(veh_id)
            vehicle_class = traci.vehicle.getVehicleClass(veh_id)
            
            data = create_unified_data(
                'induction_loop',
                sensor_id=loop_id,
                vehicle_id=veh_id,
                lane_id=traci.vehicle.getRoadID(veh_id),
                lane_index=traci.vehicle.getLaneIndex(veh_id),
                speed=str(round(addSpeedNoise(mpsToKph(speed)), 2)),
                direction=get_loop_direction(loop_id),
                distance=str(round(distance, 2)),
                lane_position=str(round(lane_position, 2)),
                vehicle_type=vType,
                vehicle_class=vehicle_class,
                route_id=traci.vehicle.getRouteID(veh_id)
            )
            data_list.append(data)
    
    return data_list

def getCamData(vehID, camera_id):
    lon, lat = CAMERA_LOOKUP[camera_id]["coordinates"].split(",")
    x, y = traci.simulation.convertGeo(float(lat), float(lon), fromGeo=True)
    p1 = [x, y]
    x, y = traci.vehicle.getPosition(vehID)
    p2 = [x, y]
    return create_unified_data(
        'camera',
        sensor_id=camera_id,
        vehicle_id=vehID,
        lane_id=traci.vehicle.getRoadID(vehID),
        lane_index=traci.vehicle.getLaneIndex(vehID),
        direction=getDirection(vehID, CAMERA_LOOKUP[camera_id]),
        distance=str(addDistanceNoise(p1, p2)),
        speed=str(round(addSpeedNoise(mpsToKph(traci.vehicle.getSpeed(vehID))), 2)),
        vehicle_type=traci.vehicle.getTypeID(vehID),
        vehicle_class=traci.vehicle.getVehicleClass(vehID),
        route_id=traci.vehicle.getRouteID(vehID) 
    )

def getProbeData(vehID):
    lane_position = traci.vehicle.getLanePosition(vehID)
    return create_unified_data(
        'probe',
        sensor_id=vehID,  # For probes, the vehicle is the sensor
        vehicle_id=vehID,
        location=str(addGeoDistanceNoise(getVehicleLocationGeo(vehID))),
        lane_position=str(round(lane_position, 2)),
        speed=str(round(addSpeedNoise(mpsToKph(traci.vehicle.getSpeed(vehID))), 2)),
        vehicle_type=traci.vehicle.getTypeID(vehID),
        vehicle_class=traci.vehicle.getVehicleClass(vehID),
        lane_id=traci.vehicle.getRoadID(vehID),  
        lane_index=traci.vehicle.getLaneIndex(vehID),  
        route_id=traci.vehicle.getRouteID(vehID) 
    )

def getTollData(vehID, p1):
    x, y = traci.vehicle.getPosition(vehID)
    p2 = [x, y]
    return create_unified_data(
        'toll_bridge',
        sensor_id='toll_bridge',
        vehicle_id=vehID,
        lane_id=traci.vehicle.getRoadID(vehID),
        lane_index=traci.vehicle.getLaneIndex(vehID),
        direction=getDirection(vehID, TOLL_BRIDGE),
        distance=str(addDistanceNoise(p1, p2)),
        speed=str(round(addSpeedNoise(mpsToKph(traci.vehicle.getSpeed(vehID))), 2)),
        vehicle_class=traci.vehicle.getVehicleClass(vehID),
        route_id=traci.vehicle.getRouteID(vehID)
        )