import cv2
import numpy as np

def image_preprocessing_process(image):
    # cv2.imwrite('./images/preprocessed/0_original.jpg', image)

    # convert to grayscale
    grayscaled_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('./images/preprocessed/1_grayscalled.jpg', grayscaled_image)

    # blur
    blurred_image = cv2.GaussianBlur(grayscaled_image, (0, 0), sigmaX=33, sigmaY=33)
    cv2.imwrite('./images/preprocessed/2_blurred.jpg', blurred_image)

    # divide
    divided_image = cv2.divide(grayscaled_image, blurred_image, scale=255)
    cv2.imwrite('./images/preprocessed/3_divided.jpg', divided_image)

    # otsu threshold
    thresholded_image = cv2.threshold(divided_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    cv2.imwrite('./images/preprocessed/4_thresholded.jpg', thresholded_image)

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morphological_closing_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_CLOSE, kernel)
    # cv2.imwrite('./images/preprocessed/5_morphology.jpg', morphological_closing_image)

    binary_image = cv2.bitwise_not(morphological_closing_image)
    # cv2.imwrite('./images/preprocessed/6_binary.jpg', binary_image)

    # Define the kernel for dilation
    kernel = np.ones((7, 7), np.uint8)
    # Perform dilation
    dilated_image = cv2.dilate(binary_image, kernel, iterations=1)
    # cv2.imwrite('./images/preprocessed/7_dilated.jpg', binary_image)

    return thresholded_image, dilated_image
