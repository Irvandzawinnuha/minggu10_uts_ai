# Sistem Cerdas Berbasis Fuzzy – Pemilihan Restoran Terbaik  
**Minggu 10 – Kecerdasan Buatan (Case-Based Reasoning)**  
**Bahasa: Python (Tanpa Library Fuzzy)**

---

## 1. Deskripsi Tugas

Diberikan file `restoran.xlsx` berisi **100 data review restoran** di kota Bandung, dengan dua atribut utama:

- **Kualitas Servis** (skala 1–100; semakin tinggi semakin baik)  
- **Harga** (Rp25.000–Rp55.000; semakin tinggi semakin mahal)

Tujuan tugas ini adalah membangun sistem **Fuzzy Logic Inference** untuk **memilih 5 restoran terbaik** berdasarkan kombinasi dari kualitas servis dan harga.

Sistem membaca file input `restoran.xlsx`, melakukan proses fuzzy inference, dan menghasilkan file output `peringkat.xlsx` berisi:

- ID/Nama restoran  
- Kualitas Servis  
- Harga  
- Skor kelayakan (hasil *defuzzification*)

---

## 2. Poin Desain dan Analisis

Berikut komponen yang perlu dianalisis dan diimplementasikan dalam laporan maupun kode program:

- Jumlah dan Nama Linguistik Setiap Atribut Input  
- Bentuk dan Batas Fungsi Keanggotaan Input  
- Aturan Inferensi (IF–THEN)  
- Metode Defuzzification  
- Bentuk dan Batas Fungsi Keanggotaan Output

---

## 3. Proses dalam Program

Program dibangun **tanpa menggunakan library fuzzy**. Proses-proses berikut diimplementasikan menggunakan fungsi atau prosedur:

1. Membaca data dari `restoran.xlsx`  
2. Fuzzifikasi nilai kualitas dan harga menjadi nilai linguistik  
3. Inferensi menggunakan aturan fuzzy IF–THEN  
4. Defuzzifikasi menggunakan metode *Centroid*  
5. Menyimpan output ke file `peringkat.xlsx`

---

## 4. Output Program

Output akhir dari program adalah:

📄 File `peringkat.xlsx` berisi 5 restoran terbaik dengan informasi:

- Nama Restoran  
- Kualitas Servis  
- Harga  
- Skor Kelayakan (hasil defuzzifikasi)

---

## 5. Kolaborasi Kelompok

Tugas ini dikerjakan secara berkelompok (2 orang):

- **Irvan Dzawin Nuha** – 1302223076  
- **Joshua Daniel Simanjuntak** – 1302220072
