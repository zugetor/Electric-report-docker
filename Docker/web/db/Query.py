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
        self._cur.execute('''SELECT * FROM user''')
        res = self._cur.fetchall()
        return res
        
    def demo2(self):
        result = self._client.query("SELECT * FROM mqtt_consumer;")
        return result.raw
        
    def sensor_list(self):
        self._cur.execute('''SELECT s.sid,s.sname,t.tname,r.rname,f.fname,b.bname,bo.bomac FROM sensor AS s INNER JOIN board AS bo ON (s.boid=bo.boid) INNER JOIN room AS r ON (bo.rid=r.rid) INNER JOIN floor AS f ON (r.fid=f.fid) INNER JOIN building AS b ON (f.bid=b.bid) INNER JOIN type as t ON (s.tid=t.tid)''')
        res = self._cur.fetchall()
        return res
        
    def room_list(self):
        self._cur.execute('''SELECT * FROM building''')
        building = self._cur.fetchall()
        self._cur.execute('''SELECT * FROM floor''')
        floor = self._cur.fetchall()
        self._cur.execute('''SELECT * FROM room''')
        room = self._cur.fetchall()
        for b in building:
            b.update({"floor":[]})
            
            for f in floor:
                f.update({'room':[]});
                if(b['bid']==f['bid']):  # select * from floor where f.bid= %s (b.bid)
                    for r in room: 
                        if(f['fid']==r['fid']): # select * from room where r.fid= %s (f.fid)
                            f['room'].append({'rid':r['rid'],'rname':r['rname']})
                    b['floor'].append({'fid':f['fid'],'fname':f['fname'],'room':f['room']})
                    
        return building
        
    def sensor_edit(self,sid,sname):
        self._cur.execute("UPDATE sensor SET sname = %s WHERE sid = %s",(sname,sid))
        
    def sensor_del(self,sid):
        self._cur.execute("DELETE FROM sensor WHERE sid = %s",(sid))
        
    def register_list(self):
        self._cur.execute('''SELECT * FROM board''')
        board = self._cur.fetchall()
        self._cur.execute('''SELECT * FROM sensor''')
        sensor = self._cur.fetchall()
        for bo in board:
            bo.update({'sensor':[]})
            light=0
            air=0
            elec=0
            for s in sensor:
                if(bo['boid']==s['boid']):
                #SELECT COUNT(CASE WHEN tid = 1 THEN 1 END) AS light ,COUNT(CASE WHEN tid = 2 THEN 1 END) AS elec  ,COUNT(CASE WHEN tid = 3 THEN 1 END) AS air FROM YourTable
                    bo['sensor'].append(s)
                    if(s['tid']==1):
                        light=light+1
                    if(s['tid']==2):
                        elec=elec+1
                    if(s['tid']==3):
                        air=air+1
            bo.update({'type':{'light':light,'elec':elec,'air':air}})
                    
        return board
    