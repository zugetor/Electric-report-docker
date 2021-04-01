from notify import linenotify
from extensions import getConfig
from db import MySQL, MongoDB, Query
from jqqb_evaluator.evaluator import Evaluator
from time import time
import datetime, pytz, reg, json
from timeout import timeout

class dbHandler():
	def __init__(self):
		self.mysql = MySQL()
		self.mongo = MongoDB()
		self.query = Query()
		cfg = getConfig()
		self.mysql.init_cfg(cfg)
		self.mongo.init_cfg(cfg)
		self._con = self.mysql.get_connection()
		self._client = self.mongo.get_client()
		self.query.init_db(self._con, self._client)
		self._db = self._client[cfg.MONGODB_COLLECTION]

	def getQuery(self):
		return self.query

	def getallMAC(self,table): #/
		allmac = self._db[table].find().distinct("message.MAC")
		return allmac

	def getallSensor(self,table,mac): #/
		result = self._db[table].find({
			"$and": [
				{"message.MAC": mac},
				{"message.s" : {"$exists" : True}}
			]
		})
		alltopic = result.distinct("topic")
		allnum = result.distinct("message.s")
		res = []
		for s in allnum:
			for topic in alltopic:
				res.append({
					"s" : s,
					"topic" : topic
				})
		return res

	def getallTopic(self,table,mac): #/
		result = self._db[table].find_one({
			"$or": [
				{"message.MAC": mac},
				{"message.s" : mac}
			]
		})
		return ['topic', result["topic"], 'MAC', result["message"]["MAC"]]

	def getLastCT(self,sid,_type="ct"):
		createdAt = 0
		res = {}
		for t in self.getTable({"sensor_type":_type}):
			rawCT = self._db[t].find({"message.s": sid}).sort("created_at", -1).limit(1)
			for CT in rawCT:
				if(CT["created_at"] > createdAt):
					res = CT
					createdAt = CT["created_at"]
		return res

	def getLastPIR(self,mac,_type="pir"):
		createdAt = 0
		res = {}
		for t in self.getTable({"sensor_type":_type}):
			rawPIR = self._db[t].find({"message.MAC": mac}).sort("created_at", -1).limit(1)
			for PIR in rawPIR:
				if(PIR["created_at"] > createdAt):
					res = PIR
					createdAt = PIR["created_at"]
		return res

	def getTable(self,devFind={}): #/
		res = []
		for _type in self._db["iot_type"].find(devFind):
			name = _type["sensor_type"] 
			if(_type["device_type"] != ''):
				name = name + "_" + _type["device_type"]
			res.append(name)
		return res

def getTimeZone():
	cfg = getConfig()
	return cfg.TIME_ZONE

def getTemplate():
	cfg = getConfig()
	return cfg.Nofify_Template

def _topic2type(topic):
	topic = topic.split("/")
	if len(topic) % 2 != 0:
		return topic[-1], topic[-2]
	else:
		return topic[-1],topic[-1]

def checkRule():
	db = dbHandler()
	query = db.getQuery()
	print("Checking Rule")
	daylst = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

	allrule = query.getRule()
	_rtype = query.getAllType()
	for rule in allrule:
		rule_name = rule["rname"]
		rjson = rule["rjson"]

		rule_json = json.loads(rjson)
		evaluator = Evaluator(rule_json)

		weekday = datetime.datetime.today().weekday()
		tz = pytz.timezone(getTimeZone())
		now1 = datetime.datetime.now(tz)
		now_date = now1.strftime("%d/%m/%Y")

		objects = []

		all_room_list = query.all_room_list()
		for building in all_room_list:
			bname = building["bname"]
			for floor in building["floor"]:
				fname = floor["fname"]
				for room in floor["room"]:
					rname = room["rname"]
					rstatus = room["rstatus"]
					tmp = {'dow': daylst[weekday+1], "time":now1.hour,"date":now_date,
							"room":[rname,rstatus],"floor":fname,"building":bname}
					rsensor = query.getRoomSensor(rname)

					for rtype in _rtype:
						tmp[rtype["inf_name"]] = 0

					for s in rsensor:
						if s["inf_type"] == "pir":
							pir_tmp = db.getLastPIR(s["bomac"])
							if(pir_tmp != {}):
								tmp["pir"] += pir_tmp["message"]["status"]
						else:
							ct_tmp = db.getLastCT(s["inf_id"],s["inf_type"])
							if(ct_tmp != {}):
								tmp[s["inf_name"]] += ct_tmp["message"]["a"]
					#print(tmp)
					objects.append(tmp)

		matched = evaluator.get_matching_objects(objects)

		tokens = query.getToken()
		all_messages = []
		line_message = ""
		for idx,match in enumerate(matched):
			match["status"] = "Free" if match["room"][1] == "0" else "Reserved"
			match["room"] = match["room"][0]
			match["rname"] = rule_name
			line_message += getTemplate().format(**match) + ("-" * 10) + "\n"
			if idx % 3 == 0:
				all_messages.append(line_message)
				line_message = ""
		all_messages.append(line_message)

		for m in all_messages:
			for token in tokens:
				if token["ntime"] + datetime.datetime.timestamp(token["nlast_time"]) <= time():
					linenotify(m,token["ntoken"],True,query)

def checkSchedule():
	db = dbHandler()
	query = db.getQuery()
	print("Checking Schedule")
	allroom = query.roomWithBPrefix()
	if len(allroom) > 0:
		burl = allroom[0]["burl"]
		allSchedule = reg.getAllSchedule(burl)
		tz = pytz.timezone(getTimeZone())
		now1 = datetime.datetime.now(tz)
		today = datetime.date.today()
		for room in allroom:
			if room["burl"] != burl:
				burl = room["burl"]
				allSchedule = reg.getAllSchedule(burl)
			roomSchedule = allSchedule.loc[(allSchedule['ROOM'] == room["rname"]) &
							(allSchedule['Day/Time'] == today),"{}:00-{}:00".format(now1.hour,now1.hour+1)]
			if len(roomSchedule) > 0 and roomSchedule[roomSchedule.index[0]]:
				query.UpdateRoomStatue(1,room["rname"])
			else:
				query.UpdateRoomStatue(0,room["rname"])

def updateNewsensor():
	db = dbHandler()
	query = db.getQuery()
	print("Checking Sensor")
	alltype = query.getAllType()
	typelst = {}
	for _type in alltype:
		typelst[_type["inf_name"]] = _type["tid"]
	for t in db.getTable():
		allmac = db.getallMAC(t)
		res = {"MAC":"","data":[]}
		for i in allmac:
			res["MAC"] = i
			sensor = db.getallSensor(t,i)
			if len(sensor) > 0: # sensor > 0 when s and topic found
				for s in sensor:
					etype,stype = _topic2type(s["topic"])
					if etype in typelst.keys():
						res["data"].append([ "{}({})-{}".format(etype,stype,int(s["s"])), int(s["s"]), t, typelst[etype] ])
			else:
				topic = db.getallTopic(t,i)
				etype,stype = _topic2type(topic[1])
				if etype in typelst.keys():
					res["data"].append([ "{}({})-{}".format(etype,stype,int(1)), 1, t, typelst[etype] ])
			query.addnewSensor(res)
			res = {"MAC":"","data":[]}