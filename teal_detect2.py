#!/usr/bin/env python3

# 10 June 2024
# Megdalia Bromhal
# References:
# https://pysource.com/2019/02/15/detecting-colors-hsv-color-space-opencv-with-python/
# https://learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
# https://pythongeeks.org/color-grayscale-and-binary-image-conversion-in-opencv/
# https://learnopencv.com/cropping-an-image-using-opencv/

# Import needed modules
import cv2
import numpy as np


def teal_mask_vision(cap):
    '''
    Gets the frame from the camera capture, converts the frames to hsv and applies the teal mask.
    Then shows the masked image (only shows teal color).
    
    param cap: access to the camera's information when activated
    return tmasked: the frame received masked with a teal hsv mask
    '''

    # Start reading from video capture
    ret, frame = cap.read()
    
    # Cropping the frame by calling crop_frame function
    cframe = crop_frame(frame)
    # May crop more when testing Yelena

    # Converting the frame to HSV so we can choose which colors to mask
    hsv_frame = cv2.cvtColor(cframe, cv2.COLOR_BGR2HSV)

    # Defining hsv ranges for teal color
    low_teal = np.array([25, 52, 72]) # Minimum hsv values # Changed from [70, 110, 30]
    # np.array([25, 52, 72]) green
    # np.array([70, 100, 15]) works for blue and teal!
    # np.array([90, 110, 30]) works for blue!
    high_teal = np.array([102, 255, 255]) # Maximum hsv values # Changed from [102, 255, 200]
    # np.array([102, 255, 255]) green
    # low_teal = np.array([186, 100, 15])
    # high_teal = np.array([178, 100, 90])
    
    # Creating the mask and putting it on the hsv-converted frame
    teal_mask = cv2.inRange(hsv_frame, low_teal, high_teal)
    
    # Performing a bitwise AND operation on the frame with the mask, returning the frame
    tmasked = cv2.bitwise_and(cframe, cframe, mask=teal_mask)
    
    return tmasked


def crop_frame(frame):
    '''
    Takes in the video frame and crops the frame to block view of objects above the maze or
    too far away. We're doing this to limit the distractions Yelena sees and help guarentee
    that Yelena is able to follow the teal disks in successive order.
    
    param frame: image frame from open CV video capture
    return cropped frame
    '''
    # print(frame.shape)
    # print((frame.shape[0] // 2), frame.shape[0])
    
    return frame[(frame.shape[0] // 2):frame.shape[0]]


def find_center(tmasked):
    '''
    Finding the center of the teal blob with Open CV's moments.
    First put masked image into grayscale, then convert to binary image.
    Then calculate centroid of moment and draw circle onto teal masked image and show.
    
    References:
    https://learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
    https://pythongeeks.org/color-grayscale-and-binary-image-conversion-in-opencv/
    
    param tmasked: the teal-masked image
    return None
    '''
    
    # Converting frame to grayscale
    gray_frame = cv2.cvtColor(tmasked, cv2.COLOR_BGR2GRAY)
    
    # Converting the grayscale frame to a binary image
    # Binary image = pixels have 2 possible intensity values: black or white (0 or 255).
    # Simpler to process and used in thresholding
    ret, thresh = cv2.threshold(gray_frame, 127, 255, 0)
    
    # Calculating the moments of the binary image
    # Moments = weighted average of image pixel intensities
    # Centroid of moment is what we're calculating here
    M = cv2.moments(thresh)
    
    # Using try/except block because if there's a black blob/issue with mask, it will keep going
    # Don't need every moment coordinate, since we're using live video and processing fast enough
    try:
        # Calculating the x and y coordinate of centroid
        tcx = int(M["m10"] / M["m00"]) # x coordinate
        tcy = int(M["m01"] / M["m00"]) # y coordinate
        
        return tcx, tcy
        
    except (ZeroDivisionError, TypeError) as e:
        ("No teal objects in frame")


def main():
    
    # Start camera, 0 means using USB camera (1 is using raspberry pi camera)
    cap = cv2.VideoCapture(0)
    
    # Using a flag to start & stop teal detection so can call off when arrive at destination
    while True:
        
        # Masking image to only find teal objects ##########
        # Getting the camera frames and applying a teal mask
        tmasked = teal_mask_vision(cap)
        
        # Showing the masked image
        #cv2.imshow("Teal Masked Image", tmasked)
        #cv2.waitKey(1) # Continuing to show the live camera feed (if 0, shows one photo only)
        
        try:
            # Finding center of teal object ####################
            tcx, tcy = find_center(tmasked)
        
            # Highlighting the centroid
            cv2.circle(tmasked, (tcx, tcy), 5, (255, 255, 255), -1)
            
            # Showing the image with the centroid
            cv2.imshow("Centroid calculated in image", tmasked)
            cv2.waitKey(1)
        except (ZeroDivisionError, TypeError) as e:
            print("No teal in image.")

if __name__ == '__main__':
    main()
# Eof