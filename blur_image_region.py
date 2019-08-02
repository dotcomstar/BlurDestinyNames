'''
This module pixelates a file.

Link to pixelation using PIL:
https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
'''

from PIL import Image
import cv2

print("Starting image blur")

image_file = "temp_image_frames/frame216.jpg"

# Open image file and save to upper folder for reference
image = Image.open(image_file)
reference_image_file = "current_working_image_before_blur.jpg"
image.save(reference_image_file)

# Resize smoothly down to 32x32 pixels
small_image = image.resize((32,32),resample=Image.BILINEAR)  # For a smoother blur, increase the size of the scaled image.

# Scale back up using NEAREST to original size
blurred_image = small_image.resize(image.size,Image.BICUBIC)

# Save
blurred_image.save('blurred_frame.png')

# Crop out a smaller section of the image
crop_rectangle = (1368, 250, 1843, 922)  # Currently, takes the hard-coded name values from clan roster page.
cropped_image = blurred_image.crop(crop_rectangle)
cropped_image.save('blurred_frame_cropped.png')

# Re-insert the smaller blurred section of the image onto the original.
image.paste(cropped_image, (crop_rectangle), None)
image.save(reference_image_file)

print("Finished image blur")
