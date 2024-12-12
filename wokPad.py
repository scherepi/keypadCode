# WRITTEN NOVEMBER 20, 2024, BY J. SCHERE
# FORKED FROM CODE I STOLE FROM SOME WEBSITE SOMEWHERE
# I AM THE BEAST I WORSHIP
import RPi.GPIO as GPIO
import time
import I2C_LCD_driver as driver
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# ROWS:

L1 = 5
L2 = 6
L3 = 13
L4 = 19

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# COLUMNS:

C1 = 25
C2 = 8
C3 = 7
C4 = 1

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# LCD SETUP

screen = driver.lcd()
screenL1 = ""
screenL2 = ""

def LCDprompt():
	global screen
	global screenL1
	screen.lcd_clear()
	screenL1 = ">"
	screen.lcd_display_string(">", 1)

def LCDclear():
	global screen
	global screenL2
	LCDprompt()
	screenL2 = "Cleared!"
	screen.lcd_display_string(screenL2, 2)

def LCDwrite(character):
	global screen
	global screenL1
	screenL1 = screenL1 + character
	screen.lcd_display_string(screenL1, 1)
	
def LCDsuccess():
	global screen
	screen.lcd_clear()
	screen.lcd_display_string("You're in!", 1)
	
# has to be declared here for the LCD's incorrect function to work, it used to be down with the rest of it
currentIncorrect = 0
maxTries = 5 # defaults to 5
def LCDincorrect():
	global screen
	global screenL2
	global currentIncorrect
	global maxTries
	triesLeft = maxTries - currentIncorrect
	screenL2 = "Tries left: " + str(triesLeft)
	screen.lcd_display_string(screenL2, 2)
def LCDlockout():
	global screen
	global screenL1
	screen.lcd_clear()
	screen.lcd_display_string("Lame.", 1)
	
# GO SET THE CODE STUFF YOURSELF! THE CONFIG FILE IS EASY TO USE.

currentInput = ""
configFile = "codepadConfig"
secretCode = ""
logDestination = ""
logFile = ""
rawKeyDestination = ""
rawKeyFile = ""
logging = False


now = datetime.now()

try:
	configFile = open(configFile)
	secretCode = configFile.readline().split(" ")[1].rstrip()
	logDestination = configFile.readline().split(" ")[1].rstrip()
	rawKeyDestination = configFile.readline().split(" ")[1].rstrip()
	maxTries = int(configFile.readline().split(" ")[1].rstrip())
except:
	print("Could not find config file, or your log file isn't set up properly. Make sure everything is properly set.")
	exit(0)

try:
	# If everything is set up properly, we can go ahead and initalize our log files for writing.
	logFile = open(logDestination, "a")
	rawKeyFile = open(rawKeyDestination, "a")
	rawKeyFile.write("\n-- start of session --\n")
	logging = True
except:
	# Aw man, logs are messed up :(
	print("Unable to initialize log file, logging will be disabled.")

def checkCode():
	# Simple function to check if the input matches our set PIN.
	global secretCode
	global currentInput
	if (secretCode == currentInput):
		currentInput = ""
		return True
	return False

def readLine(line, characters):
	global currentInput
	global currentIncorrect
	GPIO.output(line,GPIO.HIGH)
	if (GPIO.input(C1) == 1):
		currentInput += characters[0]
		LCDwrite(characters[0])
		if (logging):
			rawKeyFile.write(characters[0]) # Log raw keypresses
	if (GPIO.input(C2) == 1):
		currentInput += characters[1]
		LCDwrite(characters[1])
		if (logging):
			rawKeyFile.write(characters[1]) # Continue to log raw keypresses...
	if (GPIO.input(C3) == 1):
		if (logging):
			rawKeyFile.write(characters[2]) # Everything has to go in the raw logs.
		if (line == L4):
			# All of this will run when the 'C' button is pressed.
			if (checkCode()):
				LCDsuccess()
				#TODO: implement more interesting success behavior (LED or piezo, perhaps)
				exit(0)
			else:
				LCDincorrect()
				currentIncorrect += 1
				if (logging):
					# If log initialization was successful and you messed up, we're keeping track.
					logFile.write("FAILED ATTEMPT: " + currentInput + "\n")
				if (currentIncorrect == maxTries):
					# If you messed up enough, you're getting locked out! And we're writing a special event to the logs, just to track what an embarassment you are.
					logFile.write("!!! LOCKOUT EVENT !!! @ " + now.__str__())
					LCDlockout()
					print("Nice try. You aren't brute-forcing this.") # Gotta be a little cheeky - attitude is part of the hacker toolkit
					exit(0)
		else:
			currentInput += characters[2]
			LCDwrite(characters[2]) # Write input to LCD prompt
	if (GPIO.input(C4) == 1):
		if (logging):
			rawKeyFile.write(characters[3]) # Log the raw keystrokes...
		if (line == L3):
			# This code runs when the character "C" is inputted. 
			LCDclear()
			currentInput = ""
		else:
			LCDwrite(characters[3]) # Write the character inputted to the LCD prompt
	GPIO.output(line,GPIO.LOW)
	
try:
	print("Pressing the C key clears the current input. Pressing the \# key submits the current code.")
	LCDprompt()
	while True:
		readLine(L1, ["1", "2", "3", "A"])
		readLine(L2, ["4", "5", "6", "B"])
		readLine(L3, ["7", "8", "9", "C"])
		readLine(L4, ["*", "0", "#", "D"])
		time.sleep(0.1)
except KeyboardInterrupt:
	print("\nApplication terminated.")

