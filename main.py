#!/usr/bin/env python
import os
import sys
import cv2
from PIL import Image
import blur_image_region as b

default_video_file = "OneMinuteCollatGame.mp4"  # Replace with the name of your file.
default_video_output_file = 'blurred_video.avi'
default_video_fps = 30


# Note: Eventually, I want the arguments to be specified by the user through some sort of GUI,
# perhaps by dragging and dropping the file and typing in the file locations / FPS?.
def blur_video(video_file=default_video_file, video_output_file=default_video_output_file, video_fps=default_video_fps):
    vidcap = cv2.VideoCapture(video_file)
    successful,image = vidcap.read()  # Gets the first frame of the video for measurement purposes.
    height,width,layers = image.shape  # Measures dimensions from the first frame.
    output_video = cv2.VideoWriter(video_output_file,cv2.VideoWriter_fourcc(*'DIVX'),video_fps,(width,height))
    count = 0
    while successful:
        #image = b.blur_single_frame(image, b.clan_roster_rectangle)
        print("First successful")
        small_image = image.resize((32,32),Image.BILINEAR)  # Resizes down to 32x32 pixels.
            # For a smoother blur, increase the size of the scaled image.
        blurred_image = small_image.resize(image.size,Image.BICUBIC)  # Scales image back up using BICUBIC resample filter, thereby blurring it.
        cropped_image = blurred_image.crop(b.clan_roster_rectangle)  # Crops out a smaller section of the image.
        image.paste(cropped_image, (b.clan_roster_rectangle), None)  # Re-insert the smaller blurred section of the image onto the original.
        output_video.write(image)  # Adds the input video's frame to the output video.
        # cv2.imwrite("temp_image_frames/frame%d.jpg" % count, image)  # Saves the frame as a JPEG file for debugging purposes.
        successful,image = vidcap.read()  # Takes the next individual frame from the video and saves it as an image.
        print("Read a new frame: " + str(successful))  # This is the less-preferred printing syntax, but works with Python 2.7.
        count += 1
    output_video.release()

def main():
    print("Starting main()")
    print("Using CV2 version: " + cv2.__version__ + "\n")
    # image = b.blur_single_frame(b.sample_image_file, b.clan_roster_rectangle)
    # image.save('temp_blur_test.jpg')
    blur_video()
    print("Finished main()")

# ~~~~ Don't worry about this for now ~~~~
if __name__ == "__main__":
    main()
