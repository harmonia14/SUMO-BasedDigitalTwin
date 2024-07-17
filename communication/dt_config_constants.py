import json, pathlib

#KAFKA
KAFKA_VERSION = (7,6,1)

PORT1 = ':9092'
PORT2 = ':9093'
BROKER1_IP = 'localhost'
ENTERPRISE_IP = 'localhost'

#For multiple broker set up
# BROKER2_IP = '' 
# BROKER3_IP = '' 
# PORT3 = ':9094'
# BROKER_EP = [BROKER1_IP+PORT1,BROKER2_IP+PORT2,BROKER3_IP+PORT3]

BROKER_EP = [BROKER1_IP] #single broker setup
ENTERPRISE_EP = ENTERPRISE_IP+PORT2

ENCODING = (lambda v: json.dumps(v).encode('utf-8'))
DECODING = (lambda v: json.loads(v))
TOPICS = ["inductive_loops","probe_vehicles","toll_bridge_cameras","motorway_cameras"]
ENTERPRISE_TOPICS = ["enterprise_probe_vehicles","enterprise_motorway_cameras","enterprise_toll_bridge_cameras"]
TOPIC_LOOKUP = { "enterprise_probe_vehicles":"probe_vehicles", 
                "enterprise_motorway_cameras":"motorway_cameras",
                "enterprise_toll_bridge_cameras":"toll_bridge_cameras"}

#SUMO
# 
# 09:00 - 09:15：33300
# 19:00 - 19:15：69300
# 22:00 - 22:15：80100
# SIMULATION_DURATION = 0 + 3600 #3600 seconds = 1 hour
SIMULATION_DURATION = 79500 + 0.5
pathToConfigs = '../configuration/'
currentPath = str(pathlib.Path().resolve())
sumoBinary = "sumo-gui"
SUMO_CMD = [sumoBinary, 
            "-c", currentPath+"/"+pathToConfigs+"/M50_simulation_physical_entity.sumo.cfg"]

truckVehicleTypes = ["CAT4", "CAT2", "HDT"]
passengerVehicleTypes = ["CAV4", "CAV2", "HDC"]
autonomousVehicles = ["CAV4", "CAV2", "CAT4", "CAT2"] #equates to 20% of vehicles

#Camera locations represent real cameras located on M50 ref: https://traffic.tii.ie/
CAMERA_LOOKUP = {"M50(S) After J9 (N7)": 
                {
                    "coordinates": "53.31353873270574,-6.363575673942173", 
                    "northEdges": "345616204#1.655",
                    "southEdges": "75259388-AddedOffRampEdge",
                    "partition": int(0)
                },
                "M50(S) At J9 (N7)": 
                {
                    "coordinates": "53.32105761034455,-6.3702774491561724",
                    "northEdges": "4937552#1-AddedOnRampEdge,22941416,4937552",
                    "southEdges": "gneE0,11955830",
                    "partition": int(1)
                }, 
                "M50(S) 1.4km Before J9 (N7)":  
                {
                    "coordinates": "53.33335994735108,-6.382773162408997",
                    "northEdges": "360361373.981",
                    "southEdges": "48290550.1878",
                    "partition": int(2)
                 }, 
                "M50(N) 0.6km Before J7 (N4)": 
                {
                    "coordinates": "53.34727008589719,-6.386567333598459", 
                    "northEdges": "360361373.2643",
                    "southEdges": "48290550 ",   
                    "partition": int(3)
                },
                "M50(N) Before J7 (N4)": 
                {
                    "coordinates": "53.35269470355068,-6.38544365135953",
                    "northEdges": "492226831,4414080#0.187",
                    "southEdges": "61047111,492229071,gneJ14,61047111.165", 
                    "partition": int(4)
                },
                "M50(S) At J7 (N4)": 
                {
                    "coordinates": "53.35885146892749,-6.3834896661669625", 
                    "northEdges": "4414080#0.756.47,71324924,4414080#1-AddedOnRampEdge",
                    "southEdges": "16403446,4402297", 
                    "partition": int(5)
                },
                "M50(S) Before West Link":         
                {
                    "coordinates": "53.363722242995145,-6.382086740810554", 
                    "northEdges": "4414080#1-AddedOnRampEdge.343",
                    "southEdges": "106130759.2098", 
                    "partition": int(6)
                },
                "M50(S) Before ORT Gantry": 
                {
                    "coordinates": "53.37334705444544,-6.373142233357861" ,
                    "northEdges": "gneE7,gneE6",
                    "southEdges": "106130759.791", 
                    "partition": int(7)
                }
}

TOLL_BRIDGE = {
    "coordinates": "53.3617409,-6.3829509" ,
    "northEdges": "4414080#1-AddedOnRampEdge.343",
    "southEdges": "106130759.2098", 
}

NRA_000000001503_Northbound = [
        "NRA_000000001503_Northbound-1", 
        "NRA_000000001503_Northbound-2", 
        "NRA_000000001503_Northbound-3", 
        "NRA_000000001503_Northbound-4"
        ]

NRA_000000001503_Southbound = [
        "NRA_000000001503_Southbound-1", 
        "NRA_000000001503_Southbound-2", 
        "NRA_000000001503_Southbound-3", 
        "NRA_000000001503_Southbound-4"
        ]

# Additional induction loops
NRA_000000001508_Southbound = [
    "NRA_000000001508_Southbound-1",
    "NRA_000000001508_Southbound-2",
    "NRA_000000001508_Southbound-3",
    "NRA_000000001508_Southbound-4"
]

NRA_000000001508_Northbound = [
    "NRA_000000001508_Northbound-1",
    "NRA_000000001508_Northbound-2",
    "NRA_000000001508_Northbound-3",
    "NRA_000000001508_Northbound-4"
]

NRA_000000020047_Westbound = [
    "NRA_000000020047_Westbound-1",
    "NRA_000000020047_Westbound-2",
    "NRA_000000020047_Westbound-3",
    "NRA_000000020047_Westbound-Bus-Lane"
]

NRA_000000020047_Eastbound = [
    "NRA_000000020047_Eastbound-1",
    "NRA_000000020047_Eastbound-2",
    "NRA_000000020047_Eastbound-3",
    "NRA_000000020047_Eastbound-Bus-Lane"
]

NRA_000000001070_Eastbound = [
    "NRA_000000001070_Eastbound-1",
    "NRA_000000001070_Eastbound-2",
    "NRA_000000001070_Eastbound-3",
    "NRA_000000001070_Eastbound-4"
]

NRA_000000001070_Westbound = [
    "NRA_000000001070_Westbound-1",
    "NRA_000000001070_Westbound-2",
    "NRA_000000001070_Westbound-3",
    "NRA_000000001070_Westbound-4"
]

NRA_000000001509_Southbound = [
    "NRA_000000001509_Southbound-1",
    "NRA_000000001509_Southbound-2",
    "NRA_000000001509_Southbound-3",
    "NRA_000000001509_Southbound-4"
]

NRA_000000001509_Northbound = [
    "NRA_000000001509_Northbound-1",
    "NRA_000000001509_Northbound-2",
    "NRA_000000001509_Northbound-3",
    "NRA_000000001509_Northbound-off-slip-1",
    "NRA_000000001509_Northbound-off-slip-2"
]

N4_Eastbound = [
    "N4-E1",
    "N4-E2",
    "N4-E3"
]

N4_Westbound = [
    "N4-W1",
    "N4-W2",
    "N4-W3"
]

N7_Eastbound = [
    "N7-E1",
    "N7-E2",
    "N7-E3"
]

N7_Westbound = [
    "N7-W1",
    "N7-W2",
    "N7-W3"
]

LOOPS = [
    NRA_000000001503_Northbound,
    NRA_000000001503_Southbound, 
    NRA_000000001508_Southbound, 
    NRA_000000001508_Northbound,
    NRA_000000020047_Westbound,
    NRA_000000020047_Eastbound,
    NRA_000000001070_Eastbound,
    NRA_000000001070_Westbound,
    NRA_000000001509_Northbound,
    NRA_000000001509_Southbound,
    N4_Eastbound,
    N4_Westbound,
    N7_Eastbound,
    N7_Westbound
]

LOOP_COORDINATES = {
    'NRA_000000001503': (-6.38715, 53.34553),
    'NRA_000000001508': (-6.37144, 53.37482),
    'NRA_000000020047': (-6.39533, 53.3555),
    'NRA_000000001070': (-6.37874, 53.31607),
    'NRA_000000001509': (-6.36333, 53.31346),
    'N4': (-6.372299, 53.355114),
    'N7': (-6.356772, 53.322107)
}