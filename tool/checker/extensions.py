from flask import escape
from config import Config
from db import MySQL, MongoDB, Query

mysql = MySQL()
mongoDB = MongoDB()
query = Query()

def html_escape(inp):
	return str(escape(inp))

def toHourandMin(timeDel):
	secs = timeDel.total_seconds()
	hours = int(secs / 3600)
	minutes = int(secs / 60) % 60
	return "%02d:%02d" % (hours, minutes)

def getConfig():
	return Config