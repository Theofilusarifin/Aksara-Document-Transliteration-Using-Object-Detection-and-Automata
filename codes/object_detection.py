import os
import cv2
import shutil
from ultralytics import YOLO

def object_detection_process(image):
    try:
        TEST_LABEL_PATH = './images/result/'
        MODEL_PATH = './model/model.pt'
        RESULT_IMAGE_NAME = 'result'

        model = YOLO(MODEL_PATH)
        results = model.predict(source=image, save_txt=True, project=TEST_LABEL_PATH, name=RESULT_IMAGE_NAME)

    except Exception as e:
        # Handle YOLO model prediction error
        print(f"Object Detection Process Error: {e}")
        return None

    try:
        label_folder = os.path.join(TEST_LABEL_PATH, RESULT_IMAGE_NAME+'/labels/')
        file_to_copy = os.listdir(label_folder)[0]

        # Create the full paths for source and destination files
        source_file_path = os.path.join(label_folder, file_to_copy)
        destination_file_path = os.path.join(TEST_LABEL_PATH, 'result_label.txt') 

        shutil.copy(source_file_path, destination_file_path)

    except FileNotFoundError:
        # Handle file not found error for label file
        print("Object Detection Process Error: Label file not found.")
        return None

    except IndexError:
        # Handle index error when listing files in label_folder
        print("Object Detection Process Error: No files found in label folder.")
        return None

    except Exception as e:
        # Handle other unexpected errors
        print(f"Object Detection Process Error: {e}")
        return None

    try:
        shutil.rmtree(os.path.join(TEST_LABEL_PATH, RESULT_IMAGE_NAME))

    except FileNotFoundError:
        # Handle file not found error when trying to remove directory
        print("Object Detection Process Error: Directory not found for removal.")
        return None

    return destination_file_path

def image_result_process(original_image, annotation_path):
    try:
        # Define the labels
        labels = {
        0: 'p_ba',
        1: 'p_ca',
        2: 'p_da',
        3: 'p_dha',
        4: 'p_ha',
        5: 'p_ja',
        6: 'p_ka',
        7: 'p_la',
        8: 'p_ma',
        9: 'p_na',
        10: 'p_nya',
        11: 'p_pa',
        12: 'p_sa',
        13: 'p_ta',
        14: 'p_tha',
        15: 'p_wa',
        16: 's_cecak',
        17: 's_layar',
        18: 's_lingsa',
        19: 's_lungsa',
        20: 's_pangkon',
        21: 's_pepet',
        22: 's_suku',
        23: 's_taling',
        24: 's_tarung',
        25: 's_wignyan',
        26: 's_wulu',
        27: 'u_ba',
        28: 'u_ca',
        29: 'u_da',
        30: 'u_dha',
        31: 'u_ga',
        32: 'u_ha',
        33: 'u_ja',
        34: 'u_ka',
        35: 'u_la',
        36: 'u_ma',
        37: 'u_na',
        38: 'u_nga',
        39: 'u_nya',
        40: 'u_pa',
        41: 'u_ra',
        42: 'u_sa',
        43: 'u_ta',
        44: 'u_tha',
        45: 'u_wa',
        46: 'u_ya'
    }
    except Exception as e:
        # Handle error in defining labels
        print(f"Image Result Process Error (Defining Labels): {e}")
        return None

    try:
        # Annotations are in a text file with one line per annotation
        with open(annotation_path, 'r') as file:
            annotations = [list(map(float, line.strip().split())) for line in file]

    except FileNotFoundError:
        # Handle annotation file not found error
        print("Image Result Process Error (Annotation File Not Found): Annotation file not found.")
        return None

    except Exception as e:
        # Handle other unexpected errors
        print(f"Image Result Process Error (Reading Annotation File): {e}")
        return None

    # Convert the image to BGR if it's in grayscale
    if len(original_image.shape) == 2:
        original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)

    # Overlay annotations on the image
    try:
        for annotation in annotations:
            class_id, x_center, y_center, width, height = map(float, annotation)

            # Convert YOLO format to (x_min, y_min, x_max, y_max) format
            x_min = int((x_center - width / 2) * original_image.shape[1])
            y_min = int((y_center - height / 2) * original_image.shape[0])
            x_max = int((x_center + width / 2) * original_image.shape[1])
            y_max = int((y_center + height / 2) * original_image.shape[0])

            cv2.rectangle(original_image, (x_min, y_min), (x_max, y_max),
                          (0, 255, 0), 2)  # Draw a green rectangle

            label = f"{labels[int(class_id)]}"
            cv2.putText(original_image, label, (x_min, y_min - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

    except Exception as e:
        # Handle error in overlaying annotations
        print(f"Image Result Process Error (Overlaying Annotations): {e}")
        return None

    # Save the result image
    try:
        cv2.imwrite('./images/result/result_image.jpg', original_image)
    except Exception as e:
        # Handle error in saving the result image
        print(f"Image Result Process Error (Saving Result Image): {e}")
        return None
    
    return original_image
