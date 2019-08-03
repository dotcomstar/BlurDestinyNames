#!/usr/bin/env python
import os
import sys
import cv2
try:
    from PIL import Image
except ImportError:
    import Image
import blur_image_region as b
import pytesseract

default_input_video_file = "OneMinuteCollatGame.mp4"  # Replace with the name of your file.
default_video_output_file = 'blurred_video.avi'
default_video_fps = 30
temp_image_location = "temp_video_during_blur.jpg"

# Note: Eventually, I want the arguments to be specified by the user through some sort of GUI,
# perhaps by dragging and dropping the file and typing in the file locations / FPS?.
def blur_video(input_video_file=default_input_video_file, video_output_file_file=default_video_output_file, video_fps=default_video_fps):
    vidcap = cv2.VideoCapture(input_video_file)
    successful,image = vidcap.read()  # Gets the first frame of the video for measurement purposes.
    height,width,layers = image.shape  # Measures dimensions from the first frame.
    output_video = cv2.VideoWriter(video_output_file_file,cv2.VideoWriter_fourcc(*'DIVX'),video_fps,(width,height))
    count = 0
    while successful:
        cv2.imwrite(temp_image_location, image)
        image = b.blur_single_frame(temp_image_location, b.clan_roster_rectangle)  # NOTE: This current implementation is very jank. It involves lots of saving and reading which is probably unnecessary, but I haven't figured out how to convert uMAT types yet.
        output_video.write(cv2.imread(temp_image_location))  # Adds the input video's frame to the output video.
        # cv2.imwrite("temp_image_frames/frame%d.jpg" % count, image)  # Saves the frame as a JPEG file for debugging purposes.
        successful,image = vidcap.read()  # Takes the next individual frame from the video and saves it as an image.
        print("Read a new frame: " + str(successful) + "  --"),  # This is the less-preferred printing syntax, but works with Python 2.7.
        count += 1
    output_video.release()

def main():
    print("Starting main()")
    print("Using CV2 version: " + cv2.__version__ + "\n")
    # b.blur_single_frame(b.sample_image_file, b.clan_roster_rectangle, should_preserve_original_image=True, should_debug=True)

    list_of_character_locations = pytesseract.image_to_boxes(Image.open(b.sample_image_file))
    print("Type of return value is: " + str(type(list_of_character_locations)) + "\n")
    print(list_of_character_locations)


    list_of_character_locations = ''.join(c for c in list_of_character_locations if c.isdigit() or c == " ")  # Removes all non-numeric and non-space characters.
    x = [int(i) for i in list_of_character_locations.split()]  # Parses the data into a list.
    print(x)

    # blur_video()
    print("Finished main()")

# ~~~~ Don't worry about this for now ~~~~
if __name__ == "__main__":
    main()
