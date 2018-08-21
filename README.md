# iMirror

**This is a smart mirror with a motion sensor and an API to control and customize its interface.**

It displays weather, news and time, and also displays amazon alexa textfielfds
from cards accepting the payload from an endpoint.

Motion sensor activates mirror for 60 seconds.

Capabilities to move and show/hide widgets are implemented, remembers positions and widget preferences.

Thunderboard implemented, basic notifications implemented for temperature and CO2 levels

For Voice Control implementation  [Alexa-Voice-sdk](https://github.com/Floyd0122/avs-device-sdk) repo needs to be installed to a device on the same network.


## Basic Setup of Raspberry Pi from fresh install for iMirror and its server:


Required: 
* Internet access

```bash
sudo raspi-config
```
Turn these on in raspi-config: 

* Wait for network on boot
* Optional: VNC

To remove black borders on screen
in /boot/config.txt uncomment 
```bash
disable_overscan=1
```

Disable XSession from Blanking  
```bash
sudo apt-get install xscreensaver
```
Once installed open the Pi's preferences and change screensaver preferences to disable screenblanking.

## Installation requirements

Clone the repo:
```bash
cd /home/pi && git clone https://github.com/Floyd0122/skill-server-imirror.git
```
Prevent any Compiling errors:
```bash
sudo apt-get install build-essential libssl-dev libffi-dev python-dev libglib2.0-dev
```
Install required packages:
```bash
sudo apt-get install python3 python3-pil.imagetk
```


Install script dependencies:

```bash
cd skill-server-imirror && sudo pip3 install -r requirements.txt
```

## Get API keys:
Go to [IpStack](https://ipstack.com/signup/free) and sign up for a free developer account.
Go to [darksky.net](https://darksky.net/dev/) and sign up for a free developer account. 

Edit **interface.py** and replace the contents of WEATHER_API_TOKEN with the secret key provided on [Darksky's account page](https://darksky.net/dev/account/).
Edit **interface.py** and replace the contents of LOCATION_API_TOKEN with the secret key provided on [IpStack's account page](https://ipstack.com/quickstart/).
```python
WEATHER_API_TOKEN = '[TOKEN]' # replace with secret key provided at https://darksky.net/dev/account/
```

## Set up autostart
Add these lines to ~/.config/lxsession/LXDE/autostart to run things at startup
```bash
@lxterminal -e sudo /home/pi/skill-server-imirror/run.py #$HOME doesnt work
```

Alternatively, you can create it as a servic via systemd: [HowTo link](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)

## Generate SSL Keys

We operate the webserver over https, at this time Flask's Werkzeug on the Pi doesn't generate sufficent keys to an ad-hoc SSL context, so we generate a pair on our own.

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
Copy the results into the /home/pi/skill-server-imirror/certs/ folder.

Connect the motion sensor ito the correct GPIO PINs
```
PIR SENSOR
GPIO GND [Pin 6]
GPIO 5V [Pin 2]
GPIO 7 [Pin 26]
```

## Running
Just restart the pi and it will autostart in a terminal
Alternatively you can run it with this command:
```bash
sudo /home/pi/skill-server-imirror/run.py
```

# Docs
## API endpoints

By default istening over HTTPS on Port: 5005

### POST endpoint '/alexa'
Updates Interface with alexa's last response.


Required payload is json with 'title' and 'text' fields. Example: {'title' : 'Buzzbox', 'text' : 'turn everything on'}'
Returns {'response' : 'Update Ok'} if payload was parsed correctly

### POST endpoint '/toggle'
Responsible of turning the interface modules on and off. Json Payload is is required, example:

{'widget' : 'widgetname', 'state': 'statename'}

* widgets: alexa, clock, news, notif, weather, sensors, guide, all
* states: on, off

Returns json with {'response': 'Update OK'} if one of the commands were used.
Returns json with {'Error' : '*Error Message*'} if wrong argument was used.

### POST endpoint '/move'

Responsible of moving the interface modules. Json Payload is is required, example:

{'widget' : '*widgetname*', 'position': '*positionname*'}

* widgets: alexa, clock, news, notif, weather, sensors, guide

* positions: TOPLEFT, TOPRIGHT, TOPMID, MIDLEFT, MIDMID, MIDRIGHT, BOTLEFT, BOTMID, BOTRIGHT

  Returns json with {'response': 'Update OK'} if one of the commands were used.

  Returns json with {'Error' : '*Error Message*'} if wrong argument was used.



## Folder Structure

```
/skill-server-imirror
	run.py - Script for starting the webserver and the modules
	config.py - Creates, loads and saves config
	timer.py - a timer what stores the remaining time in a file, stops at 0
	tbsense.py - support module for tbscan.py
	font/ - fonts for the interface.py
	icons/ - icons for the interface.py
	server/
		__init__.py - Runs when server modules is called, initializes various objects
		gui_positions.py - stores enum of positions
		PIRBoot.py - Infrared sensor script
		tbscan.py - thunderboard discovery and sensor readings and their notifications
		views.py - API endpoints
		static/ - not used
		templates/ - not used

```

​	
