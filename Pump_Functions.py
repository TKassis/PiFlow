# Various PiFlow functions needed for pump control
# Flow rate arguments (Q) are in uL/min and duration (T) is in seconds
# Last updated 02/11/18 by Timothy Kassis and Paola Perez

import time
import pandas as pd
import numpy as np
import RPi.GPIO as GPIO


# Calibration function to convert flow rate in uL/min to frequency
# Values where determined from a calibration curve
def Q_to_f(Q,Pump_Number):
    if Pump_Number == 1:
        if Q <= 1:
            f = 0.001
        elif 1 < Q <= 2253.33:
            f = Q/22.19
        elif 2253.33 < Q <= 3486.67:
            f = (Q-1595)/6.25
        else:
            print('Flow rate 1 out of range')
            return

    elif Pump_Number == 2:
        if Q <= 1:
            f = 0.001
        elif 1 < Q <= 2526.67:
            f = Q/26.36
        elif 2526.67 < Q <= 3786.67:
            f = (Q-1895)/6.53
        else:
            print('Flow rate 2 out of range')
            return

    else:
        print('Pump number must be 1 or 2')
        return

    return round(f,3)

# Constant flow, supply Q1 and Q2 in uL/min and duration T in sec
def Constant_Flow(Q1, Q2, T):
    GPIO.setmode(GPIO.BCM)

    # Confvert flow rates from uL/min to frequency (Hz)
    f1 = Q_to_f(Q1,1)
    f2 = Q_to_f(Q2,2)

    # Setup power pins
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, GPIO.HIGH)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)

    # Setup data pins
    GPIO.setup(18, GPIO.OUT) # Pump 1
    GPIO.setup(17, GPIO.OUT) # Pump 2

    # Assign PWM frequency
    Pump1 = GPIO.PWM(18, f1)
    Pump2 = GPIO.PWM(17, f2)

    # Start pumps and run for given time
    Pump1.start(95)
    Pump2.start(95)
    time.sleep(T)

    # Stop pumps and clean up
    Pump1.stop()
    Pump2.stop()
    GPIO.output(19, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    GPIO.cleanup()

    print("Constant flow complete")

# Dynamic flow, supply csv file path
def Dynamic_Flow(file_path):
    GPIO.setmode(GPIO.BCM)

    # Setup power pins
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, GPIO.HIGH)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, GPIO.HIGH)

    # Setup data pins
    GPIO.setup(18, GPIO.OUT) # Pump 1
    GPIO.setup(17, GPIO.OUT) # Pump 2

    # Read file
    df = pd.read_csv(file_path)
    values = np.array(df)

    # Initialize and start pumps
    Pump1 = GPIO.PWM(18, 1)
    Pump1.start(95)
    #Pump1.ChangeFrequency(0.001)
    Pump2 = GPIO.PWM(17, 1)
    Pump2.start(95)
    #Pump2.ChangeFrequency(0.001)

    for i in range(len(values)-1):

        dt = round((values[i+1][0]) - (values[i][0]),4)
        Q1 = round(values[i][1], 1)
        Q2 = round(values[i][2], 2)

        f1 = Q_to_f(Q1,1)
        f2 = Q_to_f(Q2,2)

        if f1 > 0.01:
            Pump1.start(95)
            Pump1.ChangeFrequency(f1)
        else:
            Pump1.stop()

        if f2 > 0.01:
            Pump2.start(95)
            Pump2.ChangeFrequency(f2)
        else:
            Pump2.stop()

        time.sleep(dt)

    # Stop pumps and clean up
    Pump1.stop()
    Pump2.stop()
    GPIO.output(19, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    GPIO.cleanup()

    print("Dynamic flow complete")
