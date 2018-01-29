# skill-server-imirror


## Basic Setup of Raspberry Pi from fresh install for Mirror and Webserver:


eduroam internet access on raspberry-pi (for Anglia Ruskin Students):
(additional install scripts available on https://cat.eduroam.org/)

Add lines below to this file: /etc/wpa_supplicant/wpa_supplicant.conf 
replace username and password with yours
  

```bash
network={
  ssid="eduroam"
  key_mgmt=WPA-EAP
  pairwise=CCMP
  group=CCMP TKIP
  eap=PEAP
  ca_cert="/etc/wpa_supplicant/ca.pem"
  identity="<YOUR_USERNAME>@student.anglia.ac.uk"
  domain_suffix_match="anglia-ruskin-secure-wifi.anglia.ac.uk"
  phase2="auth=MSCHAPV2"
  password="<YOUR PASSWORD>"
}
```

>ADD ca.pem file to the same folder<

---------------------------------------------------------------------------------

```bash
sudo raspi-config
```
Turn On these: 

* Wait for network on boot
* force audio output throught 3.5 jack
* SSH+VNC (optional for remote control)

To remove black borders on screen
in /boot/config.txt uncomment 
```bash
disable_overscan=1
```

Disable XSession from Blanking  
Install xscreensaver:  
```bash
sudo apt-get update
sudo apt-get install xscreensaver
```
Once installed open the Pi's preferences and change screensaver preferences to disable screenblanking.

Download a Black theme for chrome (chromium kiosk chrome white screen when changing pages)

## Installation requirements

To Install [iMirror](https://github.com/Druanae/iMirror): follow its readme.

To install the webserver:

prevent Flask-ask (cryptography) Compiling errors:
```bash
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```

Install script dependencies:

```bash
sudo apt-get install python-flask
sudo pip install flask-ask
sudo pip install unidecode
```

Download ngrok:
```bash
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
```
Unzip to $HOME.

* To link ngrok acc with this script install authtoken.
* Register on website and follow instructions
* https://dashboard.ngrok.com/user/login

Motion sensor PIN setup
```
PIR SENSOR
GPIO GND [Pin 6]
GPIO 5V [Pin 2]
GPIO 7 [Pin 26]
```

#Installation

Download Webserver files from here to $HOME/SkillServer

Add these lines to ~/lxsession/LXDE/autostart to run things at startup
```bash
@lxterminal -e /home/pi/ngrok http 5005 & 	#lxterminal preferred over bash for debugging
@lxterminal -e /home/pi/SkillServer/run.py #$HOME doesnt work
@lxterminal -e /home/pi/SkillServer/PIRBoot.py #Motion sensor script
@lxterminal -e /home/pi/ngrok http 5005
#for black empty screen
@chromium-browser --incognito --kiosk http://localhost:5005/
```


## Alexa Skill setup
Skill Server Configuration (guide in progress):

Log In to Your Alexa Development portal, create new skill in UK or US (where you will use it)

Fill in name, description, 
In Configuration tabchoose HTTPS, give the ngrok address like this: 
	https://<NGROK_ADDRESS>/alexa_menu
    
> Every time you run NGROK it gives you a new address!!!

Choose option "it has a wildcard certificate"

Intents and slots in skill:

```
Dashboard
Map
	slot name: roomNumber type: AMAZON.NUMBER
OpenGame
Zork
```
