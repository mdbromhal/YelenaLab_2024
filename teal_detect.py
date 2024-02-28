#!/usr/bin/env python3

# 28 Feb. 2024
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

    read_image = cv2.imread("/home/mickey/scripts/Yelena_dfs/test_photos/" + photo_name) # /home/mickey/scripts/Yelena_dfs/test_photos/24-02-13_10-40-40.jpg

    hsv_frame = cv2.cvtColor(read_image, cv2.COLOR_BGR2HSV)

    # Defining hsv ranges for green color
    low_teal = np.array([70, 110, 30])
    # np.array([25, 52, 72]) green
    # np.array([70, 100, 15]) works for blue and teal!
    # np.array([90, 110, 30]) works for blue!
    high_teal = np.array([102, 255, 200])
    # np.array([102, 255, 255]) green
    # low_teal = np.array([186, 100, 15])
    # high_teal = np.array([178, 100, 90])
    teal_mask = cv2.inRange(hsv_frame, low_teal, high_teal)
    teal = cv2.bitwise_and(read_image, read_image, mask=teal_mask)

    cv2.imwrite("/home/mickey/scripts/Yelena_dfs/test_photos/teal_mask" + photo_name, teal)

    read_masked_image = cv2.imread(str(_time) + ".jpg")

    cv2.imshow("Image", read_image)
    cv2.imshow("Teal", teal)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Show image
    cv2.imshow("Test image", read_masked_image )
    cv2.waitKey(0)

    cv2.destroyAllWindows()

    # Sleep one second until take another photo
    time.sleep(1)

    Vilib.camera_close()

if __name__ == "__main__":
    main()