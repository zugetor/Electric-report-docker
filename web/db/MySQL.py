import pymysql

class MySQL:
	def __init__(self):
		self._app = None
		self._conn = None

	def init_app(self, app):
		self._app = app
		self.connect()

	def init_cfg(self, cfg):
		self._app = cfg
		self.connect_cfg()

	def connect(self):
		self._conn = pymysql.connect(host=self._app["MYSQL_HOST"], user=self._app["MYSQL_USER"], password=self._app["MYSQL_PASSWORD"], db=self._app["MYSQL_DB"],
						cursorclass=pymysql.cursors.DictCursor, autocommit=True)

	def connect_cfg(self):
		self._conn = pymysql.connect(host=self._app.MYSQL_HOST, user=self._app.MYSQL_USER, password=self._app.MYSQL_PASSWORD, db=self._app.MYSQL_DB,
						cursorclass=pymysql.cursors.DictCursor, autocommit=True)
		
	def get_connection(self):
		if self._conn == None or not self._conn.open:
			try:
				self.connect()
			except:
				self.connect_cfg()
		return self._conn

	def close(self):
		return self._conn.close()