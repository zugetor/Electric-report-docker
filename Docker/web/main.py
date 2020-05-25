from flask import Flask
from route import demo
from config import ProductionConfig, DevelopmentConfig, TestingConfig
from extensions import mysql, influx, query

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

mysql.init_app(app.config)
influx.init_app(app.config)
query.init_db(mysql.get_connection(), mysql.get_cursor(), influx.get_client())

app.register_blueprint(demo.app, url_prefix="/api")
app.register_blueprint(demo.app)

@app.route("/")
def index():
    return "<h1>Hello World</h1>"

if __name__ == "__main__":
	app.run()