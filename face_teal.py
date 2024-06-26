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


def frame_divide(frame):
    '''
    Taking a frame and determining where the center line is in the frame. This can be used to
    divide the frame into two different sections.
    Displays the frame and the line dividng the frame.
    
    param frame: image frame using to determine horizontal center of frame
    return xc: center x-coordinate of frame
    '''
    
    # Determining the size of the first image (assuming all images are the same size
    frame_shape = frame.shape
    
    # Dividing length of image in two to find center x coordinate
    xc = int(frame_shape[1] / 2) # tmasked_shape = [y, x, z]
    
    # Optional: shows where divides between left and right of image
    #divided_frame = cv2.line(frame, (xc, 0), (xc, int(frame_shape[0])), (255, 255, 255), 15)
    #cv2.imshow("Divided frame", divided_frame)
    #cv2.waitKey(1)
    
    return xc, frame_shape


def angle_line_point(x, px, py):
    '''
    Determing the positive angle between a point and a vertical line.
    Formula: arctangent of (x / y) = theta
    Takes the absolute value of the subtraction between the point's x-coordinate and the line's
        x-coordinate to calculate the horizontal distance between the point and the line. This
        is the x in the equation.
    Uses abs() because the point could be on the right or the left of the line.
    
    param x: the vertical line's x-coordinate
    param px: the point's x-coordinate
    param py: the point's y-coordinate
    return angle: the angle between the point and the vertical line
    '''
    
    # Calculating the angle between the point and the line
    angle = math.atan(abs(x - px) / py)
    
    return angle


def main():
    
    # If teal is detected, find the center #######################################
    
    # Start camera, 0 means using USB camera (1 is using raspberry pi camera)
    capture = cv2.VideoCapture(0)
    
    # Setting up Yelena's legs - Sunfounder code
    crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

    # Grabbing one cropped, masked image to use to find xc
    tmasked = teal_detect2.teal_mask_vision(capture)
    
    # Calling frame_divide to determine center x-coordinate of frame
    xc, tmasked_shape = frame_divide(tmasked)
    
    # Setting the solving flag to True so Yelena searches for teal and moves towards it until solved maze
    solving = True
    
    # Setting a count so Yelena doesn't get stuck on a past frame
    count = 0
    
    # Setting a solved count to use if Yelena can't find anymore teal
    solved_cntdwn = 16 # Calculated roughly that each turn is ~ 20 degrees
    
    # while loop runs until Yelena can't find anymore teal
    while solving:
        
        # Yelena has turned arount 180 degrees and can't find teal
        if solved_cntdwn == 0:
            
            # Have Yelena sit down and stop the loop
            yelena_move.sit(crawler=crawler)
            
            # Stop the while loop
            solving = False
        
        # Else, Yelena is still searching for/following teal
        else:
                
            # Sending camera feed to teel_detect2 to detect teal and find center
            tmasked = teal_detect2.teal_mask_vision(capture)
            
            cv2.imshow("tmasked image", tmasked)
            cv2.waitKey(1)
            
            # Using try/except block so code doesn't break when no teal object is found
            try:
                # Finding center of teal object
                tcx, tcy = teal_detect2.find_center(tmasked)
                
                # Drawing a circle on center and showing feed
                cv2.circle(tmasked, (tcx, tcy), 5, (255, 255, 255), -1)
                cv2.line(tmasked, (xc, 0), (xc, int(tmasked_shape[0])), (255, 255, 255), 5)
                cv2.imshow("Centroid calculated in image", tmasked)
                cv2.waitKey(1)
                
                # Determining the angle of the centroid from the center buffer
                angle = angle_line_point(xc, tcx, tcy)
                
                # Defining the angle of the center buffer
                cbuff = 1
                
                if (count % 8) == 1:
                    # If the centroid is to the right of the buffer
                    if (tcx > xc) and angle > cbuff:
                        print("Object to the right")
                        
                        # Using Sunfounder's code to move Yelena to the right
                        yelena_move.move_right(speed=70, crawler=crawler)
                        
                    # If the centroid is to the left of the buffer
                    elif (tcx < xc) and (tcx >= 0) and angle > cbuff:
                        print("Object to the left")
                        
                        # Using Sunfounder's code to move Yelena to the left
                        yelena_move.move_left(speed=70, crawler=crawler)
                    
                    # If the centroid is in the center line buffer
                    elif angle <= cbuff:
                        print("Object in center buffer")
                        
                        # Using Sunfounder's code to move Yelena forward
                        yelena_move.move_forward(speed=70, crawler=crawler)
                    
                    # If centroid is on bottom of frame (Yelena on top of it)
                    elif tcx < 15:
                        print("Yelena on top of object")
                        
                # Increase the count by one so Yelena takes a command every 1/8th iteration
                count += 1
            
            except (TypeError, ZeroDivisionError) as e:
                print("No teal found, in face_teal")
                
                # Having Yelena turn when she finds no teal
                yelena_move.move_left(crawler=crawler)
                
                solved_cntdwn -= 1
                
            # To save memory, we could only run find_center if there are enough teal pixels
            # But right now there's no easy way to do this that takes less memory than just running
            # this function. May improve in future.


if __name__ == '__main__':
    main()
# Eof