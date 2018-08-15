from server import flask
from flask import jsonify, request
import json
import requests
from datetime import datetime

#
# CONSTANTS
#



#WebServer routing
@flask.route('/')
def blank():
	return "Hello"

@flask.route('/alexa', methods = ['POST'])
def alexaResponse():
	json = request.get_json()
	gui.UpdateAlexa(json["title"], json["text"], datetime.now())
	return jsonify({'response' : 'Update Ok'}) #to use with Dict

#
# TODO
#
@flask.route('/toggle', methods = ['GET'])
def changeUI():
	command = request.args.get('command')
	if command == "on":
		gui.ToggleAll()
		timer.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command =="off":
		gui.GuiOff()
		timer.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "board-on":
		gui.ToggleThunderBoard()
		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "board-off":

		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "weather-on":
		gui.ToggleWeather()
		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "weather-off":

		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "clock-on":
		gui.ToggleClock()
		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "clock-off":

		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "news-on":
		gui.ToggleNews()
		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "news-off":

		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "guide-on":
		gui.ToggleGuide()
		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "guide-off":

		time.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	else:
		return jsonify({'Error' : 'Invalid command'})
	
