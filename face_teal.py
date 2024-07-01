#!/usr/bin/env python3

# Author: Megdalia Bromhal
# Date: 11 June 2024
# Purpose: script that connects movements with detecting teal, so Yelena turns to face teal disk

# Importing packages and python scripts
import cv2 # Computer vision package
import teal_detect2 # Detects teal color and finds center
from picrawler import Picrawler # Sunfounder's code we can use to move Yelena
import yelena_move # Library that has Yelena's personalized movements
import math
from time import sleep


def main():
    
    # If teal is detected, find the center #######################################
    
    # Start camera, 0 means using USB camera (1 is using raspberry pi camera)
    capture = cv2.VideoCapture(0)
    
    # Setting up Yelena's legs - Sunfounder code
    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

    # Grabbing one cropped, masked image to use to find xc
    tmasked = teal_detect2.teal_mask_vision(capture)
    
    # Calling frame_divide to determine center x-coordinate of frame
    xc, tmasked_shape = teal_detect2.frame_divide(tmasked)
    
    # Setting the solving flag to True so Yelena searches for teal and moves towards it until solved maze
    solving = True
    
    # Setting a count so Yelena doesn't get stuck on a past frame
    count = 0
    
    # Setting a solved count to use if Yelena can't find anymore teal
    solved_cntdwn = 9 # Calculated roughly that each turn is ~ 20 degrees
    
    # while loop runs until Yelena can't find anymore teal
    while solving:
        
        # Yelena has turned arount 180 degrees and can't find teal
        if solved_cntdwn == 0:
            
            # Have Yelena sit down and stop the loop
            yelena_move.sit(crawler=crawler)
            
            print("Found no more teal; stopping program.")
            # Stop the while loop
            solving = False
        
        # Else, Yelena is still searching for/following teal
        else:
                
            # Sending camera feed to teel_detect2 to detect teal and find center
            tmasked = teal_detect2.teal_mask_vision(capture)
            
            #cv2.imshow("tmasked image", tmasked)
            #cv2.waitKey(1)
            
            # Using try/except block so code doesn't break when no teal object is found
            try:
                # Finding center of teal object
                tcx, tcy = teal_detect2.find_center(tmasked)
                
                # Determining the angle of the centroid from the center buffer
                angle = teal_detect2.angle_line_point(xc, tcx, tcy)
                
                # Defining the angle of the center buffer
                cbuff = 1
                
                # Only taking a frame 1/8th of the time to make sure it's a current frame
                if (count % 8) == 1:
                    
                    # Setting the solving countdown to 4 again
                    # Making sure Yelena resets the countdown each time she finds teal again
                    solved_cntdwn = 8
                    
                    # If the centroid is to the right of the buffer
                    if teal_detect2.centroid_right(tcx, xc, angle, cbuff):

                        print("Object to the right")
                        
                        # Using Sunfounder's code to move Yelena to the right
                        yelena_move.manual_move_right(crawler=crawler, frac=2)
                        
                    # If the centroid is to the left of the buffer
                    elif teal_detect2.centroid_left(tcx, xc, angle, cbuff):

                        print("Object to the left")
                        
                        # Using Sunfounder's code to move Yelena to the left
                        yelena_move.manual_move_left(crawler=crawler, frac=2)
                    
                    # If the centroid is in the center line buffer
                    elif angle <= cbuff:
                        print("Object in center buffer")
                        
                        # If teal is on a wall in front of Yelena
                        
                        # Sunfounder's code from avoid.py
                        # Using Pins D2 and D3 for sonar
                        sonar = Ultrasonic(Pin("D2"), Pin("D3"))
                        
                        # Setting the distance we want Yelena to sit away from the teal marker
                        alert_distance = 15
                        
                        # Reading from the sonar how far the teal is
                        distance = sonar.read()
                        print(distance)
                        
                        # If the teal marker is on a wall in front of her at the predefined distance
                        if distance <= alert_distance:
                            
                            # Have her check for more teal...
                            
                            # Sit down in front of the teal
                            yelena_move.sit(speed=50, crawler=crawler)
                        
                        # Else, if the teal is on the ground or not close enough
                        else:
                            
                            # Using Sunfounder's code to move Yelena forward
                            yelena_move.move_forward(speed=70, crawler=crawler)
                        
                    # If the teal center is in the bottom of her vision, she's close
                    # But she'll stop coming for it when she gets close because she'll stop seeing it
                    # So if the centroid is close to her vision's edge, we tell her to keep moving
                    
                    # If Yelena is almost on top of the centroid, keep moving forward
                    #if (tcy >=180) and (angle <= cbuff):
                        
                        # Move forward so Yelena is on top of the teal
                        #print("Moving on top of teal")
                        
                        # Using Sunfounder's code to move Yelena forward
                        #yelena_move.move_forward(speed=70, crawler=crawler, moves=3)
                        
                        # Right now having her sit on the teal; later add turning to look for more
                        #yelena_move.sit(speed=50, crawler=crawler)
                        
                        #solving = False
                        
                # Increase the count by one so Yelena takes a command every 1/8th iteration
                count += 1
                
                # Drawing a circle on center and showing feed
                #cv2.circle(tmasked, (tcx, tcy), 5, (255, 255, 255), -1)
                #cv2.line(tmasked, (xc, 0), (xc, int(tmasked_shape[0])), (255, 255, 255), 5)
                #cv2.imshow("Centroid calculated in image", tmasked)
                #cv2.waitKey(1)
            
            except (TypeError, ZeroDivisionError) as e:
                
                #print("No teal found")
                
                # Using the count to make sure Yelena is using a recent frame
                if (count % 8) == 1:
                    print("No teal found, looking for teal. Turn Countdown: ", solved_cntdwn)
                        
                    # Having Yelena turn when she finds no teal
                    yelena_move.manual_move_left(crawler=crawler, frac=2)
                    
                    solved_cntdwn -= 1
            
                # Incrementing the count by one so Yelena takes a command every 1/8th iteration
                count += 1
                
            # To save memory, we could only run find_center if there are enough teal pixels
            # But right now there's no easy way to do this that takes less memory than just running
            # this function. May improve in future.


if __name__ == '__main__':
    main()
# Eof