from server import flask, gui, timer
from flask import jsonify, request, render_template
import json
import requests
from datetime import datetime
import server.gui_positions as gp
from server import timer




#WebServer routing
@flask.route('/')
def blank():
	return "Hello"
	

#---------------------------------------------------
# Update alexa frame with text received
#---------------------------------------------------
@flask.route('/alexa', methods = ['POST'])
def alexaResponse():
	json = request.get_json()
	gui.UpdateAlexa(json["title"], json["text"], datetime.now())
	return jsonify({'response' : 'Update Ok'}) #to use with Dict

#---------------------------------------------------
# Moves Widgets around
#---------------------------------------------------
@flask.route('/move', methods = ['GET', 'POST'])
def moveInterfaceItems():
	if request.method == 'POST':
		json = request.get_json()
		try:
			position = gp.PositionResolver(json['position'])
			if position == None:
				return jsonify({'Error': 'Nonexistent position'})
			if gui.ChangeFramePosition(json["widget"], position):
				timer.RestartTimer()
				return jsonify({'response' : 'Update Ok'})
			else:
				return jsonify({'Error': 'Wrong widget name'})
		except KeyError:
			return jsonify({'Error': 'Wrong Json structure'})
	else:
		return ("Example json: {'widget': 'widgetname', " + 
		" 'position': 'positionname'}")

#---------------------------------------------------
# Turns widgets on and off
#---------------------------------------------------
@flask.route('/toggle', methods = ['GET', 'POST'])
def changeUI():
	if request.method == 'POST':
		try:
			json = request.json()
			widget = json['widget']
			state = json['state']
			if state == 'on':
				if widget == 'all':
					if gui.GuiOn():
						timer.RestartTimer()
						return jsonify({'response' : 'Update Ok'})
					else:
						return jsonify({'Error': 'Update Failed on ToggleAll()'})
				else:
					if gui.ShowFrame(widget):
						timer.RestartTimer()
						return jsonify({'response' : 'Update Ok'})
					else:
						return jsonify({'Error': ('Update Failed on ' + widget)})
			elif state == 'off':
				if widget == 'all':
					if gui.GuiOff():
						timer.RestartTimer()
						return jsonify({'response' : 'Update Ok'})
					else:
						return jsonify({'Error': 'Update Failed on GuiOff()'})
				else:
					pass
					if gui.HideFrame(widget):
						timer.RestartTimer()
						return jsonify({'response' : 'Update Ok'})
					else:
						return jsonify({'Error': ('Update Failed on ' + widget)})
		except KeyError:
			return jsonify({"Error": "Wrong json structure"})
	
