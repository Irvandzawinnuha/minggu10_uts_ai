import pandas as pd
import math

# Membaca data dari file Excel.
try:
    df = pd.read_excel("restoran.xlsx")
    # Bersihkan dan sesuaikan nama kolom
    df.columns = df.columns.str.strip().str.capitalize()
    df = df.rename(columns={
        "Id pelanggan": "Nama",
        "Pelayanan": "Kualitas",
        "Harga": "Harga"
    })
    print("Data berhasil dibaca dari Excel.")
except Exception as e:
    print("File Excel tidak ditemukan, menggunakan data dummy.")
    data_dummy = {
        "id Pelanggan": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Pelayanan": [8, 7, 6, 9, 5, 4, 7.5, 8.5, 3, 6.5],
        "harga": [5, 6.5, 8, 4, 7, 3.5, 5.5, 6, 2, 9]
    }
    df = pd.DataFrame(data_dummy)

print(df.head())

def trapezoid(x, a, b, c, d):
    if x < a or x > d: return 0.0
    elif x < b: return (x - a) / (b - a) if b != a else 1.0
    elif x <= c: return 1.0
    else: return (d - x) / (d - c) if d != c else 1.0

def triangle(x, a, b, c):
    if x <= a or x >= c: return 0.0
    elif x < b: return (x - a) / (b - a) if b != a else 1.0
    else: return (c - x) / (c - b) if c != b else 1.0

use_large_scale = df["Kualitas"].max() > 10 or df["Harga"].max() > 100

if use_large_scale:
    def kualitas_rendah(x): return trapezoid(x, 0, 0, 40, 55)
    def kualitas_sedang(x): return triangle(x, 45, 60, 75)
    def kualitas_tinggi(x): return trapezoid(x, 70, 80, 100, 100)

    def harga_murah(x): return trapezoid(x, 25000, 25000, 30000, 40000)
    def harga_sedang(x): return triangle(x, 35000, 42500, 50000)
    def harga_mahal(x): return trapezoid(x, 45000, 50000, 55000, 55000)

    def skor_rendah(x): return trapezoid(x, 0, 0, 30, 50)
    def skor_sedang(x): return triangle(x, 30, 50, 70)
    def skor_tinggi(x): return trapezoid(x, 50, 70, 100, 100)

else:
    def kualitas_rendah(x): return trapezoid(x, 0, 0, 3, 5)
    def kualitas_sedang(x): return triangle(x, 3, 5, 7)
    def kualitas_tinggi(x): return trapezoid(x, 5, 7, 10, 10)
    def harga_murah(x): return trapezoid(x, 0, 0, 3, 5)
    def harga_sedang(x): return triangle(x, 3, 5, 7)
    def harga_mahal(x): return trapezoid(x, 5, 7, 10, 10)
    def skor_rendah(x): return trapezoid(x, 0, 0, 3, 5)
    def skor_sedang(x): return triangle(x, 3, 5, 7)
    def skor_tinggi(x): return trapezoid(x, 5, 7, 10, 10)

rules = [
    ("rendah", "murah", "sedang"),
    ("rendah", "sedang", "rendah"),
    ("rendah", "mahal", "rendah"),
    ("sedang", "murah", "tinggi"),
    ("sedang", "sedang", "sedang"),
    ("sedang", "mahal", "sedang"),
    ("tinggi", "murah", "tinggi"),
    ("tinggi", "sedang", "tinggi"),
    ("tinggi", "mahal", "sedang"),
    # Aturan tambahan untuk variasi output
    ("rendah", "murah", "tinggi"),
    ("sedang", "mahal", "rendah"),
    ("tinggi", "mahal", "rendah")
]


def fuzzify_kualitas(x):
    return {
        "rendah": kualitas_rendah(x),
        "sedang": kualitas_sedang(x),
        "tinggi": kualitas_tinggi(x)
    }

def fuzzify_harga(x):
    return {
        "murah": harga_murah(x),
        "sedang": harga_sedang(x),
        "mahal": harga_mahal(x)
    }

domain_max = 100.0 if use_large_scale else 10.0
resolution = 1.0 if use_large_scale else 0.1
x_values = [i * resolution for i in range(int(domain_max / resolution) + 1)]

hasil_scores = []
for _, row in df.iterrows():
    nama = row["Nama"]
    kualitas_val = row["Kualitas"]
    harga_val = row["Harga"]
    kualitas_membership = fuzzify_kualitas(kualitas_val)
    harga_membership = fuzzify_harga(harga_val)
    aggregated = [0.0] * len(x_values)
    for k_label, h_label, o_label in rules:
        alpha = min(kualitas_membership[k_label], harga_membership[h_label])
        if alpha <= 0: continue
        if o_label == "rendah": func = skor_rendah
        elif o_label == "sedang": func = skor_sedang
        else: func = skor_tinggi
        for i, x in enumerate(x_values):
            mu = func(x)
            aggregated[i] = max(aggregated[i], min(mu, alpha))
    numerator = sum(x * mu for x, mu in zip(x_values, aggregated))
    denominator = sum(aggregated)
    crisp_score = numerator / denominator if denominator != 0 else 0
    hasil_scores.append({
        "id Pelanggan": nama, "Pelayanan": kualitas_val, "harga": harga_val, "Skor": crisp_score
    })

df_hasil = pd.DataFrame(hasil_scores)
df_hasil = df_hasil.sort_values(by="Skor", ascending=False)
top5 = df_hasil.head(5).copy()
top5.insert(0, "Peringkat", range(1, len(top5) + 1))
top5.to_excel("peringkat.xlsx", index=False)
print("5 Restoran terbaik telah disimpan ke peringkat.xlsx")
