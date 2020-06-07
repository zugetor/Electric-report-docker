from flask import Blueprint, jsonify, request, escape
from extensions import query, html_escape

app = Blueprint('Private', __name__)
    
@app.route('/sensor/',methods=['GET'])
def sensor_list():
    response = jsonify(query.sensor_list())
    return response
    
@app.route('/room/',methods=['GET'])
def all_room_list():
    response = jsonify(query.all_room_list())
    return response
    
@app.route('/register/',methods=['GET'])
def register_list():
    return jsonify(query.register_list())
    
@app.route('/sensor',methods=['POST'])
def sensor_edit():
    sid = request.get_json()['sid']
    sname = html_escape(request.get_json()['sname'])
    query.sensor_edit(sid,sname)
    response = jsonify({'Code':'200 ok'})
    return response
    
@app.route('/sensor/del',methods=['GET'])
def sensor_del():
    sid = request.args.get('id')
    query.sensor_del(sid)
    response = jsonify({'Code':'200 ok'})
    return response
    
@app.route('/register/del',methods=['GET'])
def register_del():
    boid = request.args.get('id')
    query.register_del(boid)
    return jsonify({'Code':'200 ok'})

#@app.route('/register',methods=['POST'])
#def register_add():
    #bomac = request.form['bomac']
    #sensor = request.form['sensor']
    #query.register_add(bomac,sensor)
    #return jsonify(query.register_add(bomac,sensor))
    
@app.route('/room',methods=['POST'])
def room_add():
    rname = html_escape(request.form['rname'])
    fid = request.form['fid']
    query.room_add(rname,fid)
    return '200 OK ADD ROOM'
    
@app.route('/room/edit',methods=['POST'])
def room_edit():
    rid = request.form['rid']
    rname = html_escape(request.form['rname'])
    fid = request.form['fid']
    query.room_edit(rid,rname,fid)
    return '200 OK EDIT ROOM'
    
@app.route('/room/del',methods=['GET'])
def room_del():
    rid = request.args.get('id')
    query.room_del(rid)
    return '200 OK DEL ROOM'
    
@app.route('/floor/',methods=['POST'])
def floor_add():
    fname = html_escape(request.form['fname'])
    bid = request.form['bid']
    query.floor_add(fname,bid)
    return '200 OK ADD FLOOR'
    
@app.route('/floor/edit',methods=['POST'])
def floor_edit():
    fid = request.form['fid']
    fname = html_escape(request.form['fname'])
    bid = request.form['bid']
    query.floor_edit(fid,fname,bid)
    return '200 OK EDIT FLOOR'
    
@app.route('/floor/del',methods=['GET'])
def floor_del():
    fid = request.args.get('id')
    query.floor_del(fid)
    return '200 OK DEL FLOOR'
    
    
@app.route('/building/',methods=['POST'])
def building_add():
    bname = html_escape(request.form['bname'])
    query.building_add(bname)
    return '200 OK ADD BUILDING'
    
@app.route('/building/edit',methods=['POST'])
def building_edit():
    bid = request.form['bid']
    bname = html_escape(request.form['bname'])
    query.building_edit(bid,bname)
    return '200 OK EDIT BUILDING'
    
@app.route('/building/del',methods=['GET'])
def building_del():
    bid = request.args.get('id')
    query.building_del(bid)
    return '200 OK DEL BUILDING'