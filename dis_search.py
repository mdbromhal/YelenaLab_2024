# Megdalia Bromhal
# 5 Feb. 2024
# DFS main search file
from collections import deque

# Imports
import numpy as np


def write_map(map_array):

    try:
        map_file = open("map.txt", 'w')

        # Writing the array to the file
        map_file.writelines(str(map_array))

    except FileNotFoundError:

        # Creating a file to write the new array to
        map_file = open("map.txt", 'w')

        # Writing the array to the file
        map_file.writelines(str(map_array))


def get_start_state(map_array):
    # Getting the shape of the map array
    limit_x, limit_y = map_array.shape
    # print(map_array.shape, limit_x, limit_y)

    # Deciding the middle to start exploring
    center_x = limit_x // 2
    center_y = limit_y // 2
    # print(center_x, center_y)

    # Marking center position
    map_array[center_x, center_y] = 1
    # print(map_array)
    # This is the start state for the game

    # Return starting position
    return center_x, center_y, map_array


def dfs_search(blank_map_array):

    # Get start state
    start_x, start_y, map_array = get_start_state(blank_map_array)
    # print(start_x, start_y, map_array)

    write_map(map_array)

    # Is goal state?
    # Run camera and detect color
    # If is, complete & shutdown

    # I want it to make its own map in its head as it goes along and know where it is

if __name__ == "__main__":

    blank_map_array = np.zeros(shape=(10, 10), dtype=int)
    # print(blank_map_array)

    write_map(blank_map_array)

    dfs_search(blank_map_array)
