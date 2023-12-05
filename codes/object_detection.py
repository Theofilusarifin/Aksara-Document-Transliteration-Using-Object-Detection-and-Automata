import os
import cv2
import shutil

def prediction(model, image_path):
    TEST_LABEL_PATH = ''

    input_image = cv2.imread(image_path)
    input_image_name = os.path.splitext(os.path.basename(image_path))[0]

    results = model.predict(source=input_image, save_txt=True, project=TEST_LABEL_PATH, name=input_image_name)

    label_file = os.path.join(TEST_LABEL_PATH, input_image_name+'/labels/' + input_image_name + '.txt')
    shutil.copy(label_file, TEST_LABEL_PATH)

    folder_to_remove = os.path.join(TEST_LABEL_PATH, input_image_name)
    shutil.rmtree(folder_to_remove)