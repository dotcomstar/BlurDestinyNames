#!/usr/bin/env python
import os
import sys
import cv2

def main():
    print("Starting main()\n")
    print(cv2.__version__)
    vidcap = cv2.VideoCapture('OneMinuteCollatGame.mp4')
    successful,image = vidcap.read()
    height,width,layers = image.shape
    output_video = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*'DIVX'),30,(width,height))
    output_video.write(image)
    count = 0
    successful = True
    while successful and count < 100:
        cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
        successful,image = vidcap.read()
        output_video.write(image)
        print 'Read a new frame: ', successful
        count += 1
    output_video.release()
    print("Finished main()")

# ~~~~ Don't worry about this for now ~~~~
if __name__ == "__main__":
    main()
