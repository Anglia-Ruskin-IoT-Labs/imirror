import configparser
from enum import Enum

class Pos(Enum):
	TOPLEFT = 0
	TOPMID = 1
	TOPRIGHT = 2
	MIDLEFT = 3
	MID = 4
	MIDRIGHT = 5
	BOTLEFT = 6
	BOTMID = 7
	BOTRIGHT = 8

class Position():
	def __init__(self, _col: int, _row: int, _align: str, _pos: Pos):
		self.column = _col
		self.row = _row
		self.alignment = _align
		self.frame = None
		self.representation = _pos
		
	def __repr__(self):
		return str(self.representation)
		



class Config():
	def __init__(self):
		# Pos object inits 
		#

		self.TOPLEFT = Position(1, 1, "nw", Pos.TOPLEFT)
		self.TOPMID = Position(2, 1, "n", Pos.TOPMID)
		self.TOPRIGHT = Position(3, 1, "ne", Pos.TOPRIGHT)
		self.MIDLEFT = Position(1, 2, "w", Pos.MIDLEFT)
		self.MID = Position(2, 2, "ns", Pos.MID)
		self.MIDRIGHT = Position(3, 2, "e", Pos.MIDRIGHT)
		self.BOTLEFT = Position(1, 3, "sw", Pos.BOTLEFT)
		self.BOTMID = Position(2, 3, "s", Pos.BOTMID)
		self.BOTRIGHT = Position(3, 3, "se", Pos.BOTRIGHT)
		self.MirrorTTL = 60
		self.NotifTTL = 10
		self.AlexaTTL = 1
		self.NewsPOS = self.BOTRIGHT
		self.ClockPOS = self.TOPRIGHT
		self.WeatherPOS = self.TOPLEFT
		self.SensorPOS = self.BOTRIGHT
		self.GuidePOS = self.BOTLEFT
		self.AlexaPOS = self.BOTLEFT
		self.NotifPOS = self.MID
		confFile = 'config.cfg'
		try:
			config = configparser.ConfigParser()
			config.read(confFile)
			self.MirrorTTL = int(config['Mirror']['MirrorTTL'])
			self.NotifTTL = int(config['Mirror']['NotifTTL'])
			self.AlexaTTL = int(config['Mirror']['AlexaTTL'])
			self.NewsPOS = self.PositionResolver(str(config['Mirror']['NewsPOS']))
			self.ClockPOS = self.PositionResolver(str(config['Mirror']['ClockPOS']))
			self.WeatherPOS = self.PositionResolver(str(config['Mirror']['WeatherPOS']))
			self.SensorPOS = self.PositionResolver(str(config['Mirror']['SensorPOS']))
			self.GuidePOS = self.PositionResolver(str(config['Mirror']['GuidePOS']	))
			self.AlexaPOS = self.PositionResolver(str(config['Mirror']['AlexaPOS']))
			self.NotifPOS = self.PositionResolver(str(config['Mirror']['NotifPOS']	))
		except (IOError, KeyError):
			print("Config not found, using defaults.")
			print(self.BOTRIGHT)
			config = configparser.ConfigParser()
			config['Mirror'] = {'MirrorTTL':self.MirrorTTL,
								'NotifTTL':self.NotifTTL,
								'AlexaTTL':self.AlexaTTL,
								'NewsPOS':self.NewsPOS,
								'ClockPOS':self.ClockPOS,
								'WeatherPOS':self.WeatherPOS,
								'SensorPOS':self.SensorPOS,
								'GuidePOS':self.GuidePOS,
								'AlexaPOS':self.AlexaPOS,
								'NotifPOS':self.NotifPOS}
			with open(confFile, 'w') as configfile:
				config.write(configfile)
				
	def PositionResolver(self, _config: str) -> Position:
		if _config == str(Pos.TOPLEFT):
			return self.TOPLEFT
		elif _config == str(Pos.TOPMID):
			return self.TOPMID
		elif _config == str(Pos.TOPRIGHT):
			return self.TOPRIGHT
		elif _config == str(Pos.MIDLEFT):
			return self.MIDLEFT
		elif _config == str(Pos.MID):
			return self.MID
		elif _config == str(Pos.MIDRIGHT):
			return self.MIDRIGHT
		elif _config == str(Pos.BOTLEFT):
			return self.BOTLEFT
		elif _config == str(Pos.BOTMID):
			return self.BOTMID
		elif _config == str(Pos.BOTRIGHT):
			return self.BOTRIGHT
		else:
			return self.BOTRIGHT
