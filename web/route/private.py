from flask import Blueprint, jsonify, request, escape, session, Response
from extensions import query, html_escape, toHourandMin
from login import login_required
import json, time, hashlib

app = Blueprint('Private', __name__)

@app.route('/dashboard_list/',methods=['POST'])
def dashboard_list():
	data = json.loads(request.form.get('data'))
	unit = request.form.get('unit')
	startTime = request.form.get('startTime')
	endTime = request.form.get('endTime')
	graphType = request.form.get('graphType')
	response = jsonify(query.dashboard.dashboard_list(data,int(unit),startTime,endTime,graphType))
	# response = query.dashboard_list(data,unit,startTime,endTime,graphType)
	return response

@app.route('/sensor/',methods=['GET'])
@login_required
def sensor_list():
	response = jsonify(query.sensor.sensor_list())
	return response
	
@app.route('/allroom/',methods=['GET'])
@login_required
def all_room_list():
	response = jsonify(query.building.all_room_list())
	return response
	
@app.route('/register',methods=['GET'])
@login_required
def register_list():
	return jsonify(query.board.register_list())
	
@app.route('/sensor/',methods=['POST'])
@login_required
def sensor_edit():
	sid = request.form.get('id')
	sname = html_escape(request.form.get('name'))
	print(request.form)
	query.sensor.sensor_edit(sid,sname)
	response = jsonify({'Code':'200 ok'})
	return response
	
@app.route('/sensor/del',methods=['GET'])
@login_required
def sensor_del():
	sid = request.args.get('id')
	query.sensor.sensor_del(sid)
	response = jsonify({'Code':'200 ok'})
	return response
	
@app.route('/register/del',methods=['GET'])
@login_required
def register_del():
	boid = request.args.get('id')
	query.board.register_del(boid)
	response = jsonify({'Code':'200 ok'})
	return response
	

@app.route('/register',methods=['POST'])
@login_required
def register_register():
	boid = request.form['id']
	room = request.form['room']
	sensor = json.loads(request.form.get('sensor'))
	query.board.register_register(boid,sensor,room)
	return jsonify({'Code':'200 ok'})
	
@app.route('/room/',methods=['GET'])
@login_required
def room_list():
	fid = request.args.get('fid')
	return jsonify(query.building.room_list(fid))
	
@app.route('/room',methods=['POST'])
@login_required
def room_add():
	rname = html_escape(request.form['rname'])
	fid = request.form['fid']
	query.building.room_add(rname,fid)
	return '200 OK ADD ROOM'
	
@app.route('/room/edit',methods=['POST'])
@login_required
def room_edit():
	rid = request.form['rid']
	rname = html_escape(request.form['rname'])
	fid = request.form['fid']
	query.building.room_edit(rid,rname,fid)
	return '200 OK EDIT ROOM'
	
@app.route('/room/del',methods=['GET'])
@login_required
def room_del():
	rid = request.args.get('rid')
	query.building.room_del(rid)
	return '200 OK DEL ROOM'
	
@app.route('/floor/',methods=['GET'])
@login_required
def floor_list():
	bid = request.args.get('bid')
	return jsonify(query.building.floor_list(bid))
	
@app.route('/floor/',methods=['POST'])
@login_required
def floor_add():
	fname = html_escape(request.form['fname'])
	bid = request.form['bid']
	query.building.floor_add(fname,bid)
	return '200 OK ADD FLOOR'
	
@app.route('/floor/edit',methods=['POST'])
@login_required
def floor_edit():
	fid = request.form['fid']
	fname = html_escape(request.form['fname'])
	bid = request.form['bid']
	query.building.floor_edit(fid,fname,bid)
	return '200 OK EDIT FLOOR'
	
@app.route('/floor/del',methods=['GET'])
@login_required
def floor_del():
	fid = request.args.get('fid')
	query.building.floor_del(fid)
	return '200 OK DEL FLOOR'
	
@app.route('/building/',methods=['GET'])
@login_required
def building_list():
	return jsonify(query.building.building_list())
	
@app.route('/building/',methods=['POST'])
@login_required
def building_add():
	bname = html_escape(request.form['bname'])
	query.building.building_add(bname)
	return '200 OK ADD BUILDING'
	
@app.route('/building/edit',methods=['POST'])
@login_required
def building_edit():
	bid = request.form['bid']
	bname = html_escape(request.form['bname'])
	query.building.building_edit(bid,bname)
	return '200 OK EDIT BUILDING'
	
@app.route('/building/del',methods=['GET'])
@login_required
def building_del():
	bid = request.args.get('bid')
	query.building.building_del(bid)
	return '200 OK DEL BUILDING'

@app.route('/rule/',methods=['POST'])
@login_required
def rule_add():
	name = request.form.get('name')
	data = request.form.get('data')
	query.rule.AddRule(name,data)
	return jsonify({'Code':'200 OK'})

@app.route('/rule/edit',methods=['POST'])
@login_required
def rule_edit():
	_id = request.form.get('id')
	name = request.form.get('name')
	data = request.form.get('data')
	query.rule.UpdateRule(_id,name,data)
	return jsonify({'Code':'200 OK'})

@app.route('/rule/',methods=['GET'])
@login_required
def rule_view():
	rule = query.rule.getRule()
	return jsonify(rule)

@app.route("/rule/del",methods=["GET"])
@login_required
def rule_del():
	_id = request.args.get('id')
	query.rule.DeleteRule(_id)
	return jsonify({'Code':'200 OK'})
  
@app.route('/logs/',methods=['GET'])
@login_required
def logs_list():
	return jsonify(query.logs.get_logs())
	
@app.route('/sumLogs/',methods=['GET'])
@login_required
def summary_logs():
	return jsonify(query.logs.summary_logs())

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
	query.user.UpdateUserActive(_id,_allow)
	return jsonify({'Code':'200 OK'})
	
	
@app.route('/notify/time/edit',methods=['POST'])
@login_required
def notify_time_edit():
	unitSec = html_escape(request.form['unitSec'])
	query.notification.updateNotiTime(session['id'],unitSec)
	return '200 OK EDIT Notify'

	
@app.route('/notify/token/edit',methods=['POST'])
@login_required
def notify_token_edit():
	token = html_escape(request.form['token'])
	query.notification.updateNotiToken(session['id'],token)
	return '200 OK EDIT Notify'
	
@app.route('/token/',methods=['GET'])
@login_required
def get_token():
	return jsonify(query.notification.getToken(session['id']))

@app.route('/link',methods=['GET'])
def get_setting():
	data = request.args.get('hash')
	res = query.getSetting(data)
	if(res == None):
		return jsonify({"data": "","hash": ""})
	return jsonify({"data": res["data"],"hash": res["hash"]})

@app.route('/link',methods=['POST'])
@login_required
def set_setting():
	data = request.form.get('data')
	try:
		data = json.dumps(json.loads(data)) #minify json
	except:
		print("JSON Decode error")
	digest = hashlib.md5(data.encode()).hexdigest()
	if(data == "" or data == None):
		return Response('{"Code":"400 Bad request"}', status=400, content_type="application/json")
	res = query.newSetting(data, digest)
	# if(res.inserted_id == "" or res.inserted_id == None):
	# 	return Response('{"Code":"500 Internal Server Error"}', status=500, content_type="application/json")
	return jsonify({"Code": "200 OK", "hash": digest})