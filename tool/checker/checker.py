from notify import linenotify
from extensions import getConfig
from db import MySQL, Query
from jqqb_evaluator.evaluator import Evaluator
from time import time
import datetime, pytz, reg, json
from timeout import timeout

class dbHandler():
	def __init__(self):
		self.mysql = MySQL()
		self.query = Query()
		cfg = getConfig()
		self.mysql.init_cfg(cfg)
		self._con = self.mysql.get_connection()

	def getQuery(self):
		return self.query

	def getallMAC(self,table):
		infQuery = self.query.getInfQuery()
		result = infQuery('SELECT distinct("MAC") as MAC FROM "{}";'.format(table))
		return result.raw

	def getallSensor(self,table,mac):
		infQuery = self.query.getInfQuery()
		param = {"mac":mac}
		result = infQuery('SELECT s,topic FROM "{}" WHERE MAC=$mac;'.format(table),bind_params=param)
		return result.raw

	def getallTopic(self,table,mac):
		infQuery = self.query.getInfQuery()
		result = infQuery('SELECT topic,MAC,status FROM "{}"'.format(table))
		for sensor in result.raw["series"][0]["values"]:
			smac = sensor[2]
			topic = sensor[1]
			if(smac == mac):
				return ['topic', topic, 'MAC', smac]

	def getLastCT(self,sid,_type="ct"):
		infQuery = self.query.getInfQuery()
		param = {"s":sid}
		result = infQuery('SELECT a FROM "{}" WHERE s=$s LIMIT 1'.format(_type),bind_params=param)
		return result.raw

	def getLastPIR(self,mac,_type="pir"):
		infQuery = self.query.getInfQuery()
		param = {"mac":mac}
		result = infQuery('SELECT status FROM "{}" WHERE MAC=$mac LIMIT 1'.format(_type),bind_params=param)
		return result.raw

def getTimeZone():
	cfg = getConfig()
	return cfg.TIME_ZONE

def getTable():
	cfg = getConfig()
	return cfg.INF_TABLE

def getTemplate():
	cfg = getConfig()
	return cfg.Nofify_Template

def _topic2type(topic):
	topic = topic.split("/")
	if len(topic) % 2 != 0:
		return topic[-1], topic[-2]
	else:
		return topic[-1],topic[-1]

def getINFVal(raw):
	if len(raw["series"]) > 0:
		return raw["series"][0]["values"][0][1]
	return 0

def checkRule():
	db = dbHandler()
	query = db.getQuery()

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
							tmp["pir"] += getINFVal(pir_tmp)
						else:
							ct_tmp = db.getLastCT(s["inf_id"],s["inf_type"])
							tmp[s["inf_name"]] += getINFVal(ct_tmp)
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
					linenotify(m,token["ntoken"])

def checkSchedule():
	db = dbHandler()
	query = db.getQuery()

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

	alltype = query.getAllType()
	typelst = {}
	for _type in alltype:
		typelst[_type["inf_name"]] = _type["tid"]
	for t in getTable():
		allmac = db.getallMAC(t)
		res = {"MAC":"","data":[]}
		for i in allmac['series'][0]["values"]:
			res["MAC"] = i[1]
			sensor = db.getallSensor(t,i[1])
			if len(sensor['series']) > 0:
				slst = [[i[1],i[2]] for i in sensor['series'][0]["values"]]
				slst = list(set(tuple(sub) for sub in slst))
				for s in slst:
					etype,stype = _topic2type(s[1])
					if etype in typelst.keys():
						res["data"].append([ "{}({})-{}".format(etype,stype,int(s[0])), int(s[0]), t, typelst[etype] ])
			else:
				topic = db.getallTopic(t,i[1])
				etype,stype = _topic2type(topic[1])
				if etype in typelst.keys():
					res["data"].append([ "{}({})-{}".format(etype,stype,int(1)), 1, t, typelst[etype] ])
			query.addnewSensor(res)
			res = {"MAC":"","data":[]}