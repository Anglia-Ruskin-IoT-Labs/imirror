from flask import Flask
from timer import Timer
from config import Config



#GUI_Control:Interface
def ChangeGUI(command : str, data):
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


# ------------------------------------------------
# Initialising global dependencies
# ------------------------------------------------
configuration = Config()
flask = Flask(__name__)
timer = Timer(configuration.MirrorTTL)

# ------------------------------------------------
# Importing and initializing modules
# ------------------------------------------------
import server.interface as interface
import server.PIRBoot as PIRBoot
from server.tbscan import ThunderboardHandler
from server import views

motionSensor = PIRBoot.SensorService(ChangeGUI, timer) # MotionSensor starts after 15 seconds
gui = interface.BuildGUI(configuration.AlexaTTL, configuration.NotifTTL) # Interface starts
thunderboard = ThunderboardHandler(ChangeGUI)


# Appflow goes back to run.py
