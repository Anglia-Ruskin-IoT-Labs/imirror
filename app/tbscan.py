#!/usr/bin/python
from bluepy.btle import *
import struct
from time import sleep
from tbsense import Thunderboard
import threading
from datetime import datetime, timedelta



class ThunderboardHandler(threading.Thread):
	''' Discovers Thunderboards and gets readings
		from one, updates interface with it. 
		Handles iMirror behaviours based on readings.
	'''
	def __init__(self, _interfaceCommand):
		''' Constructor
		'''
		
		# Setting Constants
		self.MIN_TIME_BETWEEN_EVENTS = timedelta(seconds=5)
		# Setting variables to use later
		self.lastNotification = datetime.min
		self.lastTempEvent = datetime.min
		self.lastCO2Event = datetime.min
		self.lastVOCEvent = datetime.min
		self.lastCO2Reading = -1
		self.lastTempReading = -1
		self.deviceID = -1
		
		
		self.CommandInterface = _interfaceCommand
		
		threading.Thread.__init__(self)
		self.daemon = True
		self.start()
	
	
#--------------------------------------------------------------------
# Main loop
#--------------------------------------------------------------------
	def run(self):
		''' Runs when the thread starts
		'''
		self.thunderboards = self.getThunderboards()
		while True:
			message = ""
			info = ""
			if len(self.thunderboards) == 0:
				info = ("No Thunderboard Sense devices found!")
				self.thunderboards = self.getThunderboards()
			else:
				# Preparing variables
				isBoardActive = False
				devices = list()
				# iterating through available boards
				for deviceID, thunderboard in self.thunderboards.items():
					# board is the Previously used board, selected
					if deviceID == self.deviceID:
						self.thunderboard == thunderboard
						isBoardActive = True
					# board is a different board, appending its id
					else:
						devices.append(deviceID)
				# Previously used board was not found
				if not isBoardActive:
					# Selecting first available board
					self.thunderboard = self.thunderboards[devices[0]]
					self.deviceID = devices[0]
					info = ("New Device found, ID: " + str(deviceID))
				try:
					data = self.sensorLoop(self.thunderboard, deviceID)
					data["info"] = info
					self.HandleCO2(data["co2"])
					self.HandleTemperature(data["temperature"])
					self.CommandInterface("updateBoard", data)
				except (IOError, BTLEException):
					data = dict()
					data["info"] = "Broken Pipe"
					data["temperature"] = ""
					data["co2"] = ""
					data["humidity"] = ""
					data["ambientLight"] = ""
					data["uvIndex"] = ""
					data["voc"] = ""
					data["sound"] = ""
					data["pressure"] = ""
					self.CommandInterface("updateBoard", data)
					self.thunderboards = self.getThunderboards()
			sleep(0.2)


#-----------------------------------------------------------------
# Reading Handler Methods
#-----------------------------------------------------------------

	def HandleTemperature(self, reading):
		if self.AllowHandling(datetime.now()):
			if reading >= 30 and self.lastTempReading < 30:
				self.lastTempReading = reading
				self.lastTempEvent = datetime.now()
				self.lastNotification = datetime.now()
				self.CommandInterface("notif", "Ambient Temperature above 30 celsius!")
		
	
	def HandleCO2(self, reading):
		if self.AllowHandling(datetime.now()):
			# Reading in normal levels after not normal
			if reading < 1000 and self.lastCO2Reading > 1000:
				self.lastCO2Reading = reading
				self.lastNotification = datetime.now()
				self.CommandInterface("notif", "CO2 levels are back to normal.")
				# Reading back to normal
			elif reading >= 1000 and reading < 2000:
				if self.lastCO2Event + timedelta(minutes = 10) < datetime.now():
					# Reading in not recommended range
					self.lastNotification = datetime.now()
					self.lastCO2Event = datetime.now()
					self.lastCO2Reading = reading
					self.CommandInterface("notif", "CO2 levels above recommended, open the windows.")
			elif reading >= 2000:
				if self.lastCO2Event + timedelta(minutes = 1) < datetime.now():
					self.CommandInterface("notif", "CO2 levels are critical, air the room immidiately!")
					self.lastNotification = datetime.now()
					self.lastCO2Event = datetime.now()
					self.lastCO2Reading = reading
			else:
				pass





		
#------------------------------------------------
# Assist Methods
# -----------------------------------------------  
	def AllowHandling(self, time):
		if (self.lastNotification + self.MIN_TIME_BETWEEN_EVENTS) < time:
			return True
		else:
			return False


      
	def getThunderboards(self):
		''' Collects all available thunderboards
		'''
		scanner = Scanner(0)
		devices = scanner.scan(3)
		tbsense = dict()
		for dev in devices:
			scanData = dev.getScanData()
			for (adtype, desc, value) in scanData:
				if desc == 'Complete Local Name':
					if 'Thunder Sense #' in value:
						deviceId = int(value.split('#')[-1])
						tbsense[deviceId] = Thunderboard(dev)

		return tbsense

	def sensorLoop(self, tb, devId):
		''' Collects all reading into a dict, 
			and returns it.
		'''
		
		value = tb.char['power_source_type'].read()
		if ord(value) == 0x04:
			tb.coinCell = True



		text = ''
		text += '\n' + tb.name + '\n'
		data = dict()

		try:

			for key in tb.char.keys():
				if key == 'temperature':
					data['temperature'] = tb.readTemperature()
					text += 'Temperature:\t{} C\n'.format(data['temperature'])
				elif key == 'humidity':
					data['humidity'] = tb.readHumidity()
					text += 'Humidity:\t{} %RH\n'.format(data['humidity'])
				
				elif key == 'ambientLight':
					data['ambientLight'] = tb.readAmbientLight()
					text += 'Ambient Light:\t{} Lux\n'.format(data['ambientLight'])

				elif key == 'uvIndex':
					data['uvIndex'] = tb.readUvIndex()
					text += 'UV Index:\t{}\n'.format(data['uvIndex'])

				elif key == 'co2' and tb.coinCell == False:
					data['co2'] = tb.readCo2()
					text += 'eCO2:\t\t{}\n'.format(data['co2'])

				elif key == 'voc' and tb.coinCell == False:
					data['voc'] = tb.readVoc()
					text += 'tVOC:\t\t{}\n'.format(data['voc'])

				elif key == 'sound':
					data['sound'] = tb.readSound()
					text += 'Sound Level:\t{}\n'.format(data['sound'])

				elif key == 'pressure':
					data['pressure'] = tb.readPressure()
					text += 'Pressure:\t{}\n'.format(data['pressure'])

		except Exception, e:
			print(e)

		return data



	
