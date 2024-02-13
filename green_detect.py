# 13 Feb. 2023
# Megdalia Bromhal
# References: https://pysource.com/2019/02/15/detecting-colors-hsv-color-space-opencv-with-python/

# Import needed modules
from vilib import Vilib
from time import sleep
import cv2
import numpy as np

# Start camera
Vilib.camera_start(vflip=False, hflip=False)

# Display camera feed on local machine
Vilib.display(local=True)

sleep(0.8) # Wait for startup

cap = cv2.VideoCapture()
# cap = 

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # Show object with green color
    cv2.imshow("Frame", frame)
    cv2.imshow("Green", green)

    key = cv2.waitKey(1)
    if key == 27:
        break