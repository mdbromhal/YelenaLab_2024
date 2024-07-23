#!/usr/bin/env python3

# Author: Megdalia Bromhal
# Date: 23 July 2024
# Purpose: Takes in from user and camera details about environment which are then used in face_teal.py to help Yelena funciton better

# with open("env_file.txt", 'w') as env_file:
#     env_file.write("Data")
#     env_file.writelines("Data")

# Importing necessary modules
import numpy as np
import pandas as pd
import sys
import cv2



def choose_surface():
    """
    Displays options to choose from to describe the surface Yelena is on, and user is prompted to input the index corresponding to that surface.
    Error handling stops script if incorrect type (not int) or index (not in range provided) is entered.

    return surface_options[surface_index]: string, the surface the user indicated to with the entered index
    """

    # Get data from user and camera
    surface_options = ['Non-slip hardwood', 'Light carpet']

    # Initiating an index for the surface options from which the user can choose from
    index = 0
    print('\n1) Choose the surface: ')

    # Iterating through and printing the surface options
    for option in surface_options:
        print(index, " ", surface_options[index])
        index += 1

    # Asking the user for input
    surface_index = input("Please enter the index corresponding to the surface option closest to what Yelena is on: ")

    # Error handling while offering the user surface options to enter into the file
    try:

        surface_index = int(surface_index)

        # Returning surface if no errors
        return surface_options[surface_index]

    except (ValueError, IndexError) as e:
        print(e, "; Must enter integer within range of indexes provided")
        print("Exiting program. Please try again.")
        sys.exit()



def find_brightness():
    """
    Takes a photo with cv2 and sends the frame to isbright() to determine if its brightness is above the threshold.
    Writes image into directory.

    return bright: Boolean, True if bright (over threshold), False otherwise
    return brightness: float, calculated brightness with average pixels
    """
    print("\n2) Calculating if environment is light or dark")

    try:
        # Start camera, 0 means using USB camera (1 is using raspberry pi camera)
        print("Taking a photo...")
        cap = cv2.VideoCapture(0)

        # Getting frame from video capture
        ret, frame = cap.read()
        
        # Sending frame to is_bright function from https://github.com/imneonizer/How-to-find-if-an-image-is-bright-or-dark
        print("Determining if image is within brightness threshold...")
        bright, brightness = isbright(frame, dim=15)

        # Saving image into the directory for further reference
        cv2.imwrite("brightness_testframe.jpg", frame)

        return bright, brightness
    
    except cv2.error as e:
        print(e)
        print("Issue with camera. Check port number?")


# Copied from https://github.com/imneonizer/How-to-find-if-an-image-is-bright-or-dark
def isbright(image, dim=10, thresh=0.5):
    # Resize image to 10x10
    image = cv2.resize(image, (dim, dim))
    # Convert color space to LAB format and extract L channel
    L, A, B = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
    # Normalize L channel by dividing all pixel values with maximum pixel value
    L = L/np.max(L)
    # Return True if mean is greater than thresh else False
    return (np.mean(L) > thresh), np.mean(L) # MB added second item to return


def main():
    
    # Welcoming user
    print("This script is used to identify environmental characteristics in which Yelena is going to be. \nChoose the most appropriate option at each choice, and your answers will be logged in a file" + 
          " that will be accessed by other scripts used to direct Yelena's movement. \nPress cntrl-c to stop.")
    
    # Returning the surface user has chosen, if done correctly
    surface = choose_surface()
    print("\nChosen surface is", surface)
    
    try:
        # Returning the brightness of the environment
        bright, brightness = find_brightness()
        print("\nBrightness is", brightness, "which is bright with this threshold?", bright)
        
    except TypeError as e:
        print(e)
        print("Issue with unpacking returned values")

    # Determining the hsv value of the teal in front of Yelena, given current environmental conditions
    move_on = input("Please place a piece of teal paper in front of Yelena's camera, flat on the surface. Enter 'ok' when you have done so: ")

    if move_on == 'ok':
        pass
    else:
        print("Exiting program. Please try again.")
        sys.exit()

    # Defining data to be written to the file
    # env_data = []
    
    # # Defining the columns to be used in the csv file for organization
    # env_columns = ['Teal_Color', 'Surface']

    # df = pd.DataFrame(env_data, columns=env_columns)

    # df.to_csv('/home/mickey/scripts/Yelena_dfs/env_data.csv', index=False)
    
    # df = pd.read_csv('env_data.csv')
    
    # print(df)


if __name__ == "__main__":
    main()