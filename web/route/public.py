from flask import Blueprint, jsonify, request, escape
from extensions import query, html_escape, toHourandMin
import reg
import json, time

app = Blueprint('Public', __name__)

@app.route('/building/',methods=['GET'])
def building_list():
    response = jsonify(reg.getAllBuilding())
    return response
    
@app.route('/room/',methods=['GET'])
def room_list():
    prefix = request.args.get('prefix')
    if(not prefix):
        return jsonify({'message':"prefix is null"}), 400
    building = reg.getAllBuilding()
    url = list(filter(lambda x: x["prefix"].lower() == prefix.lower(), building))
    response = jsonify({'message':"Not Found"}), 400
    if(url):
        response = jsonify(reg.getAllRoomList(url[0]["url"]))
    return response
