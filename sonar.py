#!/usr/bin/env python3

# Author: Megdalia Bromhal
# Date: 1 July 2024
# Purpose: library of functions relating to sonar; some repurposed from Sunfounder's code.

# Importing necessary modules
from robot_hat import Ultrasonic
from robot_hat import Pin


def sonar_distance():
    '''
    Detects distance from object in front with sonar. Code from Sunfounder's avoid.py (comments are from me, though)

    return distance: distance from object.
    '''
    
    # Error handling in case of Pin error
    try:
        # Using Pins D2 and D3 for sonar
        sonar = Ultrasonic(Pin("D2"), Pin("D3"))

        # Reading from the sonar how far the teal is
        distance = sonar.read()

        # Returning the distance
        return distance
    except ValueError as e:
        print(e)


def within_alert_distance(distance=float, alert_distance=float):
    '''
    Checking if distance calculated from sonar is within user-defined alert distance.

    param distance: distance from object in front of sonar sensors, calculated with sonar
    param alert_distance: float used to compare distance. For example, if you wanted Yelena to stop 10 units (which are?) away from a wall, alert distance = 10.

    return True if distance is within alert distance or False if it is not
    '''
    
    # If the distance calculated from the sonar is within the alert distance
    if distance <= alert_distance: # Used from Sunfounder's avoid.py

        # Return that it is within the alert distance
        return True


def main():
    
    # Using sonar to detect distance from object in front
    dist = sonar_distance()

    print("Distance: ", dist)

    # Seeing if distance is within 25 = alert distance
    print(within_alert_distance(dist, 25))


if __name__ == '__main__':
    main()