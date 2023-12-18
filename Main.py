import cv2
import time
import numpy as np
from PIL import Image
import streamlit as st

from codes.preprocessing import image_preprocessing_process, ImagePreprocessingError
from codes.object_detection import object_detection_process, image_result_process, ObjectDetectionProcessError, ImageResultProcessError
from codes.projection_profile import projection_profile_process, ProjectionProfileError
from codes.annotation import annotations_process, AnnotationProcessError
from codes.transliteration import transliteration_fsa, TransliterationFSAError, FSAProcessError

def check_image_aspect_ratio(image):
    # Check if the image maintains a 3:4 aspect ratio
    expected_aspect_ratio = 3 / 4
    height, width, _ = image.shape
    # Calculate the actual aspect ratio
    actual_aspect_ratio = width / height
    # Define a tolerance for aspect ratio comparison
    aspect_ratio_tolerance = 0.1
    # Check if the aspect ratio is within the tolerance of the expected aspect ratio
    if not (abs(actual_aspect_ratio - expected_aspect_ratio) <= aspect_ratio_tolerance):
        raise ValueError(f"Image should maintain a 3:4 aspect ratio.")

def transliteration_pipeline(image):
    try:
         # Check image size before processing
        check_image_aspect_ratio(image)
        thresholded_image, dilated_image = image_preprocessing_process(image)
        model_input = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2RGB)
    except ImagePreprocessingError as e:
        st.error(f"Image preprocessing error: {e}")
        return
    try:
        annotation_path = object_detection_process(model_input)
        image_result_process(thresholded_image, annotation_path)
    except (ObjectDetectionProcessError, ImageResultProcessError) as e:
        st.error(f"Object detection error: {e}")
        return
    try:
        row_coordinates = projection_profile_process(dilated_image)
    except ProjectionProfileError as e:
        st.error(f"Projection profile error: {e}")
        return
    try:
        document_annotations = annotations_process(
            annotation_path, image, row_coordinates)
    except AnnotationProcessError as e:
        st.error(f"Annotation process error: {e}")
        return
    try:
        result_text = transliteration_fsa(document_annotations)
    except (TransliterationFSAError, FSAProcessError) as e:
        st.error(f"Transliteration FSA error: {e}")
        return
    time.sleep(3)
    return result_text


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
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    # Button to process transliteration
    show_process = st.button("Process Transliteration")
    image_processed = False

    try:
        # Check if the button is clicked
        if show_process:
            # Display the uploaded image if available
            if uploaded_file is not None:
                image_array = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

                with st.spinner("Processing..."):
                    result_text = transliteration_pipeline(image)
                
                if (result_text != None):
                    alert_message = "Document Transliteration has been completed."
                    show_alert(alert_message, 'success')

                    # Set the flag to indicate that the image has been processed
                    image_processed = True
            else:
                raise ValueError("Please upload a correct image.")
    except Exception as e:
        st.error(f"Error during processing: {e}")
        return

    if image_processed:
        with st.container():
            st.info(
                'Scroll for more transliteration details if the content exceeds the text area', icon="ℹ️")
            # Use columns to create two columns
            col1, col2 = st.columns(2)

            # Display the uploaded image in the left column
            image = Image.open(uploaded_file)
            col1.image(image, caption="Original Image", use_column_width=True)

            # Use a loop or any method to concatenate the tuple elements into a single string
            result_text_combined = "\n".join(["-".join(line) for line in result_text])

            col2.text_area("Transliteration Result", value=result_text_combined, height=300)

if __name__ == "__main__":
    main()
