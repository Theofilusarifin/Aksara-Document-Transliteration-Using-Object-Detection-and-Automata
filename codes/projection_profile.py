import numpy as np

def projection_profile_process(target_image, input_image):
    # CONSTANT
    TRESHOLD = 0
    ZERO_ITTERATION = 10

    # Variable pembantu
    start_putih = []
    end_putih = []
    iteration = 0

    # List untuk menyimpan hasil
    h_segmentation = []

    # Melakukan penjumlahan pada gambar secara horizontal ke samping
    h_projection = np.sum(input_image, axis=1)
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

    # Gabungkan koordinat awal dan akhir tiap segmen untuk return
    coordinates = list(zip(start_putih, end_putih))

    # Iterasi tiap koordinat awal dan akhir untuk melakukan pemotongan segmen pada gambar target
    for start, end in coordinates:
        t = target_image[start:end, :]
        h_segmentation.append(t)

    return h_segmentation, coordinates
