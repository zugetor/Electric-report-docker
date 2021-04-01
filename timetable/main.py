from flask import Flask, render_template, redirect, url_for, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from extensions import mysql, query, html_escape, getConfig
from route import public

cfg = getConfig()

app = Flask(__name__)
app.config.from_object(cfg)

app.register_blueprint(public.app, url_prefix="/api/public")

if __name__ == "__main__":
	app.run()