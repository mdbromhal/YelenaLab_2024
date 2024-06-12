#!/usr/bin/env python3

# Author: Megdalia Bromhal
# Date: 11 June 2024
# Purpose: script that connects movements with detecting teal, so Yelena turns to face teal disk

# Importing packages and python scripts
import cv2 # Computer vision package
import teal_detect2 # Detects teal color and finds center
from picrawler import Picrawler # Sunfounder's code we can use to move Yelena
import yelena_move # Library that has Yelena's personalized movements
import time


def main():
    
    # If teal is detected, find the center #######################################
    
    # Start camera, 0 means using USB camera (1 is using raspberry pi camera)
    capture = cv2.VideoCapture(0)
    
    # Set up Yelena's legs?
    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9]) 

    # We want to figure out where this is in relation to Yelena
    # i.e. to her left, to her right
        # Diagram of the coordinate frame of the masked image we're using:
        # __________ y = 0
        # |
        # |
        # |
        # |
        # |
        # x = 0
    # So now what we want to do is figure out which side of the image the centroid is on
    # Only care about the horizontal distance from center
    # xc = 639 / 2
    
    tmasked = teal_detect2.teal_mask_vision(capture)
    
    # Determining the size of the first image (assuming all images are the same size
    tmasked_shape = tmasked.shape
    
    # Dividing length of image in two to find center x coordinate
    xc = int(tmasked_shape[1] / 2) # tmasked_shape = [y, x, z]
    
    # Optional: shows where divides between left and right of image
    image = cv2.line(tmasked, (xc, 0), (xc, int(tmasked_shape[0])), (255, 255, 255), 15)
    cv2.imshow("Divided masked frame", image)
    cv2.waitKey(1)
    
    while True:
        # Sending camera feed to teel_detect2 to detect teal and find center
        tmasked = teal_detect2.teal_mask_vision(capture)
        
        # Using try/except block so code doesn't break when no teal object is found
        try:
            # Finding center of teal object
            tcx, tcy = teal_detect2.find_center(tmasked)
            
            # Drawing a circle on center and showing feed
            cv2.circle(tmasked, (tcx, tcy), 5, (255, 255, 255), -1)
            cv2.line(tmasked, (xc, 0), (xc, int(tmasked_shape[0])), (255, 255, 255), 10)
            cv2.imshow("Centroid calculated in image", tmasked)
            cv2.waitKey(1)
            
            # Determining which half the teal object is on
            if tcx > xc:
                print("Object to the right")
                
                # Basic implementation
                crawler.do_action('turn right angle', 3) # From Sunfounder's avoid.py, can put speed as parameter
                time.sleep(0.2)
                # To know how much to rotate, we need to know the angle of the camera.
                
            elif (tcx < xc) and (tcx >= 0):
                print("Object to the left")
                
                # Basic implementation
                crawler.do_action('turn left angle', 3) # From Sunfounder's avoid.py, can put speed as parameter
                time.sleep(0.2)
        except TypeError as e:
            print("No teal object found")
        # To save memory, we could only run find_center if there are enough teal pixels
        # But right now there's no easy way to do this that takes less memory than just running
        # this function. May improve in future.
        
        # Determining which half the teal object is on
        if tcx > xc:
            print("Object to the right")
            
            # Basic implementation
            crawler.do_action('turn right angle', 3) # From Sunfounder's avoid.py, can put speed as parameter
            time.sleep(0.2)
            # To know how much to rotate, we need to know the angle of the camera.
            
        elif (tcx < xc) and (tcx >= 0):
            print("Object to the left")
            
            # Basic implementation
            crawler.do_action('turn left angle', 3) # From Sunfounder's avoid.py, can put speed as parameter
            time.sleep(0.2)
                
    # If it detects teal and finds its center, turn to face the teal color
    
    # Turning
    #crawler.do_action('turn left angle', 3, speed) # From Sunfounder's avoid.py
    #time.sleep(0.2)
    
    # Sunfounder's do_action function in picrawler.py, line 124
#     def do_action(self, motion_name, step=1, speed=50):
#     try:
#         for _ in range(step): # times
#             self.move_list.stand_position = self.stand_position
#             if motion_name in ["forward", "backward", "turn left", "turn right", "turn left angle", "turn right angle"]:
#                 self.stand_position = self.stand_position + 1 & 1
#             action = self.move_list[motion_name]
#             for _step in action: # spyder motion
#                 self.do_step(_step, speed=speed)
#     except AttributeError:
#         try:
#             for _ in range(step):
#                 action_add = self.move_list_add[motion_name]
#                 for _step in action_add:
#                     self.do_step(_step, speed=speed) 
#         except KeyError:
#             print("No such action")
    
    
    # If hands are detected, determine the command
    
    


if __name__ == '__main__':
    main()
# Eof