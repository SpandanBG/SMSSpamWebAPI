#!/usr/bin/python

from flask import Flask, request, jsonify
from bin import modules as m

app = Flask(__name__)

@app.route('/sms', methods=["POST"])
def sms():
    model, vectorizer = m.loadUtils()
    features = m.extractFeatures(request.get_json(), vectorizer)
    label = model.predict(features)
    return jsonify({"results": label.tolist()})

if __name__ == "__main__":
    print("Listening on port 80")
    app.run(host="localhost", port=80)