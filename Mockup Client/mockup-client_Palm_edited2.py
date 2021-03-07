import random
import json
import paho.mqtt.client as mqtt
import time

#// MAC, flr, rm, DMID, sensorID
#/**** DM *****/
#   // 7 Floor * 2 DM
#	// V : Flr_DMID_0.LineNo, A : Flr_DMID_1.LineNo, P : Flr_DMID_2.LineNo, AE : Flr_DMID_3.1
	
#/**** CT *****/
#	// 3 Floor * 2 Room * 6 Sensors
#	// A : flr_rm_4.senorId

#/**** PIR *****/
#	// 3 Floor * 2 Room * 1 Sensor
#	// (Room == 1) ? 1 : 0;	
	
def mockupDMdata(MAC, flr, DMID):
	msg = { "MAC": MAC,
	         "VL1": float(str(flr)+str(DMID)+"0.1"),
	         "VL2": float(str(flr)+str(DMID)+"0.2"),
			 "VL3": float(str(flr)+str(DMID)+"0.3"),
			 "AL1": float(str(flr)+str(DMID)+"1.1"),
			 "AL2": float(str(flr)+str(DMID)+"1.2"), 
			 "AL3": float(str(flr)+str(DMID)+"1.3"),
			 "P1": float(str(flr)+str(DMID)+"2.1"),
			 "P2": float(str(flr)+str(DMID)+"2.2"),
			 "P3": float(str(flr)+str(DMID)+"2.3"),
			 "AE": float(str(flr)+str(DMID)+"3.1")}
	#print("Publish: {}".format(msg))
	return msg

def mockupCTdata(MAC, flr, rm, sensor):
	msg = { "MAC": MAC, "s": sensor, "a": float(str(flr)+str(rm)+"4"+"."+str(sensor)) }
	# print("Publish: {}".format(msg))
	return msg

def mockupPIRdata(MAC, rm):
	if rm==1:
		msg = { "MAC": MAC, "status": 1}
	else:
		msg = { "MAC": MAC, "status": 0}
	# print("Publish: {}".format(msg))
	return msg

host = "10.80.4.14"
port = 1883
client = mqtt.Client()
client.username_pw_set(username="test1",password="Qwer1234")
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
	time.sleep(60)
				
"""
for _ in range(999): // infinite loop
	message = mockupCTdata(1,"AA-BB-CC-DD-EE")
	client.publish("/infbuu/IF/2/IF-204/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(2,"AA-BB-CC-DD-EE")
	client.publish("/infbuu/IF/2/IF-204/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(3,"AA-BB-CC-DD-EE")
	client.publish("/infbuu/IF/2/IF-204/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(4,"AA-BB-CC-DD-EE")
	client.publish("/infbuu/IF/2/IF-204/ct/plug",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(5,"AA-BB-CC-DD-EE")
	client.publish("/infbuu/IF/2/IF-204/ct/plug",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupDMdata("AA-BB-CC-DD-EE")
	client.publish("/infbuu/IF/2/IF-204/dm/air",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupPIRdata("AA-BB-CC-DD-EE")
	client.publish("/infbuu/IF/2/IF-204/pir",json.dumps(message))
	print("Publish: {}".format(message))
	print("-"*15)
	message = mockupCTdata(1,"11-22-33-44-55")
	client.publish("/infbuu/IF/3/IF-304/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(2,"11-22-33-44-55")
	client.publish("/infbuu/IF/3/IF-304/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(3,"11-22-33-44-55")
	client.publish("/infbuu/IF/3/IF-304/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(4,"11-22-33-44-55")
	client.publish("/infbuu/IF/3/IF-304/ct/plug",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(5,"11-22-33-44-55")
	client.publish("/infbuu/IF/3/IF-304/ct/plug",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupDMdata("11-22-33-44-55")
	client.publish("/infbuu/IF/3/IF-302/dm/air",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupPIRdata("11-22-33-44-55")
	client.publish("/infbuu/IF/3/IF-304/pir",json.dumps(message))
	print("Publish: {}".format(message))
	print("-"*15)
	message = mockupCTdata(1,"55-55-55-55-55")
	client.publish("/infbuu/IF/6/IF-605/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(2,"55-55-55-55-55")
	client.publish("/infbuu/IF/6/IF-605/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(3,"55-55-55-55-55")
	client.publish("/infbuu/IF/6/IF-605/ct/light",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(4,"55-55-55-55-55")
	client.publish("/infbuu/IF/6/IF-605/ct/plug",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupCTdata(5,"55-55-55-55-55")
	client.publish("/infbuu/IF/6/IF-605/ct/plug",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupDMdata("55-55-55-55-55")
	client.publish("/infbuu/IF/6/IF-605/dm/air",json.dumps(message))
	print("Publish: {}".format(message))
	message = mockupPIRdata("55-55-55-55-55")
	client.publish("/infbuu/IF/6/IF-605/pir",json.dumps(message))
	print("Publish: {}".format(message))
	time.sleep(60)
"""
