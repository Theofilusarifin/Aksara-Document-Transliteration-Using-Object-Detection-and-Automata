import pandas as pd
import json

class AnnotationProcessError(Exception):
    pass

def annotations_process(annotation_path, image, row_coordinates):
    try:
        if annotation_path is None:
            raise AnnotationProcessError("Annotation file path is None.")

        # Membaca label
        with open('./label/labels.json', 'r') as file:
            labels = json.load(file)

        labels = {int(key): value for key, value in labels.items()}

        # Assuming annotations are in a text file with one line per annotation
        with open(annotation_path, 'r') as file:
            annotations = [list(map(float, line.strip().split())) for line in file]
    except FileNotFoundError:
        # Handle file not found error
        raise AnnotationProcessError(f"File not found: {annotation_path}")
    except json.JSONDecodeError:
        # Handle JSON decoding error
        raise AnnotationProcessError("Unable to decode JSON from labels file.")
    except AnnotationProcessError as e:
        # Reraise custom exception
        raise e

    # List untuk menyimpan hasil anotation yang sudah di proses
    document_annotations = []

    try:
        # Buat sebuah Pandas DataFrame
        columns = ["Class", "X Center", "Y Center", "Width", "Height"]
        df = pd.DataFrame(annotations, columns=columns)

        # Lakukan konversi tipe data
        df[["Class", "X Center", "Y Center", "Width", "Height"]] = df[[
            "Class", "X Center", "Y Center", "Width", "Height"]].apply(pd.to_numeric)

        # Mapping class labels
        df["Class"] = df["Class"].map(labels)

        # Mengambil tinggi dan lebar image untuk kalkulasi koordinat
        image_height, image_width, _ = image.shape

        # Kalkulasi top-left koordinat bounding box
        df['Y'] = (df['Y Center'] - 0.5 * df['Height']) * image_height
        df['X'] = (df['X Center'] - 0.5 * df['Width']) * image_width

        # Drop kolom pada dataframe yang sudah tidak dibutuhkan
        df.drop(columns=['X Center', 'Y Center', 'Width', 'Height'], axis=1, inplace=True)

        # Iterasi batasan untuk tiap segmen
        for y_start, y_end in row_coordinates:
            # Filter dataframe annotasi untuk mengumpulkan hasil anotasi pada baris segmen yang dipilih
            selected_df = df[(df['Y'] >= y_start) & (df['Y'] <= y_end)]

            y_middle = (y_start + y_end)/2
             # Check condition and update the DataFrame
            mask = (selected_df['Y'] > y_middle) & (selected_df['Class'].isin(['utama_ga', 'utama_ya', 'utama_nya', 'utama_ra']))
            selected_df.loc[mask, 'Class'] = selected_df.loc[mask, 'Class'].str.replace('utama_', 'pasangan_')

            # Urutkan hasil anotasi pada satu baris berdasarkan X untuk pembacaan dari kiri ke kanan
            selected_df = selected_df.sort_values(by=["X"])
            # Ambil label kelas pada satu baris
            class_list = selected_df['Class'].tolist()
            # Masukan hasil ke list yang akan di return
            document_annotations.append(class_list)

    except pd.errors.EmptyDataError:
        # Handle empty annotation file error
        raise AnnotationProcessError("Annotation file is empty.")
    except pd.errors.ParserError:
        # Handle parsing error for annotation file
        raise AnnotationProcessError("Unable to parse data from the annotation file.")

    return document_annotations
