from flask import escape
from db import MySQL, InfluxDB, Query

mysql = MySQL()
influx = InfluxDB()
query = Query()

def html_escape(inp):
	return str(escape(inp))