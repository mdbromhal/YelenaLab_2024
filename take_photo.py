#!/usr/bin/env python3

# Author: Megdalia Bromhal
# Date: 11 Sept. 2024
# Purpose: Takes a photo with Yelena's USB camera & writes it to photos directory, named with the timestamp

# Import section
import cv2 # OpenCV
import time # To use in timestamp


def take_photo():
    """
    Takes a photo with the USB camera and writes to photos directory.
    """
    
    try:

        print("Taking a photo...")
        
        # Start camera, 0 means using USB camera (1 is using raspberry pi camera)
        capture = cv2.VideoCapture(0)
        
        # Getting frame from video capture
        _, frame = capture.read()
        
        # Showing image that we just took (OPTIONAL)
        #cv2.imshow("Frame", frame)
        #cv2.waitKey(0)
        
        # Getting the time to use in the timestamp (Year Month Day Hour Minute Second)
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S')
        
        # Setting file directory and name
        filename = "photos/" + str(timestamp) + ".jpg"
           
        # Writing frame to a jpg file in photos directory
        cv2.imwrite(filename, frame)
        
        print(f"Saved image as {filename} successfully!")
        
    except cv2.error as e:
        print(e)
        print("Issue with camera. Check port number?")


def main():
    take_photo()


if __name__ == "__main__":
    main()