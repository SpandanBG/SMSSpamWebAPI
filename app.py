#!/usr/bin/python

from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
from bin import modules as m
from db import modules as dbm

app = Flask(__name__)
CORS(app)

config = {}

@app.route('/sms', methods=["POST"])
def sms():
    data = request.get_json()
    thread = Thread(target=dbm.msgPusher, args=(data["message"], ))
    thread.start()
    model, vectorizer = m.loadUtils()
    features = m.extractFeatures(data, vectorizer)
    label = model.predict(features)
    return jsonify({"results": label.tolist()})

@app.route('/classify/<id>/<cls>', methods=['GET'])
def classify(id, cls):
    try:
        thread = Thread(target=dbm.classPusher, args=(id,cls,))
        thread.start()
    except:
        return jsonify({"success": False})
    return jsonify({"success": True})

@app.route('/messages', methods=['GET'])
def messages():
    return jsonify(dbm.msgListGet())

if __name__ == "__main__":
    config = m.loadConfig()
    dbm.table = config['db']['tables'][0]
    dbm.rcon = dbm.r.connect(
        db=config['db']['db'], 
        user=config['db']['user'], 
        password=config['db']['password']
    )
    app.run(host=config['web']['host'], port=config['web']['port'])