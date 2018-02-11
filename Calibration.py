# Use this script to calibrate the pump flow rates
# Updated 02/11/18, Timothy Kassis

import time
import RPi.GPIO as GPIO

f1 = 0.001 # Pump 1 frequency in Hz
f2 = 300 # Pump 2 frequency in Hz
T = 10 # Run duration in sec

GPIO.setmode(GPIO.BCM)

# Setup power pins
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, GPIO.HIGH)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.HIGH)

# Setup data pins
GPIO.setup(18, GPIO.OUT) # Pump 1
GPIO.setup(17, GPIO.OUT) # Pump 2
Pump1 = GPIO.PWM(18, f1)
Pump2 = GPIO.PWM(17, f2)
Pump1.start(95)
Pump2.start(95)

# Run for a given time
time.sleep(T)

# Stop pumps and clean up
Pump1.stop()
Pump2.stop()
GPIO.output(19, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.cleanup()

print("Complete")
