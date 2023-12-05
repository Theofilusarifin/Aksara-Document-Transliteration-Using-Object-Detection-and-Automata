import cv2
import numpy as np

def image_preprocessing_process(image):
    # convert to grayscale
    grayscaled_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur
    blurred_image = cv2.GaussianBlur(grayscaled_image, (0, 0), sigmaX=33, sigmaY=33)

    # divide
    divided_image = cv2.divide(grayscaled_image, blurred_image, scale=255)

    # otsu threshold
    thresholded_image = cv2.threshold(divided_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morphological_closing_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_CLOSE, kernel)

    # _, threshold_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    binary_image = cv2.bitwise_not(morphological_closing_image)

    # Define the kernel for dilation
    kernel = np.ones((7, 7), np.uint8)
    # Perform dilation
    dilated_image = cv2.dilate(binary_image, kernel, iterations=1)

    return grayscaled_image, blurred_image, divided_image, thresholded_image, morphological_closing_image, binary_image, dilated_image
