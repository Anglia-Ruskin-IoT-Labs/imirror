#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import timer as countdown #methods for manipulating timer
import threading


GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
countdown.ZeroTimer() 
GPIO.setup(PIR_PIN, GPIO.IN)


class SensorService(threading.Thread):
	def __init__(self, commandInterface):
		threading.Thread.__init__(self)
		self.daemon = True
		self.start()
		self.parent_method = commandInterface
	def run(self):
		print "PIR Module Startup script (CTRL+C to exit)"
		time.sleep(15)
		print "Ready"
		try:
			while True:
				'''if GPIO.input(PIR_PIN) and countdown.ReadTimer() <= 0:
					countdown.RestartTimer()
					self.parent_method("showAll", "")  '''                       
				if GPIO.input(PIR_PIN):
					countdown.RestartTimer()
					self.parent_method("showAll", "") 
				elif countdown.ReadTimer() > 1:
					countdown.DecrementTimer()
					print(countdown.ReadTimer())
				elif countdown.ReadTimer() == 1:
					self.parent_method("hideAll", "")
					print("TimeOut")
					countdown.DecrementTimer()
				else:                  
					pass
				time.sleep(1)
				
		except KeyboardInterrupt:
			print'Quit'

		
#SensorService()
#while True:
#    time.sleep(1)
#    pass

####
