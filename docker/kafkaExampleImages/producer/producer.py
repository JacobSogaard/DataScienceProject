from kc import KafkaClient
from time import sleep

"""
 kafka client, python example
"""
print("start")
kClient = KafkaClient()
kClient.setup_env(['kafka1:9092', 'kafka2:9092', 'kafka3:9092'])
print("setup ok")


d = 0
print("variable initialized")


while True:
    data = {"prop A": "value A", "prop B": "value B", "iteration": str(d)}
    kClient.produce_to_env("testtopic", data)

    print(data)
    d += 1
    if d > 100000:
        break
