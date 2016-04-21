#Theodore DeRidder
#LightAlarm.py
#Personal Project: "LightAlarm"

#---Project Goal: Wake the user by any and all means possible...

# ---Current project status: User is berated by flashing lights at 7 in the morning. 
#If the user exits the bed, the load sensors will tell the Pi to stop flashing lights.
#If, at any time between 7 AM and 11 PM, the user returns/remains in bed, the system will continue to berate the user with flashing lights until the user removes himself/herself from the bed.
#If, at any time between 11 PM and 7 AM of the next morning, the user is not in bed, the system will berate the user with flashing lights.
#Sound stimuli is implemented, but I lack the funds for a set of speakers.


#---Hardware and software interface design
#Load sensors are placed in each corner with thin wood planks on each sensor in order to properly sense distributed weight.
#Analog data is interpreted by an Arduino Uno, which relays the data via serial USB input to a Raspberyy Pi.
#Serial data is formatted by the Pi, which decides wether the user is in the bed or not.
#Based on the time of day, the Pi will decide wether to initiate wake protocols or not.
#Since the Pi does not have a real-time clock, time of day must be acquired from a router, which syncs the Pi to the local EST time.
#The system allows for deviation at night, particularly if the user wished to read in bed. A button has been fixed to the system which will turn the light on for 15 min. intervals.
#The button completes a cicuit between the 3V rail and a GPIO input pin on th Pi.
#GPIO input is then interpreted through the program. Once the 15 min. is up, the program resumes normal function. 
#This function can only be performed at night, by design. (Current book: "Do Androids Dream of Electric Sheep?" by Phillip K. Dick. Inspiration for Blade Runner)

#The light is controlled by a relay. The relay takes a 3.3v input, provided by the Pi GPIO.
#Am 120V voltage is wired from a US standard outlet plug and sperated into a 4-way relay. 3.3V input triggers the relay to switch outlets on or off.
#A lamp is connected and super-glued to a specific outlet. That outlet is associated with a specific GPIO pin.

#Another outlet is for use of a 12V fan, which regulates temperature in the room.
#I live in Buffalo, so it is quite cold in 2/3 of the year.
#The fan pulls air from the vent system and is mounted behind the vent grate. 
#A thermistor is used to determine current temperature of the room.
#At the time when I implemented the thermistor, I did not have the Arduino and thus lacked Analog input capabilties.
#I had to make to using the properties of RC circuits.
#The thermistor acts as a resistor. The higher the temperature, the less resistance.
#I used this property to accurately measure the temperature of the room.
#Resistance in flux means variable charging times for a capacitor. 
#Using the capacitor time constant formula, I determined required resistance and was able to accurately measure temperature to within 1/10th's of a degree.
#All without analog input.

#The load sensors, however, require analog input.
#Although they are resistance sensors, the resistance is way to low to incorporate into the system with reasonable feedback.
#At this time, I incorporated a Hx711 amplifier, and Arduino Uno for analog input. The arduino code is inculded in a seperate file marked "HX711 Serial" in this repository
#Data processed through the Pi is normalized, averaged, and relayed to the Pi, for a consistent data input.

#The user can neutralize the alarm by scanning an NFC tag, which is in a coffee tin in the kitchen cupboard. 
#Most android smartphones have NFC capabilities. Using 'Tasker' and 'Trigger' in tandem, a simple scan of a specific NFC tag can disable the alarm
#The Pi runs a protocol to allow web-based control of GPIO ports.
#NFC inside a coffee tin encourages caffeine intake, which is difficult to sleep through.
#I would integrate automatic coffee dispensing, but it's my roomate's machine, and he doesn't trust me enough to fiddle with it.


#All other outlets are always powered, providing a second funtion as a programmable power-strip.
#The power stip has never mal-functioned in electric failure.

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---Code

#--imports
import serial                               #import 'serial': Serial is the communication through the Arduino to the Rasberry Pi. This is specifically used to transfer data from the weight sensor, to tell the pi, wether there is any weight on the system.
ser = serial.Serial('/dev/ttyACM0', 38400)  #specifies the source and format of the data from the Arduino  
import RPi.GPIO as GPIO                     #Sets GPIO mode for relay control            
import pygame                               #Python sound solution for speaker integration                
import datetime                             #Imports time solution for determining what time it is (kinda important for alarms...)
import time                                 #Imports time solution for 'sleep' method. Useful for waiting certain amount of seconds.
pygame.mixer.init()                         #Initializes the sound player
pygame.mixer.music.load("The Campfire Song Song.mp3")   #Loads the music file that the user wishes to play.
#pygame.mixer.music.play()                              #Plays the music file. Unfortunately, I do not have spare speakers for the Pi. So, this is unused. :(

#--setup
GPIO.setmode(GPIO.BCM)                  #GPIO Mode set
GPIO.setup(17,GPIO.OUT)         #light output
GPIO.setup(27,GPIO.OUT)         #fan output

GPIO.setup(24,GPIO.OUT)         #weight input
GPIO.setup(23,GPIO.OUT)         #button input

GPIO.setup(25, GPIO.OUT)        #thermal out
GPIO.setup(22, GPIO.IN)          #thermal input
GPIO.output(25, GPIO.LOW)        #initializes fan to OFF

alarmHH = 7             #Wakeup Hout
alarmD = 60             #Initial alarm duration
bedHH = 21      #Sleep Time: hour
bedMM = 0       #Sleep Time: minute
button = 0      #initializes button boolean
NFC = 0         #intializes NFC boolean
weight = 0      #intializes weight boolean
while(1):
	ser.flushInput()  #flushes serial buffer.
	serInput = ser.readline()   #reads serial line
	serInput = serInput.replace('\n', '').replace('\r', '').replace('-','') # formats serial input

	while(serInput == ""): #sometimes serial input is late. This loop waits for the data
		serInput = ser.readline()
		serInput = serInput.replace('\n', '').replace('\r', '').replace('-', '')
		print "caught!" #debugging output
#	print "weight: "  #More debugging code
#	print weight
#	print "serial input: "
#	print serInput
#	print type(serInput)

#The following interprets GPIO input into booleans
	if (GPIO.input(23) == GPIO.HIGH):
		button = 1

#Makes sure that input data is valid
	try:
		serInt = float(serInput)
	except ValueError:
		print "oops"
		print serInput
#checks weight to be enough to register as body and no as variations
	if (serInt >= 3):
		weight = 1
		print "weight: "
		print weight
		print "serInput: "
		print serInput
	else:
		weight = 0
		
#updates system time
	now = time.localtime()
	
#sleep time
	if now.tm_hour >= 23 or now.tm_hour < 7:
		GPIO.output(17,GPIO.HIGH)
		GPIO.output(27,GPIO.HIGH)
		if button:
			GPIO.output(17,False)
			sleep(900)
			GPIO.output(17,True)
			button =  0
		if not weight:
			GPIO.output(17, True)
			sleep(.5)
			GPIO.output(17, False)
			sleep(.5)

#standard alarm time
	elif now.tm_hour == 7  and not NFC:
		GPIO.output(17, True)
		GPIO.output(27, False)
		sleep(.5)
		GPIO.output(17, False)
		sleep(.5)

	else:
		if(weight):
			GPIO.output(17, False)
			sleep(.5)
			GPIO.output(17, True)
			sleep(.5)
#includes code for temperature calculation
		else:
			GPIO.output(17,False)
		
			GPIO.output(25, GPIO.LOW)
#			sleep(60)
			GPIO.output(25, GPIO.HIGH)
			timeStampBegin = time.time()
#			while(GPIO.input(22) == GPIO.LOW):
#				place =  1
			timeStampEnd = time.time()
			baseline = (.01/(timeStampEnd - timeStampBegin))*30
#			print baseline
			if(baseline <  55):
				GPIO.output(27, GPIO.LOW)
			else:
				GPIO.output(27, GPIO.HIGH)

#			print weight		
#			print serInput
