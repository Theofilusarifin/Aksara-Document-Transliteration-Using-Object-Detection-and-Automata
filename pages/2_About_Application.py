import streamlit as st


def main():
    # Sidebar with clickable buttons
    st.title('About Application')

    st.markdown("""
                ## Data Gathering and Annotation

                The first step involves the creation of a labeled dataset by annotating images on Roboflow. Each image is carefully annotated to identify and label individual Aksara characters, providing a robust dataset for training the YOLOv8 model.

                ## Model Training with YOLOv8

                The YOLOv8 model is utilized for its efficiency in object detection tasks. The annotated dataset is used to train the model, enabling it to recognize and locate Aksara characters within images. The training process involves multiple epochs, refining the model's ability to accurately detect characters.

                ## Image Detection and Preprocessing

                With the trained YOLOv8 model, new images are processed to detect Aksara characters. The detected characters undergo preprocessing steps to enhance image quality, including grayscale conversion, blurring, thresholding, and morphological operations.

                ## Horizontal Projection Profiling

                Horizontal Projection Profiling is employed to segment the image into distinct horizontal regions, allowing for the isolation of individual lines of Aksara characters. This step is crucial for accurate character recognition and subsequent transliteration.

                ## Object Detection Results Evaluation

                The results of object detection are evaluated through visualizations, including the display of a confusion matrix. This assessment provides insights into the model's performance, helping to ensure accurate character detection.

                ## Transliteration with DFA

                The labeled regions from horizontal projection profiling are processed by a Deterministic Finite Automaton (DFA). The DFA applies predefined rules for transliterating Aksara characters into their linguistic representations, resulting in accurate and consistent transliteration.

                ## Visualization of Results

                The application provides visualizations of the model predictions, including the display of annotated images, horizontal projection profiles, and the final transliteration results. These visualizations aid in understanding the processing pipeline and validating the accuracy of the transliteration.

                ## Conclusion

                The Aksara Document Transliteration application integrates advanced techniques in object detection and linguistics, offering a comprehensive solution for automatically transcribing Aksara characters from images or documents. It serves as a valuable tool for researchers, linguists, or anyone interested in the study of Aksara characters.

                [Developer LinkedIn](https://www.linkedin.com/in/theofilusarifin/)

                """)


if __name__ == "__main__":
    main()
