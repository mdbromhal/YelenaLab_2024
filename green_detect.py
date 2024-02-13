#!/usr/bin/env python3

# 13 Feb. 2023
# Megdalia Bromhal
# References: https://pysource.com/2019/02/15/detecting-colors-hsv-color-space-opencv-with-python/

# Import needed modules
from vilib import Vilib
import time
import cv2
import numpy as np


def main():
    # Start camera
    Vilib.camera_start(vflip=False, hflip=False)

    # Display camera feed on local machine
    Vilib.display(local=True)

    # Defining where to store images
    path = "/home/mickey/Pictures/vilib/photos"

    # while True:

    # First part: taking the photo and storing it
    # Defining the time so that we can name the photo by the time it was taken
    _time = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())

    # Taking the photo, naming it with the time, storing it at path
    Vilib.take_photo(str(_time), path)

    time.sleep(0.1) # Give it time to process

    # Second part: accessing the photo and finding the green in it
    read_image = cv2.imread(str(_time) + ".jpg")

    # Show image
    cv2.imshow("Test image", read_image )
    cv2.waitKey(0)

    cv2.destroyAllWindows()

    # Sleep one second until take another photo
    time.sleep(1)

    
    Vilib.camera_close()

if __name__ == "__main__":
    main()


    # while True:
    # _, frame = cap.read()
    # hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # # Green color
    # low_green = np.array([25, 52, 72])
    # high_green = np.array([102, 255, 255])
    # green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    # green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # # Show object with green color
    # cv2.imshow("Frame", frame)
    # cv2.imshow("Green", green)

    # key = cv2.waitKey(1)
    # if key == 27:
    #     break