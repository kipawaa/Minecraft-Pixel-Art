# reads from the directory ./blocks to create a table of the average colour value of each block

from PIL import Image
import os
import numpy as np

class Block_Image:
    def __init__(self, name, image_type, average_colour):
        self.name = name
        self.image_type = image_type
        self.average_colour = average_colour

def get_block_colours():
    colour_to_block = {}

# loop over files in blocks directory
    for filename in os.listdir("./blocks"):

        # open each image file
        if filename.endswith(".png"):
            print(filename)
            with Image.open("./blocks/" + filename) as image:

                if image.mode != 'RGBA':
                    image = image.convert("RGBA")

                # load the image to get the pixels
                pixels = image.load()

                average = 0 if isinstance(pixels[0,0], int) else np.zeros(len(pixels[0,0]))

                # loop over each pixel
                for y in range(image.width):
                    for x in range(image.height):

                        # update average value
                        #print(pixels[y,x], average)
                        average += pixels[y, x]
                
                # normalize and save average colour value
                colour_to_block[tuple(average / (image.width * image.height))] = filename


    return colour_to_block

if __name__ == '__main__':
    d = get_block_colours()
    for key in d:
        print(key, d[key])
