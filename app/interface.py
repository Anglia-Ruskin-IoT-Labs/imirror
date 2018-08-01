#!/usr/bin/python
"""
SmartMirror.py
A python program to output data for use with a smartmirror.
It fetches weather, news, and time information.
"""

from traceback import print_exc
from json import loads
from time import strftime
import time
from datetime import datetime, timedelta
from threading import Lock
import locale
import threading

from contextlib import contextmanager
from requests import get
from feedparser import parse
from PIL import Image, ImageTk

# try/except to use correct Tkinter library depending on device.
try:
	from mttkinter import mtTkinter as tk
except ImportError:
	import tkinter as tk

### Darksky API weather constants ###
# replace with secret key provided at https://darksky.net/dev/account/
WEATHER_API_TOKEN = '443a029b56964c639cb8f6da87415c20'
### IpStack Location API token
LOCATION_API_TOKEN = '66c1f2e2627bb5299404ddfbe5ff5185'
# For full lust of language and unit paramaeters see:
# https://darksky.net/dev/docs/forecast
WEATHER_LANG = 'en'
WEATHER_UNIT = 'uk2'
ICON_DIR = "app/icons/"
# maps
ICON_LOOKUP = {
	'clear-day': ICON_DIR + "sun.png",  # Clear Sky
	'wind': ICON_DIR + "wind.png",  # Wind
	'cloudy': ICON_DIR + "cloud.png",  # Cloudy day
	'partly-cloudy-day': ICON_DIR + "sun-cloud.png",  # Partial clouds
	'rain': ICON_DIR + "rain.png",  # Rain
	'snow': ICON_DIR + "snow.png",  # Snow
	'snow-thin': ICON_DIR + "snow.png",  # Sleet
	'fog': ICON_DIR + "fog.png",  # Fog
	'clear-night': ICON_DIR + "moon.png",  # Clear night
	'partly-cloudy-night': ICON_DIR + "moon-cloud.png",  # Partial clouds night
	'thunderstorm': ICON_DIR + "lightning.png",  # Storm
	'tornado': ICON_DIR + "tornado.png",  # tornado
	'hail': ICON_DIR + "hail.png"  # hail
}
### Locale and time constants ###
LOCALE_LOCK = Lock()
# set to your own locale. Use locale -a to list installed locales
UI_LOCALE = 'en_GB.utf-8'
# leave blank for 24h time format
TIME_FORMAT = None
# check python doc for strftime() for more date formatting options
DATE_FORMAT = "%b %d, %Y"

### Tkinter formatting constants ###
XL_TEXT = 94
LG_TEXT = 48
MD_TEXT = 28
SM_TEXT = 18
XS_TEXT = 12


@contextmanager
def setlocale(name):
	"""
	setlocale class
	used to set the locale using system locale for accurate time information.
	"""

	with LOCALE_LOCK:
		saved = locale.setlocale(locale.LC_ALL)
		try:
			yield locale.setlocale(locale.LC_ALL, name)
		finally:
			locale.setlocale(locale.LC_ALL, saved)


class Weather(tk.Frame):
	"""
	Weather class
	This class contains methods that fetch weather information.
	Weather information is based upon location.
	Location is determined using the device's IP address.
	"""


	def __init__(self, parent):
		"""
		Weather constructor.
		Stores weather information.
		"""

		tk.Frame.__init__(self, parent, bg='black')
		# data storage variables
		self.temperature = ''
		self.forecast = ''
		self.location = ''
		self.latitude = ''
		self.longitude = ''
		self.currently = ''
		self.icon = ''

		# tkinter settings
		self.degree_frame = tk.Frame(self, bg="black")
		self.degree_frame.pack(side=tk.TOP, anchor=tk.W)

		self.temperature_label = tk.Label(self.degree_frame, \
										  font=('Lato', XL_TEXT), \
										  fg='white', bg="black")
		self.temperature_label.pack(side=tk.LEFT, anchor=tk.N)

		self.icon_label = tk.Label(self.degree_frame, bg="black")
		self.icon_label.pack(side=tk.LEFT, anchor=tk.N, padx=20, pady=25)

		self.currently_label = tk.Label(self, font=('Lato', MD_TEXT), \
										fg="white", bg="black")
		self.currently_label.pack(side=tk.TOP, anchor=tk.W)

		self.forecast_label = tk.Label(self, font=('Lato', SM_TEXT), \
									   fg='white', bg='black', wraplength = 700, justify=tk.LEFT)
		self.forecast_label.pack(side=tk.TOP, anchor=tk.W)

		self.location_label = tk.Label(self, font=('Lato', SM_TEXT), \
									   fg="white", bg="black")
		self.location_label.pack(side=tk.TOP, anchor=tk.W)

		self.get_location()
		self.get_weather()


	def get_location(self):
		"""
		get_location
		Method to fetch device location based upon IP address.
		"""

		try:
			### Fetch location using freegeoip API ###
			# store location URL. Uses IP fetched by get_ip() in variable
			location_req_url = ("http://api.ipstack.com/" + str(self.get_ip()) +
								"?access_key=" + LOCATION_API_TOKEN + "&output=json&legacy=1")
			# fetch data from URL in location_req_url and store in variable
			req = get(location_req_url)
			# convert fetched data to python object and store in variable
			location_obj = loads(req.text)

			# change latitude variable if device has moved.
			if self.latitude != location_obj['latitude']:
				self.latitude = location_obj['latitude']
				# change latitude variable if device has moved.
				if self.longitude != location_obj['longitude']:
					self.longitude = location_obj['longitude']

			# get current location and store in tmp variable
			location_tmp = "%s, %s" % \
					(location_obj['city'], location_obj['region_code'])

			# update weather information
			if self.location != location_tmp:
				self.location = location_tmp
				self.location_label.config(text=location_tmp)

		except Exception as exc:
			print_exc()
			return "Error: %s. Cannot get location." % exc

	def get_weather(self):
		"""
		get_weather
		Method that fetches weather information
		"""

		try:
			### Get weather information using Darksky API ###
			# store the darksky API URL in variable
			weather_req_url =\
				"https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" \
				% (WEATHER_API_TOKEN, self.latitude, self.longitude,\
				   WEATHER_LANG, WEATHER_UNIT)
			# fetch data from URL in weather_req_url and store in a variable
			req = get(weather_req_url)
			# convert fetched data to puthon object and store in variable
			weather_obj = loads(req.text)

			### Assign weather information to variables ###
			# store unicode degree character in variable
			degree_sign = u'\N{DEGREE SIGN}'
			# get current temperature and store in tmp variable
			temperature_tmp = "%s%s" % \
					(str(int(weather_obj['currently']['temperature'])), \
					 degree_sign)
			# get current weather summary and store in tmp variable
			currently_tmp = weather_obj['currently']['summary']
			# get the forecast summary and store it in tmp variable
			forecast_tmp = weather_obj['hourly']['summary']
			# get the ID of the icon and store in variable
			icon_id = weather_obj['currently']['icon']
			icon_tmp = None

			# fetch weather icon informaton stored in weather_obj
			if icon_id in ICON_LOOKUP:
				icon_tmp = ICON_LOOKUP[icon_id]

			if icon_tmp is not None:
				if self.icon != icon_tmp:
					# set self.icon to the new icon
					self.icon = icon_tmp
					# open the image file
					image = Image.open(icon_tmp)
					# resize the image and antialias
					image = image.resize((100, 100), Image.ANTIALIAS)
					image = image.convert('RGB')
					# convert image to tkinter object and store in variable
					photo = ImageTk.PhotoImage(image)

					# apply settings to self.icon_label
					self.icon_label.config(image=photo)
					self.icon_label.image = photo
			else:
				# remove image
				self.icon_label.config(image='')

			# update weather information
			if self.currently != currently_tmp:
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
		"""
		get_ip
		gets the IP address of the device and returns it
		"""

		try:
			### Fetch IP address using IPify API ###
			# store ipify API URL in variable
			ip_url = "https://api.ipify.org?format=json"
			# fetch data from URL in ip_url and store in variable
			req = get(ip_url)
			# convert fetched data to python object and store in variable
			ip_obj = loads(req.text)

			# return value stored in 'ip' JSON attribute
			return ip_obj['ip']

		except Exception as exc:
			print_exc()
			return "Error: %s. Cannot get IP." % exc


class Clock(tk.Frame):
	"""
	Clock class
	Outputs date and time info to tkinter GUI.
	"""
	def __init__(self, parent):
		"""
		Clock constructor
		Stores time information and tkinter configuration options.
		"""

		self.time = ''
		self.day = ''
		self.date = ''

		tk.Frame.__init__(self, parent, bg='black')
		self.time_label = tk.Label(self, font=('Lato', LG_TEXT),\
								   fg="white", bg="black")
		self.time_label.pack(side=tk.TOP, anchor=tk.E, fill=tk.X)

		self.date_label = tk.Label(self, font=('Lato', SM_TEXT),\
								   fg="white", bg="black")
		self.date_label.pack(side=tk.TOP, anchor=tk.E)

		self.day_label = tk.Label(self, font=('Lato', SM_TEXT),\
								  fg="white", bg="black")
		self.day_label.pack(side=tk.TOP, anchor=tk.E)
		self.update_time()

	def update_time(self):
		"""
		update_time method
		updates the time using system locale.
		"""

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


class News(tk.Frame):
	"""
	News class
	Fetches news from BBC RSS feed and outputs top 5 headlines.
	"""


	def __init__(self, parent):
		"""
		News contructor
		stores headline data for News object
		"""

		tk.Frame.__init__(self, parent)
		self.config(bg='black')
		self.title = 'News'
		self.news_label = tk.Label(self, text=self.title, \
								   font=('Lato', MD_TEXT), \
								   fg='white', bg='black')
		self.news_label.pack(side=tk.TOP, anchor=tk.E)
		self.headlines_label = tk.Label(self, font=('Lato', SM_TEXT), \
							  fg='white', bg='black', wraplength = 800)
		self.headlines_label.pack(side=tk.TOP, anchor=tk.E)

		self.get_news()

	def get_news(self):
		"""
		get_news class
		fetches XML data from the BBC using feedparser
		"""

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
		
class ThunderBoardSensor(tk.Frame):
	""" Displays all sensors reading on the thunderbird
	"""	
	
	def __init__(self, parent):
		'''Constructor'''
			
		tk.Frame.__init__(self, parent, bg='black')
		self.title = 'Thunderboard sensors'
		self.title_label = tk.Label(self, text=self.title, \
									font=('Lato', MD_TEXT), \
								    fg='white', bg='black')
		self.title_label.pack(side=tk.TOP, anchor=tk.E)
		self.readings_label = tk.Label(self, text = "Thunderboard not available",
								   font=('Lato', XS_TEXT),
								   fg='white', bg='black', wraplength = 500, justify = tk.LEFT)
		self.readings_label.pack(side=tk.TOP, anchor=tk.E)

								  
	
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
			
			

class Alexa(tk.Frame):
	""" Prints the sent textfields what are passed in.
	"""
		
	def __init__(self, parent):
		""" Constructor """
		tk.Frame.__init__(self, parent, bg='black')
		self.title = ''
		self.alexa_label = tk.Label(self, text=self.title, \
								   font=('Lato', MD_TEXT), \
								   fg='white', bg='black')
		self.alexa_label.pack(side=tk.TOP, anchor=tk.W)
		self.text_label = tk.Label(self, text = "",
								   font=('Lato', SM_TEXT),
								   fg='white', bg='black', wraplength = 500, justify = tk.LEFT)
		self.text_label.pack(side=tk.TOP, anchor=tk.N)
		self.IsTextOld()
	
		
	def GetText(self, _title, _text, _time):
		''' Changes Alexa frames text and updates 
		'''
		self.text_label.config(text=_text)
		self.alexa_label.config(text=_title)
		self.lastMessage = _time
		
	def IsTextOld(self):
		''' Deletes All text from alexa frame if the last message is
			older than 5 minutes.
		'''
		try:
			if (self.lastMessage + timedelta(minutes = 5)) < datetime.now():
				self.text_label.config(text="")
				self.alexa_label.config(text="")
				self.loop = self.after(5000, self.IsTextOld)
				
			else:
				self.loop = self.after(5000, self.IsTextOld)
				pass
		# No Message is passed in yet
		except AttributeError:
			self.loop = self.after(5000, self.IsTextOld)
			pass
			
class PopUp(tk.Frame):
	''' Label that destroys itself after 5 seconds
	'''
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg='black')
		self.title = 'Notification'
		self.alexa_label = tk.Label(self, text=self.title, \
								   font=('Lato', MD_TEXT), \
								   fg='white', bg='black')
		self.alexa_label.pack(side=tk.TOP, anchor=tk.N)
		self.text_label = tk.Label(self, text = '',
								   font=('Lato', SM_TEXT),
								   fg='white', bg='black')
		self.text_label.pack(side=tk.TOP, anchor=tk.N)
		
		
		
		
	def UpdateText(self, _text):
		self.text_label.config(text = _text)
		

		

class BuildGUI(threading.Thread):
	"""
	BuildGUI class
	draws the GUI and contains methods for toggling fullcreen
	"""

	"""
	BuildGUI constructor
	sets the configuration options for the GUI and builds it.
	Self starts on a different thread.
	"""
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True
		self.start()
		
	def callback(self):
		self.root.quit()
		
	def run(self):
		# Creating Window, config
		self.root = tk.Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.config(background='black')
		self.root.attributes("-fullscreen", True)
		self.state = False
		
		# Creating frames
		self.weather_parent = tk.Frame(self.root, background='black')
		self.clock_parent = tk.Frame(self.root, background='black')
		self.news_parent = tk.Frame(self.root, background='black')
		self.alexa_parent = tk.Frame(self.root, background='black')
		self.thunderboard_parent = tk.Frame(self.root, background='black')
		self.overlay_frame = tk.Frame(self.root, background='black')

		# Creating the grid
		self.root.grid_rowconfigure(1, weight=1)
		self.root.grid_columnconfigure(1, weight=1)
	
		
		
		
		## Putting the modules into their objects
		# clock
		self.clock = Clock(self.clock_parent)
		self.clock.pack(side=tk.RIGHT, padx=50, pady=50, fill=tk.NONE, expand=tk.NO)
		# weather
		self.weather = Weather(self.weather_parent)
		self.weather.pack(side=tk.LEFT, padx=50, pady=50, fill=tk.NONE, expand=tk.NO)
		# news
		self.news = News(self.news_parent)
		self.news.pack(side=tk.RIGHT, padx=50, pady=50, fill=tk.NONE, expand=tk.YES)
		self.news.headlines_label.config(justify=tk.RIGHT)
		# alexa
		self.alexa = Alexa(self.alexa_parent)
		self.alexa.pack(side=tk.LEFT, padx=50, pady=50, fill=tk.NONE, expand=tk.NO)
		self.alexa.alexa_label.config(justify=tk.RIGHT)
		# thunderboard
		self.thunderboard = ThunderBoardSensor(self.thunderboard_parent)
		self.thunderboard.pack(side=tk.RIGHT, padx=50, pady=50, fill=tk.NONE, expand=tk.NO)
		self.thunderboard.readings_label.config(justify=tk.RIGHT)

		# popup
		self.notif = PopUp(self.overlay_frame)
		self.notif.pack(side=tk.RIGHT, padx=50, pady=50, fill=tk.NONE, expand=tk.NO)
		
		# Toggles between fot testing
		self.root.bind("<Return>", self.toggle_fullscreen)
		self.root.bind("<Escape>", self.end_fullscreen)
		self.root.bind("<Up>", self.GuiOff)
		self.root.bind("2", self.ToggleWeather)
		self.root.bind("3", self.ToggleClock)
		self.root.bind("1", self.ToggleNews)
		#self.root.bind("4", self.ToggleAlexa)
		self.root.bind("5", self.ToggleThunderBoard)
		self.root.bind("6", self.SendNotification)
		self.root.bind("<Escape>", self.ToggleAll)
		
		# Gui is disabled by Default
		self.GuiOff()
		self.__HideNotifications()
		self.root.mainloop()

		
		
	
		
	def __HideNotifications(self):
		if self.overlay_frame is not None:
			self.overlay_frame.grid_forget()
		self.root.after(7000, lambda: self.__HideNotifications())
		
		
	def toggle_fullscreen(self, event=None):
		"""
		toggle_fullscreen method
		toggles the GUI's fullscreen state when user presses return
		"""

		self.state = not self.state
		self.root.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		"""
		end_fullscreen method
		ends the GUI's fullscreen state when user presses escape.
		"""
		self.state = False
		self.root.attributes("-fullscreen", False)
		return "break"
	
	def GuiOff(self, event=None):
		''' Removes all frames from the screen, 
			leaving it blank
		'''
		if self.weather_parent.winfo_ismapped():
			self.weather_parent.grid_forget()
		if self.news_parent.winfo_ismapped():
			self.news_parent.grid_forget()
		if self.clock_parent.winfo_ismapped():
			self.clock_parent.grid_forget()
		if self.thunderboard_parent.winfo_ismapped():
			self.thunderboard_parent.grid_forget()
		if self.alexa_parent.winfo_ismapped():
			self.alexa_parent.grid_forget()
		return "break"
	
	def ToggleWeather(self, event=None):
		''' Turns on the Weather Frame
		'''
		if not self.weather_parent.winfo_ismapped():
			self.weather_parent.grid(row=0, columnspan = 2, sticky="nw")
		return "break"
	
	def ToggleClock(self, event=None):
		''' Turns on the Clock frame
		'''
		if not self.clock_parent.winfo_ismapped():
			self.clock_parent.grid(row=0, column = 2, sticky="ne")
		return "break"
	
	def ToggleNews(self, event=None):
		''' Turns on the news frame
		'''
		if self.thunderboard_parent.winfo_ismapped():
			self.thunderboard_parent.grid_forget()
		self.news_parent.grid(row=2, column = 1, columnspan = 2, sticky="se")
		return "break"
		

	
	def ToggleThunderBoard(self, event=None):
		''' Turns Thunderboard frame on
		'''
		if self.news_parent.winfo_ismapped():
			self.news_parent.grid_forget()
		self.thunderboard_parent.grid(row=2, column = 1, columnspan = 2, sticky="e")
		
	
	def ToggleAll(self, event=None):
		''' Turns all Frames on
		'''
		if self.news_parent.winfo_ismapped():
			pass
		elif self.thunderboard_parent.winfo_ismapped():
			pass
		else:
			self.ToggleNews()
			
			
		self.ToggleClock()	
		self.ToggleWeather()
		return "break"
		
	def SendNotification(self, _text, event=None):
		self.notif.UpdateText(_text)
		self.overlay_frame.grid(row=1, column=1, sticky='ns')
		
	
		
	def UpdateAlexa(self, _title, _text, _time, event=None):
		''' Updates the text in Alexa Frame
		'''
		self.alexa_parent.grid(row=2, column = 0, sticky="sw")
		self.alexa.GetText(_title, _text, _time)
		
	def UpdateThunderboard(self, _data, event=None):
		self.thunderboard.UpdateReadings(_data)
		

# Start the program.
# BuildGUI can be called from  outside as a threadsafe operation
#def run():
#	WINDOW = BuildGUI()
		
		
