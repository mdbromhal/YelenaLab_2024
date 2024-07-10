#!/usr/bin/env python3

# Importing necessary modules
from robot_hat import Ultrasonic
from robot_hat import Pin
import sys,time,random
import gpiozero

# https://www.geeksforgeeks.org/progress-bars-in-python/
def progressBar(count_value, total, suffix=''):
    bar_length = 100
    filled_up_Length = int(round(bar_length* count_value / float(total)))
    percentage = round(100.0 * count_value/float(total),1)
    bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
    sys.stdout.flush()
#This code is Contributed by PL VISHNUPPRIYAN


def iterate_pins(pins):
   '''
   Function that tries sonar with each combination of 2 pins from provided list. 
   Returns list of successful (not zero cm away) pin combinations, as well as a list of tried pin combinations.

   param pins: list of pin names to send to robot_hat Pin()

   return tried, success: lists of tried and successful pin combinations
   '''

   # Calculate the total number of iterations -- help with logic for progress bar from ChatGPT
   total_iterations = len(pins) ** 2
   
   # Creating empty arrays for tried and successes to append pin combinations to
   tried = []
   success = []

   error = []

   # Initializing a count to keep track of loop's progress with progress bar
   count = 0

   # For each pin in pin list
   for pin1 in pins:
      # Try with every pin
      for pin2 in pins:

         try:

            # Append combination of pins tried to tried list
            tried.append((pin1, pin2))

            # Test with sonar
            sonar = Ultrasonic(Pin(pin1), Pin(pin2))

            # Reading from the sonar how object is
            distance = sonar.read()

            # If the distance is not 0, put into success list
            if distance != 0:
               success.append((pin1, pin2))

         except gpiozero.exc.GPIOPinInUse as e:
            error.append((pin1, pin2))

         # Bop the count up by 1 to keep track of progress
         count += 1

         # Code for progress bar
         time.sleep(random.random())
         progressBar(count, total_iterations - 1)

   print("Clearing......................................................................................................")
   print("\nTried combinations of pins in list: \n", tried)
   print("\nSuccessful combinations of pins in list: \n", success)
   print("\nError combinations of pins in list: \n", error)


def main ():
   dict_1 = {
      "D0":  17,
      "D1":  18,
      "D2":  27,
      "D3":  22,
      "D4":  23,
      "D5":  24,
      "D6":  25,
      "D7":  4,
      "D8":  5,
      "D9":  6,
      "D10": 12,
      "D11": 13,
      "D12": 19,
      "D13": 16,
      "D14": 26,
      "D15": 20,
      "D16": 21, 
      "SW":  19,
      "USER": 19,        
      "LED": 26,
      "BOARD_TYPE": 12,
      "RST": 16,
      "BLEINT": 13,
      "BLERST": 20,
      "MCURST": 21,
   }

   dict_2 = {
      "D0":  17,
      "D1":   4, # Changed
      "D2":  27,
      "D3":  22,
      "D4":  23,
      "D5":  24,
      "D6":  25, # Removed
      "D7":   4, # Removed
      "D8":   5, # Removed
      "D9":   6,
      "D10": 12,
      "D11": 13,
      "D12": 19,
      "D13": 16,
      "D14": 26,
      "D15": 20,
      "D16": 21,     
      "SW":  25, # Changed
      "USER": 25,
      "LED": 26,
      "BOARD_TYPE": 12,
      "RST": 16,
      "BLEINT": 13,
      "BLERST": 20,
      "MCURST":  5, # Changed
   }

   # Trying with dictionary 1
   iterate_pins(pins = dict_1.keys())

   # print("\nTried combinations of pins in dict_1: \n", tried_pins1)
   # print("\nSuccessful pin combinations in dict_1: \n", successful_pins1)
   # print("\nError pin combinations in dict_1: \n", error_pins1)

   # Trying with dictionary 2
   print()
   iterate_pins(pins = dict_2.keys(), )

   # print("\nTried combinations of pins in dict_2: \n", tried_pins2)
   # print("\nSuccessful pin combinations in dict_2: \n", successful_pins2)
   # print("\nError pin combinations in dict_2: \n", error_pins2)


if __name__== '__main__':
   main()