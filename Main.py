import cv2
import time
import numpy as np
from PIL import Image
import streamlit as st

from streamlit_image_comparison import image_comparison
from codes.preprocessing import image_preprocessing_process
from codes.object_detection import object_detection_process
from codes.object_detection import image_result_process
from codes.projection_profile import projection_profile_process
from codes.annotation import annotations_process
from codes.transliteration import dfa_process

def transliteration_pipeline(image):
    global result_text

    thresholded_image, dilated_image = image_preprocessing_process(image)
    model_input = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2RGB)

    annotation_path = object_detection_process(model_input)
    image_result_process(thresholded_image, annotation_path)

    row_coordinates = projection_profile_process(dilated_image)

    document_annotations = annotations_process(
        annotation_path, image, row_coordinates)

    result_text = dfa_process(document_annotations)

    time.sleep(3)


def show_alert(alert_message, type='warning'):
    # Placeholder for the warning message
    alert_placeholder = st.empty()
    if type == 'warning':
        # Display the warning message
        alert_placeholder.warning(alert_message)
    elif type == 'success':
        alert_placeholder.success(alert_message)
    # Automatically fade away after 3 seconds (adjust as needed)
    time.sleep(3)
    alert_placeholder.empty()  # Clear the warning message


def main():
    st.title('Aksara Document Transliteration')

    # File uploader for image upload
    uploaded_file = st.file_uploader(
        "Upload Image", type=["jpg", "jpeg", "png"])

    # Button to process transliteration
    show_process = st.button("Process Transliteration")
    image_processed = False
    # Check if the button is clicked
    if show_process:
        # Display the uploaded image if available
        if uploaded_file is not None:
            image_array = np.array(
                bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            with st.spinner("Processing..."):
                transliteration_pipeline(image)

            alert_message = "Document Transliteration has been completed."
            show_alert(alert_message, 'success')

            # Set the flag to indicate that the image has been processed
            image_processed = True
        else:
            alert_message = "Please input a correct image."
            show_alert(alert_message, 'warning')

    if image_processed:
        # HOME TAB
        with st.container():
            st.info(
                'Scroll for more transliteration details if the content exceeds the text area', icon="ℹ️")
            # Use columns to create two columns
            col1, col2 = st.columns(2)

            # Display the uploaded image in the left column
            image = Image.open(uploaded_file)
            col1.image(image, caption="Original Image", use_column_width=True)

            # Use a loop or any method to concatenate the tuple elements into a single string
            result_text_combined = "\n".join(
                [" ".join(line) for line in result_text])

            col2.text_area("Transliteration Result",
                           value=result_text_combined, height=300)

if __name__ == "__main__":
    main()
