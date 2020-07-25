from flask import Blueprint, jsonify, request, escape
from extensions import query, html_escape, toHourandMin
from login import login_required
import json, time

app = Blueprint('Private', __name__)

@app.route('/dashboard_list/',methods=['POST'])
@login_required
def dashboard_list():
	data = json.loads(request.form.get('data'))
	unit = request.form.get('unit')
	startTime = request.form.get('startTime')
	endTime = request.form.get('endTime')
	response = jsonify(query.dashboard_list(data,unit,startTime,endTime))
	return response

@app.route('/sensor/',methods=['GET'])
@login_required
def sensor_list():
	response = jsonify(query.sensor_list())
	return response
	
@app.route('/allroom/',methods=['GET'])
@login_required
def all_room_list():
	response = jsonify(query.all_room_list())
	return response
	
@app.route('/register',methods=['GET'])
@login_required
def register_list():
	return jsonify(query.register_list())
	
@app.route('/sensor/',methods=['POST'])
@login_required
def sensor_edit():
	sid = request.form.get('id')
	sname = html_escape(request.form.get('name'))
	print(request.form)
	query.sensor_edit(sid,sname)
	response = jsonify({'Code':'200 ok'})
	return response
	
@app.route('/sensor/del',methods=['GET'])
@login_required
def sensor_del():
	sid = request.args.get('id')
	query.sensor_del(sid)
	response = jsonify({'Code':'200 ok'})
	return response
	
@app.route('/register/del',methods=['GET'])
@login_required
def register_del():
	boid = request.args.get('id')
	query.register_del(boid)
	

@app.route('/register',methods=['POST'])
@login_required
def register_register():
	boid = request.form['id']
	room = request.form['room']
	sensor = json.loads(request.form.get('sensor'))
	query.register_register(boid,sensor,room)
	return jsonify({'Code':'200 ok'})
	
@app.route('/room/',methods=['GET'])
@login_required
def room_list():
	fid = request.args.get('fid')
	return jsonify(query.room_list(fid))
	
@app.route('/room',methods=['POST'])
@login_required
def room_add():
	rname = html_escape(request.form['rname'])
	fid = request.form['fid']
	query.room_add(rname,fid)
	return '200 OK ADD ROOM'
	
@app.route('/room/edit',methods=['POST'])
@login_required
def room_edit():
	rid = request.form['rid']
	rname = html_escape(request.form['rname'])
	fid = request.form['fid']
	query.room_edit(rid,rname,fid)
	return '200 OK EDIT ROOM'
	
@app.route('/room/del',methods=['GET'])
@login_required
def room_del():
	rid = request.args.get('rid')
	query.room_del(rid)
	return '200 OK DEL ROOM'
	
@app.route('/floor/',methods=['GET'])
@login_required
def floor_list():
	bid = request.args.get('bid')
	return jsonify(query.floor_list(bid))
	
@app.route('/floor/',methods=['POST'])
@login_required
def floor_add():
	fname = html_escape(request.form['fname'])
	bid = request.form['bid']
	query.floor_add(fname,bid)
	return '200 OK ADD FLOOR'
	
@app.route('/floor/edit',methods=['POST'])
@login_required
def floor_edit():
	fid = request.form['fid']
	fname = html_escape(request.form['fname'])
	bid = request.form['bid']
	query.floor_edit(fid,fname,bid)
	return '200 OK EDIT FLOOR'
	
@app.route('/floor/del',methods=['GET'])
@login_required
def floor_del():
	fid = request.args.get('fid')
	query.floor_del(fid)
	return '200 OK DEL FLOOR'
	
@app.route('/building/',methods=['GET'])
@login_required
def building_list():
	return jsonify(query.building_list())
	
@app.route('/building/',methods=['POST'])
@login_required
def building_add():
	bname = html_escape(request.form['bname'])
	query.building_add(bname)
	return '200 OK ADD BUILDING'
	
@app.route('/building/edit',methods=['POST'])
@login_required
def building_edit():
	bid = request.form['bid']
	bname = html_escape(request.form['bname'])
	query.building_edit(bid,bname)
	return '200 OK EDIT BUILDING'
	
@app.route('/building/del',methods=['GET'])
@login_required
def building_del():
	bid = request.args.get('bid')
	query.building_del(bid)
	return '200 OK DEL BUILDING'

@app.route('/rule/',methods=['POST'])
@login_required
def rule_add():
	name = request.form.get('name')
	data = request.form.get('data')
	query.AddRule(name,data)
	return jsonify({'Code':'200 OK'})

@app.route('/rule/edit',methods=['POST'])
@login_required
def rule_edit():
	_id = request.form.get('id')
	name = request.form.get('name')
	data = request.form.get('data')
	query.UpdateRule(_id,name,data)
	return jsonify({'Code':'200 OK'})

@app.route('/rule/',methods=['GET'])
@login_required
def rule_view():
	rule = query.getRule()
	return jsonify(rule)

@app.route("/rule/del",methods=["GET"])
@login_required
def rule_del():
	_id = request.args.get('id')
	query.DeleteRule(_id)
	return jsonify({'Code':'200 OK'})
  
@app.route('/logs/',methods=['GET'])
@login_required
def logs_list():
	return jsonify(query.get_logs())
	
@app.route('/sumLogs/',methods=['GET'])
@login_required
def summary_logs():
	return jsonify(query.summary_logs())

@app.route("/autoadd",methods=["POST"])
@login_required
def auto_add():
	prefix = request.form.get('prefix')
	data = json.loads(request.form.get('data'))
	query.auto_add_room(prefix,data)
	return jsonify({'Code':'200 OK'})

@app.route("/active",methods=["GET"])
@login_required
def user_active():
	_id = request.args.get('id')
	_allow = request.args.get('allow')
	try:
		if int(_allow) != 0 and int(_allow) != 1:
			_allow = 0
	except:
		_allow = 0
	query.UpdateUserActive(_id,_allow)
	return jsonify({'Code':'200 OK'})