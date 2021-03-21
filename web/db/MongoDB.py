import pymongo 

class MongoDB:
	def __init__(self):
		self._app = None
		self._client = None

	def init_app(self, app):
		self._app = app
		self.connect()

	def init_cfg(self, cfg):
		self._app = cfg
		self.connect_cfg()

	def connect(self):
		self._client = pymongo.MongoClient(self._app["MONGODB_URL"])
		return self._client

	def connect_cfg(self):
		self._client = pymongo.MongoClient(self._app.MONGODB_URL)
		return self._client
		
	def get_client(self):
		if not self._client:
			try:
				return self.connect()
			except:
				return self.connect_cfg()
		return self._client