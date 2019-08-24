# blur_image_region.py
'''
This module pixelates a file.

Link to pixelation using PIL:
https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
'''

try:
    from PIL import Image
except ImportError:
    import Image
from math import ceil  # Used for rounding up.
import cv2
import pytesseract
import numpy

sample_image_file = "temp_image_frames/frame217.jpg"
clan_roster_rectangle = (1368, 250, 1843, 922)  # Currently, takes the hard-coded name values from clan roster page.

def initialize_video(video_file):
    return cv2.VideoCapture(video_file)

# TODO: Fix this command.
def convert_cv2_to_pil(cv2_image):
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv2_image)
    return pil_image

# TODO: Fix this command.
def convert_pil_to_cv2(pil_image):
    cv2_image = numpy.array(pil_image)
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    cv2_image = cv2_image[:, :, ::-1].copy()
    return cv2_image


# This function takes an image as a parameter, and returns that image with
# all of its text blurred out.
def process_frame(image_to_process):
    image_to_process = convert_cv2_to_pil(image_to_process)
    blurred_image = blur(image_to_process)
    list_of_character_locations = find_characters(image_to_process)
    for character in list_of_character_locations:
        image = crop_character_and_place_in_larger_image(image_to_process, blurred_image, character)
    image = convert_pil_to_cv2(image)
    return image


# This function takes as parameters an image and an optional floating point
# number to determine the blurriness of the image. This function will return
# the same input image, but entirely blurred.
# Note: For a smoother blur, increase the size of the scaled image.
def blur(image_to_process, resize_ratio=(1.0/30.0)):
    smaller_image_size = (int(ceil(image_to_process.size[0] * resize_ratio)), int(ceil(image_to_process.size[1] * resize_ratio)))
    small_image = image_to_process.resize(smaller_image_size, resample=Image.BILINEAR)  # Shrinks image down to a much smaller size.
    blurred_image = small_image.resize(image_to_process.size, resample=Image.NEAREST)  # Scales image back up to its original size using the NEAREST resample filter, thereby blurring it.
    return blurred_image


# This function takes as parameters an image and an optional boolean for
# debugging purposes. This function will parse the image for text, and return
# the locations of each text character as a 2D tuple (static array).
# The debugging boolean will print the results at each step along the way.
def find_characters(image_to_process, should_debug=False):
    unicode_wall_of_character_locations = pytesseract.image_to_boxes(image_to_process)  # Note: Takes Image file, not CV2 image.
    if should_debug:
        print("All the characters and their locations in Unicode are: ")
        print(unicode_wall_of_character_locations)
    string_wall_of_character_locations = repr(unicode_wall_of_character_locations)  # Converts the unicode file to a string
    if should_debug:
        print("\nThe characters in string format: ")
        print(string_wall_of_character_locations)
    string_wall_of_character_locations = string_wall_of_character_locations.replace("\\n", " ")  # Replaces all newlines with a space character.
    if should_debug:
        print("\nAll newlines should now be spaces: ")
        print(string_wall_of_character_locations)
    string_tuple_of_character_locations = tuple(i for i in string_wall_of_character_locations.split())  # Parses the data into a tuple (a static array).
    if should_debug:
        print("\nUnsplit tuple with size: " + str(len(string_tuple_of_character_locations)))
        print(str(string_tuple_of_character_locations) + "\n")
    split_tuple_of_character_locations = tuple(string_tuple_of_character_locations[a : (a + 6)] for a in range(0, len(string_tuple_of_character_locations), 6))  # Splits the tuple every 6 positions.
    if should_debug:
        print("Split tuple with size: " + str(len(string_tuple_of_character_locations)))
        print(split_tuple_of_character_locations)
    return split_tuple_of_character_locations


def finish_video(video_file):
    video_file.release()
