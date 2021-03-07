from flask import escape
from config import Config, ProductionConfig, DevelopmentConfig
from db import MySQL, InfluxDB, Query

mysql = MySQL()
influx = InfluxDB()
query = Query()

def html_escape(inp):
	return str(escape(inp))

def toHourandMin(timeDel):
	secs = timeDel.total_seconds()
	hours = int(secs / 3600)
	minutes = int(secs / 60) % 60
	return "%02d:%02d" % (hours, minutes)

def getConfig():
	cfg = ProductionConfig
	if Config.ENABLE_DEV:
		cfg = DevelopmentConfig
	return cfg