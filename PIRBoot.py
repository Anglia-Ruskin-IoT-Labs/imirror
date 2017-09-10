#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import webbrowser
import os
import timer as countdown #methods for manipulating timer

################################################################
#Every Webbrowser request can be changed to an interface method#
################################################################

GPIO.setmode(GPIO.BCM)

PIR_PIN = 7
countdown.ZeroTimer() 

GPIO.setup(PIR_PIN, GPIO.IN)



print "PIR Module Startup script (CTRL+C to exit)"
time.sleep(2)
print "Ready"



#While       
try:
        while True:
                if GPIO.input(PIR_PIN) and countdown.ReadTimer() <= 0:
                        countdown.RestartTimer()
                        #Alexa stop
                        webbrowser.open('http://0.0.0.0:5005/welcome', new=0, autoraise=True) #
                        time.sleep(1)
                        #alexa welcome audio line?                            
                elif GPIO.input(PIR_PIN):
                        countdown.RestartTimer()
                        time.sleep(1)                        
                else:
                        if countdown.ReadTimer() == 0:
                                webbrowser.open('http://0.0.0.0:5005/', new=0, autoraise=True) #black screen
                                #stop alexa session
                        countdown.DecrementTimer()
                        time.sleep(1)
                        print(countdown.ReadTimer())
                        

                        

except KeyboardInterrupt:
        print'Quit'


####
