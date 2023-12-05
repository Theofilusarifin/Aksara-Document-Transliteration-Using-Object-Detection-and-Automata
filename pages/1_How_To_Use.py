import streamlit as st

def main():
    # Sidebar with clickable buttons
    st.title('How To Use')

    # Explanation about your app
    st.markdown("""
        ## Aksara Document Transliteration App

        Welcome to the Aksara Document Transliteration App! This app allows you to upload an image containing Aksara characters and perform transliteration.

        **Follow these steps:**

        1. **Upload Image:**
            - Click on the "Upload Image" button to select an image file (supported formats: jpg, jpeg, png).
        
        2. **Process Transliteration:**
            - Click on the "Process Transliteration" button to start the transliteration process.
        
        3. **View Results:**
            - After processing, the original image and the transliteration results will be displayed.
            - You can click on the image to zoom in and see the preprocessing steps more clearly.
        
        4. **Explore Tabs:**
            - Navigate through the tabs for more details:
                - **Home:** Displays the original image and transliteration results.
                - **Preprocessing:** Shows the preprocessing steps with a visual representation.
                - **Object Detection:** Allows you to compare the original and processed images.
    """)

if __name__ == "__main__":
    main()
