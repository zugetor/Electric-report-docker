from flask import Flask, render_template
from route import private, page
from config import ProductionConfig, DevelopmentConfig, TestingConfig
from extensions import mysql, influx, query, html_escape

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

mysql.init_app(app.config)
influx.init_app(app.config)
query.init_db(mysql.get_connection(), mysql.get_cursor(), influx.get_client())

app.register_blueprint(page.app)
app.register_blueprint(private.app, url_prefix="/api/private")

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