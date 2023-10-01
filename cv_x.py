import cv2
import numpy as np
import os

def validate_file(file_path):
    """Check if file exists"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    return True

def load_image(file_path):
    """Load an image from the specified file"""
    validate_file(file_path)
    image = cv2.imread(file_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)  # convert to BGRA

def save_image(image, output_path):
    """Save an image to the specified file"""
    cv2.imwrite(output_path, image)

def filter_orange(image):
    """Filter an image to keep only the orange parts and make other parts transparent"""
    # Convert the image from BGRA to BGR and then to HSV color space.
    hsv = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2HSV)

    # Define the range of orange color in HSV
    lower_orange = np.array([10, 150, 150])  # adjust these values
    upper_orange = np.array([30, 255, 255])  # adjust these values

    # Create a mask for orange parts
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Create a 4-channel image with transparent background
    transparent_image = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

    # Replace orange parts with the original color and alpha channel to 255
    transparent_image[mask > 0] = image[mask > 0]
    transparent_image[..., 3] = 0  # initially set all alpha to 0 (transparent)
    transparent_image[mask > 0, 3] = 255  # set alpha to 255 (opaque) for orange parts

    return transparent_image

if __name__ == "__main__":
    input_path = 'wms-2.png'
    output_path = 'wms-2_output_image.png'  # Save as PNG to keep the transparency
    
    original_image = load_image(input_path)
    orange_filtered_image = filter_orange(original_image)
    save_image(orange_filtered_image, output_path)
