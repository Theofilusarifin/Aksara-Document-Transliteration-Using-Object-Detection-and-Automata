import numpy as np


def projection_profile_process(input_image):
    try:
        # CONSTANT
        TRESHOLD = 0
        ZERO_ITTERATION = 10

        # Variable pembantu
        start_putih = []
        end_putih = []
        iteration = 0

        # Melakukan penjumlahan pada gambar secara horizontal ke samping
        h_projection = np.sum(input_image, axis=1)

    except Exception as e:
        # Handle error in horizontal projection
        print(f"Projection Profile Process Error (Horizontal Projection): {e}")
        return None

    try:
        # Melakukan iterasi pada tiap titik horizontal
        for x, value in enumerate(h_projection):
            # Jumlah pixel value lebih besar dari 0 (Terdapat garis)
            if value > TRESHOLD:
                # Reset iteration
                iteration = 0
                # Merupaakan segmen awal
                if len(start_putih) == len(end_putih):
                    # Tambahkan titik koordinat sebagai segmen awal
                    start_putih.append(x)
            # Merupakan bagian kosong tanpa ada garis
            else:
                # Menambahkan iterasi
                iteration += 1
                # Apabila iterasi sudah lebih dari 15 satuan, menandakan
                if iteration >= ZERO_ITTERATION:
                    # Apabila segmen sebelumnya belum diakhiri
                    if len(start_putih) == (len(end_putih) + 1):
                        # Reset iteration
                        iteration = 0
                        # Tutup segmen
                        end_putih.append(x)

        # Iterasi terakhir
        if len(start_putih) == len(end_putih) + 1:
            # Akhiri segmen apabila belum tertutup
            if len(start_putih) == (len(end_putih) + 1):
                end_putih.append(len(h_projection))

    except Exception as e:
        # Handle error in iteration or segment closing
        print(f"Projection Profile Process Error (Iteration or Segment Closing): {e}")
        return None

    # Gabungkan koordinat awal dan akhir tiap segmen untuk return
    row_coordinates = list(zip(start_putih, end_putih))

    return row_coordinates