from flask import Blueprint, jsonify, request
from extensions import query

app = Blueprint('DEMO', __name__)

@app.route('/demo')
def demo():
    return jsonify(query.demo1())
    
@app.route('/demo2')
def demo2():
    return jsonify(query.demo2())
    
@app.route('/sensor/list',methods=['GET'])
def sensor_list():
    return jsonify(query.sensor_list())
    
@app.route('/room/list',methods=['GET'])
def room_list():
    return jsonify(query.room_list())
    
    
@app.route('/sensor/edit',methods=['POST'])
def sensor_edit():
    sid = request.form['sid']
    sname = request.form['sname']
    query.sensor_edit(sid,sname)
    return '200 OK EDIT'
    
@app.route('/sensor/del',methods=['DELETE'])
def sensor_del():
    sid = request.form['sid']
    query.sensor_del(sid)
    return '200 OK DELETE'
    
@app.route('/register/list',methods=['GET'])
def register_list():
    return jsonify(query.register_list())
