from app import app
from flask import render_template, jsonify
from app import response_pool
from flask_ask import Ask, statement, question, session, convert_errors
import json
import requests
import time
import unidecode
import webbrowser
import timer as countdown
import interface
import PIRBoot
import threading

#Interface Control method
def ChangeInterface(str):
    if (str == "show"):
        gui.toggle_all()
    elif (str == "hide"):
        gui.toggle_gui()

ask = Ask(app, "/alexa_menu")
gui = interface.BuildGUI()
motionSensor = PIRBoot.SensorService(ChangeInterface)

speech = {'response': ""} #string stores the skill responses



        
#Save alexa responses - function saves a little time
def SaveAnswer(text):
    speech['response'] = text

#WebServer routing
@app.route('/')
def blank():
    return render_template("blank.html")

@app.route('/alexa') #to return Alexa response as json? I don't know think this works properly as flask wraps it in html
def alexaResponse():
    return jsonify(speech) #to use with Dict

@app.route('/index')
def index():
        countdown.RestartTimer() #every time user interaction is happening this needs to run
	return render_template("index.html")

@app.route('/welcome')
def welcome():
    welcome_message = response_pool.randomResponse()
    countdown.RestartTimer()
    return render_template("welcome.html", welcome_message = welcome_message)

@app.route('/menu')
def menu():
    countdown.RestartTimer()
    return render_template("menu.html")



#SkillServer Routing
@ask.launch #at skill Launch
def start_skill():
    welcome_message = 'This is the menu, plesase choose one app to try out. To open them, just say their names. To exit, just say goodbye.'
    SaveAnswer(welcome_message)
    countdown.RestartTimer()
    #webbrowser.open('http://0.0.0.0:5005/menu', new=0) #open interface - only menu
    gui.toggle_gui()
    #gui.toggle_menu() not yet implemented
    return question(welcome_message) \
    .reprompt("I didn't get that. Which app you'd like to choose?")

@ask.intent("OpenGame")
def opening_play():
    headlines = get_headlines()
    instructions = 'Opening the Balancing game.'
    #Implementation not set yet - Where the skillserver will run; where the script will run
    countdown.RestartTimer()
    SaveAnswer(Insturctions)
    gui.toggle_gui()
    return statement(instructions)

@ask.intent("Zork")
def opening_zork():
    bye_text = 'Opening zork.'
    countdown.RestartTimer()
    SaveAnswer(bye_text)
    #Launching Different skill on lambda - displaying responses not available
    return statement(bye_text)

@ask.intent("Dashboard")
def dashboard():
    text = 'Opening the dashboard.'
    #open interface.py all modules except menu
    countdown.RestartTimer()
    SaveAnswer(text)
    gui.toggle_all()
    return statement(text)

@ask.intent("Map", convert={'roomNumber': int}) #Testing flask-ask capability - unnecessary
def map(roomNumber):
    if roomNumber == 109:
        text = "Room 109 is on the first floor, on the right after you went up on the stairs"
        SaveAnswer(text)
        countdown.RestartTimer()
        return statement(text)
    elif roomNumber == 105:
        text = "Room 105 is on the first floor"
        SaveAnswer(text)
        countdown.RestartTimer()
        return statement(text)
    else:
        chooseRoom = "If you are looking for a specific room, please tell me its number like this: I'm looking for room 100."
        SaveAnswer(text)
        countdown.RestartTimer()
        webbrowser.open('http://0.0.0.0:5005/map')
        return question(chooseRoom)

@ask.session_ended
def session_ended():
    return "{}", 200