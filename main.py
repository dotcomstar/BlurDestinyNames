#!/usr/bin/env python
# main.py
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

    image_file = Image.open(b.sample_image_file)
    image_file = b.convert_pil_to_cv2(image_file)
    image_file = b.convert_cv2_to_pil(image_file)

    b.find_characters(image_file, should_debug=True)

    exit()

    b.blur_video(b.default_video_input_file)

    print("Finished main()")

# ~~~~ Don't worry about this for now ~~~~
if __name__ == "__main__":
    main()
