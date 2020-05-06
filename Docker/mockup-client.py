import random
import json
import paho.mqtt.client as mqtt

def mockupdata():
	return {"volt": random.randint(215, 220), "amp": random.randint(1, 3), "watt": random.randint(5, 10), "sid": 1, "nid": "be:e3:df:c7:62:c4"}

host = "mqtt.eclipse.org"
port = 1883
client = mqtt.Client()
client.connect(host,port)
for _ in range(10):
	message = mockupdata()
	client.publish("IFMON/digitalmeter",json.dumps(message))
	print("Publish: {}".format(message))