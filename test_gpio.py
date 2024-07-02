#!/usr/bin/env python3

# From ChatGPT
from gpiozero import DistanceSensor
from time import sleep

# Define the pins (BCM numbering)
TRIG = 23
ECHO = 24

# Initialize the distance sensor
sonar = DistanceSensor(echo=ECHO, trigger=TRIG)

try:
    while True:
        distance = sonar.distance * 100  # Convert to cm
        print(f"Distance: {distance:.2f} cm")
        sleep(1)
except KeyboardInterrupt:
    print("Script interrupted.")




