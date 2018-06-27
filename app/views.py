from app import server
from flask import jsonify, request
import json
import requests
import time
import timer as countdown
import interface
import PIRBoot

#Interface Control method
def ChangeInterface(str):
    if (str == "show"):
        gui.toggle_all()
    elif (str == "hide"):
        gui.toggle_gui()

gui = interface.BuildGUI()
motionSensor = PIRBoot.SensorService(ChangeInterface)





#WebServer routing
@server.route('/')
def blank():
    return "Hello"

@server.route('/alexa', methods = ['PUT'])
def alexaResponse():
    json = request.get_json()
    return jsonify({'response' : 'Update Ok'}) #to use with Dict
