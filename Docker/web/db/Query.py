import reg
import json

class Query:

	def __init__(self):
		self._conn = None
		self._client = None

	def init_db(self,conn,client):
		self._conn = conn
		self._client = client

	def _newCursor(self):
		return self._conn.cursor()

	def _CloseCursor(self,cursor):
		return cursor.close()
		
	def dashboard_list(self,data):
		_cur = self._newCursor()
		tmp=[]
		for i in range(len(data)):
			if(data[i]['type'] == "sensor"): 
				result = self._client.query(query='select sum(volt) as volt ,sum(amp) as amp ,sum(watt) as watt from mqtt_consumer where sid=$sid group by time(10m);',params={"params":json.dumps({'sid':data[i]['id']})})
				tmp.append({'name':data[i]['name'],'volt':[],'amp':[],'watt':[]})
				for d in result.raw['series'][0]['values']:
					tmp[i]['volt'].append({'t':d[0],'y':d[1]})
					tmp[i]['amp'].append({'t':d[0],'y':d[2]})
					tmp[i]['watt'].append({'t':d[0],'y':d[3]})
			if(data[i]['type'] == "room"): 
				tmp.append({'name':data[i]['name'],'volt':[],'amp':[],'watt':[]})
				_cur.execute("select s.sid from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid where r.rid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				qry = "select sum(volt) as volt ,sum(amp) as amp ,sum(watt) as watt from mqtt_consumer where "
				for index in range(len(sensor)):
					if(index == len(sensor)-1):
						qry+='sid = '+str(sensor[index]['sid'])
					else:
						qry+='sid = '+str(sensor[index]['sid'])+' or '
				if(len(sensor) != 0):
					qry+=' group by time(10m);'
					result = self._client.query(query=qry)
					for d in result.raw['series'][0]['values']:
						tmp[i]['volt'].append({'t':d[0],'y':d[1]})
						tmp[i]['amp'].append({'t':d[0],'y':d[2]})
						tmp[i]['watt'].append({'t':d[0],'y':d[3]})
			if(data[i]['type'] == "floor"): 
				tmp.append({'name':data[i]['name'],'volt':[],'amp':[],'watt':[]})
				_cur.execute("select s.sid from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid where f.fid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				qry = "select sum(volt) as volt ,sum(amp) as amp ,sum(watt) as watt from mqtt_consumer where "
				for index in range(len(sensor)):
					if(index == len(sensor)-1):
						qry+='sid = '+str(sensor[index]['sid'])
					else:
						qry+='sid = '+str(sensor[index]['sid'])+' or '
				if(len(sensor) != 0):
					qry+=' group by time(10m);'
					result = self._client.query(query=qry)
					for d in result.raw['series'][0]['values']:
						tmp[i]['volt'].append({'t':d[0],'y':d[1]})
						tmp[i]['amp'].append({'t':d[0],'y':d[2]})
						tmp[i]['watt'].append({'t':d[0],'y':d[3]})
			if(data[i]['type'] == "building"): 
				tmp.append({'name':data[i]['name'],'volt':[],'amp':[],'watt':[]})
				_cur.execute("select s.sid from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid inner join building as b on b.bid=f.bid where b.bid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				qry = "select sum(volt) as volt ,sum(amp) as amp ,sum(watt) as watt from mqtt_consumer where "
				for index in range(len(sensor)):
					if(index == len(sensor)-1):
						qry+='sid = '+str(sensor[index]['sid'])
					else:
						qry+='sid = '+str(sensor[index]['sid'])+' or '
				if(len(sensor) != 0):
					qry+=' group by time(10m);'
					result = self._client.query(query=qry)
					for d in result.raw['series'][0]['values']:
						tmp[i]['volt'].append({'t':d[0],'y':d[1]})
						tmp[i]['amp'].append({'t':d[0],'y':d[2]})
						tmp[i]['watt'].append({'t':d[0],'y':d[3]})
		self._CloseCursor(_cur)
		return tmp

	def sensor_list(self):
		_cur = self._newCursor()
		_cur.execute("SELECT s.sid,s.sname,t.tname,r.rname,f.fname,b.bname,bo.bomac,r.rid,f.fid,b.bid FROM sensor AS s INNER JOIN board AS bo ON (s.boid=bo.boid) INNER JOIN room AS r ON (bo.rid=r.rid) INNER JOIN floor AS f ON (r.fid=f.fid) INNER JOIN building AS b ON (f.bid=b.bid) INNER JOIN type as t ON (s.tid=t.tid)")
		res = _cur.fetchall()
		self._CloseCursor(_cur)
		return res

	def all_room_list(self):
		_cur = self._newCursor()
		_cur.execute("SELECT * FROM building")
		building = _cur.fetchall()
		for b in building:
			b.update({"floor":[]})
			_cur.execute("SELECT fid,fname FROM floor WHERE bid = %s",(b['bid'],))
			floor = _cur.fetchall()
			for f in floor:
				f.update({'room':[]})
				_cur.execute("SELECT rid,rname FROM room WHERE fid = %s",(f['fid'],))
				room = _cur.fetchall()
				for r in room:
					f['room'].append(r)
				b['floor'].append(f)
		self._CloseCursor(_cur)
		return building

	def sensor_edit(self,sid,sname):
		_cur = self._newCursor()
		_cur.execute("UPDATE sensor SET sname = %s WHERE sid = %s",(sname,sid))
		self._CloseCursor(_cur)

	def sensor_del(self,sid):
		_cur = self._newCursor()
		_cur.execute("DELETE FROM sensor WHERE sid = %s",(sid,))
		self._CloseCursor(_cur)

	def register_list(self):
		_cur = self._newCursor()
		_cur.execute("SELECT bo.boid,bo.bomac,bo.register,bo.time,bo.rid,f.fid,b.bid,r.rname,f.fname,b.bname FROM board as bo INNER JOIN room as r ON bo.rid=r.rid INNER JOIN floor as f ON f.fid=r.fid INNER JOIN building as b ON b.bid=f.bid")
		board = _cur.fetchall()
		for bo in board:
			bo.update({'sensor':[]})
			_cur.execute("SELECT s.sid,s.sname,s.tid,t.tname FROM sensor as s INNER JOIN type as t ON s.tid=t.tid WHERE boid = %s",(bo['boid']))
			sensor = _cur.fetchall()
			for s in sensor:
				bo['sensor'].append(s)
			_cur.execute("SELECT COUNT(CASE WHEN tid = 1 THEN 1 END) AS light ,COUNT(CASE WHEN tid = 2 THEN 1 END) AS elec ,COUNT(CASE WHEN tid = 3 THEN 1 END) AS air ,COUNT(CASE WHEN tid = 4 THEN 1 END) AS motion FROM sensor WHERE boid = %s",(bo['boid']))
			count = _cur.fetchall()
			bo.update({'type':{'light':count[0]['light'],'electricity':count[0]['elec'],'air conditioner':count[0]['air'],'motion':count[0]['motion']}})
		self._CloseCursor(_cur)
		return board

	def register_add(self,bomac,sensor):
		_cur = self._newCursor()
		_cur.execute("INSERT INTO board (bomac,register) VALUES (%s, 0)",(bomac,))
		_cur.execute("SELECT * FROM board WHERE bomac = %s",(bomac,))
		board = _cur.fetchall()
		for s in sensor:
			#_cur.execute("INSERT INTO sensor (tid,boid) VALUES (%s, %s)",(s['tid'],board['boid'])) #waiting for param valid
			print('')
		self._CloseCursor(_cur)

	def register_register(self,boid,sensor,rid):
		_cur = self._newCursor()
		_cur.execute("UPDATE board SET rid=%s , register = 1 WHERE boid = %s",(rid,boid))
		for s in sensor:
			_cur.execute("UPDATE sensor SET sname=%s WHERE sid=%s",(s['name'],s['id']))
		self._CloseCursor(_cur)

	def register_del(self,boid):
		_cur = self._newCursor()
		_cur.execute("DELETE FROM sensor WHERE boid = %s",(boid,))
		_cur.execute("DELETE FROM board WHERE boid = %s",(boid,))
		self._CloseCursor(_cur)

	def room_add(self,rname,fid):
		_cur = self._newCursor()
		_cur.execute("INSERT INTO room (rname,fid) VALUES (%s,%s)",(rname,fid))
		self._CloseCursor(_cur)

	def room_edit(self,rid,rname,fid):
		_cur = self._newCursor()
		_cur.execute("UPDATE room SET rname = %s , fid = %s WHERE rid = %s",(rname,fid,rid))
		self._CloseCursor(_cur)

	def room_del(self,rid):
		_cur = self._newCursor()
		_cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid SET board.register= 0 , board.rid=null WHERE room.rid = %s",(rid)) #SET board.rid to null and change board status to unregister
		_cur.execute("DELETE FROM room WHERE rid = %s",(rid,))
		self._CloseCursor(_cur)

	def floor_add(self,fname,bid):
		_cur = self._newCursor()
		_cur.execute("INSERT INTO floor (fname,bid) VALUES (%s,%s)",(fname,bid))
		self._CloseCursor(_cur)

	def floor_edit(self,fid,fname,bid):
		_cur = self._newCursor()
		if(fid == 1):
			return
		_cur.execute("UPDATE floor SET fname = %s , bid = %s WHERE fid = %s",(fname,bid,fid))
		self._CloseCursor(_cur)

	def floor_del(self,fid):
		if(fid == 1):
			return
		_cur = self._newCursor()
		_cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid INNER JOIN floor ON room.fid=floor.fid SET board.register= 0 , board.rid=null WHERE floor.fid = %s",(fid))
		_cur.execute("DELETE FROM room WHERE fid = %s",(fid,))
		_cur.execute("DELETE FROM floor WHERE fid = %s",(fid,))
		self._CloseCursor(_cur)

	def building_add(self,bname):
		_cur = self._newCursor()
		_cur.execute("INSERT INTO building (bname) VALUES (%s)",(bname,))
		self._CloseCursor(_cur)

	def building_edit(self,bid,bname):
		if(bid == 1):
			return
		_cur = self._newCursor()
		_cur.execute("UPDATE building SET bname = %s WHERE bid = %s",(bname,bid))
		self._CloseCursor(_cur)

	def building_del(self,bid):
		if(bid == 1):
			return
		_cur = self._newCursor()
		_cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid INNER JOIN floor ON room.fid=floor.fid INNER JOIN building ON building.bid=floor.bid SET	 board.register= 0 , board.rid=null WHERE building.bid = %s",(bid,))
		_cur.execute("DELETE room FROM room INNER JOIN floor ON room.fid = floor.fid WHERE floor.bid = %s",(bid,))
		_cur.execute("DELETE FROM floor WHERE bid = %s",(bid,))
		_cur.execute("DELETE FROM building WHERE bid = %s",(bid,))
		self._CloseCursor(_cur)

	def register_user(self,user,email,password):
		_cur = self._newCursor()
		_cur.execute("INSERT INTO `user` (`username`, `email`, `password`, `is_active`, `flogout`, `create_time`) VALUES (%s, %s, %s, '0', '0', CURRENT_TIMESTAMP)",
			(user,email,password))
		self._CloseCursor(_cur)

	def get_userByid(self,id):
		_cur = self._newCursor()
		_cur.execute("SELECT * FROM `user` WHERE `id` = %s",(id,))
		res = _cur.fetchone()
		self._CloseCursor(_cur)
		return res

	def get_userLogin(self,user):
		_cur = self._newCursor()
		_cur.execute("SELECT * FROM `user` WHERE (`username` = %s OR `email` = %s)",(user,user))
		res = _cur.fetchone()
		self._CloseCursor(_cur)
		return res

	#board.rid can be null

	def building_list(self):
		_cur = self._newCursor()
		_cur.execute("SELECT * FROM building")
		res = _cur.fetchall()
		self._CloseCursor(_cur)
		return res

	def floor_list(self,bid):
		_cur = self._newCursor()
		_cur.execute("SELECT * FROM floor where bid = %s",(bid,))
		res = _cur.fetchall()
		self._CloseCursor(_cur)
		return res

	def room_list(self,fid):
		_cur = self._newCursor()
		_cur.execute("SELECT * FROM room where fid = %s",(fid,))
		res = _cur.fetchall()
		self._CloseCursor(_cur)
		return res

	def getAllType(self):
		_cur = self._newCursor()
		_cur.execute("SELECT * FROM type")
		res = _cur.fetchall()
		self._CloseCursor(_cur)
		return res

	def AddRule(self,rname,rjson):
		_cur = self._newCursor()
		_cur.execute('INSERT INTO `rule` (`ruid`, `rname`, `rjson`) VALUES (NULL, %s, %s)',(rname,rjson))
		self._CloseCursor(_cur)

	def UpdateRule(self,ruid,rname,rjson):
		_cur = self._newCursor()
		_cur.execute("UPDATE `rule` SET rname = %s,rjson = %s WHERE ruid = %s",(rname,rjson,ruid))
		self._CloseCursor(_cur)

	def getRule(self):
		_cur = self._newCursor()
		_cur.execute("SELECT * FROM rule")
		res = _cur.fetchall()
		self._CloseCursor(_cur)
		return res

	def DeleteRule(self,ruid):
		_cur = self._newCursor()
		_cur.execute("DELETE FROM rule WHERE ruid = %s",(ruid,))
		self._CloseCursor(_cur)

	def new_log(self,message):
		_cur = self._newCursor()
		_cur.execute("DELETE FROM logs WHERE create_time <	(CURRENT_TIMESTAMP - INTERVAL 3 MONTH)")
		_cur.execute("INSERT INTO `logs` (`lid`, `message`, `create_time`) VALUES (NULL, %s, CURRENT_TIMESTAMP)",(message,))
		self._CloseCursor(_cur)

	def get_logs(self):
		_cur = self._newCursor()
		_cur.execute("SELECT * from logs")
		res = _cur.fetchall()
		self._CloseCursor(_cur)
		return res
	
	def summary_logs(self):
		_cur = self._newCursor()
		_cur.execute("SELECT COUNT(lid) as sum_logs FROM logs")
		temp1 = _cur.fetchall()
		_cur.execute("SELECT create_time as lastest FROM logs ORDER BY lid DESC LIMIT 1")
		temp2 = _cur.fetchall()
		res={}
		res.update(temp1[0])
		res.update(temp2[0])
		self._CloseCursor(_cur)
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

