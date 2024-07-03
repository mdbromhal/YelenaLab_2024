#!/usr/bin/env python3

# # From ChatGPT
# import time
# import RPi.GPIO as GPIO

# # Set GPIO mode
# GPIO.setmode(GPIO.BCM)

# # Define GPIO pins
# TRIG = 23  # Change to your TRIG pin
# ECHO = 24  # Change to your ECHO pin

# # Set up GPIO pins
# GPIO.setup(TRIG, GPIO.OUT)
# GPIO.setup(ECHO, GPIO.IN)

# def get_distance():
#     # Ensure the TRIG pin is low
#     GPIO.output(TRIG, False)
#     time.sleep(2)  # Increase delay to allow sensor to settle

#     # Generate a 10us pulse on TRIG
#     GPIO.output(TRIG, True)
#     time.sleep(0.00001)
#     GPIO.output(TRIG, False)

#     # Wait for ECHO to go high and measure the duration
#     pulse_start = time.time()
#     while GPIO.input(ECHO) == 0:
#         pulse_start = time.time()

#     pulse_end = time.time()
#     while GPIO.input(ECHO) == 1:
#         pulse_end = time.time()

#     # Calculate the duration and distance
#     pulse_duration = pulse_end - pulse_start
#     distance = pulse_duration * 17150  # Speed of sound in cm/us
#     distance = round(distance, 2)
    
#     # Handle out-of-range readings
#     if distance > 400 or distance < 2:
#         distance = None  # or set to a specific error value
    
#     return distance

# try:
#     while True:
#         dist = get_distance()
#         if dist is not None:
#             print(f"Distance: {dist} cm")
#         else:
#             print("Out of range")
#         time.sleep(1)
# except KeyboardInterrupt:
#     GPIO.cleanup()

# From https://learn.voltaat.com/tutorials/how-to-use-ultrasonic-sensor-with-raspberry-pi-5
from gpiozero import DistanceSensor  # Import the DistanceSensor class from the gpiozero library
from time import sleep  # Import the sleep function from the time module for delay

# Initialize the ultrasonic sensor
sensor = DistanceSensor(echo=24, trigger=23, max_distance=5)

def measure_distance():

   distance = int(sensor.distance * 100)  # Measure the distance and convert it to an integer

   print(distance)


measure_distance()