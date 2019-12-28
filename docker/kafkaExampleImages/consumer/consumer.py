from kc import KafkaClient

"""
 kafka client, python example
"""

kClient = KafkaClient()
kClient.setup_env(['kafka1:9092', 'kafka2:9092', 'kafka3:9092'])

kClient.subscribe_to_env('c1', 'group1', "testtopic")


class ResponseHandler:

    def handle(self, message):
        print("Received record from %s. Content: %s. At Time: %s" %
              (message.topic, message.value, message.timestamp))


rh = ResponseHandler()
kClient.consume('c1', rh)
