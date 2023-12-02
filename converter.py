from PIL import Image
from block_colour_values import get_average_block_colours, get_median_block_colours
import numpy as np
import os


def get_closest_file(colour, colour_data):
    # return the closest colour in get_block_colours to colour

    # cast input to numpy array
    target_colour = np.array(colour)

    closest_dist = 10000
    closest_file = ""
    for colour, filename in colour_data:
        dist = np.linalg.norm(colour - target_colour) 
        if dist < closest_dist:
            closest_dist = dist
            closest_file = filename
    return closest_file


if __name__ == "__main__":
    # get image file
    user = input("input the name of your art file, with the extension: ")
    with Image.open(user.strip()) as image:
        if image.mode != "RGBA":
            image = image.convert('RGBA')

        # check for resizing
        user = input("would you like to resize? This *WILL* distort the image if the aspect ratio is changed. (y/n): ")
        if (user == "y"):
            # get desired resize dimensions
            user = input("input your desired image size in the format \"width height\": ")
            dims = tuple([int(i) for i in user.split()])

            # resize image
            image = image.resize(dims, resample=Image.Resampling.LANCZOS)

        print("finished resizing")

        # get block palette
        user = input("would you like to use all blocks (a), or suvival blocks (s)? (a/s): ")
        block_directory = os.path.abspath(os.getcwd())
        if user == "s":
            block_directory += "/survival blocks/"
        else:
            block_directory += "/all blocks/"

        # convert to pixel art
        # get colour data from file
        user = input("approximate colours using average or median? (a/m): ")
        if user == "a":
            colour_data = get_average_block_colours(block_directory)
        else:
            colour_data = get_median_block_colours(block_directory)
        
        print("got block data")

        # create a new image
        mc_art = Image.new('RGBA', (image.width*16, image.height*16))

        # get pixels from input image
        pixels = image.load()
        print("loaded input image")

        # for each pixel
        for x in range(image.width):
            for y in range(image.height):
                # get the best approximation of this pixel
                with Image.open(block_directory + get_closest_file(pixels[x,y], colour_data)) as block_image:
                    mc_art.paste(block_image, box=(16*x, 16*y))
        print("generated approximation")

        # show the resulting image
        mc_art.show()
