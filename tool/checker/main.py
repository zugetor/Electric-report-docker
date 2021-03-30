import time, check
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

@tl.job(interval=timedelta(seconds=3))
def sample_job_every_2s():
    print("2s job current time : {}".format(time.ctime()))
    try:
        check.auto_sensor()
    except:
        print("Execution expired")

tl.start()

while True:
  try:
    time.sleep(1)
  except KeyboardInterrupt:
    tl.stop()
    break