from app import server
from flask import jsonify, request
import json
import requests
from datetime import datetime
from timer import Timer
import interface
import PIRBoot
from tbscan import ThunderboardHandler

#
# CONSTANTS
#


MIRROR_TTL = 60 	# in seconds
ALEXA_FRAME_TTL = 1	# in minutes
NOTIF_TTL = 10		# in seconds


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
	elif (command == "guide"):
		gui.ToggleGuide()

timer = Timer(MIRROR_TTL)
gui = interface.BuildGUI(ALEXA_FRAME_TTL, NOTIF_TTL)
motionSensor = PIRBoot.SensorService(ChangeGUI, timer)
thunderboard = ThunderboardHandler(ChangeGUI)





#WebServer routing
@server.route('/')
def blank():
	return "Hello"

@server.route('/alexa', methods = ['POST'])
def alexaResponse():
	json = request.get_json()
	gui.UpdateAlexa(json["title"], json["text"], datetime.now())
	return jsonify({'response' : 'Update Ok'}) #to use with Dict

#
# TODO
#
@server.route('/toggle', methods = ['GET'])
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
	
