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
import time

default_video_input_file = "OneMinuteCollatGame.mp4"  # Replace with the name of your file.
default_video_output_location = 'blurred_video.avi'
default_video_fps = 30
temp_image_location = "temp_image_during_blur.jpg"
sample_image_file = "temp_image_frames/frame217.jpg"

# Note: Eventually, I want the arguments to be specified by the user through some sort of GUI,
# perhaps by dragging and dropping the file and typing in the file locations / FPS?.
def blur_video(video_input_file, video_output_location=default_video_output_location, video_fps=default_video_fps, verbose=False):
    start_time = time.time()  # Use time.monotonic() in Python 3.3+.
    num_frames_processed = 0
    print("Processing video. This could take a while ...")
    try:
        video_file = initialize_video(video_input_file)
        successful, current_frame = video_file.read()  # Gets the first frame of the video for measurement purposes.
        height, width, layers = current_frame.shape  # Measures dimensions from the first frame.
        output_video = cv2.VideoWriter(video_output_location, cv2.VideoWriter_fourcc(*'DIVX'), video_fps, (width, height))  # Formats the video.
        while successful:
            current_frame = process_frame(current_frame)
            output_video.write(current_frame)  # Adds the input video's frame to the output video.
            successful, current_frame = video_file.read()  # Takes the next individual frame from the video and saves it as an image.
            num_frames_processed += 1
            if verbose:
                print("Read a new frame: " + str(successful) + "\n"),  # Used for debugging. Note: This is the less-preferred printing syntax, but works with Python 2.7.
    except KeyboardInterrupt:
        print("\n\nVideo generation manually interrupted.")
    finish_video(output_video, video_output_location)
    print("Elapsed time = " + str(time.time() - start_time) + " seconds.")
    print(str(num_frames_processed) + " frames processed")  # TODO: Mention total number of frames in the video.


def initialize_video(video_file):
    return cv2.VideoCapture(video_file)


# TODO: Optimize this command so it does not need to read and write each time.
# Note also that this leads to differences in the characters found with
# find_characters()
def convert_cv2_to_pil(cv2_image):
    cv2.imwrite(temp_image_location, cv2_image)
    pil_image = Image.open(temp_image_location)
    # cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    # pil_image = Image.fromarray(cv2_image)
    return pil_image


# TODO: Optimize this command so it does not need to read and write each time.
# Note also that this leads to differences in the characters found with
# find_characters()
def convert_pil_to_cv2(pil_image):
    pil_image.save(temp_image_location, "JPEG")
    pil_image.close()
    cv2_image = cv2.imread(temp_image_location, cv2.IMREAD_COLOR)
    # pil_image = pil_image.convert('RGB')
    # cv2_image = numpy.array(pil_image)
    # cv2_image = cv2_image[:, :, ::-1].copy()
    # # cv2_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_BGR2RGB)
    # # cv2_image = cv2_image[:, :, ::-1].copy()
    return cv2_image


# This function takes a PIL image as a parameter, and returns that image with
# all of its text blurred out.
def process_frame(image_to_process):
    image_to_process = convert_cv2_to_pil(image_to_process)
    blurred_image = blur(image_to_process)
    list_of_character_locations = find_characters(image_to_process)
    image_to_process = convert_pil_to_cv2(image_to_process)
    image = blur_all_characters(image_to_process, blurred_image, list_of_character_locations)
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

# This function takes as parameters an unblurred image, its blurred equivalent,
# and a list of all the characters in the image formatted as
# ('single character', 'x1', 'x2', 'y1', 'y2', '0')
# TODO: Check if bounding boxes return x1 y1 notation, or top, left, width, height.
# https://stackoverflow.com/questions/20831612/getting-the-bounding-box-of-the-recognized-words-using-python-tesseract
def blur_all_characters(image_to_process, blurred_image, list_of_character_locations):
    # TODO: Implement this function
    processed_image = image_to_process
    for character in list_of_character_locations:
        try:
            start_point = (int(character[1]), int(character[2]))  # x1, y1
            end_point = (int(character[3]), int(character[4]))  # x2, y2
            color = (255, 0, 0)  # Blue in BGR.
            thickness = 2  # Measured in pixels.
            processed_image = cv2.rectangle(processed_image,
                                        start_point,
                                        end_point,
                                        color,
                                        thickness)
        except IndexError:
            print("\n\nError: Index out of bounds.")
            print("Offending character tuple: " + str(character) + " on image of size " + str(processed_image.shape))
            print("All characters = " + str(list_of_character_locations))
            pil_image = convert_cv2_to_pil(image_to_process)
            print("Re-finding characters: " + str(find_characters(pil_image, should_debug = True)))
    return processed_image

def finish_video(video_file, output_file_name):
    video_file.release()
    print("\n\nVideo saved to " + output_file_name)

