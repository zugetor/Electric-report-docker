import random
import json
import paho.mqtt.client as mqtt

def mockupdata():
	return { "MAC": "00-11-22-33-44-55", "VL1": random.randint(215, 220), "VL2": random.randint(215, 220),
			 "VL3": random.randint(215, 220), "AL1": random.randint(5, 10), "AL2": random.randint(5, 10), 
			 "AL3": random.randint(5, 10),"P1": random.randint(10, 100), "P2": random.randint(10, 100),
			  "P3": random.randint(10, 100), "AE": random.randint(10, 100)}

def mockupdata1():
	return { "MAC": "AA-BB-CC-DD-EE-FF", "s1": random.randint(5, 10), "s2": random.randint(5, 10),
			 "s3": random.randint(5, 10), "s4": random.randint(5, 10), "s5": random.randint(5, 10),
			 "s6": random.randint(5, 10) }

def mockupdata2():
	return { "MAC": "GG-HH-II-JJ-KK-LL", "status": random.randint(0, 1)}

host = "broker.mqttdashboard.com"
port = 1883
client = mqtt.Client()
client.connect(host,port)
for _ in range(10):
	message = mockupdata()
	client.publish("/infbuu/IF/1/IF-102/dm/air",json.dumps(message))
	message = mockupdata1()
	client.publish("/infbuu/IF/11/IF-204/ct/plug",json.dumps(message))
	message = mockupdata2()
	client.publish("/infbuu/IF/11/IF-204/pir",json.dumps(message))
	print("Publish: {}".format(message))