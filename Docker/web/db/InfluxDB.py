from influxdb import InfluxDBClient

class InfluxDB:
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
		self._client = InfluxDBClient(self._app["INFLUX_HOST"], 8086, self._app["INFLUX_USER"], self._app["INFLUX_PASSWORD"], self._app["INFLUX_DB"])
		return self._client

	def connect_cfg(self):
		self._client = InfluxDBClient(self._app.INFLUX_HOST, 8086, self._app.INFLUX_USER, self._app.INFLUX_PASSWORD, self._app.INFLUX_DB)
		return self._client
		
	def get_client(self):
		if not self._client:
			return self.connect()
		return self._client