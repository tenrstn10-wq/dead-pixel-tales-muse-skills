---
name: stickman-narration-timing
description: Tulis narasi stickman (English) dengan jatah kata per adegan supaya pas dan sinkron dengan durasi video, tidak pernah melebihi. Pengguna merekam voiceover dan membuat subtitle sendiri; Muse hanya menulis teks narasinya.
---

# Narration Timing

Muse **hanya menulis teks narasi**. Muse tidak membuat voiceover/TTS dan tidak membuat subtitle (pengguna mengerjakannya sendiri). Narasi tidak boleh melebihi durasi video dan harus benar-benar pas per adegan.

## Input
Rencana adegan: nomor adegan, durasi tiap adegan (detik), dan rencana jeda dramatis (kalau ada).

## Rumus jatah kata
- Kecepatan bicara: **2.2 kata/detik** (horor, bercerita pelan). Pakai 2.5 untuk komedi/aksi cepat.
- Pemakaian efektif tiap adegan = durasi - 0.5 dtk (0.3 dtk jeda awal, 0.2 dtk jeda akhir) - total jeda dramatis di adegan itu.
- Maks kata = lantai(pemakaian efektif x kecepatan).
- Cara menghitung kata: kontraksi (don't, it's) = 1 kata; angka ditulis dengan kata; kata 4 suku kata atau lebih dihitung 2.
- Jeda: "..." = 0.5 dtk, "—" = 0.3 dtk, jeda dramatis kosong = tulis eksplisit (mis. [pause 1s]).

## Cara menulis
- Bahasa Inggris sederhana, bahasa lisan, kalimat pendek (maks 8 kata).
- Hindari kata yang sulit diucapkan cepat atau nama panjang.
- Adegan hook: narasi mulai di 0.3 dtk pertama.
- Momen paling seram boleh tanpa kata. Diam itu bagian dari narasi.
- Satu ide per adegan. Jangan menjelaskan apa yang sudah terlihat di gambar.

## Output (wajib berupa tabel)
| Scene | Durasi | Jeda | Maks kata | Narasi | Kata aktual | Perkiraan waktu bicara | Status |
|---|---|---|---|---|---|---|---|

- Perkiraan waktu bicara = kata aktual / kecepatan + jeda.
- Status "OK" hanya kalau waktu bicara + 0.5 dtk <= durasi adegan.
- Kalau ada yang "LEWAT", **potong sendiri sampai OK**. Jangan serahkan masalahnya ke pengguna.
- Di bawah tabel tulis total: jumlah kata, total waktu bicara, total durasi video, sisa waktu.
- Setelah tabel, tulis narasi penuh dalam satu blok bersih (tanpa tabel) supaya pengguna gampang membaca saat merekam.

## Cek konsistensi (wajib sebelum diserahkan)
Periksa dan perbaiki sendiri:
1. **Urutan aksi:** tidak ada kalimat yang bertentangan dengan kejadian sebelumnya (mis. sudah menoleh lalu bilang "terpaksa menoleh"). Satu aturan legenda hanya dilanggar sekali.
2. **Sudut pandang (POV):** sama di narasi, judul, dan deskripsi (semua "I", atau semua orang ketiga).
3. **Twist:** ada petunjuk yang cukup di narasi dan gambar supaya penonton paham tanpa penjelasan panjang.
4. **Narasi cocok dengan visual** tiap adegan, dan tidak menjelaskan apa yang sudah terlihat.

## Naskah rekam berdurasi (WAJIB, ini yang diserahkan ke pengguna)
Setelah tabel jatah kata lolos semua, serahkan juga naskah rekam dengan waktu per baris supaya pengguna gampang merekam dan menyinkronkan di editor. Format waktu `m:ss.d` (menit:detik.persepuluh).

Tiap adegan satu blok:
```
Adegan 1 · 0:00.0–0:07.0 (7.0 dtk)
Mulai 0:00.3 · estimasi selesai 0:06.2 · batas akhir 0:06.8
"In Indonesia, they say: if you hear hopping behind you, never look back."
```
Aturan:
- **Mulai** = awal adegan + 0.3 dtk. **Estimasi selesai** = mulai + (kata aktual / kecepatan bicara) + jeda. **Batas akhir** = akhir adegan - 0.2 dtk. Estimasi selesai tidak boleh melewati batas akhir.
- Jeda dramatis ditulis sebagai baris sendiri dengan waktunya, mis. `[jeda 1.0 dtk · 0:20.0–0:21.0]`.
- Waktu adegan berurutan, tidak tumpang tindih, dan adegan terakhir berakhir tepat di durasi video.
- Di akhir tulis: total durasi video, total waktu bicara, dan sisa waktu hening.
- Kalau waktu adegan berubah (mis. shot list direvisi), hitung ulang semua waktu.

## Revisi
Kalau pengguna bilang satu baris terlalu panjang saat dibaca, pangkas baris itu sampai sesuai jatah, lalu hitung ulang total.
