#!/usr/bin/env python
import os
import sys
import cv2
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import blur_image_region as b

def main():
    print("Starting main()")
    print("Using CV2 version: " + cv2.__version__ + "\n")

    # test_convert_pil_to_cv2()

    # image_file = Image.open(b.sample_image_file)
    # image_file = b.convert_pil_to_cv2(image_file)
    # image_file = b.convert_cv2_to_pil(image_file)
    # b.find_characters(image_file, should_debug=True)  # This line should work
    #                                                     # in the final version.

    four_corners = Image.open("quick_brown_fox.png")
    b.find_characters(four_corners, should_debug = True)
    print("\nToString = " + pytesseract.image_to_string(four_corners))
    print("\nToData:\n" + pytesseract.image_to_data(four_corners))
    print("\nToOSD = " + pytesseract.image_to_osd(four_corners))
    exit()

    b.blur_video(b.default_video_input_file)  # TODO: Enable GUI input for these parameters.

    print("\nFinished main()")

def test_convert_cv2_to_pil():
    video_file = cv2.VideoCapture(b.default_video_input_file)
    successful, current_frame = video_file.read()  # Gets the first frame of
        # the video for measurement purposes.
    height, width, layers = current_frame.shape  # Measures dimensions from the first frame.
    while successful:
        successful, current_frame = video_file.read()  # Takes the next
            # individual frame from the video and saves it as an image.
        print("Read a new frame: " + str(successful) + "  --"),  # Used for debugging. Note: This is the less-preferred printing syntax, but works with Python 2.7.
        current_frame = b.convert_cv2_to_pil(current_frame)  # The actual conversion.
        current_frame.save("./test_convert_cv2_to_pil.jpg")
        print("Successfully converted to and saved PIL image")


def test_convert_pil_to_cv2():
    output_video_location = './test_convert_pil_to_cv2.avi'
    current_frame = Image.open('temp_image_frames/frame0.jpg')  # The main line.
    # current_frame = cv2.imread('temp_image_frames/frame0.jpg')  # Something cheeky to test. It works.
    height, width = current_frame.size
    output_video = cv2.VideoWriter(output_video_location,
                                   cv2.VideoWriter_fourcc(*'MJPG'),
                                   b.default_video_fps,
                                   (width, height))  # Formats the video.

    current_frame = b.convert_pil_to_cv2(current_frame)  # The actual conversion.
    count = 0
    while count < 100:
        output_video.write(current_frame)  # Adds the input video's frame to the output video.
        print("Read a new frame successfully"),  # Used for debugging. Note: This is the less-preferred printing syntax, but works with Python 2.7
        count += 1.
    b.finish_video(output_video, output_video_location)


# ~~~~ Don't worry about this for now ~~~~
if __name__ == "__main__":
    main()
