from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from route import private, page, public
from config import ProductionConfig, DevelopmentConfig, TestingConfig
from extensions import mysql, influx, query, html_escape
from checker import checkRule, checkSchedule
import atexit

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

mysql.init_app(app.config)
influx.init_app(app.config)
query.init_db(mysql.get_connection(), influx.get_client())

app.register_blueprint(page.app)
app.register_blueprint(private.app, url_prefix="/api/private")
app.register_blueprint(public.app, url_prefix="/api/public")

scheduler = BackgroundScheduler()
scheduler.add_job(func=checkRule, trigger="interval", minutes=5)
scheduler.add_job(func=checkSchedule, trigger="interval", hours=1)

scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def index():
	return render_template("sensor_view.html")

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