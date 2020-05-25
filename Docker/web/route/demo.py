from flask import Blueprint, jsonify
from extensions import query

app = Blueprint('DEMO', __name__)

@app.route('/demo')
def demo():
    return jsonify(query.demo1())
    
@app.route('/demo2')
def demo2():
    return jsonify(query.demo2())