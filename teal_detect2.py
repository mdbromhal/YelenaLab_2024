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
import math


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
    low_teal = np.array([70, 100, 15]) # [70, 100, 15] # Minimum hsv values 
    # Changed from [70, 110, 30]
    # [25, 52, 72] works for green!
    # [70, 100, 15] works for blue and teal!
    # [90, 110, 30] works for blue!
    #[70, 100, 15] works for teal!
    # [25, 25, 25]
    # [70, 10, 15] close
    # [33, 100, 100] close neon green
    # [70, 35, 45] teal a little

    high_teal = np.array([102, 255, 190])  # [102, 255, 190] # Maximum hsv values 
    # [102, 255, 200] works for teal!
    # [102, 255, 255] works for green!
    # [102, 255, 200] works for green and teal!
    # [102, 255, 255] works for blue and teal!
    # [102, 255, 190] works for teal in dark lighting!
    # [102, 255, 160] works for teal in bright lighting!
    # [190, 190, 200]
    # [80, 255, 160] close
    # [(53, 255, 255)] close neon green
    # [102, 255, 200] teal a little
    
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
        ("Error finding center in teal_detect2")


# Used in face_teal.py
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


def centroid_right(centroid_x, center_x, angle, center_buffer=0):
    '''
    Determines if the centroid is to the right of a vertical center line and buffer.

    param centroid_x: x-coordinate of the centroid
    param center_x: x-coordinate of the frame's center line
    param angle: angle of the centroid from the center of the frame.
    param center_buffer: the angle of buffer to be considered neither to the right or left

    return True if centroid is to the right of the center line or False if it is not
    '''

    return (centroid_x > center_x) and (angle > center_buffer)


def centroid_left(centroid_x, center_x, angle, center_buffer=0):
    '''
    Determines if the centroid is to the left of a vertical center line and buffer.

    param centroid_x: x-coordinate of the centroid
    param center_x: x-coordinate of the frame's center line
    param angle: angle of the centroid from the center of the frame.
    param center_buffer: the angle of buffer to be considered neither to the right or left

    return True if centroid is to the right of the center line or False if it is not    
    '''

    return (centroid_x < center_x) and (centroid_x >= 0) and (angle > center_buffer)


def main():
    
    # Start camera, 0 means using USB camera (1 is using raspberry pi camera)
    cap = cv2.VideoCapture(0)
    
    # Using a flag to start & stop teal detection so can call off when arrive at destination
    while True:
        
        # Masking image to only find teal objects ##########
        # Getting the camera frames and applying a teal mask
        tmasked = teal_mask_vision(cap)
        
        # Showing the masked image
        cv2.imshow("Teal Masked Image", tmasked)
        cv2.waitKey(1) # Continuing to show the live camera feed (if 0, shows one photo only)
        
        try:
            # Finding center of teal object ####################
            tcx, tcy = find_center(tmasked)
        
            # Highlighting the centroid
            cv2.circle(tmasked, (tcx, tcy), 5, (255, 255, 255), -1)
            
            # Showing the image with the centroid
            # cv2.imshow("Centroid calculated in image", tmasked)
            #cv2.waitKey(1)
            print("Found teal!")

        except (ZeroDivisionError, TypeError) as e:
            print("Error finding teal in teal_detect2")

if __name__ == '__main__':
    main()
# Eof
