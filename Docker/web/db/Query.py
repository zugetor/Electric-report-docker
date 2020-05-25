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