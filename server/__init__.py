from flask import Flask
from timer import Timer
import config

#GUI_Control:Interface
def ChangeGUI(command : str, data):
	if (command == "showAll"):
		gui.GuiOn()
	elif (command == "hideAll"):
		gui.GuiOff()
	elif (command == "updateBoard"):
		gui.UpdateThunderboard(data)
	elif (command == "notif"):
		gui.SendNotification(data)


# ------------------------------------------------
# Initialising global dependencies
# ------------------------------------------------
flask = Flask(__name__)
timer = Timer(config.MirrorTTL)

# ------------------------------------------------
# Importing and initializing modules
# ------------------------------------------------
import server.interface as interface
import server.PIRBoot as PIRBoot
from server.tbscan import ThunderboardHandler

motionSensor = PIRBoot.SensorService(ChangeGUI, timer) # MotionSensor starts after 15 seconds
gui = interface.BuildGUI(config.AlexaTTL, config.NotifTTL) # Interface starts
thunderboard = ThunderboardHandler(ChangeGUI)

from server import views
# Appflow goes back to run.py
