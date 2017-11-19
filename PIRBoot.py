#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import timer as countdown #methods for manipulating timer
import threading

################################################################
#Every Webbrowser request can be changed to an interface method#
################################################################

GPIO.setmode(GPIO.BCM)

PIR_PIN = 7
countdown.ZeroTimer() 

GPIO.setup(PIR_PIN, GPIO.IN)


class Run(threading.Thread):
    def __init__(self, parent_function):
        threading.Thread.__init__(self)
        self.start(parent_function)


def start(parent_func):
    print "PIR Module Startup script (CTRL+C to exit)"
    time.sleep(2)
    print "Ready"



#While
    try:
            while True:
                    if GPIO.input(PIR_PIN) and countdown.ReadTimer() <= 0:
                            countdown.RestartTimer()
                            #Alexa stop
                            parent_func("show")
                            time.sleep(1)
                            #alexa welcome audio line?                            
                    elif GPIO.input(PIR_PIN):
                            countdown.RestartTimer()
                            time.sleep(1)                        
                    else:
                            if countdown.ReadTimer() == 0:
                                parent_func("hide")
                                #stop alexa session
                            countdown.DecrementTimer()
                            time.sleep(1)
                            print(countdown.ReadTimer())
                        

                        

    except KeyboardInterrupt:
            print'Quit'


####
