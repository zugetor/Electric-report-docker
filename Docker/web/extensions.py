from flask import escape
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