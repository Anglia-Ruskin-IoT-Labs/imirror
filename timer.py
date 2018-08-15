#!/usr/bin/python3
import time
import threading


class Timer(threading.Thread):
	def __init__(self, _timeframe):
		self.TIMEFRAME = _timeframe
		self.lock = threading.Lock()
		threading.Thread.__init__(self)
		self.daemon = True
		self.start()
		
			
	def run(self):
		self.__ZeroTimer()
		while True:
			if self.ReadTimer() > 0:
				self.__DecrementTimer()
			else:
				pass
			time.sleep(1)
		
	def RestartTimer(self):
		''' To be used when an user interacts with
			the interface in any way.
		'''
		while self.lock.locked():
			continue
		self.lock.acquire()
		counter = open('/tmp/counter', 'w')
		value = str(self.TIMEFRAME)
		counter.write(value)
		counter.close()
		self.lock.release()
		

	def __ZeroTimer(self):
		''' Set the timer file to default
		'''
		while self.lock.locked():
			continue
		self.lock.acquire()
		counter = open('/tmp/counter', 'w')
		value = str('0           ')
		counter.write(value)
		counter.close()
		self.lock.release()

	def __DecrementTimer(self):
		''' 
		'''
		while self.lock.locked():
			continue
		self.lock.acquire()
		counter = open('/tmp/counter', 'r+')
		value = counter.read()
		temp = int(value) - 1
		# String with spaces to overwrite everything in file too
		rewrite = str(temp) + "            "
		counter.seek(0)
		counter.write(rewrite)
		counter.truncate()
		counter.close()
		self.lock.release()

	def ReadTimer(self):
		while self.lock.locked():
			continue
		self.lock.acquire()
		counter = open('/tmp/counter', 'r')
		tmp = counter.read()
		value = int(tmp)
		counter.close()
		self.lock.release()
		return value
