# WRITTEN NOVEMBER 14, 2024, BY J. SCHERE
# I AM THE BEAST I WORSHIP
import RPi.GPIO as GPIO
import time

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

def readLine(line, characters):
	GPIO.output(line,GPIO.HIGH)
	if (GPIO.input(C1) == 1):
		print(characters[0] + " || " + str(line) + "C1")
	if (GPIO.input(C2) == 1):
		print(characters[1] + " || " + str(line) + "C2")
	if (GPIO.input(C3) == 1):
		print(characters[2] + " || " + str(line) + "C3")
	if (GPIO.input(C4) == 1):
		print(characters[3] + " || " + str(line) + "C4")
	GPIO.output(line,GPIO.LOW)
	
try:
	while True:
		readLine(L1, ["1", "2", "3", "A"])
		readLine(L2, ["4", "5", "6", "B"])
		readLine(L3, ["7", "8", "9", "C"])
		readLine(L4, ["*", "0", "#", "D"])
		time.sleep(0.1)
except KeyboardInterrupt:
	print("\nApplication terminated.")
