from PIL import Image
from block_colour_values import get_block_colours
import numpy as np
import os

def write_colours_to_file(colour_file):
    colour_data = get_block_colours()

    for data in colour_data:
        colour_file.write(f"{data[0][0]} {data[0][1]} {data[0][2]} {data[0][3]} {data[1]}\n")

def get_colours_from_file(colour_file):
    data = []
    for line in colour_file:
        line = line.strip().split()
        data.append(tuple((np.array([line[0], line[1], line[2], line[3]]).astype(float), line[4])))
    return data


def get_closest_colour(colour, colour_data):
    # return the closest colour in get_block_colours to colour

    # cast input to numpy array
    target_colour = np.array(colour)

    closest = np.zeros(4)
    closest_dist = 10000
    for colour,_ in colour_data:
        dist = np.linalg.norm(colour - target_colour) 
        if dist < closest_dist:
            closest = colour
            closest_dist = dist
    return closest

if __name__ == "__main__":
    # get image file
    user=input("input the name of your art file, with the extension: ")
    with Image.open(user.strip()) as image:

        # check for resizing
        user=input("would you like to resize? (y/n): ")
        if (user == "y"):
            # get desired resize dimensions
            user = input("input your desired image size in the format \"width height\": ")
            dims = tuple([int(i) for i in user.split()])

            # resize image
            image = image.resize(dims)

        print("finished resizing")

        # convert to pixel art
        if not os.path.isfile("./colour_data.txt"):
            with open("./colour_data.txt", "w") as colour_file:
                write_colours_to_file(colour_file)

        with open("./colour_data.txt") as colour_file:
            # get colour data from file
            colour_data = get_colours_from_file(colour_file)
            print("got block data")

            # create a new image
            approximation = np.zeros((image.width, image.height, 4))

            # get pixels from input image
            pixels=image.load()
            print("loaded input image")

            # for each pixel
            for y in range(image.height):
                for x in range(image.width):
                    # get the best approximation of this pixel
                    approximation[y,x, :] = get_closest_colour(pixels[x,y], colour_data)
            print("generated approximation")

            # show the resulting image
            mc_art = Image.fromarray(approximation.astype('uint8'))
            mc_art.show()
