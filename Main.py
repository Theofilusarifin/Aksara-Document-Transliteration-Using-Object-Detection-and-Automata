import cv2
from PIL import Image
import streamlit as st
from streamlit_image_comparison import image_comparison

from codes.preprocessing import image_preprocessing_process
from codes.object_detection import object_detection_process

# set page config
st.set_page_config(page_title="Aksara Document Object Detection", layout="centered")


def main():
    st.title('Aksara Document Transliteration')

    # File uploader for image upload
    uploaded_file = st.file_uploader(
        "Upload Image", type=["jpg", "jpeg", "png"])

    # Button to toggle image comparison visibility
    show_image_comparison_button = st.button("Process Transliteration")

    # Boolean flag to control image comparison visibility
    show_image_comparison = False

    # Check if the button is clicked
    if show_image_comparison_button:
        # Display the uploaded image if available
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            grayscaled_image, blurred_image, divided_image, thresholded_image, morphological_closing_image, binary_image, dilated_image = image_preprocessing_process(image)
            show_image_comparison = not show_image_comparison

    if show_image_comparison:
        home_tab, preprocessing_tab, od_tab = st.tabs(
            ["Home", "Preprocessing", "Object Detection"])

        home_tab.subheader('Home')

        preprocessing_tab.subheader('Preprocessing')

        od_tab.subheader('Object Detection')
        # create container directly within the tab
        with od_tab.container():
            # render image-comparison
            image_comparison(
                img1="image1.jpg",
                img2="image2.jpg",
                label1="Input Image",
                label2="Object Detection Result"
            )


if __name__ == "__main__":
    main()
