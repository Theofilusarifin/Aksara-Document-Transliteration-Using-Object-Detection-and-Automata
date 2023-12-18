import cv2
import numpy as np

class ImagePreprocessingError(Exception):
    pass

def image_preprocessing_process(image):
    try:
        # convert to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    except Exception as e:
        # Handle error in converting to grayscale
        raise ImagePreprocessingError(f"Grayscale Conversion Error: {e}")

    try:
        # otsu threshold
        thresholded_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    except Exception as e:
        # Handle error in Otsu thresholding
        raise ImagePreprocessingError(f"Otsu Threshold Error: {e}")

    try:
        # Bitwise not
        binary_image = cv2.bitwise_not(thresholded_image)

    except Exception as e:
        # Handle error in bitwise NOT operation
        raise ImagePreprocessingError(f"Bitwise NOT Error: {e}")

    try:
        # Define the kernel for dilation
        kernel = np.ones((7, 7), np.uint8)
        # Perform dilation
        dilated_image = cv2.dilate(binary_image, kernel, iterations=1)

    except Exception as e:
        # Handle error in dilation
        raise ImagePreprocessingError(f"Dilation Error: {e}")

    try:
        # Find contours and filter out small areas
        contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_area_threshold = 50  # Adjust the threshold as needed

        # Contour Filtering
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area_threshold:
                cv2.drawContours(dilated_image, [contour], 0, 0, -1)

    except Exception as e:
        # Handle error in finding contours or contour filtering
        raise ImagePreprocessingError(f"Contour Processing Error: {e}")

    return thresholded_image, dilated_image