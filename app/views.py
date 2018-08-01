from app import server
from flask import jsonify, request
import json
import requests
from datetime import datetime
import timer as countdown
import interface
import PIRBoot
from tbscan import ThunderboardHandler

#GUI_Control:Interface
def ChangeGUI(command, data):
	if (command == "showAll"):
		gui.ToggleAll()
	elif (command == "hideAll"):
		gui.GuiOff()
	elif (command == "updateBoard"):
		gui.UpdateThunderboard(data)
	elif (command == "notif"):
		gui.SendNotification(data)

gui = interface.BuildGUI()
motionSensor = PIRBoot.SensorService(ChangeGUI)
thunderboard = ThunderboardHandler(ChangeGUI)





#WebServer routing
@server.route('/')
def blank():
	return "Hello"

@server.route('/alexa', methods = ['POST'])
def alexaResponse():
	json = request.get_json()
	gui.UpdateAlexa(json["title"], json["text"], datetime.now())
	countdown.RestartTimer()
	return jsonify({'response' : 'Update Ok'}) #to use with Dict

#
# TODO
#
@server.route('/toggle', methods = ['GET'])
def changeUI():
	command = request.args.get('command')
	if command == "on":
		gui.ToggleAll()
		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command =="off":
		gui.GuiOff()
		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "board-on":
		gui.ToggleThunderBoard()
		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "board-off":

		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "weather-on":
		gui.ToggleWeather()
		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "weather-off":

		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "clock-on":
		gui.ToggleClock()
		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "clock-off":

		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "news-on":
		gui.ToggleNews()
		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "news-off":

		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "guide-on":

		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	elif command == "guide-off":

		countdown.RestartTimer()
		return jsonify({'response' : 'Update Ok'})
	else:
		return jsonify({'Error' : 'Invalid command'})
	
