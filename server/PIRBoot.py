#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import threading


GPIO.setmode(GPIO.BCM)
PIR_PIN = 7 
GPIO.setup(PIR_PIN, GPIO.IN)


class SensorService(threading.Thread):
	def __init__(self, commandInterface, countdown):
		threading.Thread.__init__(self)
		self.daemon = True
		self.start()
		self.parent_method = commandInterface
		self.countdown = countdown
		self.MirrorSelfStarted = False
	def run(self):
		print('PIR Module Startup script (CTRL+C to exit)')
		time.sleep(15)
		print("Ready")
		try:
			while True:
				# Screen is off and Movement is sensed
				if GPIO.input(PIR_PIN) and self.countdown.ReadTimer() <= 0:
					self.countdown.RestartTimer()
					self.parent_method("showAll", "") 
					self.parent_method("guide", "")
					self.MirrorSelfStarted = True
				# Screen is on and movement is sensed                 
				elif GPIO.input(PIR_PIN) and self.countdown.ReadTimer() > 1:
					self.countdown.RestartTimer()
				# No movement, Screen on
				elif self.countdown.ReadTimer() > 1:
					print(self.countdown.ReadTimer())
				# No movement, countdown at threshold, turning screen off
				elif self.countdown.ReadTimer() == 1:
					self.parent_method("hideAll", "")
					self.MirrorSelfStarted = False
					print("TimeOut")
				# Screen is off, no movement, countdown below threshold
				elif self.countdown.ReadTimer() < 1:
					pass
				else:                  
					pass
				time.sleep(0.5)
				
		except KeyboardInterrupt:
			print('Quit')

