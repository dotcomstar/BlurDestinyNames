#!/usr/bin/env python
import os
import sys
import cv2

def main():
    print("Starting main()\n")
    print(cv2.__version__)
    vidcap = cv2.VideoCapture('OneMinuteCollatGame.mp4')  # Replace with the name of your file.
        # Note: Eventually, I want this to be input by the user in a GUI, or perhaps by dragging and
        # dropping the file.
    successful,image = vidcap.read()
    height,width,layers = image.shape
    output_video = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*'DIVX'),30,(width,height))  # Specified the output file and FPS.
        # The same comment above about user input in GUI also applies here.
    output_video.write(image)  # The first frame is written to the video.
    count = 0
    successful = True
    while successful and count < 100:
        cv2.imwrite("frame%d.jpg" % count, image)  # Saves the frame as JPEG file.
        successful,image = vidcap.read()  # Takes individual frame from the video and saves as an image.
        output_video.write(image)  # Adds that image to the outputted video file.
        print("Read a new frame: " + str(successful))  # This is the less-preferred printing syntax, but works with Python 2.7.
        count += 1
    output_video.release()
    print("Finished main()")

# ~~~~ Don't worry about this for now ~~~~
if __name__ == "__main__":
    main()
