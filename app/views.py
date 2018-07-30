from app import server
from flask import jsonify, request
import json
import requests
from datetime import datetime
import timer as countdown
import interface
import PIRBoot

#GUI Control Interface
def ChangeGUI(str):
    if (str == "show"):
        gui.ToggleAll()
    elif (str == "hide"):
        gui.GuiOff()

gui = interface.BuildGUI()
motionSensor = PIRBoot.SensorService(ChangeGUI)





#WebServer routing
@server.route('/')
def blank():
    return "Hello"

@server.route('/alexa', methods = ['POST'])
def alexaResponse():
    json = request.get_json()
    gui.UpdateAlexa(json["title"], json["text"], datetime.now())
    return jsonify({'response' : 'Update Ok'}) #to use with Dict
