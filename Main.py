import cv2
from PIL import Image
import streamlit as st
from streamlit_image_comparison import image_comparison

# set page config
st.set_page_config(page_title="Image-Comparison Example", layout="centered")

def main():
    st.title('Aksara Document Transliteration')

    home_tab, preprocessing_tab, od_tab = st.tabs(["Home", "Preprocessing", "Object Detection"])

    home_tab.subheader('Home')
    
    preprocessing_tab.subheader('Preprocessing')

    od_tab.subheader('Object Detection')
    # create container directly within the tab
    with od_tab.container():
        # render image-comparison
        image_comparison(
            img1="image1.jpg",
            img2="image2.jpg",
        )

if __name__ == "__main__":
    main()
