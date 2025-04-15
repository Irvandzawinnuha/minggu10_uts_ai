import pandas as pd
import math

# Membaca data dari file Excel.
# Jika file tidak ada, maka menggunakan data dummy sebagai gantinya.
try:
    # Ubah "restoran.xlsx" ke nama file Excel sesuai kebutuhan.
    df = pd.read_excel("restoran.xlsx")
    print("Data berhasil dibaca dari Excel.")
except Exception as e:
    # Jika file tidak ditemukan atau terjadi error, buat data dummy.
    print("File Excel tidak ditemukan, menggunakan data dummy.")
    # Data dummy: daftar restoran dengan kualitas dan harga
    data_dummy = {
        "Nama": ["Restoran A", "Restoran B", "Restoran C", "Restoran D", "Restoran E",
                "Restoran F", "Restoran G", "Restoran H", "Restoran I", "Restoran J"],
        # Kualitas (misal skala 0-10, semakin tinggi semakin bagus kualitas)
        "Kualitas": [8, 7, 6, 9, 5, 4, 7.5, 8.5, 3, 6.5],
        # Harga (misal skala 0-10, semakin tinggi semakin mahal)
        "Harga": [5, 6.5, 8, 4, 7, 3.5, 5.5, 6, 2, 9]
    }
    df = pd.DataFrame(data_dummy)

# Tampilkan beberapa data untuk verifikasi (opsional)
print(df.head())

# Definisi fungsi keanggotaan trapezoid dan segitiga (berlaku umum untuk segala skala).
def trapezoid(x, a, b, c, d):
    """
    Fungsi keanggotaan trapezoid.
    Nilai keanggotaan = 0 untuk x < a atau x > d.
    Nilai keanggotaan = (x - a) / (b - a) untuk a <= x < b (meningkat).
    Nilai keanggotaan = 1 untuk b <= x <= c (bagian atas trapezoid).
    Nilai keanggotaan = (d - x) / (d - c) untuk c < x < d (menurun).
    """
    if x < a:
        return 0.0
    if x > d:
        return 0.0
    if x < b:
        # fase naik
        return (x - a) / (b - a) if (b - a) != 0 else 1.0
    if x <= c:
        # puncak trapezoid (nilai 1)
        return 1.0
    # x > c dan x < d (fase turun)
    return (d - x) / (d - c) if (d - c) != 0 else 1.0

def triangle(x, a, b, c):
    """
    Fungsi keanggotaan segitiga.
    Nilai keanggotaan = 0 untuk x <= a atau x >= c.
    Nilai keanggotaan = (x - a) / (b - a) untuk a < x < b (meningkat).
    Nilai keanggotaan = (c - x) / (c - b) untuk b <= x < c (menurun).
    """
    if x <= a or x >= c:
        return 0.0
    if x < b:
        # fase naik segitiga
        return (x - a) / (b - a) if (b - a) != 0 else 1.0
    # b <= x < c (fase turun)
    return (c - x) / (c - b) if (c - b) != 0 else 1.0

# Tentukan skala data (apakah menggunakan skala besar seperti data asli atau skala 0-10).
use_large_scale = False
try:
    # Jika data kualitas atau harga memiliki nilai maksimum besar, gunakan skala data asli.
    if df["Kualitas"].max() > 10 or df["Harga"].max() > 100:
        use_large_scale = True
except Exception as e:
    pass

# Definisikan fungsi keanggotaan untuk variabel kualitas, harga, dan output berdasarkan skala data.
if use_large_scale:
    # Skala data asli (contoh: Kualitas 1-100, Harga 25000-55000).
    # Kualitas (1-100): rendah, sedang, tinggi.
    def kualitas_rendah(x):
        return trapezoid(x, 0, 0, 30, 50)       # Nilai kualitas <=30 sepenuhnya RENDAH, turun hingga 0 di 50.
    def kualitas_sedang(x):
        return triangle(x, 30, 50, 70)          # Nilai kualitas di sekitar 50 dianggap SEDANG (puncak di 50).
    def kualitas_tinggi(x):
        return trapezoid(x, 50, 70, 100, 100)   # Nilai kualitas >=70 sepenuhnya TINGGI, naik dari 50 ke 1 pada 70.
    # Harga (contoh 25000-55000): murah, sedang, mahal.
    def harga_murah(x):
        return trapezoid(x, 25000, 25000, 35000, 45000)  # Harga <=35000 sepenuhnya MURAH, turun hingga 0 di 45000.
    def harga_sedang(x):
        return triangle(x, 35000, 45000, 55000)          # Harga ~45000 dianggap SEDANG (puncak di 45000).
    def harga_mahal(x):
        return trapezoid(x, 45000, 50000, 55000, 55000)  # Harga >=50000 sepenuhnya MAHAL, naik dari 45000 ke 1 pada 50000.
    # Output skor rekomendasi (0-100): rendah, sedang, tinggi.
    def skor_rendah(x):
        return trapezoid(x, 0, 0, 30, 50)
    def skor_sedang(x):
        return triangle(x, 30, 50, 70)
    def skor_tinggi(x):
        return trapezoid(x, 50, 70, 100, 100)
else:
    # Skala data 0-10 (data dummy atau data yang telah dinormalisasi ke 0-10).
    # Kualitas (0-10): rendah, sedang, tinggi.
    def kualitas_rendah(x):
        return trapezoid(x, 0, 0, 3, 5)
    def kualitas_sedang(x):
        return triangle(x, 3, 5, 7)
    def kualitas_tinggi(x):
        return trapezoid(x, 5, 7, 10, 10)
    # Harga (0-10): murah, sedang, mahal.
    def harga_murah(x):
        return trapezoid(x, 0, 0, 3, 5)
    def harga_sedang(x):
        return triangle(x, 3, 5, 7)
    def harga_mahal(x):
        return trapezoid(x, 5, 7, 10, 10)
    # Output skor rekomendasi (0-10): rendah, sedang, tinggi.
    def skor_rendah(x):
        return trapezoid(x, 0, 0, 3, 5)
    def skor_sedang(x):
        return triangle(x, 3, 5, 7)
    def skor_tinggi(x):
        return trapezoid(x, 5, 7, 10, 10)

# Daftar aturan fuzzy (IF-THEN rules).
# Setiap aturan berformat: (kualitas, harga, output)
# Menggunakan 9 aturan berdasarkan kombinasi 3 tingkat kualitas dan 3 tingkat harga.
rules = [
    ("rendah", "murah", "sedang"),   # Jika Kualitas RENDAH dan Harga MURAH maka skor SEDANG
    ("rendah", "sedang", "rendah"),  # Jika Kualitas RENDAH dan Harga SEDANG maka skor RENDAH
    ("rendah", "mahal", "rendah"),   # Jika Kualitas RENDAH dan Harga MAHAL maka skor RENDAH
    ("sedang", "murah", "tinggi"),   # Jika Kualitas SEDANG dan Harga MURAH maka skor TINGGI
    ("sedang", "sedang", "sedang"),  # Jika Kualitas SEDANG dan Harga SEDANG maka skor SEDANG
    ("sedang", "mahal", "rendah"),   # Jika Kualitas SEDANG dan Harga MAHAL maka skor RENDAH
    ("tinggi", "murah", "tinggi"),   # Jika Kualitas TINGGI dan Harga MURAH maka skor TINGGI
    ("tinggi", "sedang", "tinggi"),  # Jika Kualitas TINGGI dan Harga SEDANG maka skor TINGGI
    ("tinggi", "mahal", "sedang")    # Jika Kualitas TINGGI dan Harga MAHAL maka skor SEDANG
]

# Fungsi untuk mendapatkan nilai membership fuzzy untuk kualitas berdasarkan labelnya
def fuzzify_kualitas(x):
    return {
        "rendah": kualitas_rendah(x),
        "sedang": kualitas_sedang(x),
        "tinggi": kualitas_tinggi(x)
    }

# Fungsi untuk mendapatkan nilai membership fuzzy untuk harga berdasarkan labelnya
def fuzzify_harga(x):
    return {
        "murah": harga_murah(x),
        "sedang": harga_sedang(x),
        "mahal": harga_mahal(x)
    }

# Siapkan domain untuk variabel output berdasarkan skala (untuk defuzzifikasi).
if use_large_scale:
    domain_max = 100.0
    resolution = 1.0   # langkah 1.0 untuk skala 0-100
else:
    domain_max = 10.0
    resolution = 0.1   # langkah 0.1 untuk skala 0-10
x_values = [i * resolution for i in range(int(domain_max / resolution) + 1)]

# Proses inferensi fuzzy dan defuzzifikasi untuk setiap restoran.
hasil_scores = []  # list untuk menyimpan skor akhir tiap restoran
for idx, row in df.iterrows():
    nama = row["Nama"]
    kualitas_val = row["Kualitas"]
    harga_val = row["Harga"]
    # Fuzzifikasi: dapatkan derajat membership untuk nilai kualitas dan harga ini.
    kualitas_membership = fuzzify_kualitas(kualitas_val)
    harga_membership = fuzzify_harga(harga_val)
    # Inisialisasi list untuk agregasi membership output (semua nilai awal 0).
    aggregated_membership = [0.0] * len(x_values)
    # Terapkan setiap aturan fuzzy
    for (kualitas_label, harga_label, output_label) in rules:
        # Derajat keanggotaan (firing strength) aturan = MIN(membership kualitas_label, membership harga_label)
        alpha = min(kualitas_membership[kualitas_label], harga_membership[harga_label])
        if alpha <= 0:
            # Jika derajat 0, aturan ini tidak berkontribusi
            continue
        # Tentukan fungsi keanggotaan output mana yang dipakai sesuai output_label
        if output_label == "rendah":
            output_membership_func = skor_rendah
        elif output_label == "sedang":
            output_membership_func = skor_sedang
        elif output_label == "tinggi":
            output_membership_func = skor_tinggi
        # Lakukan implikasi (Mamdani: potong membership output dengan nilai alpha)
        for j, x in enumerate(x_values):
            # Nilai membership output sebelum diimplikasikan
            mu_out = output_membership_func(x)
            # Membership setelah implikasi (dipotong oleh alpha)
            if mu_out > alpha:
                mu_out = alpha
            # Gabungkan dengan agregasi OR (max) ke himpunan output agregat
            if mu_out > aggregated_membership[j]:
                aggregated_membership[j] = mu_out
    # Defuzzifikasi dengan metode centroid (center of gravity)
    # centroid = (sum x * mu(x)) / (sum mu(x))
    numerator = 0.0
    denominator = 0.0
    for j, x in enumerate(x_values):
        mu = aggregated_membership[j]
        numerator += x * mu
        denominator += mu
    if denominator == 0:
        crisp_score = 0
    else:
        crisp_score = numerator / denominator
    # Simpan hasil skor crisp untuk restoran ini
    hasil_scores.append({"Nama": nama, "Kualitas": kualitas_val, "Harga": harga_val, "Skor": crisp_score})

# Buat DataFrame dari hasil skor
df_hasil = pd.DataFrame(hasil_scores)
# Urutkan berdasarkan skor descending (skor tertinggi ke terendah)
df_hasil = df_hasil.sort_values(by="Skor", ascending=False)
# Ambil 5 restoran terbaik
top5 = df_hasil.head(5).copy()
# Tambahkan kolom peringkat (1-5)
top5.insert(0, "Peringkat", range(1, len(top5) + 1))

# Simpan top 5 ke file Excel "peringkat.xlsx"
top5.to_excel("peringkat.xlsx", index=False)
print("5 Restoran terbaik telah disimpan ke peringkat.xlsx")
