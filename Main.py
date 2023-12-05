import os
import io
import cv2
import time
import numpy as np
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt

from streamlit_image_comparison import image_comparison
from codes.preprocessing import image_preprocessing_process
from codes.object_detection import object_detection_process
from codes.object_detection import image_result_process
from codes.projection_profile import projection_profile_process
from codes.annotation import annotations_process
from codes.transliteration import dfa_process

# set page config
st.set_page_config(
    page_title="Aksara Document Object Detection", layout="centered")

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

            alert_message = "Document Transliteration has been successfully completed."
            show_alert(alert_message, 'success')

            # Set the flag to indicate that the image has been processed
            image_processed = True
        else:
            alert_message = "Please input a correct image."
            show_alert(alert_message, 'warning')

    if image_processed:
        home_tab, preprocessing_tab, od_tab = st.tabs(
            ["🏠 Home", "🛠️ Preprocessing", "👁️‍🗨 Object Detection"]
        )

        # HOME TAB
        with home_tab.container():
            # Use columns to create two columns
            col1, col2 = st.columns(2)

            # Display the uploaded image in the left column
            image = Image.open(uploaded_file)
            col1.image(image, caption="Original Image", use_column_width=True)

            # Dummy processing (replace this with your actual processing logic)
            # Use a loop or any method to concatenate the tuple elements into a single string
            result_text_combined = "\n".join(
                [" ".join(line) for line in result_text])

            col2.text_area("Transliteration Result",
                           value=result_text_combined, height=300)

        # PREPROCESSING TAB
        with preprocessing_tab.container():
            st.info(
                'Click the image to zoom in and see the preprocessing steps more clearly', icon="ℹ️")
            # Path to the folder containing preprocessed images
            preprocessed_folder = "./images/preprocessed/"
            # Get a list of all image files in the folder
            image_files = [f for f in os.listdir(
                preprocessed_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

            rows, cols = 1, 4
            fig, axes = plt.subplots(rows, cols, figsize=(15, 5))

            for j in range(cols):
                index = j
                if index < len(image_files):
                    image_path = os.path.join(
                        preprocessed_folder, image_files[index])

                    # Load image using PIL
                    img = Image.open(image_path)

                    image_name = image_files[index].split('_')[1].split('.')[0]
                    # Display image on the subplot
                    axes[j].imshow(img, cmap='gray')
                    axes[j].axis("off")  # Turn off axis labels
                    axes[j].set_title(f"Step {index+1}\n{image_name}")

            # Adjust the top spacing to prevent cutting off the top of the images
            plt.subplots_adjust(top=0.9)

            # Convert Matplotlib plot to PNG image
            image_stream = io.BytesIO()
            plt.savefig(image_stream, format='png')
            plt.close()

            # Display the image in Streamlit
            st.image(image_stream, use_column_width=True)

        # create container directly within the tab
        with od_tab.container():
            st.info(
                'Use the slider to compare the original and processed image', icon="ℹ️")
            
            with st.expander("Label Explanation"):
                    st.write("The labels used in the object detection represent different types of characters:")
                    st.write("- `u_'something'`: Aksara Utama")
                    st.write("- `p_'something'`: Aksara Pasangan")
                    st.write("- `s_'something'`: Aksara Sandhangan")

            processed_image = cv2.imread('./images/result/result_image.jpg')
            # render image-comparison
            image_comparison(
                img1=image,
                img2=processed_image,
                width=700,
                make_responsive=False,
            )


if __name__ == "__main__":
    main()
