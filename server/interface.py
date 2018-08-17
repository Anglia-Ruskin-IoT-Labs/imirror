#!/usr/bin/python3
"""
SmartMirror.py
A python program to output data for use with a smartmirror.
It fetches weather, news, and time information.
"""
from traceback import print_exc			# installed modules
from json import loads
from time import strftime
import time
from datetime import datetime, timedelta
from threading import Lock
import locale
import threading
import pathlib
from contextlib import contextmanager
from requests import get
from feedparser import parse
import PIL.Image, PIL.ImageTk
from tkinter import *					# Recommended way for tkinter

from server.gui_positions import Pos	# custom modules
import config as cfg

# --------------------------------------------------------
# Constants
# --------------------------------------------------------

### Darksky API weather constants ###
# For full lust of language and unit paramaeters see:
# https://darksky.net/dev/docs/forecast
#
# Replace with secret key provided at https://darksky.net/dev/account/
WEATHER_API_TOKEN = '443a029b56964c639cb8f6da87415c20'

### IpStack Location API token
# replace with key provided on https://ipstack.com/dashboard
LOCATION_API_TOKEN = '66c1f2e2627bb5299404ddfbe5ff5185'
WEATHER_LANG = 'en'
WEATHER_UNIT = 'uk2'
ICON_DIR = "icons/"

ICON_LOOKUP = {
	'clear-day': ICON_DIR + "sun.png",  			# Clear Sky
	'wind': ICON_DIR + "wind.png", 					# Wind
	'cloudy': ICON_DIR + "cloud.png",  				# Cloudy day
	'partly-cloudy-day': ICON_DIR + "sun-cloud.png",# Partial clouds
	'rain': ICON_DIR + "rain.png",  				# Rain
	'snow': ICON_DIR + "snow.png",  				# Snow
	'snow-thin': ICON_DIR + "snow.png", 			# Sleet
	'fog': ICON_DIR + "fog.png",  					# Fog
	'clear-night': ICON_DIR + "moon.png", 			# Clear night
	'partly-cloudy-night': ICON_DIR + "moon-cloud.png",# Partial clouds night
	'thunderstorm': ICON_DIR + "lightning.png",  	# Storm
	'tornado': ICON_DIR + "tornado.png",  			# tornado
	'hail': ICON_DIR + "hail.png"  					# hail
}
### Locale and time constants ###
LOCALE_LOCK = Lock()
UI_LOCALE = 'en_GB.utf-8'							# set to your own locale. Use locale -a to list installed locales
TIME_FORMAT = None									# leave blank for 24h time format
DATE_FORMAT = "%b %d, %Y"							# check python doc for strftime() for more date formatting options

### Tkinter formatting constants ###
XL_TEXT = 94
LG_TEXT = 48
MD_TEXT = 28
SM_TEXT = 18
XS_TEXT = 12

@contextmanager
def setlocale(name):
	"""	used to set the locale using system locale for 
	accurate time information.	"""
	with LOCALE_LOCK:
		saved = locale.setlocale(locale.LC_ALL)
		try:
			yield locale.setlocale(locale.LC_ALL, name)
		finally:
			locale.setlocale(locale.LC_ALL, saved)

# --------------------------------------------------------
# Widgets
# --------------------------------------------------------
class Weather(Frame):
	"""	This class contains methods that fetch weather information.
	Weather information is based upon location.
	Location is determined using the device's IP address. """
	def __init__(self, parent):
		"""Constructor, Stores weather information."""
		Frame.__init__(self, parent, bg='black')
		self.temperature = ''										# data storage variables
		self.forecast = ''
		self.location = ''
		self.latitude = ''
		self.longitude = ''
		self.currently = ''
		self.icon = ''
		
		self.degree_frame = Frame(self, bg="black")					# tkinter settings
		self.degree_frame.pack(side=TOP, anchor=W)
		self.temperature_label = Label(self.degree_frame, \
			 font=('Lato', XL_TEXT),fg='white', bg="black")
		self.temperature_label.pack(side=LEFT, anchor=N)
		self.icon_label = Label(self.degree_frame, bg="black")
		self.icon_label.pack(side=LEFT, anchor=N, padx=20, pady=25)
		self.currently_label = Label(self, font=('Lato', MD_TEXT), \
			fg="white", bg="black")
		self.currently_label.pack(side=TOP, anchor=W)
		self.forecast_label = Label(self, font=('Lato', SM_TEXT), \
			fg='white', bg='black', wraplength = 700, justify=LEFT)
		self.forecast_label.pack(side=TOP, anchor=W)
		self.location_label = Label(self, font=('Lato', SM_TEXT), \
			fg="white", bg="black")
		self.location_label.pack(side=TOP, anchor=W)

		self.get_location()											#running methods
		self.get_weather()


	def get_location(self):
		"""	Method to fetch device location based upon IP address. """
		try:
			### Fetch location using freegeoip API ###
			# store location URL. Uses IP fetched by get_ip() in variable
			location_req_url = ("http://api.ipstack.com/" + str(self.get_ip()) +
								"?access_key=" + LOCATION_API_TOKEN + "&output=json&legacy=1")
			req = get(location_req_url)							# fetch data from URL
			location_obj = loads(req.text)						# convert fetched data to object
			if self.latitude != location_obj['latitude']:		# change latitude variable if device has moved.
				self.latitude = location_obj['latitude']
			if self.longitude != location_obj['longitude']:		# change latitude variable if device has moved.
				self.longitude = location_obj['longitude']
			location_tmp = "%s, %s" % \
					(location_obj['city'], location_obj['region_code']) # get current location and store in tmp variable
			if self.location != location_tmp:					# update weather information
				self.location = location_tmp
				self.location_label.config(text=location_tmp)
		except Exception as exc:
			print_exc()
			return "Error: %s. Cannot get location." % exc

	def get_weather(self):
		"""	Method that fetches weather information """
		try:
			### Get weather information using Darksky API ###
			# store the darksky API URL in variable
			weather_req_url =\
				"https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" \
				% (WEATHER_API_TOKEN, self.latitude, self.longitude,\
				   WEATHER_LANG, WEATHER_UNIT)
			req = get(weather_req_url) 								# fetch data from URL
			weather_obj = loads(req.text) 							# convert fetched data to object
			### Assign weather information to variables ###
			degree_sign = u'\N{DEGREE SIGN}'
			temperature_tmp = "%s%s" % \
					(str(int(weather_obj['currently']['temperature'])), \
					 degree_sign)									# Current temperature
			currently_tmp = weather_obj['currently']['summary'] 	# Current Weather
			forecast_tmp = weather_obj['hourly']['summary']			# Frorecast
			icon_id = weather_obj['currently']['icon']				# Weather icon id
			icon_tmp = None
			if icon_id in ICON_LOOKUP:								# weather icon lookup
				icon_tmp = ICON_LOOKUP[icon_id]

			if icon_tmp is not None:
				if self.icon != icon_tmp:														
					self.icon = icon_tmp							# set self.icon to the new icon
					image = PIL.Image.open(pathlib.Path(icon_tmp))	# open the image file
					image = image.resize((100, 100), PIL.Image.ANTIALIAS)# resize the image and antialias
					image = image.convert('RGB')
					photo = PIL.ImageTk.PhotoImage(image)			# convert image to tkinter object and store in variable
					self.icon_label.config(image=photo)				# apply settings to self.icon_label
					self.icon_label.image = photo
			else:	# remove image
				self.icon_label.config(image='')
			if self.currently != currently_tmp:						# update all weather information
				self.currently = currently_tmp
				self.currently_label.config(text=currently_tmp)
			if self.forecast != forecast_tmp:
				self.forecast = forecast_tmp
				self.forecast_label.config(text=forecast_tmp)
			if self.temperature != temperature_tmp:
				self.temperature = temperature_tmp
				self.temperature_label.config(text=temperature_tmp)
		except Exception as exc:
			print_exc()
			print("Error %s. Cannot get weather." % exc)
		self.after(300000, self.get_weather)


	@staticmethod
	def get_ip():
		"""	gets the IP address of the device and returns it """
		try:
			### Fetch IP address using IPify API ###
			# store ipify API URL in variable
			ip_url = "https://api.ipify.org?format=json"
			req = get(ip_url)							# fetch data from URL
			ip_obj = loads(req.text)					# convert fetched data to object
			return ip_obj['ip']							# return value
		except Exception as exc:
			print_exc()
			return "Error: %s. Cannot get IP." % exc


class Clock(Frame):
	"""
	Clock class
	Outputs date and time info to tkinter GUI.
	"""
	def __init__(self, parent):
		"""	Clock constructor, Stores time information and tkinter 
		configuration options. """
		self.time = ''
		self.day = ''
		self.date = ''

		Frame.__init__(self, parent, bg='black')
		self.time_label = Label(self, font=('Lato', LG_TEXT),\
								   fg="white", bg="black")
		self.time_label.pack(side=TOP, anchor=E, fill=X)

		self.date_label = Label(self, font=('Lato', SM_TEXT),\
								   fg="white", bg="black")
		self.date_label.pack(side=TOP, anchor=E)

		self.day_label = Label(self, font=('Lato', SM_TEXT),\
								  fg="white", bg="black")
		self.day_label.pack(side=TOP, anchor=E)
		self.update_time()

	def update_time(self):
		"""	update_time method
		updates the time using system locale."""
		with setlocale(UI_LOCALE):
			if TIME_FORMAT == 12:
				time_tmp = strftime('%I:%M %p')
			else:
				time_tmp = strftime('%H:%M')

			day_tmp = strftime('%A')
			date_tmp = strftime(DATE_FORMAT)

			if time_tmp != self.time:
				self.time = time_tmp
				self.time_label.config(text=time_tmp)
			if date_tmp != self.date:
				self.date = date_tmp
				self.date_label.config(text=date_tmp)
			if day_tmp != self.day:
				self.day = day_tmp
				self.day_label.config(text=day_tmp)

			self.time_label.after(200, self.update_time)


class News(Frame):
	"""
	News class
	Fetches news from BBC RSS feed and outputs top 5 headlines.
	"""
	def __init__(self, parent):
		"""	contructor, stores headline data for News object """
		Frame.__init__(self, parent)
		self.config(bg='black')
		self.title = 'News'
		self.news_label = Label(self, text=self.title, \
								   font=('Lato', MD_TEXT), \
								   fg='white', bg='black')
		self.news_label.pack(side=TOP, anchor=E)
		self.headlines_label = Label(self, font=('Lato', SM_TEXT), \
							  fg='white', bg='black', wraplength = 800)
		self.headlines_label.pack(side=TOP, anchor=E)

		self.get_news()

	def get_news(self):
		"""	fetches XML data from the BBC using feedparser """
		try:
			# reset headline info in headline_container
			self.headlines_label.config(text="")

			### Fetch XML data from news website ###
			# store XML url in variable
			news_url = "http://feeds.bbci.co.uk/news/uk/rss.xml"
			# parse XML data into Python object and store in variable
			feed = parse(news_url)
			# store headlines in array
			headlines = []
			# iterate through XML and store first 5 headlines in self.headlines
			index = 0
			for item in feed.entries[0:5]:
				# create child widgets containing
				headlines.insert(index, item.title)
				index += 1

			# join the contents of headlines into
			headlines_tmp = '\n'.join(headlines)
			self.headlines_label.config(text=headlines_tmp)
		except Exception as exc:
			print_exc()
			print("Error %s. Cannot get news." % exc)
		self.after(300000, self.get_news)
		
class ThunderBoardSensor(Frame):
	""" Displays all sensors reading on the thunderbird"""
	def __init__(self, parent):
		'''Constructor'''
		Frame.__init__(self, parent, bg='black')
		self.title = 'Thunderboard sensors'
		self.title_label = Label(self, text=self.title, \
									font=('Lato', MD_TEXT), \
								    fg='white', bg='black')
		self.title_label.pack(side=TOP, anchor=E)
		self.readings_label = Label(self, text = "Thunderboard not available",
								   font=('Lato', XS_TEXT),
								   fg='white', bg='black', wraplength = 500, justify = LEFT)
		self.readings_label.pack(side=TOP, anchor=E)

	def UpdateReadings(self, data):
		message = (str(data["info"]) + "\n" + 
					"Temperature: " + str(data["temperature"]) + "\n" + 
					"Humidity: " + str(data["humidity"]) + "\n" + 
					"Ambient Light: " + str(data["ambientLight"]) + "\n" + 
					"UV index: " + str(data["uvIndex"]) + "\n" + 
					"CO2 level: " + str(data["co2"]) + "\n" + 
					"VOC level: " + str(data["voc"]) + "\n" + 
					"Sound level: " + str(data["sound"]) + "\n" + 
					"Pressure: " + str(data["pressure"]) + "\n")
		self.readings_label.config(text=message)	
			
			

class Alexa(Frame):
	""" Prints the sent textfields what are passed in."""
	def __init__(self, parent, frameTtl):
		""" Constructor """		
		self.ALEXA_VISIBLE = frameTtl # in seconds
		Frame.__init__(self, parent, bg='black')		
		self.title = ''
		self.alexa_label = Label(self, text=self.title, \
								   font=('Lato', MD_TEXT), \
								   fg='white', bg='black')
		self.alexa_label.pack(side=TOP, anchor=W)
		self.text_label = Label(self, text = "",
								   font=('Lato', SM_TEXT),
								   fg='white', bg='black', wraplength = 500, justify = LEFT)
		self.text_label.pack(side=TOP, anchor=N)
			
	def GetText(self, _title, _text, _time):
		''' Changes Alexa frames text and updates 
		'''
		self.text_label.config(text=_text)
		self.alexa_label.config(text=_title)
		self.lastMessage = _time
			
class PopUp(Frame):
	''' Label that destroys itself after 5 seconds
	'''	
	def __init__(self, parent):
		Frame.__init__(self, parent, bg='black')
		
		self.title = 'Notification'
		self.title_label = Label(self, text=self.title, \
								   font=('Lato', MD_TEXT), \
								   fg='white', bg='black')
		self.title_label.pack(side=TOP, anchor=N)
		self.text_label = Label(self, text = '',
								   font=('Lato', SM_TEXT),
								   fg='white', bg='black', width = 200, 
								   wraplength = 200)
		self.text_label.pack(side=TOP, anchor=N)
			
	def UpdateText(self, _text):
		self.text_label.config(text = _text)
		
class Guide(Frame):
	'''Guide for beginners
	'''
	def __init__(self, parent):
		Frame.__init__(self, parent, bg='black')
		self.title = 'Guide'
		self.guide = "To begin to interact with me " + \
	    "you can say 'Alexa, open iMirror from " + \
	    "Anglia Ruskin'. You can also interact with " + \
	    "Alexa as you normally would. There are more skills " + \
	    "to open, like: 'BuzzBox from Anglia Ruskin', and " + \
	    "'Zork from Anglia Ruskin'"
		self.title_label = Label(self, text=self.title, \
								   font=('Lato', MD_TEXT), \
								   fg='white', bg='black', justify = LEFT)
		self.title_label.pack(side=TOP, anchor=W)
		self.text_label = Label(self, text = self.guide,
								   font=('Lato', SM_TEXT),
								   fg='white', bg='black', justify = LEFT,
								   wraplength = 500)
		self.text_label.pack(side=TOP, anchor=N)
		
		
# --------------------------------------------------------
# Tkinter Main Window
# --------------------------------------------------------	
class BuildGUI(threading.Thread):
	"""
	BuildGUI class
	draws the GUI and contains methods for toggling fullcreen
	"""
	def __init__(self, _alexa_ttl: int, _notif_ttl: int):
		"""
		BuildGUI constructor
		sets the configuration options for the GUI and builds it.
		Self starts on a different thread.
		"""
		self.NOTIF_VISIBLE = _notif_ttl
		self.ALEXA_VISIBLE = _alexa_ttl
		# Variables to store names of overwritten widgets
		self.lastBeforeAlexa = None
		self.lastBeforeNotif = None
		self.lastNotification = datetime.min
		threading.Thread.__init__(self)
		self.daemon = True
		self.start()
		
	def callback(self):
		self.root.quit()
		
	def run(self):
		# Creating Window, config
		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.config(background='black')
		self.root.attributes("-fullscreen", True)
		self.state = False
		
		# Creating the grid
		self.root.grid_rowconfigure(1, weight=0, minsize = 360)
		self.root.grid_rowconfigure(2, weight=1, minsize = 360)
		self.root.grid_rowconfigure(3, weight=0, minsize = 360)
		self.root.grid_columnconfigure(1, weight=0, minsize = 360)
		self.root.grid_columnconfigure(2, weight=1, minsize = 360)
		self.root.grid_columnconfigure(3, weight=0, minsize = 360)

		# ---------------------------------------------------
		# Creating Frames
		# ---------------------------------------------------
		
		# clock
		self.clock_parent = Frame(self.root, name = cfg.CLOCK_NAME, background='black')
		self.clock = Clock(self.clock_parent)
		self.clock.pack(side=RIGHT, padx=50, pady=50, fill=NONE, expand=NO)
		# weather
		self.weather_parent = Frame(self.root, name = cfg.WEATHER_NAME, background='black')
		self.weather = Weather(self.weather_parent)
		self.weather.pack(side=LEFT, padx=50, pady=50, fill=NONE, expand=NO)
		# news
		self.news_parent = Frame(self.root, name = cfg.NEWS_NAME, background='black')
		self.news = News(self.news_parent)
		self.news.pack(side=RIGHT, padx=50, pady=50, fill=NONE, expand=NO)
		self.news.headlines_label.config(justify=RIGHT)
		# alexa
		self.alexa_parent = Frame(self.root, name = cfg.ALEXA_NAME, background='black')
		self.alexa = Alexa(self.alexa_parent, self.ALEXA_VISIBLE)
		self.alexa.pack(side=LEFT, padx=50, pady=50, fill=NONE, expand=NO)
		self.alexa.alexa_label.config(justify=RIGHT)
		# thunderboard
		self.thunderboard_parent = Frame(self.root, name = cfg.SENSORS_NAME, background='black')
		self.thunderboard = ThunderBoardSensor(self.thunderboard_parent)
		self.thunderboard.pack(side=RIGHT, padx=50, pady=50, fill=NONE, expand=NO)
		self.thunderboard.readings_label.config(justify=RIGHT)
		# Notification Overlay
		self.overlay_frame = Frame(self.root, name = cfg.NOTIF_NAME, background='black')
		self.notif = PopUp(self.overlay_frame)
		self.notif.pack(side=RIGHT, padx=50, pady=50, fill=NONE, expand=NO)
		# guide
		self.guide_frame = Frame(self.root, name = cfg.GUIDE_NAME, background='black')
		self.guide = Guide(self.guide_frame)
		self.guide.pack(side=LEFT, padx=50, pady=50, fill=NONE, expand=NO)

		# Module Mappings
		self.frames = {
			cfg.ALEXA_NAME: self.alexa_parent,
			cfg.NOTIF_NAME: self.overlay_frame,
			cfg.CLOCK_NAME: self.clock_parent,
			cfg.NEWS_NAME: self.news_parent,
			cfg.WEATHER_NAME: self.weather_parent,
			cfg.GUIDE_NAME: self.guide_frame,
			cfg.SENSORS_NAME: self.thunderboard_parent
		}
				
		# ------------------------------------------------------
		# Keybindings for testing
		# -----------------------------------------------------
		self.root.bind("<Return>", self.toggle_fullscreen)
		self.root.bind("<Escape>", self.end_fullscreen)
		self.root.bind("<Up>", self.GuiOff)
		self.root.bind("2", lambda event, a="news": 
                            self.ToggleFrame(a))
		self.root.bind("3", lambda event, a="clock": 
                            self.ToggleFrame(a))
		self.root.bind("1", lambda event, a="weather": 
                            self.ToggleFrame(a))
		self.root.bind("4", lambda event, a="guide": 
                            self.ToggleFrame(a))
		self.root.bind("5", lambda event, a="sensors": 
                            self.ToggleFrame(a))
		self.root.bind("6", self.SendNotification)
		self.root.bind("7", self.GuiOff)
		self.root.bind("8", self.GuiOn)
		self.root.bind("9", lambda event, a="alexa", b="test", c=datetime.now(): 
                            self.UpdateAlexa(a, b, c))
		self.root.bind("<Escape>", self.GuiOn)
		
		
		# Gui is disabled by Default
		self.GuiOff()
		self.__HideNotifications()
		self.root.mainloop()
	
	def __HideNotifications(self):
		''' Hides notifications after a given time 
		specified in config '''
		if self.overlay_frame.winfo_ismapped() and \
				(self.lastNotification + timedelta(seconds = self.NOTIF_VISIBLE)) < datetime.now():
			self.overlay_frame.grid_forget()
			if self.lastBeforeNotif is not None: # Bring the overwritten widget back
				self.ToggleFrame(self.lastBeforeNotif)
				self.lastBeforeNotif = None # Reset
		if self.alexa_parent.winfo_ismapped() and \
				(self.alexa.lastMessage + timedelta(seconds = self.ALEXA_VISIBLE)) < datetime.now():
			self.alexa_parent.grid_forget()
			print(self.alexa.lastMessage)
			if self.lastBeforeAlexa is not None:
				self.ToggleFrame(self.lastBeforeAlexa)
				self.lastBeforeAlexa = None
		self.root.after(1000, lambda: self.__HideNotifications())	
		
	def toggle_fullscreen(self, event=None):
		""" toggles the GUI's fullscreen state when user presses return	"""
		self.state = not self.state
		self.root.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		""" ends the GUI's fullscreen state when user presses escape. """
		self.state = False
		self.root.attributes("-fullscreen", False)
		return "break"

# ---------------------------------------------------
# User Callable Methods
# ---------------------------------------------------
	def ShowFrame(self, _frame: str) -> bool:
		'''Same as ToggleFrame, but with weight
		increment (user action happened)'''
		if self.ToggleFrame(_frame):
			value = cfg.frameWeights.get(_frame)
			value += 1
			cfg.frameWeights[_frame] = value
			return True
		else:
			return False

	def HideFrame(self, _frame: str) -> bool:
		'''Hides and decrements weighting by 1'''
		try:	
			self.frames[_frame].grid_forget()
			value = cfg.frameWeights.get(_frame)
			value -= 1
			cfg.frameWeights[_frame] = value
			return True
		except Exception as e:
			print_exc()
			print("Cant turn GUI off, Error: " + str(e))
			return False


	def GuiOff(self, event=None) -> bool:
		""" Removes all widgets from the screen """
		try:
			frames = list(self.root.winfo_children())
			for frame in frames:
				frame.grid_forget()
			return True
		except Exception as e:
			print_exc()
			print("Cant turn GUI off, Error: " + str(e))
			return False

	def GuiOn(self, event=None):
		''' Turns preferred Widgets on.
		If there are more widgets for the same space, 
		Uses the most asked for one.'''
		try:
			positions = dict()
			# Collects widgets positions, exlucdes ALEXA_NAME and NOTIF_NAME
			for name, position in cfg.framePositions.items():  
				if str(name) == cfg.ALEXA_NAME or str(name) == cfg.NOTIF_NAME: 	# Exceptions
					pass
				elif str(position) in positions: # Existing position, append
					temp = positions.get(str(position))
					temp.append(name)
					positions[str(position)] = temp
				else:
					positions[str(position)] = [str(name)] # New position
			# Selects most asked for widget for each position		
			for position, names in positions.items():
				widgetWeights = dict()
				for name in names:
					widgetWeights[str(name)] = cfg.frameWeights[name]
				highestWidget = max(widgetWeights, key=widgetWeights.get)
				self.ToggleFrame(highestWidget)
			return True
		except Exception as e:
			print_exc()
			print("GuiOn failed with errors, Error: " + str(e))
			return False

	def ChangeFramePosition(self, _frame: str, _position: Pos) -> bool:
		"""Changes a Widget saved Position and saves it to the mappings
		   and config."""
		try:
			cfg.framePositions[_frame] = _position
			#if frame.winfo_ismapped():
			self.ToggleFrame(_frame)
			return True
		except Exception as e:
			print_exc()
			print("Cant turn GUI off, Error: " + str(e))
			return False

# ----------------------------------------------
# Machine Callable Methods
# ----------------------------------------------

	def ToggleFrame(self, _frame: str) -> bool:
		"""Turns a passed in widget on, hiding everything what was on the
		   same position."""
		try:
			frame = self.frames.get(_frame)
			#----------------------------------------------------
			# Hide modules visible at the same position
			for name, position in cfg.framePositions.items():   
				if position == cfg.framePositions[frame.winfo_name()]:
					if self.frames[name].winfo_ismapped():
						self.frames[name].grid_forget()
			#----------------------------------------------------
			# Show given frame
			frame.grid(
				row = cfg.framePositions[frame.winfo_name()].value.row, 
				column = cfg.framePositions[frame.winfo_name()].value.column, 
				sticky = cfg.framePositions[frame.winfo_name()].value.alignment)
			return True
		except Exception as e:
			print_exc()
			print("Can't turn widget on, Error: " + str(e))
			return False
		
	def SendNotification(self, _text, event=None):
		for name, position in cfg.framePositions.items():   
			if position == cfg.framePositions[cfg.NOTIF_NAME]:
				if self.frames[name].winfo_ismapped():
					self.lastBeforeNotif = name # Important to bring back widget
					self.frames[name].grid_forget() 
		self.notif.UpdateText(_text)
		self.ToggleFrame(cfg.NOTIF_NAME)
		self.lastNotification = datetime.now()
		
	def UpdateAlexa(self, _title, _text, _time, event=None):
		''' Updates the text in Alexa Frame
		'''
		# Hide modules visible at the same position
		for name, position in cfg.framePositions.items():   
			if position == cfg.framePositions[cfg.ALEXA_NAME]:
				if self.frames[name].winfo_ismapped() and not name == cfg.ALEXA_NAME:
					self.lastBeforeAlexa = name  # Important to bring back widget
					self.frames[name].grid_forget()
		self.alexa.GetText(_title, _text, _time)
		self.ToggleFrame(cfg.ALEXA_NAME)
		
	def UpdateThunderboard(self, _data, event=None):
		self.thunderboard.UpdateReadings(_data)
	
# Self Init
#def run():
#	WINDOW = BuildGUI()
		
		
