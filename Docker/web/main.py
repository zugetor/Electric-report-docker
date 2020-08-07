from flask import Flask, render_template, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from route import private, page, public
from extensions import mysql, influx, query, html_escape, getConfig
from checker import checkRule, checkSchedule, updateNewsensor
import atexit

cfg = getConfig()

app = Flask(__name__)
app.config.from_object(cfg)

mysql.init_app(app.config)
influx.init_app(app.config)
query.init_db(mysql.get_connection(), influx.get_client())

app.register_blueprint(page.app)
app.register_blueprint(private.app, url_prefix="/api/private")
app.register_blueprint(public.app, url_prefix="/api/public")

scheduler = BackgroundScheduler()
scheduler.add_job(func=checkRule, trigger="interval", minutes=cfg.RULE_UPDATE)
scheduler.add_job(func=checkSchedule, trigger="interval", minutes=cfg.SCHEDULE_UPDATE)
scheduler.add_job(func=updateNewsensor, trigger="interval", minutes=cfg.SENSOR_UPDATE)

scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def index():
	return redirect(url_for('Page.graph_view'))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(403)
def page_forbidden(e):
	return render_template('403.html'), 403

@app.errorhandler(405)
def method_not_allow(e):
	return render_template('405.html'), 405

@app.errorhandler(500)
def server_error(e):
	return render_template('500.html'), 500

if __name__ == "__main__":
	app.run()