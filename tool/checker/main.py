import time, checker
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

# @tl.job(interval=timedelta(seconds=10))
# def ruleChecker():
# 	try:
# 		checker.checkRule()
# 	except Exception as e:
# 		print("Except: ", e)

@tl.job(interval=timedelta(seconds=10))
def scheduleChecker():
	try:
		checker.checkSchedule()
	except Exception as e:
		print("Except: ", e)

@tl.job(interval=timedelta(seconds=10))
def sensorChecker():
	try:
		checker.updateNewsensor()
	except Exception as e:
		print("Except: ", e)
		
tl.start()

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		tl.stop()
		break