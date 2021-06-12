import reg
import json
from cache import timed_lru_cache

class Query:

	def __init__(self):
		self._conn = None
		self._client = None
		self.notification = self.Notification(self)
		self.logs = self.Logs(self)
		self.building = self.Building(self)
		self.dashboard = self.Dashboard(self)
		self.sensor = self.Sensor(self)
		self.board = self.Board(self)
		self.user = self.User(self)
		self.rule = self.Rule(self)

	def init_db(self,conn,client):
		self._conn = conn
		self._client = client

	def _newCursor(self):
		self._conn.ping()
		return self._conn.cursor()

	def _CloseCursor(self,cursor):
		cursor.close()
		return self._conn.close()

	def fetchAll(self,sql,param=None):
		_cur = self._newCursor()
		if param:
			_cur.execute(sql,param)
		else:
			_cur.execute(sql)
		res = _cur.fetchall()
		self._CloseCursor(_cur)
		return res

	def fetchOne(self,sql,param=None):
		_cur = self._newCursor()
		if param:
			_cur.execute(sql,param)
		else:
			_cur.execute(sql)
		res = _cur.fetchone()
		self._CloseCursor(_cur)
		return res

	def execute(self,sql,param=None):
		_cur = self._newCursor()
		if param:
			res = _cur.execute(sql,param)
		else:
			res = _cur.execute(sql)
		self._CloseCursor(_cur)
		return res
	
	class Dashboard:

		def __init__(self,query):
			self.query = query

		@timed_lru_cache(30)
		def dashboard_list(self,data,unit,startTime,endTime,graphType):
			_cur = self.query._newCursor()
			sensorType = ["light","air","plug","all"]
			dmType = ["VL1","VL2","VL3","AL1","AL2","AL3","P1","P2","P3","AE"]
			tmp=[] #for compare and separate graph
			tmp2={'name':"",'ct':[{}],'volt':[{},{},{}],'amp':[{},{},{}],'watt':[{},{},{}],'ae':[{}]} #for combine graph
			ct=[] #collect data and query one time for combine
			dm=[] #collect data and query one time for combine
			nameCombine=""
			sensorTypeCombine=[];
			for i in range(len(data)):
				name = data[i]['name']
				if(data[i]['type'][0:2] == "ct"):
					nameCombine+=data[i]['name']+", "
					tmp.append({'name':name,'ct':[{}]})
					_cur.execute("select s.inf_id,bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid where s.sid = %s",(data[i]['id']))
					sensor = _cur.fetchall()
					ct.append(sensor[0])
					if(len(sensor) != 0):
						pipeline = [{"$match": {"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },"message.s":sensor[0]['inf_id'],"message.MAC":sensor[0]['bomac']}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message.a"}}},{ "$sort": { '_id': 1 }},{"$addFields": { "y":{"$round":["$y",2]},"t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{ "$unset": "_id" }]
						result = list(self.query._client.iot_data[data[i]['type']].aggregate(pipeline))
						if(len(result)>0):
							tmp[i]['ct'][0].update({data[i]['type']:{'name':'','values':[]}})
							tmp[i]['ct'][0][data[i]['type']].update({'name':name+"_"+data[i]['type']})
							tmp[i]['ct'][0][data[i]['type']]['values'].extend(result)
				if(data[i]['type'][0:2] == "dm"):
					nameCombine+=data[i]['name']+", "
					tmp.append({'name':name,'volt':[{},{},{}],'amp':[{},{},{}],'watt':[{},{},{}],'ae':[{}],'ct':[{}]})
					_cur.execute("select bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid where s.sid = %s",(data[i]['id']))
					sensor = _cur.fetchall()
					dm.append(sensor[0])
					if(len(sensor) != 0):
						for x in dmType:
							pipeline = [{"$match": {"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },"message.MAC":sensor[0]['bomac']}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message."+x}}},{ "$sort": { '_id': 1 }},{"$addFields": {"y":{"$round":["$y",2]}, "t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{ "$unset": "_id" }]
							result = list(self.query._client.iot_data[data[i]['type']].aggregate(pipeline))
							if(len(result)>0):
								if(x[0:2]=="VL"):
									tmp[i]['volt'][int(x[-1])-1].update({data[i]['type']:{'name':'','values':[]}})
									tmp[i]['volt'][int(x[-1])-1][data[i]['type']].update({'name':name+"_"+x+"_"+data[i]['type']})
									tmp[i]['volt'][int(x[-1])-1][data[i]['type']]['values'].extend(result)
								elif(x[0:2]=="AL"):
									tmp[i]['amp'][int(x[-1])-1].update({data[i]['type']:{'name':'','values':[]}})
									tmp[i]['amp'][int(x[-1])-1][data[i]['type']].update({'name':name+"_"+x+"_"+data[i]['type']})
									tmp[i]['amp'][int(x[-1])-1][data[i]['type']]['values'].extend(result)
								elif(x[0:1]=="P"):
									tmp[i]['watt'][int(x[-1])-1].update({data[i]['type']:{'name':'','values':[]}})
									tmp[i]['watt'][int(x[-1])-1][data[i]['type']].update({'name':name+"_"+x+"_"+data[i]['type']})
									tmp[i]['watt'][int(x[-1])-1][data[i]['type']]['values'].extend(result)
								elif(x[0:2]=="AE"):
									tmp[i]['ae'][0].update({data[i]['type']:{'name':'','values':[]}})
									tmp[i]['ae'][0][data[i]['type']].update({'name':name+"_"+x+"_"+data[i]['type']})
									tmp[i]['ae'][0][data[i]['type']]['values'].extend(result)
				if(data[i]['type'] == "room" or data[i]['type'] == "floor" or data[i]['type'] == "building"):
					sensorTypeCombine.append(data[i]['sensorType'])
					if(data[i]['type'] == "room"):
						nameCombine+=data[i]['name']+", "
						_cur.execute("select bo.bomac from board as bo inner join room as r on bo.rid=r.rid where r.rid = %s",(data[i]['id']))
					if(data[i]['type'] == "floor"): 
						nameCombine+='floor '+data[i]['name']+", "
						name = 'floor '+data[i]['name']
						_cur.execute("select bo.bomac from board as bo inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid where f.fid = %s",(data[i]['id']))
					if(data[i]['type'] == "building"):
						nameCombine+=data[i]['name']+", "
						_cur.execute("select bo.bomac from board as bo inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid inner join building as b on b.bid=f.bid where b.bid = %s",(data[i]['id']))
					tmp.append({'name':name,'volt':[{},{},{}],'amp':[{},{},{}],'watt':[{},{},{}],'ae':[{}],'ct':[{}]})
					sensor = _cur.fetchall()
					if(len(sensor) != 0):
						bomac = []
						for index in range(len(sensor)):
							dm.append(sensor[index])
							bomac.append(sensor[index]['bomac'])
						for x in dmType:
							pipeline = [{"$match": {"message.MAC":{"$in":bomac },"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message."+x},}},{ "$sort": { '_id': 1 } },{"$addFields": { "y":{"$round":["$y",2]},"t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{"$unset": "_id" }]
							if data[i]['sensorType'] == "allType":
								lookupPipeline = [{"$match": {"message.MAC":{"$in":bomac },"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message."+x},}},{ "$sort": { '_id': 1 } },{"$addFields": { "t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{"$match": {"$expr":{"$eq":["$t","$$tt"]}}},{"$unset": "_id" }]
								pipeline = [{"$match": {"message.MAC":{"$in":bomac },"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message."+x},}},{ "$sort": { '_id': 1 } },{"$addFields": { "t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{"$unset": "_id" },
								{"$lookup":{"from": "dm_plug","let":{"tt" : "$t"},"pipeline": lookupPipeline,"as": "dm_plug"}},
								{"$lookup":{"from": "dm_light","let":{"tt" : "$t"},"pipeline": lookupPipeline,"as": "dm_air"}},
								{"$lookup":{"from": "dm_all","let":{"tt" : "$t"},"pipeline": lookupPipeline,"as": "dm_all"}},
								{"$project":{"t":1,"y":{"$round":[{"$avg":[{"$first":"$dm_light.y"},{"$first":"$dm_plug.y"},{"$first":"$dm_all.y"},"$y"]},2]}}}
								]
								result = list(self.query._client.iot_data["dm_air"].aggregate(pipeline))
								if(len(result)>0):
									if(x[0:2]=="VL"):
										tmp[i]['volt'][int(x[-1])-1].update({"allType":{'name':'','values':[]}})
										tmp[i]['volt'][int(x[-1])-1]["allType"].update({'name':name+"_"+x+"_allType"})
										tmp[i]['volt'][int(x[-1])-1]["allType"]['values'].extend(result)
									elif(x[0:2]=="AL"):
										tmp[i]['amp'][int(x[-1])-1].update({"allType":{'name':'','values':[]}})
										tmp[i]['amp'][int(x[-1])-1]["allType"].update({'name':name+"_"+x+"_allType"})
										tmp[i]['amp'][int(x[-1])-1]["allType"]['values'].extend(result)
									elif(x[0:1]=="P"):
										tmp[i]['watt'][int(x[-1])-1].update({"allType":{'name':'','values':[]}})
										tmp[i]['watt'][int(x[-1])-1]["allType"].update({'name':name+"_"+x+"_allType"})
										tmp[i]['watt'][int(x[-1])-1]["allType"]['values'].extend(result)		
									elif(x[0:2]=="AE"):
										tmp[i]['ae'][0].update({"allType":{'name':'','values':[]}})
										tmp[i]['ae'][0]["allType"].update({'name':name+"_"+x+"_allType"})
										tmp[i]['ae'][0]["allType"]['values'].extend(result)
							elif data[i]['sensorType'] != "allType":
								result = list(self.query._client.iot_data["dm_"+data[i]['sensorType']].aggregate(pipeline))
								if(len(result)>0):
									if(x[0:2]=="VL"):
										tmp[i]['volt'][int(x[-1])-1].update({data[i]['sensorType']:{'name':'','values':[]}})
										tmp[i]['volt'][int(x[-1])-1][data[i]['sensorType']].update({'name':name+"_"+x+"_"+data[i]['sensorType']})
										tmp[i]['volt'][int(x[-1])-1][data[i]['sensorType']]['values'].extend(result)
									elif(x[0:2]=="AL"):
										tmp[i]['amp'][int(x[-1])-1].update({data[i]['sensorType']:{'name':'','values':[]}})
										tmp[i]['amp'][int(x[-1])-1][data[i]['sensorType']].update({'name':name+"_"+x+"_"+data[i]['sensorType']})
										tmp[i]['amp'][int(x[-1])-1][data[i]['sensorType']]['values'].extend(result)
									elif(x[0:1]=="P"):
										tmp[i]['watt'][int(x[-1])-1].update({data[i]['sensorType']:{'name':'','values':[]}})
										tmp[i]['watt'][int(x[-1])-1][data[i]['sensorType']].update({'name':name+"_"+x+"_"+data[i]['sensorType']})
										tmp[i]['watt'][int(x[-1])-1][data[i]['sensorType']]['values'].extend(result)		
									elif(x[0:2]=="AE"):
										tmp[i]['ae'][0].update({data[i]['sensorType']:{'name':'','values':[]}})
										tmp[i]['ae'][0][data[i]['sensorType']].update({'name':name+"_"+x+"_"+data[i]['sensorType']})
										tmp[i]['ae'][0][data[i]['sensorType']]['values'].extend(result)
					if(data[i]['type'] == "room"):
						_cur.execute("select s.inf_id,bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid where r.rid = %s",(data[i]['id']))
					if(data[i]['type'] == "floor"):
						_cur.execute("select s.inf_id,bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid where f.fid = %s",(data[i]['id']))
					if(data[i]['type'] == "building"):
						_cur.execute("select s.inf_id,bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid inner join building as b on b.bid=f.bid where b.bid = %s",(data[i]['id']))
					sensor = _cur.fetchall()
					if(len(sensor) != 0):
						bomac = []
						sid = []
						for index in range(len(sensor)):
							ct.append(sensor[index])
							bomac.append(sensor[index]['bomac'])
							sid.append(sensor[index]['inf_id'])
						pipeline = [{"$match": {"message.MAC":{"$in":bomac },"message.s":{"$in":sid },"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message.a"},}},{ "$sort": { '_id': 1 } },{"$addFields": { "y":{"$round":["$y",2]},"t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{"$unset": "_id" }]
						if data[i]['sensorType'] == "allType":
							lookupPipeline = [{"$match": {"message.MAC":{"$in":bomac },"message.s":{"$in":sid },"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message.a"},}},{ "$sort": { '_id': 1 } },{"$addFields": { "t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{"$match": {"$expr":{"$eq":["$t","$$tt"]}}},{"$unset": "_id" }]
							pipeline = [{"$match": {"message.MAC":{"$in":bomac },"message.s":{"$in":sid },"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message.a"},}},{ "$sort": { '_id': 1 } },{"$addFields": { "t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{"$unset": "_id" },
							{"$lookup":{"from": "ct_plug","let":{"tt" : "$t"},"pipeline": lookupPipeline,"as": "ct_plug"}},
							{"$lookup":{"from": "ct_air","let":{"tt" : "$t"},"pipeline": lookupPipeline,"as": "ct_air"}},
							{"$lookup":{"from": "ct_all","let":{"tt" : "$t"},"pipeline": lookupPipeline,"as": "ct_all"}},
							{"$project":{"t":1,"y":{"$round":[{"$avg":[{"$first":"$ct_air.y"},{"$first":"$ct_plug.y"},{"$first":"$ct_all.y"},"$y"]},2]}}}
							]
							result = list(self.query._client.iot_data["ct_light"].aggregate(pipeline))
							if(len(result)>0):
								tmp[i]['ct'][0].update({"allType":{'name':'','values':[]}})
								tmp[i]['ct'][0]["allType"].update({'name':name+"_CT_allType"})
								tmp[i]['ct'][0]["allType"]['values'].extend(result)
						elif data[i]['sensorType'] != "allType":
							result = list(self.query._client.iot_data["ct_"+data[i]['sensorType']].aggregate(pipeline))
							if(len(result)>0):
								tmp[i]['ct'][0].update({data[i]['sensorType']:{'name':'','values':[]}})
								tmp[i]['ct'][0][data[i]['sensorType']].update({'name':name+"_CT_"+data[i]['sensorType']})
								tmp[i]['ct'][0][data[i]['sensorType']]['values'].extend(result)
			
			sensorTypeCombine = list(dict.fromkeys(sensorTypeCombine))
			if 'allType' in sensorTypeCombine:
				sensorTypeCombine = ['light','air','plug','all']
			if(len(dm) != 0):
				bomac = []
				for index in range(len(dm)):
					bomac.append(dm[index]['bomac'])
				for x in dmType:
					pipeline = [{"$match": {"message.MAC":{"$in":bomac },"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message."+x},}},{ "$sort": { '_id': 1 } },{"$addFields": { "y":{"$round":["$y",2]},"t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{"$unset": "_id" }]
					for sType in sensorTypeCombine:
						result = list(self.query._client.iot_data["dm_"+sType].aggregate(pipeline))
						if(len(result)>0):
							if(x[0:2]=="VL"):
								tmp2['volt'][int(x[-1])-1].update({sType:{'name':'','values':[]}})
								tmp2['volt'][int(x[-1])-1][sType].update({'name':nameCombine+"_"+x+"_"+sType})
								tmp2['volt'][int(x[-1])-1][sType]['values'].extend(result)
							elif(x[0:2]=="AL"):
								tmp2['amp'][int(x[-1])-1].update({sType:{'name':'','values':[]}})
								tmp2['amp'][int(x[-1])-1][sType].update({'name':nameCombine+"_"+x+"_"+sType})
								tmp2['amp'][int(x[-1])-1][sType]['values'].extend(result)
							elif(x[0:1]=="P"):
								tmp2['watt'][int(x[-1])-1].update({sType:{'name':'','values':[]}})
								tmp2['watt'][int(x[-1])-1][sType].update({'name':nameCombine+"_"+x+"_"+sType})
								tmp2['watt'][int(x[-1])-1][sType]['values'].extend(result)
							elif(x[0:2]=="AE"):
								tmp2['ae'][0].update({sType:{'name':'','values':[]}})
								tmp2['ae'][0][sType].update({'name':nameCombine+"_"+x+"_"+sType})
								tmp2['ae'][0][sType]['values'].extend(result)
			if(len(ct) != 0):
				bomac = []
				sid = []
				for index in range(len(ct)):
					bomac.append(ct[index]['bomac'])
					sid.append(ct[index]['inf_id'])
				pipeline = [{"$match": {"message.MAC":{"$in":bomac },"message.s":{"$in":sid },"created_at" : {"$gte": int(startTime),"$lt" : int(endTime) },}},{"$group":{"_id":{ '$multiply':[{'$subtract' :[ {'$divide' : ['$created_at', unit ]}, { '$mod' : [{'$divide' : ['$created_at', unit ]},1] } ] },unit*1000]},"y": { "$avg": "$message.a"},}},{ "$sort": { '_id': 1 } },{"$addFields": { "y":{"$round":["$y",2]},"t":{"$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": {"$toDate" :"$_id"} }} }},{"$unset": "_id" }]
				for sType in sensorTypeCombine:
					result = list(self.query._client.iot_data["ct_"+sType].aggregate(pipeline))
					if(len(result)>0):
						tmp2['ct'][0].update({sType:{'name':'','values':[]}})
						tmp2['ct'][0][sType].update({'name':nameCombine+"_CT_"+sType})
						tmp2['ct'][0][sType]['values'].extend(result)
			self.query._CloseCursor(_cur)
			response = [tmp,tmp2]
			return response

	class Sensor:

		def __init__(self,query):
			self.query = query
	
		def sensor_list(self):
			res = self.query.fetchAll("SELECT s.inf_type,s.sid,s.sname,t.tname,r.rname,f.fname,b.bname,bo.bomac,r.rid,f.fid,b.bid FROM sensor AS s INNER JOIN board AS bo ON (s.boid=bo.boid) INNER JOIN room AS r ON (bo.rid=r.rid) INNER JOIN floor AS f ON (r.fid=f.fid) INNER JOIN building AS b ON (f.bid=b.bid) INNER JOIN type as t ON (s.tid=t.tid)")
			return res

		def sensor_edit(self,sid,sname):
			self.query.execute("UPDATE sensor SET sname = %s WHERE sid = %s",(sname,sid))

		def sensor_del(self,sid):
			self.query.execute("DELETE FROM sensor WHERE sid = %s",(sid,))


	class Building:

		def __init__(self,query):
			self.query = query

		@timed_lru_cache(1)
		def all_room_list(self):
			_cur = self.query._newCursor()
			_cur.execute("SELECT * FROM building")
			building = _cur.fetchall()
			for b in building:
				b.update({"floor":[]})
				_cur.execute("SELECT fid,fname FROM floor WHERE bid = %s",(b['bid'],))
				floor = _cur.fetchall()
				for f in floor:
					f.update({'room':[]})
					_cur.execute("SELECT rid,rname,rstatus FROM room WHERE fid = %s",(f['fid'],))
					room = _cur.fetchall()
					for r in room:
						f['room'].append(r)
					b['floor'].append(f)
			self.query._CloseCursor(_cur)
			return building

		def room_add(self,rname,fid):
			self.query.execute("INSERT INTO room (rname,fid) VALUES (%s,%s)",(rname,fid))

		def room_edit(self,rid,rname,fid):
			self.query.execute("UPDATE room SET rname = %s , fid = %s WHERE rid = %s",(rname,fid,rid))

		def room_del(self,rid):
			_cur = self.query._newCursor()
			_cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid SET board.register= 0 , board.rid=null WHERE room.rid = %s",(rid)) #SET board.rid to null and change board status to unregister
			_cur.execute("DELETE FROM room WHERE rid = %s",(rid,))
			self.query._CloseCursor(_cur)

		def floor_add(self,fname,bid):
			self.query.execute("INSERT INTO floor (fname,bid) VALUES (%s,%s)",(fname,bid))

		def floor_edit(self,fid,fname,bid):
			if(fid == 1):
				return
			self.query.execute("UPDATE floor SET fname = %s , bid = %s WHERE fid = %s",(fname,bid,fid))

		def floor_del(self,fid):
			if(fid == 1):
				return
			_cur = self.query._newCursor()
			_cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid INNER JOIN floor ON room.fid=floor.fid SET board.register= 0 , board.rid=null WHERE floor.fid = %s",(fid))
			_cur.execute("DELETE FROM room WHERE fid = %s",(fid,))
			_cur.execute("DELETE FROM floor WHERE fid = %s",(fid,))
			self.query._CloseCursor(_cur)

		def building_add(self,bname):
			self.query.execute("INSERT INTO building (bname) VALUES (%s)",(bname,))

		def building_edit(self,bid,bname):
			if(bid == 1):
				return
			self.query.execute("UPDATE building SET bname = %s WHERE bid = %s",(bname,bid))

		def building_del(self,bid):
			if(bid == 1):
				return
			_cur = self.query._newCursor()
			_cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid INNER JOIN floor ON room.fid=floor.fid INNER JOIN building ON building.bid=floor.bid SET	 board.register= 0 , board.rid=null WHERE building.bid = %s",(bid,))
			_cur.execute("DELETE room FROM room INNER JOIN floor ON room.fid = floor.fid WHERE floor.bid = %s",(bid,))
			_cur.execute("DELETE FROM floor WHERE bid = %s",(bid,))
			_cur.execute("DELETE FROM building WHERE bid = %s",(bid,))
			self.query._CloseCursor(_cur)

		def building_list(self):
			res = self.query.fetchAll("SELECT * FROM building")
			return res

		def floor_list(self,bid):
			res = self.query.fetchAll("SELECT * FROM floor where bid = %s",(bid,))
			return res

		def room_list(self,fid):
			res = self.query.fetchAll("SELECT * FROM room where fid = %s",(fid,))
			return res

	class Board:

		def __init__(self,query):
			self.query = query

		@timed_lru_cache(1)
		def register_list(self):
			_cur = self.query._newCursor()
			_cur.execute("SELECT bo.boid,bo.bomac,bo.register,bo.time,bo.rid,f.fid,b.bid,r.rname,f.fname,b.bname FROM board as bo INNER JOIN room as r ON bo.rid=r.rid INNER JOIN floor as f ON f.fid=r.fid INNER JOIN building as b ON b.bid=f.bid")
			board = _cur.fetchall()
			for bo in board:
				bo.update({'sensor':[]})
				_cur.execute("SELECT s.sid,s.sname,s.tid,t.tname FROM sensor as s INNER JOIN type as t ON s.tid=t.tid WHERE boid = %s",(bo['boid']))
				sensor = _cur.fetchall()
				for s in sensor:
					bo['sensor'].append(s)
				alltype = {}
				_cur.execute("SELECT * FROM type")
				for _type in _cur.fetchall():
					_cur.execute("SELECT COUNT(sid) AS COUNT FROM sensor WHERE boid = %s AND tid = %s",(bo['boid'], _type["tid"]))
					count = _cur.fetchone()
					alltype[_type["inf_name"]] = count["COUNT"]
				bo.update({'type':alltype})
			self.query._CloseCursor(_cur)
			return board

		def register_add(self,bomac,sensor):
			_cur = self.query._newCursor()
			_cur.execute("INSERT INTO board (bomac,register) VALUES (%s, 0)",(bomac,))
			_cur.execute("SELECT * FROM board WHERE bomac = %s",(bomac,))
			board = _cur.fetchall()
			for s in sensor:
				#_cur.execute("INSERT INTO sensor (tid,boid) VALUES (%s, %s)",(s['tid'],board['boid'])) #waiting for param valid
				print('')
			self.query._CloseCursor(_cur)

		def register_register(self,boid,sensor,rid):
			_cur = self.query._newCursor()
			_cur.execute("UPDATE board SET rid=%s , register = 1 WHERE boid = %s",(rid,boid))
			for s in sensor:
				_cur.execute("UPDATE sensor SET sname=%s WHERE sid=%s",(s['name'],s['id']))
			self.query._CloseCursor(_cur)

		def register_del(self,boid):
			_cur = self.query._newCursor()
			_cur.execute("DELETE FROM sensor WHERE boid = %s",(boid,))
			_cur.execute("DELETE FROM board WHERE boid = %s",(boid,))
			self.query._CloseCursor(_cur)

		#def schema_list(self):
		#	self.query._client.iot_data

	
	class User:

		def __init__(self,query):
			self.query = query

		def register_user(self,user,email,password):
			self.query.execute("INSERT INTO `user` (`username`, `email`, `password`, `is_active`, `flogout`, `create_time`) VALUES (%s, %s, %s, '0', '0', CURRENT_TIMESTAMP)",
				(user,email,password))

		def get_userByid(self,id):
			res = self.query.fetchOne("SELECT * FROM `user` WHERE `id` = %s",(id,))
			return res

		def get_userLogin(self,user):
			res = self.query.fetchOne("SELECT * FROM `user` WHERE (`username` = %s OR `email` = %s)",(user,user))
			return res

		def Updatepassword(self,username,password):
			self.query.execute("UPDATE `user` SET password = %s WHERE username = %s",(password,username))

		def getAllUser(self):
			res = self.query.fetchAll("SELECT * FROM user")
			return res

		def UpdateUserActive(self,_id,activate):
			user = self.getAllUser()
			if(len(user) > 1):
				self.query.execute("UPDATE `user` SET is_active = %s WHERE id = %s",(activate,_id))


	class Rule:

		def __init__(self,query):
			self.query = query

		def AddRule(self,rname,rjson):
			self.query.execute('INSERT INTO `rule` (`ruid`, `rname`, `rjson`) VALUES (NULL, %s, %s)',(rname,rjson))

		def UpdateRule(self,ruid,rname,rjson):
			self.query.execute("UPDATE `rule` SET rname = %s,rjson = %s WHERE ruid = %s",(rname,rjson,ruid))

		def getRule(self):
			res = self.query.fetchAll("SELECT * FROM rule")
			return res

		def DeleteRule(self,ruid):
			self.query.execute("DELETE FROM rule WHERE ruid = %s",(ruid,))
		
		def getCondition(self):
			allType = self.query._client["iot_data"]["iot_type"].find()
			res = []
			for _type in allType:
				sType = _type["sensor_type"]
				dType = _type["device_type"]
				for schema in _type["schema"].keys():
					if(_type["schema"][schema] == "int"):
						tmp = {}
						tmp["name"] = "{}({})_{}".format(sType, dType, schema) 
						tmp["id"] = "{}_{}_{}".format(sType, dType, schema)
						res.append(tmp)
			return res




	def getAllType(self):
		res = self.fetchAll("SELECT * FROM type")
		return res

	
	class Logs:

		def __init__(self,query):
			self.query = query
		
		def new_log(self,message,token):
			_cur = self.query._newCursor()
			_cur.execute("DELETE FROM logs WHERE create_time <	(CURRENT_TIMESTAMP - INTERVAL 3 MONTH)")
			_cur.execute("INSERT INTO `logs` (`lid`, `message`, `create_time`) VALUES (NULL, %s, CURRENT_TIMESTAMP)",(message,))
			_cur.execute("UPDATE `notify` SET `nlast_time` = CURRENT_TIMESTAMP WHERE `notify`.`ntoken` = %s",(token,))
			self.query._CloseCursor(_cur)

		def get_logs(self):
			res = self.query.fetchAll("SELECT * from logs")
			return res
		
		def summary_logs(self):
			_cur = self.query._newCursor()
			_cur.execute("SELECT COUNT(lid) as sum_logs FROM logs")
			temp1 = _cur.fetchall()
			_cur.execute("SELECT create_time as lastest FROM logs ORDER BY lid DESC LIMIT 1")
			temp2 = _cur.fetchall()
			res={}
			res.update(temp1[0])
			res.update(temp2[0])
			self.query._CloseCursor(_cur)
			return res
	


	def auto_add_room(self,prefix,data):
		_cur = self._newCursor()
		building = reg.getAllBuilding()
		building = list(filter(lambda x: x["prefix"].lower() == prefix.lower(), building))
		if(building):
			_cur.execute("""INSERT INTO building (bname, bprefix, burl) 
				SELECT * FROM (SELECT %s AS bname, %s AS bprefix, %s AS burl) AS tmp 
				WHERE NOT EXISTS ( SELECT bprefix FROM building WHERE bprefix = %s )""",(building[0]["name"],building[0]["prefix"],building[0]["url"],building[0]["prefix"]))
			_cur.execute("SELECT bid FROM building WHERE bprefix = %s",(building[0]["prefix"],))
			bid = _cur.fetchone()["bid"]
			floor = list(set([x[1] for x in data]))
			floor.sort()
			floor_id = {}
			for i in floor:
				_cur.execute("""INSERT INTO floor (fname, bid) 
					SELECT * FROM (SELECT %s AS fname, %s AS bid) AS tmp 
					WHERE NOT EXISTS ( SELECT fname, bid FROM floor WHERE fname = %s AND bid = %s)""",(i,bid,i,bid))
				_cur.execute("SELECT fid FROM floor WHERE fname = %s AND bid = %s",(i,bid))
				floor_id[i] = str(_cur.fetchone()["fid"])
			for i in data:
				_cur.execute("""INSERT INTO room (rname, fid ) 
					SELECT * FROM (SELECT %s AS rname, %s AS fid ) AS tmp 
					WHERE NOT EXISTS ( SELECT rname, fid  FROM room WHERE rname = %s AND fid = %s)""",(i[0],floor_id[i[1]],i[0],floor_id[i[1]]))
		self._CloseCursor(_cur)



	

	def roomWithBPrefix(self):
		res = self.fetchAll("SELECT r.rid,r.rname,r.rstatus,b.burl FROM room r INNER JOIN floor f ON r.fid = f.fid INNER JOIN building b ON f.bid = b.bid WHERE b.burl != ''")
		return res

	def UpdateRoomStatue(self,status,name):
		self.execute("UPDATE `room` SET rstatus = %s WHERE rname = %s",(status,name))

	def addnewSensor(self,data):
		_cur = self._newCursor()
		mac = data["MAC"]
		_cur.execute("""INSERT INTO board(`bomac`, `register`, `time`, `rid`) 
						SELECT * FROM (SELECT %s AS bomac, 0 AS register, CURRENT_TIMESTAMP AS time, '1' AS rid) AS tmp 
						WHERE NOT EXISTS ( SELECT bomac FROM board WHERE bomac = %s)""",(mac,mac))
		_cur.execute("SELECT boid FROM board WHERE bomac = %s",(mac,))
		lastid = _cur.fetchone()["boid"]
		for s in data["data"]:
			_cur.execute("""INSERT INTO `sensor` (`sname`, `inf_id`, `inf_type`, `tid`, `boid`)
							SELECT * FROM (SELECT %s AS sname, %s AS inf_id, %s AS inf_type, %s AS tid, %s AS boid) AS tmp 
							WHERE NOT EXISTS ( SELECT inf_id,inf_type,tid,boid FROM sensor WHERE inf_id = %s AND inf_type = %s AND tid = %s AND boid = %s)""",
							(s[0],s[1],s[2],s[3],lastid,s[1],s[2],s[3],lastid))
		self._CloseCursor(_cur)

	
	
	class Notification:

		def __init__(self,query):
			self.query = query

		def getToken(self,uid):
			res = self.query.fetchAll("SELECT * FROM notify where user_id= %s;",(uid))
			return res

		def updateNotiTime(self,uid,unitSec):
			self.query.execute("UPDATE `notify` SET ntime= %s WHERE `user_id` = %s;",(unitSec,uid))
			
		def updateNotiToken(self,uid,token):
			lst_token = self.query.fetchOne("SELECT `nid` FROM `notify` WHERE `user_id` = %s",(uid))
			if lst_token:
				self.query.execute("UPDATE `notify` SET ntoken= %s",(token))
			else:
				self.query.execute("INSERT INTO `notify` (`nid`, `ntoken`, `ntime`, `nlast_time`, `user_id`) VALUES (NULL, %s, 10, CURRENT_TIMESTAMP, %s);",(token,uid))



	def getRoomSensor(self,rname):
		res = self.fetchAll("""SELECT s.inf_id,s.inf_type,b.bomac,t.inf_name FROM sensor s 
								INNER JOIN type t ON s.tid = t.tid 
								INNER JOIN board b ON s.boid = b.boid 
								INNER JOIN room r ON b.rid = r.rid 
								WHERE s.inf_type IS NOT NULL AND r.rname = %s AND b.register = 1""",(rname,))
		return res

	def newSetting(self, data, digest):
		#Check if it already exist
		setting = self.getSetting(digest)
		if(setting == None):
			doc = {"data":data,"hash": digest}
			res = self._client["iot_data"]["graph_setting"].insert_one(doc)
			return res

	def getSetting(self, digest):
		res = self._client["iot_data"]["graph_setting"].find_one({"hash": digest})
		return res