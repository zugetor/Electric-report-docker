from flask import Flask, render_template, redirect, url_for, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from extensions import mysql, influx, query, html_escape, getConfig
from checker import checkRule, checkSchedule, updateNewsensor
import atexit

cfg = getConfig()

app = Flask(__name__)
app.config.from_object(cfg)

mysql.init_app(app.config)
influx.init_app(app.config)
query.init_db(mysql.get_connection(), influx.get_client())



job_config = {'max_instances': 10}

scheduler = BackgroundScheduler(job_defaults=job_config)
scheduler.add_job(func=checkRule, trigger="interval", minutes=cfg.RULE_UPDATE)
scheduler.add_job(func=checkSchedule, trigger="interval", minutes=cfg.SCHEDULE_UPDATE)
scheduler.add_job(func=updateNewsensor, trigger="interval", minutes=cfg.SENSOR_UPDATE)

scheduler.start()
atexit.register(lambda: scheduler.shutdown())



if __name__ == "__main__":
	app.run()