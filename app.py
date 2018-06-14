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
    model, vectorizer = m.loadUtils()
    features = m.extractFeatures(data, vectorizer)
    labels = model.predict(features)
    thread = Thread(target=dbm.msgPusher, args=(data["message"], labels, ))
    thread.start()
    return jsonify({"results": labels.tolist()})

@app.route('/classify/<id>/<label>', methods=['GET'])
def classify(id, label):
    return jsonify({
        "success": dbm.classPusher(id, label)
    })

@app.route('/messages', methods=['GET'])
def messages():
    return jsonify(dbm.msgListGet())

if __name__ == "__main__":
    config = m.loadConfig()
    dbm.dbConnect(config['db'])
    app.run(host=config['web']['host'], port=config['web']['port'])