from flask import Blueprint, render_template, request

app = Blueprint('Page', __name__)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/graph_view")
def graph_view():
    return render_template("graph_view.html")

@app.route("/logs")
def logs():
    return render_template("logs.html")

@app.route("/settings")
def settings():
    return render_template("notification - setting.html")

@app.route("/sensor_add")
def sensor_add():
    return render_template("sensor_add_v1.html")

@app.route("/conditions")
def conditions():
    return render_template("sensor_condition.html")

@app.route("/sensor_view")
def sensor_view():
    return render_template("sensor_view.html")    