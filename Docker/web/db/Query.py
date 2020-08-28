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

	def getInfQuery(self):
		return self._client.query
		
	def dashboard_list(self,data,unit,startTime,endTime,graphType):
		_cur = self._newCursor()
		tmp=[] #for compare and separate graph
		tmp2={'name':"",'ct':[{'values':[]}],'volt':[{'values':[]},{'values':[]},{'values':[]}],'amp':[{'values':[]},{'values':[]},{'values':[]}],'watt':[{'values':[]},{'values':[]},{'values':[]}],'ae':[{'values':[]}]} #for combine graph
		ct=[] #collect data and query one time for combine
		dm=[] #collect data and query one time for combine
		nameCombine=""
		for i in range(len(data)):
			name = data[i]['name']
			if(data[i]['type'] == "ct"):
				nameCombine+=data[i]['name']+", "
				tmp.append({'name':name,'ct':[{'values':[]}]})
				_cur.execute("select s.inf_id,bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid where s.sid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				ct.append(sensor[0])
				if(len(sensor) != 0):
					#result = self._client.query(query='select sum(volt)/$div as volt ,sum(amp)/$div as amp ,sum(watt)/$div as watt from mqtt_consumer where sid=$sid and time>=$startTime and time<=$endTime group by time($unit);',params={"params":json.dumps({'sid':data[i]['id'],'unit':unit,'div':div,'startTime':startTime,'endTime':endTime})})
					result = self._client.query('select sum(a) as amp from ct where s='+str(sensor[0]['inf_id'])+' and MAC=\''+str(sensor[0]['bomac'])+'\' and time>='+startTime+' and time<='+endTime+' group by time('+unit+')')
					if(len(result.raw['series'])>0):
						tmp[i]['ct'][0].update({'name':name+"_ct"})
						for d in result.raw['series'][0]['values']:
							tmp[i]['ct'][0]['values'].append({'t':d[0],'y':d[1]})
			if(data[i]['type'] == "dm"):
				nameCombine+=data[i]['name']+", "
				tmp.append({'name':name,'volt':[{'values':[]},{'values':[]},{'values':[]}],'amp':[{'values':[]},{'values':[]},{'values':[]}],'watt':[{'values':[]},{'values':[]},{'values':[]}],'ae':[{'values':[]}],'ct':[{'values':[]}]})
				_cur.execute("select bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid where s.sid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				dm.append(sensor[0])
				if(len(sensor) != 0):
					qry = "select sum(VL1) as VL1 ,sum(VL2) as VL2 ,sum(VL3) as VL3 ,sum(AL1) as AL1 ,sum(AL2) as AL2 ,sum(AL3) as AL3,sum(P1) as P1 ,sum(P2) as P2 ,sum(P3) as P3 ,sum(AE) as AE from dm where MAC=\'"+str(sensor[0]['bomac'])+"\' and time>="+startTime+" and time<="+endTime+" group by time("+unit+")"
					result = self._client.query(query=qry)
					if(len(result.raw['series'])>0):
						tmp[i]['volt'][0].update({'name':name+"_VL1"})
						tmp[i]['volt'][1].update({'name':name+"_VL2"})
						tmp[i]['volt'][2].update({'name':name+"_VL3"})
						tmp[i]['amp'][0].update({'name':name+"_AL1"})
						tmp[i]['amp'][1].update({'name':name+"_AL2"})
						tmp[i]['amp'][2].update({'name':name+"_AL3"})
						tmp[i]['watt'][0].update({'name':name+"_P1"})
						tmp[i]['watt'][1].update({'name':name+"_P2"})
						tmp[i]['watt'][2].update({'name':name+"_P3"})
						tmp[i]['ae'][0].update({'name':name+"_AE"})
						for d in result.raw['series'][0]['values']:
							tmp[i]['volt'][0]['values'].append({'t':d[0],'y':d[1]})
							tmp[i]['volt'][1]['values'].append({'t':d[0],'y':d[2]})
							tmp[i]['volt'][2]['values'].append({'t':d[0],'y':d[3]})
							tmp[i]['amp'][0]['values'].append({'t':d[0],'y':d[4]})
							tmp[i]['amp'][1]['values'].append({'t':d[0],'y':d[5]})
							tmp[i]['amp'][2]['values'].append({'t':d[0],'y':d[6]})
							tmp[i]['watt'][0]['values'].append({'t':d[0],'y':d[7]})
							tmp[i]['watt'][1]['values'].append({'t':d[0],'y':d[8]})
							tmp[i]['watt'][2]['values'].append({'t':d[0],'y':d[9]})
							tmp[i]['ae'][0]['values'].append({'t':d[0],'y':d[10]})
			if(data[i]['type'] == "room"):
				nameCombine+=data[i]['name']+", "
				tmp.append({'name':name,'volt':[{'values':[]},{'values':[]},{'values':[]}],'amp':[{'values':[]},{'values':[]},{'values':[]}],'watt':[{'values':[]},{'values':[]},{'values':[]}],'ae':[{'values':[]}],'ct':[{'values':[]}]})
				_cur.execute("select bo.bomac from board as bo inner join room as r on bo.rid=r.rid where r.rid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				if(len(sensor) != 0):
					qry = "select sum(VL1) as VL1 ,sum(VL2) as VL2 ,sum(VL3) as VL3 ,sum(AL1) as AL1 ,sum(AL2) as AL2 ,sum(AL3) as AL3,sum(P1) as P1 ,sum(P2) as P2 ,sum(P3) as P3 ,sum(AE) as AE from dm where (time>="+str(startTime)+" and time<="+str(endTime)+") and "
					for index in range(len(sensor)):
						dm.append(sensor[index])
						if(index == len(sensor)-1):
							qry+='MAC = \''+str(sensor[index]['bomac'])+'\''
						else:
							qry+='MAC = \''+str(sensor[index]['bomac'])+'\' or '
					qry+=' group by time('+unit+');'
					result = self._client.query(query=qry)
					if(len(result.raw['series'])>0):
						tmp[i]['volt'][0].update({'name':name+"_VL1"})
						tmp[i]['volt'][1].update({'name':name+"_VL2"})
						tmp[i]['volt'][2].update({'name':name+"_VL3"})
						tmp[i]['amp'][0].update({'name':name+"_AL1"})
						tmp[i]['amp'][1].update({'name':name+"_AL2"})
						tmp[i]['amp'][2].update({'name':name+"_AL3"})
						tmp[i]['watt'][0].update({'name':name+"_P1"})
						tmp[i]['watt'][1].update({'name':name+"_P2"})
						tmp[i]['watt'][2].update({'name':name+"_P3"})
						tmp[i]['ae'][0].update({'name':name+"_AE"})
						for d in result.raw['series'][0]['values']:
							tmp[i]['volt'][0]['values'].append({'t':d[0],'y':d[1]})
							tmp[i]['volt'][1]['values'].append({'t':d[0],'y':d[2]})
							tmp[i]['volt'][2]['values'].append({'t':d[0],'y':d[3]})
							tmp[i]['amp'][0]['values'].append({'t':d[0],'y':d[4]})
							tmp[i]['amp'][1]['values'].append({'t':d[0],'y':d[5]})
							tmp[i]['amp'][2]['values'].append({'t':d[0],'y':d[6]})
							tmp[i]['watt'][0]['values'].append({'t':d[0],'y':d[7]})
							tmp[i]['watt'][1]['values'].append({'t':d[0],'y':d[8]})
							tmp[i]['watt'][2]['values'].append({'t':d[0],'y':d[9]})
							tmp[i]['ae'][0]['values'].append({'t':d[0],'y':d[10]})
				_cur.execute("select s.inf_id,bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid where r.rid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				if(len(sensor) != 0):
					qry = "select sum(a) as a from ct where (time>="+str(startTime)+" and time<="+str(endTime)+") and "
					for index in range(len(sensor)):
						ct.append(sensor[index])
						if(index == len(sensor)-1):
							qry+='(MAC = \''+str(sensor[index]['bomac'])+'\' and s = '+str(sensor[index]['inf_id'])+') '
						else:
							qry+='(MAC = \''+str(sensor[index]['bomac'])+'\' and s = '+str(sensor[index]['inf_id'])+') or '
					qry+=' group by time('+unit+');'
					result = self._client.query(query=qry)
					if(len(result.raw['series'])>0):
						tmp[i]['ct'][0].update({'name':name+"_CT"})
						for d in result.raw['series'][0]['values']:
							tmp[i]['ct'][0]['values'].append({'t':d[0],'y':d[1]})
			if(data[i]['type'] == "floor"): 
				nameCombine+='floor '+data[i]['name']+", "
				name = 'floor '+data[i]['name']
				tmp.append({'name':name,'volt':[{'values':[]},{'values':[]},{'values':[]}],'amp':[{'values':[]},{'values':[]},{'values':[]}],'watt':[{'values':[]},{'values':[]},{'values':[]}],'ae':[{'values':[]}],'ct':[{'values':[]}]})
				_cur.execute("select bo.bomac from board as bo inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid where f.fid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				if(len(sensor) != 0):
					qry = "select sum(VL1) as VL1 ,sum(VL2) as VL2 ,sum(VL3) as VL3 ,sum(AL1) as AL1 ,sum(AL2) as AL2 ,sum(AL3) as AL3,sum(P1) as P1 ,sum(P2) as P2 ,sum(P3) as P3 ,sum(AE) as AE from dm where (time>="+str(startTime)+" and time<="+str(endTime)+") and "
					for index in range(len(sensor)):
						dm.append(sensor[index])
						if(index == len(sensor)-1):
							qry+='MAC = \''+str(sensor[index]['bomac'])+'\''
						else:
							qry+='MAC = \''+str(sensor[index]['bomac'])+'\' or '
					qry+=' group by time('+unit+');'
					result = self._client.query(query=qry)
					if(len(result.raw['series'])>0):
						tmp[i]['volt'][0].update({'name':name+"_VL1"})
						tmp[i]['volt'][1].update({'name':name+"_VL2"})
						tmp[i]['volt'][2].update({'name':name+"_VL3"})
						tmp[i]['amp'][0].update({'name':name+"_AL1"})
						tmp[i]['amp'][1].update({'name':name+"_AL2"})
						tmp[i]['amp'][2].update({'name':name+"_AL3"})
						tmp[i]['watt'][0].update({'name':name+"_P1"})
						tmp[i]['watt'][1].update({'name':name+"_P2"})
						tmp[i]['watt'][2].update({'name':name+"_P3"})
						tmp[i]['ae'][0].update({'name':name+"_AE"})
						for d in result.raw['series'][0]['values']:
							tmp[i]['volt'][0]['values'].append({'t':d[0],'y':d[1]})
							tmp[i]['volt'][1]['values'].append({'t':d[0],'y':d[2]})
							tmp[i]['volt'][2]['values'].append({'t':d[0],'y':d[3]})
							tmp[i]['amp'][0]['values'].append({'t':d[0],'y':d[4]})
							tmp[i]['amp'][1]['values'].append({'t':d[0],'y':d[5]})
							tmp[i]['amp'][2]['values'].append({'t':d[0],'y':d[6]})
							tmp[i]['watt'][0]['values'].append({'t':d[0],'y':d[7]})
							tmp[i]['watt'][1]['values'].append({'t':d[0],'y':d[8]})
							tmp[i]['watt'][2]['values'].append({'t':d[0],'y':d[9]})
							tmp[i]['ae'][0]['values'].append({'t':d[0],'y':d[10]})
				_cur.execute("select s.inf_id,bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid where f.fid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				if(len(sensor) != 0):
					qry = "select sum(a) as a from ct where (time>="+str(startTime)+" and time<="+str(endTime)+") and "
					for index in range(len(sensor)):
						ct.append(sensor[index])
						if(index == len(sensor)-1):
							qry+='(MAC = \''+str(sensor[index]['bomac'])+'\' and s = '+str(sensor[index]['inf_id'])+') '
						else:
							qry+='(MAC = \''+str(sensor[index]['bomac'])+'\' and s = '+str(sensor[index]['inf_id'])+') or '
					qry+=' group by time('+unit+');'
					result = self._client.query(query=qry)
					if(len(result.raw['series'])>0):
						tmp[i]['ct'][0].update({'name':name+"_CT"})
						for d in result.raw['series'][0]['values']:
							tmp[i]['ct'][0]['values'].append({'t':d[0],'y':d[1]})
			if(data[i]['type'] == "building"): 
				nameCombine+=data[i]['name']+", "
				tmp.append({'name':name,'volt':[{'values':[]},{'values':[]},{'values':[]}],'amp':[{'values':[]},{'values':[]},{'values':[]}],'watt':[{'values':[]},{'values':[]},{'values':[]}],'ae':[{'values':[]}],'ct':[{'values':[]}]})
				_cur.execute("select bo.bomac from board as bo inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid inner join building as b on b.bid=f.bid where b.bid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				if(len(sensor) != 0):
					qry = "select sum(VL1) as VL1 ,sum(VL2) as VL2 ,sum(VL3) as VL3 ,sum(AL1) as AL1 ,sum(AL2) as AL2 ,sum(AL3) as AL3,sum(P1) as P1 ,sum(P2) as P2 ,sum(P3) as P3 ,sum(AE) as AE from dm where (time>="+str(startTime)+" and time<="+str(endTime)+") and "
					for index in range(len(sensor)):
						dm.append(sensor[index])
						if(index == len(sensor)-1):
							qry+='MAC = \''+str(sensor[index]['bomac'])+'\''
						else:
							qry+='MAC = \''+str(sensor[index]['bomac'])+'\' or '
					qry+=' group by time('+unit+');'
					result = self._client.query(query=qry)
					if(len(result.raw['series'])>0):
						tmp[i]['volt'][0].update({'name':name+"_VL1"})
						tmp[i]['volt'][1].update({'name':name+"_VL2"})
						tmp[i]['volt'][2].update({'name':name+"_VL3"})
						tmp[i]['amp'][0].update({'name':name+"_AL1"})
						tmp[i]['amp'][1].update({'name':name+"_AL2"})
						tmp[i]['amp'][2].update({'name':name+"_AL3"})
						tmp[i]['watt'][0].update({'name':name+"_P1"})
						tmp[i]['watt'][1].update({'name':name+"_P2"})
						tmp[i]['watt'][2].update({'name':name+"_P3"})
						tmp[i]['ae'][0].update({'name':name+"_AE"})
						for d in result.raw['series'][0]['values']:
							tmp[i]['volt'][0]['values'].append({'t':d[0],'y':d[1]})
							tmp[i]['volt'][1]['values'].append({'t':d[0],'y':d[2]})
							tmp[i]['volt'][2]['values'].append({'t':d[0],'y':d[3]})
							tmp[i]['amp'][0]['values'].append({'t':d[0],'y':d[4]})
							tmp[i]['amp'][1]['values'].append({'t':d[0],'y':d[5]})
							tmp[i]['amp'][2]['values'].append({'t':d[0],'y':d[6]})
							tmp[i]['watt'][0]['values'].append({'t':d[0],'y':d[7]})
							tmp[i]['watt'][1]['values'].append({'t':d[0],'y':d[8]})
							tmp[i]['watt'][2]['values'].append({'t':d[0],'y':d[9]})
							tmp[i]['ae'][0]['values'].append({'t':d[0],'y':d[10]})
				_cur.execute("select s.inf_id,bo.bomac from sensor as s inner join board as bo on bo.boid=s.boid inner join room as r on bo.rid=r.rid inner join floor as f on f.fid=r.fid inner join building as b on b.bid=f.bid where b.bid = %s",(data[i]['id']))
				sensor = _cur.fetchall()
				if(len(sensor) != 0):
					qry = "select sum(a) as a from ct where (time>="+str(startTime)+" and time<="+str(endTime)+") and "
					for index in range(len(sensor)):
						ct.append(sensor[index])
						if(index == len(sensor)-1):
							qry+='(MAC = \''+str(sensor[index]['bomac'])+'\' and s = '+str(sensor[index]['inf_id'])+') '
						else:
							qry+='(MAC = \''+str(sensor[index]['bomac'])+'\' and s = '+str(sensor[index]['inf_id'])+') or '
					qry+=' group by time('+unit+');'
					result = self._client.query(query=qry)
					if(len(result.raw['series'])>0):
						tmp[i]['ct'][0].update({'name':name+"_CT"})
						for d in result.raw['series'][0]['values']:
							tmp[i]['ct'][0]['values'].append({'t':d[0],'y':d[1]})
		if(len(dm) != 0):
			qry = "select sum(VL1) as VL1 ,sum(VL2) as VL2 ,sum(VL3) as VL3 ,sum(AL1) as AL1 ,sum(AL2) as AL2 ,sum(AL3) as AL3,sum(P1) as P1 ,sum(P2) as P2 ,sum(P3) as P3 ,sum(AE) as AE from dm where (time>="+str(startTime)+" and time<="+str(endTime)+") and "
			for index in range(len(dm)):
				if(index == len(dm)-1):
					qry+='MAC = \''+str(dm[index]['bomac'])+'\''
				else:
					qry+='MAC = \''+str(dm[index]['bomac'])+'\' or '
			qry+=' group by time('+unit+');'
			result = self._client.query(query=qry)
			if(len(result.raw['series'])>0):
				tmp2['volt'][0].update({'name':nameCombine+"_VL1"})
				tmp2['volt'][1].update({'name':nameCombine+"_VL2"})
				tmp2['volt'][2].update({'name':nameCombine+"_VL3"})
				tmp2['amp'][0].update({'name':nameCombine+"_AL1"})
				tmp2['amp'][1].update({'name':nameCombine+"_AL2"})
				tmp2['amp'][2].update({'name':nameCombine+"_AL3"})
				tmp2['watt'][0].update({'name':nameCombine+"_P1"})
				tmp2['watt'][1].update({'name':nameCombine+"_P2"})
				tmp2['watt'][2].update({'name':nameCombine+"_P3"})
				tmp2['ae'][0].update({'name':nameCombine+"_AE"})
				for d in result.raw['series'][0]['values']:
					tmp2['volt'][0]['values'].append({'t':d[0],'y':d[1]})
					tmp2['volt'][1]['values'].append({'t':d[0],'y':d[2]})
					tmp2['volt'][2]['values'].append({'t':d[0],'y':d[3]})
					tmp2['amp'][0]['values'].append({'t':d[0],'y':d[4]})
					tmp2['amp'][1]['values'].append({'t':d[0],'y':d[5]})
					tmp2['amp'][2]['values'].append({'t':d[0],'y':d[6]})
					tmp2['watt'][0]['values'].append({'t':d[0],'y':d[7]})
					tmp2['watt'][1]['values'].append({'t':d[0],'y':d[8]})
					tmp2['watt'][2]['values'].append({'t':d[0],'y':d[9]})
					tmp2['ae'][0]['values'].append({'t':d[0],'y':d[10]})
		if(len(ct) != 0):
			qry = "select sum(a) as a from ct where (time>="+str(startTime)+" and time<="+str(endTime)+") and "
			for index in range(len(ct)):
				if(index == len(ct)-1):
					qry+='(MAC = \''+str(ct[index]['bomac'])+'\' and s = '+str(ct[index]['inf_id'])+') '
				else:
					qry+='(MAC = \''+str(ct[index]['bomac'])+'\' and s = '+str(ct[index]['inf_id'])+') or '
			qry+=' group by time('+unit+');'
			result = self._client.query(query=qry)
			if(len(result.raw['series'])>0):
				tmp2['ct'][0].update({'name':nameCombine+"_CT"})
				for d in result.raw['series'][0]['values']:
					tmp2['ct'][0]['values'].append({'t':d[0],'y':d[1]})
		self._CloseCursor(_cur)
		if(graphType=="CompareAndSeparate"):
			return tmp
		if(graphType=="Combine"):
			return tmp2

	def sensor_list(self):
		res = self.fetchAll("SELECT s.inf_type,s.sid,s.sname,t.tname,r.rname,f.fname,b.bname,bo.bomac,r.rid,f.fid,b.bid FROM sensor AS s INNER JOIN board AS bo ON (s.boid=bo.boid) INNER JOIN room AS r ON (bo.rid=r.rid) INNER JOIN floor AS f ON (r.fid=f.fid) INNER JOIN building AS b ON (f.bid=b.bid) INNER JOIN type as t ON (s.tid=t.tid)")
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
				_cur.execute("SELECT rid,rname,rstatus FROM room WHERE fid = %s",(f['fid'],))
				room = _cur.fetchall()
				for r in room:
					f['room'].append(r)
				b['floor'].append(f)
		self._CloseCursor(_cur)
		return building

	def sensor_edit(self,sid,sname):
		self.execute("UPDATE sensor SET sname = %s WHERE sid = %s",(sname,sid))

	def sensor_del(self,sid):
		self.execute("DELETE FROM sensor WHERE sid = %s",(sid,))

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
		self.execute("INSERT INTO room (rname,fid) VALUES (%s,%s)",(rname,fid))

	def room_edit(self,rid,rname,fid):
		self.execute("UPDATE room SET rname = %s , fid = %s WHERE rid = %s",(rname,fid,rid))

	def room_del(self,rid):
		_cur = self._newCursor()
		_cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid SET board.register= 0 , board.rid=null WHERE room.rid = %s",(rid)) #SET board.rid to null and change board status to unregister
		_cur.execute("DELETE FROM room WHERE rid = %s",(rid,))
		self._CloseCursor(_cur)

	def floor_add(self,fname,bid):
		self.execute("INSERT INTO floor (fname,bid) VALUES (%s,%s)",(fname,bid))

	def floor_edit(self,fid,fname,bid):
		if(fid == 1):
			return
		self.execute("UPDATE floor SET fname = %s , bid = %s WHERE fid = %s",(fname,bid,fid))

	def floor_del(self,fid):
		if(fid == 1):
			return
		_cur = self._newCursor()
		_cur.execute("UPDATE board INNER JOIN room ON board.rid = room.rid INNER JOIN floor ON room.fid=floor.fid SET board.register= 0 , board.rid=null WHERE floor.fid = %s",(fid))
		_cur.execute("DELETE FROM room WHERE fid = %s",(fid,))
		_cur.execute("DELETE FROM floor WHERE fid = %s",(fid,))
		self._CloseCursor(_cur)

	def building_add(self,bname):
		self.execute("INSERT INTO building (bname) VALUES (%s)",(bname,))

	def building_edit(self,bid,bname):
		if(bid == 1):
			return
		self.execute("UPDATE building SET bname = %s WHERE bid = %s",(bname,bid))

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
		self.execute("INSERT INTO `user` (`username`, `email`, `password`, `is_active`, `flogout`, `create_time`) VALUES (%s, %s, %s, '0', '0', CURRENT_TIMESTAMP)",
			(user,email,password))

	def get_userByid(self,id):
		res = self.fetchOne("SELECT * FROM `user` WHERE `id` = %s",(id,))
		return res

	def get_userLogin(self,user):
		res = self.fetchOne("SELECT * FROM `user` WHERE (`username` = %s OR `email` = %s)",(user,user))
		return res

	def building_list(self):
		res = self.fetchAll("SELECT * FROM building")
		return res

	def floor_list(self,bid):
		res = self.fetchAll("SELECT * FROM floor where bid = %s",(bid,))
		return res

	def room_list(self,fid):
		res = self.fetchAll("SELECT * FROM room where fid = %s",(fid,))
		return res

	def getAllType(self):
		res = self.fetchAll("SELECT * FROM type")
		return res

	def AddRule(self,rname,rjson):
		self.execute('INSERT INTO `rule` (`ruid`, `rname`, `rjson`) VALUES (NULL, %s, %s)',(rname,rjson))

	def UpdateRule(self,ruid,rname,rjson):
		self.execute("UPDATE `rule` SET rname = %s,rjson = %s WHERE ruid = %s",(rname,rjson,ruid))

	def getRule(self):
		res = self.fetchAll("SELECT * FROM rule")
		return res

	def DeleteRule(self,ruid):
		self.execute("DELETE FROM rule WHERE ruid = %s",(ruid,))

	def new_log(self,message,token):
		_cur = self._newCursor()
		_cur.execute("DELETE FROM logs WHERE create_time <	(CURRENT_TIMESTAMP - INTERVAL 3 MONTH)")
		_cur.execute("INSERT INTO `logs` (`lid`, `message`, `create_time`) VALUES (NULL, %s, CURRENT_TIMESTAMP)",(message,))
		_cur.execute("UPDATE `notify` SET `nlast_time` = CURRENT_TIMESTAMP WHERE `notify`.`ntoken` = %s",(token,))
		self._CloseCursor(_cur)

	def get_logs(self):
		res = self.fetchAll("SELECT * from logs")
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

	def Updatepassword(self,username,password):
		self.execute("UPDATE `user` SET password = %s WHERE username = %s",(password,username))

	def getAllUser(self):
		res = self.fetchAll("SELECT * FROM user")
		return res

	def UpdateUserActive(self,_id,activate):
		self.execute("UPDATE `user` SET is_active = %s WHERE id = %s",(activate,_id))

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

	def getToken(self):
		res = self.fetchAll("SELECT * FROM notify")
		return res

		
	def updateNotiTime(self,unitSec):
		self.execute("UPDATE `notify` SET ntime= %s",(unitSec))
		
	def updateNotiToken(self,token):
		self.execute("UPDATE `notify` SET ntoken= %s",(token))


	def getRoomSensor(self,rname):
		res = self.fetchAll("""SELECT s.inf_id,s.inf_type,b.bomac,t.inf_name FROM sensor s 
								INNER JOIN type t ON s.tid = t.tid 
								INNER JOIN board b ON s.boid = b.boid 
								INNER JOIN room r ON b.rid = r.rid 
								WHERE s.inf_type IS NOT NULL AND r.rname = %s AND b.register = 1""",(rname,))
		return res

