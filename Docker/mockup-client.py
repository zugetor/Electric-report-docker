import random
import json
import paho.mqtt.client as mqtt
import time

def mockupdata(x):
	return {"volt": random.randint(215, 220), "amp": random.randint(1, 3), "watt": random.randint(5, 10), "sid": x, "nid": "be:e3:df:c7:62:c4"}

while 1==1:
	host = "broker.mqttdashboard.com"
	port = 1883
	client = mqtt.Client()
	client.connect(host,port)
	message = mockupdata(1)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(2)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(3)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(4)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(5)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(6)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(7)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(8)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(9)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupdata(10)
	client.publish("electric/light",json.dumps(message))
	print("Publish: {}".format(message))
	time.sleep(600)