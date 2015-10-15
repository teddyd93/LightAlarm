import RPi.GPIO as GPIO
import datetime
import time
from time import sleep

GPIO.setup(11,GPIO.OUT) // maps gpio pins to the relays
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(13,False) // sets pins on
GPIO.output(15,False)
GPIO.setup(18,GPIO.IN) // sets input from button
alarmHH = 7
alarmD = 15
bedHH = 23
bedMM = 0
button = 0

while(1):
        if GPIO.input(18):
                button = 1

        now = time.localtime()

        if now.tm_hour >= 23 or now.tm_hour < 7: // Pin turns off after 11
and before 7 unless the button is pressed
                GPIO.output(11,True)
                if button:
                        GPIO.output(11,False)
                        sleep(900)
                        GPIO.output(11,True)
                        button =  0


        elif now.tm_hour == 7 and now.tm_min < 15  and not button: // This
flashes the pin for 1/2 second bursts for 15 unless                the
button is pressed
                GPIO.output(11,True)
                sleep(.5)
                GPIO.output(11, False)
                sleep(.5)

        else:  // if all else failes, the light is on
                GPIO.output(11,False)
                button=1

        #       print now.tm_hou
