from dt_sensor_data_generator import (getProbeVehicleIDs, getCamVehicleIDs, getTollVehicleIDs, 
                         getInductionLoopVehicleIDs, getProbeData, getCamData, 
                         getTollData, getLoopData)
from dt_config_constants import (CAMERA_LOOKUP, LOOPS, BROKER_EP, ENTERPRISE_EP, 
                       ENTERPRISE_TOPICS, KAFKA_VERSION)
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewPartitions, NewTopic
from kafka.errors import TopicAlreadyExistsError
import traci

# Functions for working with kafka topics and partitions

def createTopics(topics, broker):
    admin_client = KafkaAdminClient(bootstrap_servers=broker, api_version=KAFKA_VERSION)
    
    existing_topics = admin_client.list_topics()
    
    new_topics = [
        NewTopic(name=topic.name, num_partitions=topic.num_partitions, replication_factor=topic.replication_factor)
        for topic in topics if topic.name not in existing_topics
    ]
    
    if new_topics:
        try:
            admin_client.create_topics(new_topics=new_topics, validate_only=False)
            print(f"Created topics in {broker}")
            for topic in new_topics:
                print(topic.name)
                print("partitions:", get_partitions_number(broker, topic.name))
        except TopicAlreadyExistsError as e:
            print(f"Topic already exists: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No new topics to create")

def appendTopics(topics, numPartitions, topic_name):
    topics.append(NewTopic(name=topic_name, num_partitions=numPartitions, replication_factor=1))
    return topics

def delete_topics(topics, broker):
    admin_client = KafkaAdminClient(bootstrap_servers=broker, api_version=KAFKA_VERSION)
    admin_client.delete_topics(topics=topics)
    print("Deleted topics")

def get_partitions_number(broker, topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker,
        api_version=KAFKA_VERSION
    )
    partitions = consumer.partitions_for_topic(topic)
    return len(partitions)

def initTopics():
    for topic in list(KafkaConsumer(bootstrap_servers=BROKER_EP, api_version=KAFKA_VERSION).topics()):
         delete_topics([topic], BROKER_EP)
        
    for topic in list(KafkaConsumer(bootstrap_servers=ENTERPRISE_EP, api_version=KAFKA_VERSION).topics()):
        delete_topics([topic], ENTERPRISE_EP) 
    topics = []
    enterprise_topics = []
    topics = appendTopics(topics, 14, "inductive_loops")
    topics = appendTopics(topics, 8, "motorway_cameras")
    topics = appendTopics(topics, 2, "toll_bridge_cameras")
    topics = appendTopics(topics, 10, "probe_vehicles")  
    for topic in ENTERPRISE_TOPICS:
        enterprise_topics = appendTopics(enterprise_topics, 1, topic)
    createTopics(topics, BROKER_EP)  
    createTopics(enterprise_topics, ENTERPRISE_EP)

def getPartition(msg):
    if msg.topic == 'enterprise_motorway_cameras':
        return CAMERA_LOOKUP[msg.value['sensor_id']]["partition"]
    return None

def createNewPartitions(server, topic, partitions):
    admin_client = KafkaAdminClient(bootstrap_servers=server, api_version=KAFKA_VERSION)
    topic_partitions = {}
    topic_partitions[topic] = NewPartitions(total_count=partitions)
    admin_client.create_partitions(topic_partitions)

# Functions for sending data to kafka brokers

def sendProbeData(vehicleIDs, producer, topic, allow_new_vehicles):
    probes = getProbeVehicleIDs(vehicleIDs, allow_new_vehicles)
    for vehID in probes:
        data = getProbeData(vehID, allow_new_vehicles)
        if data:
            sendData(data, producer, topic, None, allow_new_vehicles)

def sendCamData(vehicleIDs, producer, topic, allow_new_vehicles):
    for cam in CAMERA_LOOKUP:
        camVehicles = getCamVehicleIDs(cam, vehicleIDs, allow_new_vehicles)
        for vehID in camVehicles:
            data = getCamData(vehID, cam, allow_new_vehicles)
            if data:
                sendData(data, producer, topic, None, allow_new_vehicles)

def sendTollData(vehicleIDs, producer, topic, allow_new_vehicles):
    x, y = traci.simulation.convertGeo(float("-6.3829509"), float("53.3617409"), fromGeo=True)
    p1 = [x, y]
    tollVehicles = getTollVehicleIDs(vehicleIDs, p1, allow_new_vehicles)
    for vehID in tollVehicles:
        data = getTollData(vehID, p1, allow_new_vehicles)
        if data:
            sendData(data, producer, topic, None, allow_new_vehicles)

def sendInductionLoopData(vehicleIDs, producer, topic, allow_new_vehicles):
    for loop_group in LOOPS:
        for loop_id in loop_group:
            data_list = getLoopData(loop_id, allow_new_vehicles)
            for data in data_list:
                if data:
                    sendData(data, producer, topic, None, allow_new_vehicles)
                    
def sendData(data, producer, topic, partition, allow_new_vehicles):
    if allow_new_vehicles or (data['vehicle_id'] in traci.vehicle.getIDList()):
        producer.send(topic=topic, value=data, partition=partition)