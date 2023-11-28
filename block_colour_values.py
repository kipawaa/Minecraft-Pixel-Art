# reads from the directory ./blocks to create a table of the average colour value of each block

from PIL import Image
import os
import numpy as np

def get_average_block_colours(directory):
    colour_to_block = []

    # loop over files in blocks directory
    for filename in os.listdir(directory):

        # open each image file
        if filename.endswith(".png"):
            with Image.open(directory + filename) as image:

                # convert image to RGBA so that all images are compatible
                if image.mode != 'RGBA':
                    image = image.convert("RGBA")
                
                # normalize and save average colour value
                colour_to_block.append((np.average(np.array(image), axis=(0,1)), filename))

    return colour_to_block


def get_median_block_colours(directory):
    colour_to_block = []

    # loop over files in blocks directory
    for filename in os.listdir(directory):

        # open each image file
        if filename.endswith(".png"):
            with Image.open(directory + filename) as image:

                # convert image to RGBA so that all images are compatible
                if image.mode != 'RGBA':
                    image = image.convert("RGBA")
                
                # normalize and save average colour value
                colour_to_block.append((np.median(np.array(image), axis=(0,1)), filename))

    return colour_to_block


if __name__ == '__main__':
    colours = get_block_colours()
    for colour, filename in colours:
        print(colour, filename)
