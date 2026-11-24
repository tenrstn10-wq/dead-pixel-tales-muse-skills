---
name: stickman-backgrounds
description: Tempat dan latar belakang untuk video stickman: pustaka setting universal, aturan layout dan kesinambungan ruangan, palet cahaya per suasana. Pakai saat menentukan lokasi cerita dan menulis bagian SCENE pada prompt visual.
---

# Stickman Backgrounds

Latar adalah setengah dari kesan "bagus". Tujuannya detail, punya kedalaman, dan **konsisten sepanjang satu cerita**.

## Location bible (wajib, 1 per cerita)
Sebelum membuat adegan, tulis satu paragraf deskripsi lokasi yang tetap: tata letak (pintu di kiri, jendela di kanan, dst), benda tetap, jenis cahaya, palet warna. Tempel PERSIS sama di setiap adegan di lokasi itu. Kalau pindah lokasi, buat blok baru.

## Aturan umum
- Tiga lapisan kedalaman: depan (siluet/benda dekat), tengah (tempat aksi), belakang (dinding/langit/jauh).
- Cahaya punya sumber jelas (lampu, jendela, layar). Satu aksen warna per adegan.
- Detail secukupnya, 5-8 benda khas, bukan penuh sesak.
- Kesinambungan: posisi pintu, tangga, perabot tidak berpindah antar adegan.
- Tanpa teks terbaca di latar (papan, layar). Tanpa merek nyata.
- Bagian bawah 25% frame bersih dari objek penting (area subtitle).

## Pustaka setting universal
| Setting | Elemen khas | Cahaya dan palet | Cocok untuk |
|---|---|---|---|
| Lift gedung malam | pintu logam, panel tombol, indikator lantai, cermin buram | lampu putih dingin berkedip, abu dan hijau pucat | everyday-horror, twist |
| Lorong hotel | karpet pola, deretan pintu, lampu dinding, ujung lorong gelap | kuning redup + bayangan panjang | rules-horror |
| Apartemen/kamar | kasur, jendela, meja, lampu tidur | biru malam + satu lampu hangat | wholesome-scary, komedi |
| Kantor malam | meja kosong, monitor menyala, lampu mati sebagian | biru dingin + cahaya layar | everyday-horror |
| Tangga darurat | pagar besi, lampu neon, bayangan menurun | hijau/putih pucat, kontras tinggi | rules-horror |
| Jalan sepi malam | lampu jalan, kabut tipis, halte | oranye lampu + biru gelap | twist, legenda |
| Minimarket 24 jam | rak, lampu neon terang, kaca gelap di luar | putih terang vs gelap pekat di luar | dark-comedy, twist |
| Hutan/jalan desa | pepohonan siluet, kabut, bulan | biru-hijau gelap + cahaya bulan | local-legend |
| Rumah kosong | debu, perabot ditutup kain, cahaya lewat celah | abu hangat + berkas cahaya | everyday-horror |
| Sekolah/kampus malam | koridor panjang, loker, ruang kelas kosong | hijau neon pucat, bayangan | rules-horror |

Setting khas Indonesia (kos-kosan, warung, pos ronda, angkot) boleh untuk local-legend, dengan 1 kalimat pengantar di narasi.

## Palet pixel (mode default)
Satu palet dasar per cerita (maks 16 warna). Pilih menurut suasana:
| Suasana | Warna dasar | Aksen |
|---|---|---|
| Malam seram | biru tua `#0b0d24`, `#1f1a45`, ungu `#3f2c6b` | merah `#ff2a4d` atau hijau pucat |
| Neon kota | ungu gelap + biru malam | pink `#ff4f9a` dan cyan `#4fe3ff` |
| Hangat/penutup | ungu-pink senja, oranye | kuning `#f7d98b` |
| Sunset retro (gaya referensi) | ungu muda, pink, oranye | hijau palem gelap |
Gradasi langit dan cahaya pakai dithering catur. Jendela menyala = kotak kuning kecil. Lampu jalan = kerucut cahaya dither. Contoh lengkap: `stickman-visual-style/references/pixel-style-sample.png`.

## Cahaya menurut alur cerita
- Setup: terang/hangat, ruangan terlihat jelas.
- Eskalasi: sumber cahaya berkurang, bayangan memanjang.
- Puncak: kontras ekstrem, satu aksen merah atau cahaya tunggal.
- Penutup: kembali hangat (atau tetap gelap untuk horor murni).

## Latar satu kanvas dan close-up
- Gambar tiap lokasi sebagai satu kanvas besar, lalu "kamera" menggeser atau memotongnya dengan kelipatan pixel utuh. Jangan menyambung potongan latar (muncul kotak atau tepi keras).
- Latar close-up tidak boleh polos. Gunakan bagian latar yang sama dengan lokasi (pagar, dinding, daun, lampu lengkap dengan kerucut cahayanya).

## Cek
Layout sama dengan location bible, tidak ada teks acak, cahaya masuk akal, area bawah bersih.
