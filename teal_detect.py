#!/usr/bin/env python3

# 24 Feb. 2023
# Megdalia Bromhal
# References: https://pysource.com/2019/02/15/detecting-colors-hsv-color-space-opencv-with-python/, 
# https://github.com/larguncw/PyRoboCar/blob/main/driver/code/RaspberryPi/opencv_test.py

# Import needed modules
import cv2
import numpy as np


def main():

    # From pirobo car help
    camera = cv2.VideoCapture(-1)
    camera.set(3, 640)
    camera.set(4, 480)


    # Defining hsv ranges for teal color
    low_teal = np.array([186, 100, 15])
    high_teal = np.array([178, 100, 90])
  
    while( camera.isOpened()):
        _, image = camera.read()        
        cv2.imshow('Original', image)

        hsv_frame = cv2.cvtColor(read_image, cv2.COLOR_BGR2HSV)

        # Defining the teal mask and running it on the image
        teal_mask = cv2.inRange(hsv_frame, low_teal, high_teal)
        teal = cv2.bitwise_and(image, image, mask=teal_mask)

if __name__ == "__main__":
    main()
