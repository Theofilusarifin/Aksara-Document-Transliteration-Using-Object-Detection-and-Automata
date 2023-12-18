import streamlit as st

def main():
    st.title('How To Use')

    st.markdown("""
        ## Aksara Document Transliteration App

        Welcome to the Aksara Document Transliteration App! This app allows you to upload an image containing Aksara characters and perform transliteration.

        **Follow these steps:**

        1. **Upload Image:**
            - Click on the "Upload Image" button to select an image file (supported formats: jpg, jpeg, png).
            - The image should have 3 (width) :4 (height) ratio for optimal processing.
                
        2. **Process Transliteration:**
            - Click on the "Process Transliteration" button to start the transliteration process.
        
        3. **View Results:**
            - After processing, the original image and the transliteration results will be displayed.
    """)

if __name__ == "__main__":
    main()
