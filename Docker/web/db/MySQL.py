import pymysql

class MySQL:
	def __init__(self):
		self._app = None
		self._conn = None

	def init_app(self, app):
		self._app = app
		self.connect()

	def connect(self):
		self._conn = pymysql.connect(host=self._app["MYSQL_HOST"], user=self._app["MYSQL_USER"], password=self._app["MYSQL_PASSWORD"], db=self._app["MYSQL_DB"],
						cursorclass=pymysql.cursors.DictCursor, autocommit=True)
		
	def get_connection(self):
		if not self._conn:
			self.connect()
		return self._conn