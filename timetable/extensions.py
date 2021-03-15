from flask import escape
from config import Config, ProductionConfig, DevelopmentConfig
from db import MySQL, InfluxDB, Query

mysql = MySQL()
influx = InfluxDB()
query = Query()

def html_escape(inp):
	return str(escape(inp))

def getConfig():
	cfg = ProductionConfig
	if Config.ENABLE_DEV:
		cfg = DevelopmentConfig
	return cfg