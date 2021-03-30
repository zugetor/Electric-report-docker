import json

class Query:

	def __init__(self):
		self._conn = None
		self._client = None

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
		with self._newCursor() as _cur:
			if param:
				_cur.execute(sql,param)
			else:
				_cur.execute(sql)
			res = _cur.fetchall()
			return res
		return None

	def fetchOne(self,sql,param=None):
		with self._newCursor() as _cur:
			if param:
				_cur.execute(sql,param)
			else:
				_cur.execute(sql)
			res = _cur.fetchone()
			return res
		return None

	def execute(self,sql,param=None):
		with self._newCursor() as _cur:
			if param:
				res = _cur.execute(sql,param)
			else:
				res = _cur.execute(sql)
			return res
		return None

	def all_room_list(self):
		with self._newCursor() as _cur:
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
			return building
		return None

	def getAllType(self):
		res = self.fetchAll("SELECT * FROM type")
		return res

	def getRule(self):
		res = self.fetchAll("SELECT * FROM rule")
		return res

	def new_log(self,message,token):
		with self._newCursor() as _cur:
			_cur.execute("DELETE FROM logs WHERE create_time <	(CURRENT_TIMESTAMP - INTERVAL 3 MONTH)")
			_cur.execute("INSERT INTO `logs` (`lid`, `message`, `create_time`) VALUES (NULL, %s, CURRENT_TIMESTAMP)",(message,))
			_cur.execute("UPDATE `notify` SET `nlast_time` = CURRENT_TIMESTAMP WHERE `notify`.`ntoken` = %s",(token,))
		return None

	def roomWithBPrefix(self):
		res = self.fetchAll("SELECT r.rid,r.rname,r.rstatus,b.burl FROM room r INNER JOIN floor f ON r.fid = f.fid INNER JOIN building b ON f.bid = b.bid WHERE b.burl != ''")
		return res

	def UpdateRoomStatue(self,status,name):
		self.execute("UPDATE `room` SET rstatus = %s WHERE rname = %s",(status,name))

	def addnewSensor(self,data):
		with self._newCursor() as _cur:
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
		return None

	def getToken(self):
		res = self.fetchAll("SELECT * FROM notify")
		return res

	def getRoomSensor(self,rname):
		res = self.fetchAll("""SELECT s.inf_id,s.inf_type,b.bomac,t.inf_name FROM sensor s 
								INNER JOIN type t ON s.tid = t.tid 
								INNER JOIN board b ON s.boid = b.boid 
								INNER JOIN room r ON b.rid = r.rid 
								WHERE s.inf_type IS NOT NULL AND r.rname = %s AND b.register = 1""",(rname,))
		return res