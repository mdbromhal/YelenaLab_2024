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


def stay():
    '''
    Function that doesn't do anything as of yet. Yelena doesn't move, so she stays still.
    
    return None
    '''
    
    print("\nCommand received: STAY")


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


def main():
    
    # Telling Yelena to sit
    sit()
    
    #move_left()


if __name__ == '__main__':
    main()
# Eof (end of file)