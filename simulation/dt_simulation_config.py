# dt_simulation_config.py

import json
import math

# SUMO Configuration
SUMO_BINARY = "sumo-gui"
SUMO_CONFIG_FILE = "../configuration/M50_simulation_digital_twin.sumo.cfg"
SUMO_NET_FILE = "../configuration/M50network.net.xml"
SUMO_ROUTE_FILE = "../configuration/M50_routes.rou.xml"
SUMO_CMD = [
    SUMO_BINARY, 
    "-c", "../configuration/M50_simulation_digital_twin.sumo.cfg",
    "--log", "sumo_detailed.log",
    "--message-log", "sumo_messages.log",
    "--error-log", "sumo_errors.log",
    "--no-step-log", "true",
    "--duration-log.disable", "false",
    "--lanechange.duration", "5",
    "--collision.action", "warn",
    "--time-to-teleport", "-1",
    "--eager-insert", "true",
    "--random", "false"
]



# Kafka Configuration
KAFKA_VERSION = (7, 6, 0)
KAFKA_BROKER_IP = 'localhost'
KAFKA_BROKER_ENDPOINT = [KAFKA_BROKER_IP]
KAFKA_DECODING = lambda v: json.loads(v)

# Kafka Topics
KAFKA_TOPICS = [
    "motorway_cameras",
    "toll_bridge_cameras", 
    "probe_vehicles", 
    "inductive_loops"
]

# Simulation Parameters
MAX_SIMULATION_TIME = 79500.5  # in seconds
CAMERA_VIEW_RADIUS = 150  # in meters
SPEED_DISCREPANCY_THRESHOLD = 5.0  # in m/s
DISTANCE_DISCREPANCY_THRESHOLD = 10.0  # in meters

# Earth Constants
EARTH_EQUATORIAL_RADIUS = 6378137.0
EARTH_EQUATORIAL_METERS_PER_DEGREE = math.pi * EARTH_EQUATORIAL_RADIUS / 180

# Camera Configurations
CAMERA_LOOKUP = {
    "M50(S) After J9 (N7)": {
        "coordinates": "53.31353873270574,-6.363575673942173",
        "northEdges": "345616204#1.655",
        "southEdges": "75259388-AddedOffRampEdge",
        "partition": 0
    },
    "M50(S) At J9 (N7)": {
        "coordinates": "53.32105761034455,-6.3702774491561724",
        "northEdges": "4937552#1-AddedOnRampEdge,22941416,4937552",
        "southEdges": "gneE0,11955830",
        "partition": 1
    },
    "M50(S) 1.4km Before J9 (N7)": {
        "coordinates": "53.33335994735108,-6.382773162408997",
        "northEdges": "360361373.981",
        "southEdges": "48290550.1878",
        "partition": 2
    },
    "M50(N) 0.6km Before J7 (N4)": {
        "coordinates": "53.34727008589719,-6.386567333598459",
        "northEdges": "360361373.2643",
        "southEdges": "48290550",
        "partition": 3
    },
    "M50(N) Before J7 (N4)": {
        "coordinates": "53.35269470355068,-6.38544365135953",
        "northEdges": "492226831,4414080#0.187",
        "southEdges": "61047111,492229071,gneJ14,61047111.165",
        "partition": 4
    },
    "M50(S) At J7 (N4)": {
        "coordinates": "53.35885146892749,-6.3834896661669625",
        "northEdges": "4414080#0.756.47,71324924,4414080#1-AddedOnRampEdge",
        "southEdges": "16403446,4402297",
        "partition": 5
    },
    "M50(S) Before West Link": {
        "coordinates": "53.363722242995145,-6.382086740810554",
        "northEdges": "4414080#1-AddedOnRampEdge.343",
        "southEdges": "106130759.2098",
        "partition": 6
    },
    "M50(S) Before ORT Gantry": {
        "coordinates": "53.37334705444544,-6.373142233357861",
        "northEdges": "gneE7,gneE6",
        "southEdges": "106130759.791",
        "partition": 7
    }
}

# Toll Bridge Configuration
TOLL_BRIDGE = {
    "coordinates": "53.3617409,-6.3829509",
    "northEdges": "4414080#1-AddedOnRampEdge.343",
    "southEdges": "106130759.2098",
}

# Induction Loop Configurations
INDUCTION_LOOPS = {
    "NRA_000000001503_Northbound": [
        "NRA_000000001503_Northbound-1", 
        "NRA_000000001503_Northbound-2", 
        "NRA_000000001503_Northbound-3", 
        "NRA_000000001503_Northbound-4"
    ],
    "NRA_000000001503_Southbound": [
        "NRA_000000001503_Southbound-1", 
        "NRA_000000001503_Southbound-2", 
        "NRA_000000001503_Southbound-3", 
        "NRA_000000001503_Southbound-4"
    ],
    "NRA_000000001508_Southbound": [
        "NRA_000000001508_Southbound-1",
        "NRA_000000001508_Southbound-2",
        "NRA_000000001508_Southbound-3",
        "NRA_000000001508_Southbound-4"
    ],
    "NRA_000000001508_Northbound": [
        "NRA_000000001508_Northbound-1",
        "NRA_000000001508_Northbound-2",
        "NRA_000000001508_Northbound-3",
        "NRA_000000001508_Northbound-4"
    ],
    "NRA_000000020047_Westbound": [
        "NRA_000000020047_Westbound-1",
        "NRA_000000020047_Westbound-2",
        "NRA_000000020047_Westbound-3",
        "NRA_000000020047_Westbound-Bus-Lane"
    ],
    "NRA_000000020047_Eastbound": [
        "NRA_000000020047_Eastbound-1",
        "NRA_000000020047_Eastbound-2",
        "NRA_000000020047_Eastbound-3",
        "NRA_000000020047_Eastbound-Bus-Lane"
    ],
    "NRA_000000001070_Eastbound": [
        "NRA_000000001070_Eastbound-1",
        "NRA_000000001070_Eastbound-2",
        "NRA_000000001070_Eastbound-3",
        "NRA_000000001070_Eastbound-4"
    ],
    "NRA_000000001070_Westbound": [
        "NRA_000000001070_Westbound-1",
        "NRA_000000001070_Westbound-2",
        "NRA_000000001070_Westbound-3",
        "NRA_000000001070_Westbound-4"
    ],
    "NRA_000000001509_Southbound": [
        "NRA_000000001509_Southbound-1",
        "NRA_000000001509_Southbound-2",
        "NRA_000000001509_Southbound-3",
        "NRA_000000001509_Southbound-4"
    ],
    "NRA_000000001509_Northbound": [
        "NRA_000000001509_Northbound-1",
        "NRA_000000001509_Northbound-2",
        "NRA_000000001509_Northbound-3",
        "NRA_000000001509_Northbound-off-slip-1",
        "NRA_000000001509_Northbound-off-slip-2"
    ],
    "N4_Eastbound": [
        "N4-E1",
        "N4-E2",
        "N4-E3"
    ],
    "N4_Westbound": [
        "N4-W1",
        "N4-W2",
        "N4-W3"
    ],
    "N7_Eastbound": [
        "N7-E1",
        "N7-E2",
        "N7-E3"
    ],
    "N7_Westbound": [
        "N7-W1",
        "N7-W2",
        "N7-W3"
    ]
}

# Compile all induction loops into a single list
ALL_INDUCTION_LOOPS = [loop for group in INDUCTION_LOOPS.values() for loop in group]

