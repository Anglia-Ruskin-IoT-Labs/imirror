from server import flask, gui, timer
from flask import jsonify, request, render_template
import json
import requests
from datetime import datetime
import server.gui_positions as gp




#WebServer routing
@flask.route('/')
def blank():
	return "Hello"

@flask.route('/alexa', methods = ['POST'])
def alexaResponse():
	json = request.get_json()
	gui.UpdateAlexa(json["title"], json["text"], datetime.now())
	return jsonify({'response' : 'Update Ok'}) #to use with Dict

@flask.route('/move', methods = ['GET', 'POST'])
def moveInterfaceItems():
	if request.method == 'POST':
		json = request.get_json()
		try:
			position = gp.PositionResolver(json['position'])
			if gui.ChangeFramePosition(json["widget"], position ):
				return jsonify({'response' : 'Update Ok'})
			else:
				return jsonify({'Error': 'Wrong widget name'})
		except KeyError:
			return jsonify({'Error': 'Wrong Json structure'})
	else:
		return ("Example json: {'widget': 'widgetname', " + 
		" 'position': 'positionname'}")

#
# TODO
#
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
						return jsonify({'response' : 'Update Ok'})
					else:
						return jsonify({'Error': 'Update Failed on ToggleAll()'})
				else:
					if gui.ShowFrame(widget):
						return jsonify({'response' : 'Update Ok'})
					else:
						return jsonify({'Error': ('Update Failed on ' + widget)})
			elif state == 'off':
				if widget == 'all':
					if gui.GuiOff():
						return jsonify({'response' : 'Update Ok'})
					else:
						return jsonify({'Error': 'Update Failed on GuiOff()'})
				else:
					pass
					if gui.HideFrame(widget):
						return jsonify({'response' : 'Update Ok'})
					else:
						return jsonify({'Error': ('Update Failed on ' + widget)})
		except KeyError:
			return jsonify({"Error": "Wrong json structure"})
	
