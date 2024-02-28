#!/usr/bin/env python3

# 24 Feb. 2023
# Megdalia Bromhal
# References: https://pysource.com/2019/02/15/detecting-colors-hsv-color-space-opencv-with-python/,
# https://github.com/larguncw/PyRoboCar/blob/main/driver/code/RaspberryPi/opencv_test.py

# Import needed modules
import cv2
import numpy as np


def main():

    # From display vilib file from example directory

    from vilib import Vilib

    #Vilib.camera_start(vflip=False,hflip=False) # vflip:vertical flip, hflip:horizontal Flip
    # local:local display, web:web display
    # when local=True, the image window will be displayed on the system desktop
    # when web=True, the image window will be displayed on the web browser at http://localhost:9000/mjpg
    #Vilib.display(local=True,web=False)
    #print('\npress Ctrl+C to exit')
    # try:
    #    main()
    #    while True:
    #        pass
    #except KeyboardInterrupt:
    #    pass
    #except Exception as e:
    #    print(f"\033[31mERROR: {e}\033[m")
    #finally:
    # Vilib.camera_close()

    # From pirobo car help
    camera = cv2.VideoCapture(1)
    #camera.set(3, 640)
    #camera.set(4, 480)


    # Defining hsv ranges for teal color
    #low_teal = np.array([70, 110, 30])
    #high_teal = np.array([102, 255, 200])

    while(camera.isOpened()):
        _, image = camera.read()
        cv2.imshow('Original', image)
#
       # hsv_frame = cv2.cvtColor(read_image, cv2.COLOR_BGR2HSV)

        # Defining the teal mask and running it on the image
      #  teal_mask = cv2.inRange(hsv_frame, low_teal, high_teal)
     #   teal = cv2.bitwise_and(image, image, mask=teal_mask)


if __name__ == "__main__":
    main()