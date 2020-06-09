import json

class Query:

	def __init__(self):
		self._conn = None
		self._cur = None
		self._client = None
		
	def init_db(self,conn,cur,client):
		self._conn = conn
		self._cur = cur
		self._client = client
		
	def demo1(self):
		self._cur.execute("SELECT * FROM user")
		res = self._cur.fetchall()
		return res
		
	def demo2(self):
		result = self._client.query("SELECT * FROM mqtt_consumer;")
		return result.raw
		
	def sensor_list(self):
		self._cur.execute("SELECT s.sid,s.sname,t.tname,r.rname,f.fname,b.bname,bo.bomac,r.rid,f.fid,b.bid FROM sensor AS s INNER JOIN board AS bo ON (s.boid=bo.boid) INNER JOIN room AS r ON (bo.rid=r.rid) INNER JOIN floor AS f ON (r.fid=f.fid) INNER JOIN building AS b ON (f.bid=b.bid) INNER JOIN type as t ON (s.tid=t.tid)")
		res = self._cur.fetchall()
		return res
		
	def all_room_list(self):
		self._cur.execute("SELECT * FROM building")
		building = self._cur.fetchall()
		for b in building:
			b.update({"floor":[]})
			self._cur.execute("SELECT fid,fname FROM floor WHERE bid = %s",(b['bid']))
			floor = self._cur.fetchall()
			for f in floor:
				f.update({'room':[]})
				self._cur.execute("SELECT rid,rname FROM room WHERE fid = %s",(f['fid']))
				room = self._cur.fetchall()
				for r in room: 
					f['room'].append(r)
				b['floor'].append(f)		
		return building
		
	def sensor_edit(self,sid,sname):
		self._cur.execute("UPDATE sensor SET sname = %s WHERE sid = %s",(sname,sid))
		
	def sensor_del(self,sid):
		self._cur.execute("DELETE FROM sensor WHERE sid = %s",(sid))
		
	def register_list(self):
		self._cur.execute("SELECT * FROM board")
		board = self._cur.fetchall()
		for bo in board:
			bo.update({'sensor':[]})
			self._cur.execute("SELECT sid,sname FROM sensor WHERE boid = %s",(bo['boid']))
			sensor = self._cur.fetchall()
			for s in sensor:
				bo['sensor'].append(s)
			self._cur.execute("SELECT COUNT(CASE WHEN tid = 1 THEN 1 END) AS light ,COUNT(CASE WHEN tid = 2 THEN 1 END) AS elec	 ,COUNT(CASE WHEN tid = 3 THEN 1 END) AS air FROM sensor WHERE boid = %s",(bo['boid']))
			count = self._cur.fetchall()
			bo.update({'type':{'light':count[0]['light'],'elec':count[0]['elec'],'air':count[0]['air']}})
					
		return board
		
	def register_add(self,bomac,sensor):
		self._cur.execute("INSERT INTO board (bomac,register) VALUES (%s, 0)",(bomac))
		self._cur.execute("SELECT * FROM board WHERE bomac = %s",(bomac))
		board = self._cur.fetchall()
		for s in sensor:
			#self._cur.execute("INSERT INTO sensor (tid,boid) VALUES (%s, %s)",(s['tid'],board['boid'])) #waiting for param valid
			print('')
		
	def register_register(self,boid,sensor,rid):
		self._cur.execute("UPDATE board SET rid=%s , register = 1 WHERE boid = %s",(rid,boid))
		for s in sensor:
			#self._cur.execute("UPDATE sensor SET sname=%s WHERE sid = %s",(s['sname'],s['sid'])) #waiting for param valid
			print('')
		
	def register_del(self,boid):
		self._cur.execute("DELETE FROM sensor WHERE boid = %s",(boid))	 # waiting for rules to delete
		self._cur.execute("DELETE FROM board WHERE boid = %s",(boid))
		
	
	def room_add(self,rname,fid):
		self._cur.execute("INSERT INTO room (rname,fid) VALUES (%s,%s)",(rname,fid))
	
	def room_edit(self,rid,rname,fid):
		self._cur.execute("UPDATE room SET rname = %s , fid = %s WHERE rid = %s",(rname,fid,rid))
		
	def room_del(self,rid):
		self._cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid SET board.register= 0 , board.rid=null WHERE room.rid = %s",(rid)) #SET board.rid to null and change board status to unregister
		self._cur.execute("DELETE FROM room WHERE rid = %s",(rid))
	
	def floor_add(self,fname,bid):
		self._cur.execute("INSERT INTO floor (fname,bid) VALUES (%s,%s)",(fname,bid))
	
	def floor_edit(self,fid,fname,bid):
		self._cur.execute("UPDATE floor SET fname = %s , bid = %s WHERE fid = %s",(fname,bid,fid))
		
	def floor_del(self,fid):
		self._cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid INNER JOIN floor ON room.fid=floor.fid SET board.register= 0 , board.rid=null WHERE floor.fid = %s",(fid))
		self._cur.execute("DELETE FROM room WHERE fid = %s",(fid))
		self._cur.execute("DELETE FROM floor WHERE fid = %s",(fid))
		
	def building_add(self,bname):
		self._cur.execute("INSERT INTO building (bname) VALUES (%s)",(bname))
	
	def building_edit(self,bid,bname):
		self._cur.execute("UPDATE building SET bname = %s WHERE bid = %s",(bname,bid))
		
	def building_del(self,bid):
		self._cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid INNER JOIN floor ON room.fid=floor.fid INNER JOIN building ON building.bid=floor.bid SET  board.register= 0 , board.rid=null WHERE building.bid = %s",(bid))
		self._cur.execute("DELETE room FROM room INNER JOIN floor ON room.fid = floor.fid WHERE floor.bid = %s",(bid))
		self._cur.execute("DELETE FROM floor WHERE bid = %s",(bid))
		self._cur.execute("DELETE FROM building WHERE bid = %s",(bid))

	def register_user(self,user,email,password):
		self._cur.execute("INSERT INTO `user` (`username`, `email`, `password`, `activate`, `flogout`, `create_time`) VALUES (%s, %s, %s, '0', '0', CURRENT_TIMESTAMP)",
			(user,email,password))

	def get_userByid(self,id):
		self._cur.execute("SELECT * FROM `user` WHERE `id` = %s",(id))
		res = self._cur.fetchone()
		return res

	def get_userLogin(self,user):
		self._cur.execute("SELECT * FROM `user` WHERE (`username` = %s OR `email` = %s)",(user,user))
		res = self._cur.fetchone()
		return res
		
	#board.rid can be null
	#sensor type_tid must change to only tid
	
	def building_list(self):
		self._cur.execute("SELECT * FROM building")
		res = self._cur.fetchall()
		return res	
	
	def floor_list(self,bid):
		self._cur.execute("SELECT * FROM floor where bid = %s",(bid))
		res = self._cur.fetchall()
		return res
		
	def room_list(self,fid):
		self._cur.execute("SELECT * FROM room where fid = %s",(fid))
		res = self._cur.fetchall()
		return res
	

