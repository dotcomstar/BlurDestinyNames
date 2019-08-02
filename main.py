#!/usr/bin/env python
import os
import sys
import cv2
from PIL import Image

# Note: Eventually, I want this to be specified by the user through some sort of GUI,
# perhaps by dragging and dropping the file.
video_file = "OneMinuteCollatGame.mp4"  # Replace with the name of your file.
video_output_file = 'blurred_video.avi'
video_fps = 30

def main():
    print("Starting main()")
    print("Using CV2 version: " + cv2.__version__ + "\n")

    vidcap = cv2.VideoCapture(video_file)
    successful,image = vidcap.read()  # Gets the first frame of the video
    height,width,layers = image.shape  # Takes dimension measurements from the first frame
    output_video = cv2.VideoWriter(video_output_file,cv2.VideoWriter_fourcc(*'DIVX'),video_fps,(width,height))
    output_video.write(image)  # The first frame is written to the video.
    count = 0
    successful = True
    while successful:
        cv2.imwrite("temp_image_frames/frame%d.jpg" % count, image)  # Saves the frame as JPEG file.
        successful,image = vidcap.read()  # Takes individual frame from the video and saves as an image.
        output_video.write(image)  # Adds that image to the outputted video file.
        print("Read a new frame: " + str(successful))  # This is the less-preferred printing syntax, but works with Python 2.7.
        count += 1
    output_video.release()
    print("Finished main()")

# ~~~~ Don't worry about this for now ~~~~
if __name__ == "__main__":
    main()
