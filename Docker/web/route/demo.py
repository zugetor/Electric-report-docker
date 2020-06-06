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
    response = jsonify(query.sensor_list())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    
@app.route('/room/list',methods=['GET'])
def all_room_list():
    response = jsonify(query.all_room_list())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    
    
@app.route('/sensor/edit',methods=['PUT'])
def sensor_edit():
    sid = request.get_json()['sid']
    sname = request.get_json()['sname']
    query.sensor_edit(sid,sname)
    response = jsonify({'Code':'200 ok'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    
@app.route('/sensor/del',methods=['DELETE'])
def sensor_del():
    sid = request.get_json()['sid']
    query.sensor_del(sid)
    response = jsonify({'Code':'200 ok'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    
@app.route('/register/list',methods=['GET'])
def register_list():
    return jsonify(query.register_list())
    
@app.route('/register/del',methods=['DELETE'])
def register_del():
    boid = request.form['boid']
    query.register_del(boid)
    return '200 OK DELETE'

#@app.route('/register/add',methods=['POST'])
#def register_add():
    #bomac = request.form['bomac']
    #sensor = request.form['sensor']
    #query.register_add(bomac,sensor)
    #return jsonify(query.register_add(bomac,sensor))
    
@app.route('/room/add',methods=['POST'])
def room_add():
    rname = request.form['rname']
    fid = request.form['fid']
    query.room_add(rname,fid)
    return '200 OK ADD ROOM'
    
@app.route('/room/edit',methods=['PUT'])
def room_edit():
    rid = request.form['rid']
    rname = request.form['rname']
    fid = request.form['fid']
    query.room_edit(rid,rname,fid)
    return '200 OK EDIT ROOM'
    
@app.route('/room/del',methods=['DELETE'])
def room_del():
    rid = request.form['rid']
    query.room_del(rid)
    return '200 OK DEL ROOM'
    
@app.route('/floor/add',methods=['POST'])
def floor_add():
    fname = request.form['fname']
    bid = request.form['bid']
    query.floor_add(fname,bid)
    return '200 OK ADD FLOOR'
    
@app.route('/floor/edit',methods=['PUT'])
def floor_edit():
    fid = request.form['fid']
    fname = request.form['fname']
    bid = request.form['bid']
    query.floor_edit(fid,fname,bid)
    return '200 OK EDIT FLOOR'
    
@app.route('/floor/del',methods=['DELETE'])
def floor_del():
    fid = request.form['fid']
    query.floor_del(fid)
    return '200 OK DEL FLOOR'
    
    
@app.route('/building/add',methods=['POST'])
def building_add():
    bname = request.form['bname']
    query.building_add(bname)
    return '200 OK ADD BUILDING'
    
@app.route('/building/edit',methods=['PUT'])
def building_edit():
    bid = request.form['bid']
    bname = request.form['bname']
    query.building_edit(bid,bname)
    return '200 OK EDIT BUILDING'
    
@app.route('/building/del',methods=['DELETE'])
def building_del():
    bid = request.form['bid']
    query.building_del(bid)
    return '200 OK DEL BUILDING'