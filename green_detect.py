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
   # Vilib.display(local=True)

    # Defining where to store images
    path = "/home/mickey/scripts/Yelena_dfs/test_photos"

    # while True:

    # First part: taking the photo and storing it
    # Defining the time so that we can name the photo by the time it was taken
    _time = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())

    time.sleep(1)
    # Taking the photo, naming it with the time, storing it at path
    Vilib.take_photo(str(_time), path)

    # Printing where the photo will be saved
    print("\nThe photo save as:%s/%s.jpg"%(path, _time))
    time.sleep(0.1) # Give it time to process

    # Naming the file
    photo_name = str(_time) + ".jpg"

    # Second part: accessing the photo and finding the green in it
<<<<<<< HEAD
    read_image = cv2.imread("/home/mickey/scripts/Yelena_dfs/test_photos/" + photo_name) # /home/mickey/scripts/Yelena_dfs/test_photos/24-02-13_10-40-40.jpg

    hsv_frame = cv2.cvtColor(read_image, cv2.COLOR_BGR2HSV)

    # Defining hsv ranges for green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(read_image, read_image, mask=green_mask)


    cv2.imshow("Image", read_image)
    cv2.imshow("Green", green)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("/home/mickey/scripts/Yelena_dfs/test_photos/green_mask" + photo_name, green)
=======
    read_image = cv2.imread(str(_time) + ".jpg")

    # Show image
    cv2.imshow("Test image", read_image )
    cv2.waitKey(0)

    cv2.destroyAllWindows()
>>>>>>> ceb80185df1dd0dba0ff67195376afb82f612ce8

    # Sleep one second until take another photo
    time.sleep(1)

    Vilib.camera_close()

if __name__ == "__main__":
    main()
