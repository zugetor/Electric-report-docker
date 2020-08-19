import random
import json
import paho.mqtt.client as mqtt
import time

def mockupDMdata(MAC, flr, DMID):
	msg = { "MAC": MAC,
	         "VL1": str(flr)+str(DMID)+"0.1",
	         "VL2": str(flr)+str(DMID)+"0.2",
			 "VL3": str(flr)+str(DMID)+"0.3",
			 "AL1": str(flr)+str(DMID)+"1.1",
			 "AL2": str(flr)+str(DMID)+"1.2", 
			 "AL3": str(flr)+str(DMID)+"1.3",
			 "P1": str(flr)+str(DMID)+"2.1",
			 "P2": str(flr)+str(DMID)+"2.2",
			 "P3": str(flr)+str(DMID)+"2.3",
			 "AE": str(flr)+str(DMID)+"3.1"}
	print("Publish: {}".format(msg))
	return msg

def mockupCTdata(MAC, flr, rm, sensor):
	msg = { "MAC": MAC, "s": sensor, "a": str(flr)+str(rm)+"4"+"."+str(sensor) }
	print("Publish: {}".format(msg))
	return msg

def mockupPIRdata(MAC, rm):
	if rm==1:
		msg = { "MAC": MAC, "status": "1"}
	else:
		msg = { "MAC": MAC, "status": "0"}
	print("Publish: {}".format(msg))
	return msg

host = "broker.mqttdashboard.com"
port = 1883
client = mqtt.Client()
client.connect(host,port)
for floor in range(1, 8):
	MAC1 = "F" + str(floor)
	if floor < 4:
		for room in range(1, 3):
			MAC2 = MAC1 + "-R" + str(room)
			for sensor in range(1, 7):
				MAC3 = MAC2 + "-S" + str(sensor) + "-DD-EE-FF"
				message = mockupCTdata(MAC3, floor, room, sensor)
				if sensor < 4 :
					client.publish("/infbuu/IF/"+str(floor)+"/IF-"+str(floor)+"0"+str(room)+"/ct/light",json.dumps(message))
				else :
					client.publish("/infbuu/IF/"+str(floor)+"/IF-"+str(floor)+"0"+str(room)+"/ct/plug",json.dumps(message))
				if sensor < 2:
					message = mockupPIRdata(MAC3, room)
					client.publish("/infbuu/IF/"+str(floor)+"/IF-"+str(floor)+"0"+str(room)+"/pir",json.dumps(message))
	message = mockupDMdata(MAC1+"-D1"+"-CC-DD-EE-FF", floor, 1)
	client.publish("/infbuu/IF/"+str(floor)+"/IF-"+str(floor)+"03/dm/air",json.dumps(message))
	message = mockupDMdata(MAC1+"-D2"+"-CC-DD-EE-FF", floor, 2)
	client.publish("/infbuu/IF/"+str(floor)+"/IF-"+str(floor)+"03/dm/all",json.dumps(message))






