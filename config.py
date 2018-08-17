import configparser
from enum import Enum
import atexit
import server.gui_positions as gp
from datetime import datetime


confFile = 'config.cfg'
## --------------------------------------------------------------
## Widget names, these can be called through 
## interface.ToggleFrame("name")
## --------------------------------------------------------------
ALEXA_NAME = 'alexa'
CLOCK_NAME = 'clock'
NEWS_NAME = 'news'
WEATHER_NAME = 'weather'
SENSORS_NAME = 'sensors'
NOTIF_NAME = 'notif'
GUIDE_NAME = 'guide'

#-----------------------------------
# DEFAULTS
#-----------------------------------

framePositions = {
	GUIDE_NAME : gp.Pos.BOTLEFT,
	ALEXA_NAME : gp.Pos.BOTLEFT,
	NOTIF_NAME : gp.Pos.MIDMID,
	WEATHER_NAME : gp.Pos.TOPLEFT,
	CLOCK_NAME : gp.Pos.TOPRIGHT,
	NEWS_NAME : gp.Pos.BOTRIGHT,
	SENSORS_NAME : gp.Pos.BOTRIGHT
}

# Decimal values can be use to decide priority if
# widgets are weighted the same. Users can't change decimals, only 
# the whole values
# 
# Alexa and notification weightings are set
frameWeights = {
	GUIDE_NAME : 1.2,
	ALEXA_NAME : 99999999.1, 	# Have precedence over anything but notif
	NOTIF_NAME : 99999999.2,	# Have precedence over anything
	WEATHER_NAME : 1.5,
	CLOCK_NAME : 1.4,
	NEWS_NAME : 1.3,
	SENSORS_NAME : 1.1
}
MirrorTTL = 60 #in seconds
NotifTTL = 10
AlexaTTL = 10
config = configparser.ConfigParser()


def main():		
	try:
		config.read(confFile)
		# Assigning config to variables outside of function scope
		global MirrorTTL
		MirrorTTL = int(config['Mirror']['MirrorTTL'])
		global NotifTTL
		NotifTTL = int(config['Mirror']['NotifTTL'])
		global AlexaTTL
		AlexaTTL = int(config['Mirror']['AlexaTTL'])
		framePositions[NEWS_NAME] = gp.PositionResolver(str(config['WIDGET_POSITIONS'][NEWS_NAME].name))
		framePositions[GUIDE_NAME] = gp.PositionResolver(str(config['WIDGET_POSITIONS'][GUIDE_NAME].name))
		framePositions[ALEXA_NAME] = gp.PositionResolver(str(config['WIDGET_POSITIONS'][ALEXA_NAME].name))
		framePositions[NOTIF_NAME] = gp.PositionResolver(str(config['WIDGET_POSITIONS'][NOTIF_NAME].name))
		framePositions[WEATHER_NAME] = gp.PositionResolver(str(config['WIDGET_POSITIONS'][WEATHER_NAME].name))
		framePositions[CLOCK_NAME] = gp.PositionResolver(str(config['WIDGET_POSITIONS'][CLOCK_NAME].name))
		framePositions[SENSORS_NAME] = gp.PositionResolver(str(config['WIDGET_POSITIONS'][SENSORS_NAME].name))
		frameWeights[NEWS_NAME] = (float(config['WIDGET_WEIGHTS'][NEWS_NAME]))
		frameWeights[GUIDE_NAME] = (float(config['WIDGET_WEIGHTS'][GUIDE_NAME]))
		frameWeights[ALEXA_NAME] = (float(config['WIDGET_WEIGHTS'][ALEXA_NAME]))
		frameWeights[NOTIF_NAME] = (float(config['WIDGET_WEIGHTS'][NOTIF_NAME]))
		frameWeights[WEATHER_NAME] = (float(config['WIDGET_WEIGHTS'][WEATHER_NAME]))
		frameWeights[CLOCK_NAME] = (float(config['WIDGET_WEIGHTS'][CLOCK_NAME]))
		frameWeights[SENSORS_NAME] = (float(config['WIDGET_WEIGHTS'][SENSORS_NAME]))
	except (IOError, KeyError):
		print("Config not found.")
		

def Write():
	config['Mirror'] = {'MirrorTTL':MirrorTTL,
							'NotifTTL':NotifTTL,
							'AlexaTTL':AlexaTTL}
	config.set("Mirror", "; TTL values are in seconds.", "")
	config['WIDGET_POSITIONS'] = {
							NEWS_NAME:framePositions[NEWS_NAME].name,
							CLOCK_NAME:framePositions[CLOCK_NAME].name,
							WEATHER_NAME:framePositions[WEATHER_NAME].name,
							SENSORS_NAME:framePositions[SENSORS_NAME].name,
							GUIDE_NAME:framePositions[GUIDE_NAME].name,
							ALEXA_NAME:framePositions[ALEXA_NAME].name,
							NOTIF_NAME:framePositions[NOTIF_NAME].name}
	config.set('WIDGET_POSITIONS', "; Avaliable values are: TOPLEFT,TOPMID " +
    	"TOPRIGHT, MIDLEFT, MID, MIDRIGHT \nBOTLEFT, BOTMID, BOTRIGHT", "")
	config['WIDGET_WEIGHTS'] = frameWeights
	with open(confFile, 'w') as configfile:
		config.write(configfile)



#------------------------------------------------
#
#-------------------------------------------------
def exit_handler():
	Write()

atexit.register(exit_handler)



def __init__():
	main()



