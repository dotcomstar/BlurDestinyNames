'''
This module pixelates a file.

Link to pixelation using PIL:
https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
'''

from PIL import Image

sample_image_file = "temp_image_frames/frame216.jpg"
default_location_to_save_reference_image = "current_working_image_before_blur.jpg"
clan_roster_rectangle = (1368, 250, 1843, 922)  # Currently, takes the hard-coded name values from clan roster page.

# This function takes in an image and a 2x2 or 4x4 tuple specifying where on the image to blur.
# The function returns a new image with the specified region blurred with a bicubic resample.
def blur_single_frame(image_file, region_to_blur):
    print("Starting blur_single_frame()")
    image = Image.open(image_file)  # Opens image file.
    small_image = image.resize((32,32),resample=Image.BILINEAR)  # Resizes down to 32x32 pixels.
        # For a smoother blur, increase the size of the scaled image.
    blurred_image = small_image.resize(image.size,Image.BICUBIC)  # Scales image back up using BICUBIC resample filter, thereby blurring it..
    cropped_image = blurred_image.crop(region_to_blur)  # Crops out a smaller section of the image.
    image.paste(cropped_image, (region_to_blur), None)  # Re-insert the smaller blurred section of the image onto the original.
    return image  # Returns the new blurred iamge.
    print("Finished blur_single_frame()")


def debug_blur_single_frame(image_file, region_to_blur, location_to_save_reference_image=default_location_to_save_reference_image):
    print("Starting debug_blur_single_frame()")

    # Open image file and save to upper folder for reference
    image = Image.open(image_file)
    image.save(location_to_save_reference_image)

    # Resize smoothly down to 32x32 pixels
    small_image = image.resize((32,32),resample=Image.BILINEAR)  # For a smoother blur, increase the size of the scaled image.

    # Scale back up using BICUBIC resample filter
    blurred_image = small_image.resize(image.size,Image.BICUBIC)

    # Save the blurred frame
    blurred_image.save('blurred_frame.png')

    # Crop out a smaller section of the image
    cropped_image = blurred_image.crop(region_to_blur)
    cropped_image.save('blurred_frame_cropped.png')

    # Re-insert the smaller blurred section of the image onto the original.
    image.paste(cropped_image, (region_to_blur), None)
    image.save(location_to_save_reference_image)

    print("Finished debug_blur_single_frame()")
