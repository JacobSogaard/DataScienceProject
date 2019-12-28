#!/usr/bin/env python3.7.2

from json import dumps
from json import loads
from kafka import KafkaProducer 
from kafka import KafkaConsumer
import confluent_kafka.admin
import threading

"""
kafka-python is best used with newer brokers (0.9+), but is backwards-compatible with older versions (to 0.8.0). 
Some features will only be enabled on newer brokers. For example, fully coordinated consumer groups – i.e., 
dynamic partition assignment to multiple consumers in the same group – requires use of 0.9+ kafka brokers. 
Supporting this feature for earlier broker releases would require writing and maintaining custom leadership election 
and membership / health check code (perhaps using zookeeper or consul). For older brokers, you can achieve something 
similar by manually assigning different partitions to each consumer instance with config management tools like chef, 
ansible, etc. This approach will work fine, though it does not support rebalancing on failures. 
See <https://kafka-python.readthedocs.io/en/master/compatibility.html> for more details.
"""

class KafkaClient():

    def __init__(self):
        self.kafka_admin = None
        self.__producer = None
        self.__consumers = {}
        self.__brokers = []
        self.__thread_pool = {}
        self.exit = False
    
    def get_consumer(self, key:str):
        if self.__consumers.__contains__(key):
            return self.__consumers[key]
        else:
            return None

    def setup_env(self, brokers:list): # TODO: Make a way to setup nessecary topics and groups, so that sub and pub auto-detects.
        self.__brokers = brokers
    
    def connect_admin(self, broker:str):
        self.kafka_admin = confluent_kafka.admin.AdminClient({
                    'bootstrap.servers':broker
            })

    def create_topic(self, topic:str, partitions:int, replicas:int):
        if topic not in self.kafka_admin.list_topics().topics.keys():
            self.kafka_admin.create_topics([confluent_kafka.admin.NewTopic(topic, partitions, replicas),])

    def delete_topics(self, topics:list):
        self.kafka_admin.delete_topics(topics)
        
    def subscribe_to_env(self, key:str, group:str, topic:str):
        self.subscribe(key, self.__brokers, group, topic)

    """
    Used for subscribing to a topic or to several topics.
    Automatically loads the message received into a JSON object.
    """
    def subscribe(self, key:str, brokers:list, group:str, topic:str, interval_ms=1000, offset='earliest'):
        consumer = KafkaConsumer(
                    topic,                                                  # the topic to consume from
                    bootstrap_servers=brokers,                              # list of brokers -> ['localhost:9092', ...]
                    auto_offset_reset=offset,                               # handles where the consumer restarts reading after breaking down or being turned off (can be set to lates or earliest)
                    enable_auto_commit=True,                                # makes sure the consumer commits its read offset every interval
                    auto_commit_interval_ms=interval_ms,                    # the interval to read at
                    group_id=group,                                         # group id
                    value_deserializer=lambda x: x.decode('utf-8')   
            )
        self.__consumers.update({key:consumer})
    
    def produce_to_env(self, topic:str, message):
        self.produce(topic, self.__brokers, message)

    """
    Used for publishing. Automatically dumps the message to JSON.
    Publishes to the set of brokers.
    """
    def produce(self, topic:str, brokers:list, message):
        if self.__producer is None:
            self.__producer = KafkaProducer(
                    bootstrap_servers=brokers,                              # list of brokers -> ['localhost:9092', ...]
                    value_serializer=lambda x: dumps(x).encode('utf-8')     # function that defines how the data should be serialized before published
            )
        self.__producer.send(topic, value=message)

    def list_topics(self):
        topics = list(self.kafka_admin.list_topics().topics.keys())
        if 'root' in topics:
            topics.remove('root')
        return topics
    
    def admin_list_topics(self):
        return list(self.kafka_admin.list_topics().topics.keys())

    def consume(self, key:str, rh):
        """
        consume receives a response handler (rh)
        starts the response handler in a separate thread (if that was truly possible in python)
        """
        def handle():
            for message in self.get_consumer(key):
                if self.exit == True:
                    pass
                rh.handle(message)    
        t = threading.Thread(target=handle)
        self.__thread_pool.update({key:t})
        t.start()
    
    def close(self):
        self.exit = True
        for key in list(self.__consumers.keys()):
            if self.__thread_pool.__contains__(key):
                self.__thread_pool[key].join()
                del self.__thread_pool[key]
            try:
                self.__consumers[key].close()
            except Exception:
                pass
            del self.__consumers[key]
        self.__consumers = {}