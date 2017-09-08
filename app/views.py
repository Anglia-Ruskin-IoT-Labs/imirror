from app import app
from flask import render_template, jsonify
from app import response_pool
from flask_ask import Ask, statement, question, session, convert_errors
import json
import requests
import time
import unidecode
import webbrowser
#import timer

ask = Ask(app, "/alexa_menu")
speech = {'response': "lol"}

def SaveAnswer(text):
    speech['response'] = text

@app.route('/')
def blank():
    return render_template("blank.html")

@app.route('/alexa')
def alexaResponse():
    return jsonify(speech)

@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/welcome')
def welcome():
    welcome_message = response_pool.randomResponse()
    return render_template("welcome.html", welcome_message = welcome_message)

@app.route('/menu')
def menu():
    return render_template("menu.html")


#ask-flask part

@ask.launch
def start_skill():
    welcome_message = 'This is the menu, plesase choose one app to try out. To open them, just say their names. To exit, just say goodbye.'
    SaveAnswer(welcome_message)
    webbrowser.open('http://0.0.0.0:5005/menu', new=0)
    return question(welcome_message) \
    .reprompt("I didn't get that. Which app you'd like to choose?")

@ask.intent("OpenPlay")
def opening_play():
    headlines = get_headlines()
    instructions = 'Opening the Balancing game.'
    SaveAnswer(Insturctions)
    return statement(instructions)

@ask.intent("OpenZork")
def opening_zork():
    bye_text = 'Opening zork.'
    SaveAnswer(bye_text)
    return statement(bye_text)

@ask.intent("Dashboard")
def dashboard():
    text = 'Opening the dashboard.'
    #open interface.py
    SaveAnswer(text)
    return statement(text)

@ask.intent("Map", convert={'roomNumber': int})
def map(roomNumber):
    if roomNumber == 109:
        text = "Room 109 is on the first floor, on the right after you went up on the stairs"
        SaveAnswer(text)
        return statement(text)
    elif roomNumber == 105:
        text = "Room 105 is on the first floor"
        SaveAnswer(text)
        return statement(text)
    else:
        chooseRoom = "If you are looking for a specific room, please tell me its number like this: I'm looking for room 100."
        SaveAnswer(text)
        webbrowser.open('http://0.0.0.0:5005/map')
        return question(chooseRoom)

@ask.session_ended
def session_ended():
    return "{}", 200