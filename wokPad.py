# WRITTEN NOVEMBER 20, 2024, BY J. SCHERE
# FORKED FROM CODE I STOLE FROM SOME WEBSITE SOMEWHERE
# I AM THE BEAST I WORSHIP
import RPi.GPIO as GPIO
import time
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

C4 = 1
C3 = 7
C2 = 8
C1 = 25

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# GO SET THE CODE STUFF YOURSELF! THE CONFIG FILE IS EASY JSON.

currentInput = ""
configFile = "codepadConfig"
secretCode = ""
logDestination = ""
logFile = ""
logging = False
maxTries = 5 # defaults to 5
currentIncorrect = 0

now = datetime.now()

try:
	configFile = open(configFile)
	secretCode = configFile.readline().split(" ")[1].rstrip()
	logDestination = configFile.readline().split(" ")[1].rstrip()
	maxTries = int(configFile.readline().split(" ")[1].rstrip())
except:
	print("Could not find config file, or your log file isn't set up properly. Make sure everything is properly set.")
	exit(0)

try: 
	logFile = open(logDestination, "a")
	logging = True
except:
	print("Unable to initialize log file, logging will be disabled.")

def checkCode():
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
		#print(characters[0] + " || " + str(line) + "C1")
		currentInput += characters[0]
		print("> " + currentInput)
	if (GPIO.input(C2) == 1):
		#print(characters[1] + " || " + str(line) + "C2")
		currentInput += characters[1]
		print("> " + currentInput)
	if (GPIO.input(C3) == 1):
		#print(characters[2] + " || " + str(line) + "C3")
		if (line == L4):
			if (checkCode()):
				print("Congratulations! You got the code!")
				exit(0)
			else:
				print("Incorrect code.")
				currentIncorrect += 1
				if (logging):
					logFile.write("FAILED ATTEMPT: " + currentInput + "\n")
				if (currentIncorrect == maxTries):
					logFile.write("!!! LOCKOUT EVENT !!! @ " + now.__str__())
					print("Nice try. You aren't brute-forcing this.")
					exit(0)
		else:
			currentInput += characters[2]
			print("> " + currentInput)
	if (GPIO.input(C4) == 1):
		if (line == L3):
			print("Input cleared!")
			currentInput = ""
		else:
			currentInput += characters[3]
			print("> " + currentInput)
		# print(characters[3] + " || " + str(line) + "C4")
	GPIO.output(line,GPIO.LOW)
	
try:
	print("Pressing the C key clears the current input. Pressing the \# key submits the current code.")
	while True:
		readLine(L1, ["1", "2", "3", "A"])
		readLine(L2, ["4", "5", "6", "B"])
		readLine(L3, ["7", "8", "9", "C"])
		readLine(L4, ["*", "0", "#", "D"])
		time.sleep(0.1)
except KeyboardInterrupt:
	print("\nApplication terminated.")

