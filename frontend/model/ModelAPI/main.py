from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
import numpy as np
from datetime import datetime
from Model import Model

app = Flask(__name__)

m = Model.PredictionModel("./ModelFiles")


@app.route("/waittime", methods=['POST'])
def main():
	data = {}
	try:
		data = request.get_json()
	except: 
		return error("Request could not be parsed succesfully")
	try:
		predicted_wait_time = predict(data)
	except(KeyError):
		return error('A required field is missing from the provided json')
	test_result = {}
	test_result["status"] = "success"
	test_result["time"] = f"{int(predicted_wait_time[0,0])}"
	return jsonify(test_result)


def predict(data):
	timestamp = datetime.strptime(data['DateTime'], '%Y-%m-%d %H:%M:%S')
	park = data['Park']
	ride = data['Ride']
	predicted = m.predict(timestamp, park, ride)
	return predicted


def error(error_message=''):
	error_result = {}
	error_result["status"] = 'error'
	error_result["message"] = error_message
	return jsonify(error_result)

if __name__ == '__main__':
	# Tests
	app_server = WSGIServer(("", 3300), app)
	app_server.serve_forever()