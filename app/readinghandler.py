#!/usr/bin/python
from bluepy.btle import *
import struct
from datetime import datetime
from tbsense import Thunderboard
import threading



    
    
class ThunderboardHandler(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
        self.daemon = True
        self.start()
        self.MIN_INTERVAL = datetime.timedelta(seconds = 10)
        self.deviceID = int()
        
        
	def getThunderboards(self):
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

	def GetActiveBoard(self):
		self.thunderboards = self.getThunderboards()
		if len(self.thunderboards) == 0:
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
				
		return self.thunderboard
