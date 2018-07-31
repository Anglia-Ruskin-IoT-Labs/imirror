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
    return jsonify({'response' : 'Update Ok'}) #to use with Dict
