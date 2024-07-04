#!/usr/bin/env python3

# Author: Megdalia Bromhal
# Date: 3 June 2024
# Purpose: library-ish of movement command functions

# Importing necessary modules
from picrawler import Picrawler
import time

def sit(speed=50, crawler=Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])):
    '''
    Function using Sunfounder's code to make Yelena sit.
    Format follows order: [right front],[left front],[left rear],[right rear]
    
    param speed: the speed Yelena performs the tasks.
    param crawler: setting up Yelena's legs
    return None
    
    '''
    print('\nCommand received: SIT')

    # Defining where we want Yelena's legs to go to make her sit
    new_step=[[20, 0, 0], [20, 0, 0], [20, 0, 0], [20, -5, 0]]
    # sit = [[50, 50, -33], [50, 50, -33], [50, 50, -33], [50, 50, -33]]
    
    # Using Sunfounder's code to move Yelena to sit as we've defined
    crawler.do_step(new_step, speed)
    time.sleep(0.2)


def move_forward(speed=50, crawler=Picrawler([10,11,12,4,5,6,1,2,3,7,8,9]), moves=2):
    '''
    Function using Sunfounder's code to make Yelena move forward.
    
    param speed: the speed Yelena performs the tasks.
    param crawler: setting up Yelena's legs
    param moves: number of moves to complete movement (how much to move forward); [1=min, 3=max?]
    return None
    '''
    
    print('\nCommand received: MOVE FORWARD')
    
    # Using a predefined movement (Sunfounder) to move Yelena forward
    crawler.do_action('forward', moves, speed)
    time.sleep(0.2)


def stand(speed=50, crawler=Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])):
    '''
    Function that defines a standing pose for Yelena.
    Format follows order: [right front],[left front],[left rear],[right rear]
    
    param speed: the speed Yelena performs the movement(s)
    param crawler: setting up Yelena's legs; Sunfounder's code
    return None
    '''
    
    print("\nCommand received: STAND")
    
    # Defining the movement to stand
    legs_coordinates = [[50, 50, -80], [50, 50, -80], [50, 50, -80], [50, 50, -80]]
    
    # Using Sunfounder's code to move Yelena to this defined position
    crawler.do_step(legs_coordinates, speed)
    time.sleep(0.2)


def move_right(speed=50, crawler=Picrawler([10,11,12,4,5,6,1,2,3,7,8,9]), moves=1):
    '''
    Function that uses Sunfounder's code (avoid.py) to turn Yelena to the right by 3.
    
    param speed: the speed Yelena performs the movement
    param crawler: setting up Yelena's legs (Sunfounder's code)
    param moves: number of moves to complete movement (how much to move right); [1=min, 3=max?]
    return None
    '''
    
    # Using a predefined movement command to move Yelena to the right
    crawler.do_action('turn right angle', moves, speed) 
    time.sleep(0.2)


def move_left(speed=50, crawler=Picrawler([10,11,12,4,5,6,1,2,3,7,8,9]), moves=1):
    '''
    Function that uses Sunfounder's code to turn Yelena to the left.
    
    param speed: the speed Yelena performs the movement
    param crawler: setting up Yelena's legs (Sunfounder's code)
    param moves: number of moves to complete movement (how much to move forward); [1=min, 3=max?]
    return None
    '''
    
    # Using a predefined movement command to move Yelena to the left
    crawler.do_action('turn left angle', moves, speed)
    time.sleep(0.2)


def manual_move_right(speed=50, crawler=Picrawler([10,11,12,4,5,6,1,2,3,7,8,9]), frac=1):
    '''
    Function that manually defines where Yelena's legs are to go to turn right.    
    Format follows order: [right front],[left front],[left rear],[right rear]
    
    param speed: the speed Yelena performs movement
    param crawler: setting up Yelena's legs (Sunfounder's code)
    param frac: fraction to determine how much to split up turn. 1 = full turn, 2 = 50% turn, ect.
    return None
    '''
    
    # Want 100% of Yelena's movement
    if frac <= 1:
        x = 0 # Setting her leg on the y-axis, which is the max movement
    
    # Else want 25% of Yelena's movement
    elif frac > 1:
        x = 50  # Setting it so her legs move ~1/4 of the way, so she turns less

    # Defining where to put legs to prepare for movement
    # `setup = [[50 // frac, 0, 0], [50 // frac, 50 // frac, 20], [50 // frac, 0, 0], [50 // frac, 50 // frac, 20]]`
    setup = [[50, 0, 0], [50, 50, 20], [50, 0, 0], [50, 50, 20]]
    
    # Defining where to put legs to move Yelena to the right
    # movement = [[0, 50 // frac, 0], [50 // frac, 0, 0], [0, 50 // frac, 0], [50 // frac, 0, 0]]
    movement = [[x, 50, 0], [x, 50, 0], [x, 50, 0], [x, 50, 0]]
    
    # Using Sunfounder's code to pass our new setup movement
    crawler.do_step(setup, speed)
    time.sleep(0.2)
    
    # Again sending the movement to Sunfounder's code to move Yelena
    crawler.do_step(movement, speed)
    time.sleep(0.2)
    
    # Resetting Yelena's position with her legs up so she can turn again if need be
    reset = [[50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50]]
    crawler.do_step(reset, speed)
    time.sleep(0.2)


def manual_move_left(speed=50, crawler=Picrawler([10,11,12,4,5,6,1,2,3,7,8,9]), frac=1):
    '''
    Function that manually defines where Yelena's legs are to go to turn left.    
    Format follows order: [right front],[left front],[left rear],[right rear]
    
    param speed: the speed Yelena performs movement
    param crawler: setting up Yelena's legs (Sunfounder's code)
    frac: fraction to determine how much to split up turn. 1 = full turn, 2 = 50% turn, ect.
    return None
    '''

    # Want 100% of Yelena's movement
    if frac <= 1:
        y = 0 # Setting her leg on the x-axis, which is the max movement

    # Else want 25% of Yelena's movement
    elif frac > 1:
        y = 50 # Setting it so her legs move ~1/4 of the way, so she turns less

    # Defining where to put legs to prepare for movement
    # setup1 = [[0, 50 // frac, 0], [50 // frac, 50 // frac, 20], [0, 50 // frac, 0], [50 // frac, 0, 0]]
    setup1 = [[0, 50, 0], [50, 50, 20], [0, 50, 0], [50, 0, 0]]
    
    # Defining where to put legs to move Yelena to the right
    # movement = [[50 // frac, 0, 0], [0, 50 // frac, 0], [50 // frac, 0, 0], [0, 50 // frac, 0]]
    movement = [[50, y, 0], [50, y, 0], [50, y, 0], [50, y, 0]]
    
    # Using Sunfounder's code to pass our new setup movement
    crawler.do_step(setup1, speed)
    time.sleep(0.2)
    
    # Again sending the movement to Sunfounder's code to move Yelena
    crawler.do_step(movement, speed)
    time.sleep(0.2)
    
    # Resetting Yelena's position with her legs up so she can turn again if need be
    reset = [[50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50]]
    crawler.do_step(reset, speed)
    time.sleep(0.2)


def main():
    
    # Telling Yelena to sit
    sit() 


if __name__ == '__main__':
    main()
# Eof (end of file)