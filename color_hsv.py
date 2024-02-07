# Yelena's green color detection in frame
# Megdalia Bromhal
# 7 Feb 2024
# Reference: https://pysource.com/2019/02/15/detecting-colors-hsv-color-space-opencv-with-python/

# Import modules
import cv2
import numpy as np

capture = cv2.VideoCapture(0)

while True:
  -, frame = capture.read()
  hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # What does this do?

  # Defining the HSV ranges of green color
  low_green = np.array([])
  high_green = np.array([])
  
  


                           
    # Red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
