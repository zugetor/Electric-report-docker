from notify import linenotify
from extensions import query
import datetime, pytz, reg

def checkRule():
	return None

def checkSchedule(TIME_ZONE="Asia/Bangkok"):
	allroom = query.roomWithBPrefix()
	burl = allroom[0]["burl"]
	allSchedule = reg.getAllSchedule(burl)
	tz = pytz.timezone(TIME_ZONE)
	now1 = datetime.datetime.now(tz)
	today = datetime.date.today()
	for room in allroom:
		if room["burl"] != burl:
			burl = room["burl"]
			allSchedule = reg.getAllSchedule(burl)
		roomSchedule = allSchedule.loc[(allSchedule['ROOM'] == room["rname"]) &
						(allSchedule['Day/Time'] == today),"{}:00-{}:00".format(now1.hour,now1.hour+1)]
		if len(roomSchedule) > 0 and roomSchedule[roomSchedule.index[0]]:
			query.UpdateRoomStatue(1,room["rname"])
		else:
			query.UpdateRoomStatue(0,room["rname"])

def updateNewsensor():
	return None