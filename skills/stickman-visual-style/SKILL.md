---
name: stickman-visual-style
description: Gaya visual dan teknis video stickman storytelling untuk YouTube Shorts. Default: pixel art retro 9:16 dirender lewat kode (grid, palet, dithering, animasi per langkah). Alternatif: ilustrasi sinematik. Karakter dan latar ada di skill sendiri.
---

# Stickman Visual Style

Skill ini mengatur **gaya dan teknis**. Desain karakter ada di `stickman-character`, tempat dan latar di `stickman-backgrounds`. Contoh hasil: `references/pixel-style-sample.png`, dan kode contoh: `scripts/pixel_scene_example.py`.

## Mode default: PIXEL ART RETRO

### Format
- Vertikal **9:16**. Render di grid kecil **135x240**, lalu perbesar **8x** (nearest neighbor) menjadi 1080x1920.
- 30 fps untuk output, tapi gerakan karakter dan latar diubah **per langkah (12 fps)** supaya terasa seperti animasi pixel.
- Kosongkan sekitar 25% bagian bawah dari elemen penting (area subtitle pengguna) dan ±10% atas.
- Tanpa teks di dalam gambar.

### Aturan pixel
- **Tanpa anti-aliasing dan tanpa smoothing.** Semua pixel kotak, tegas, dan ukurannya sama di seluruh frame.
- Palet terbatas: maksimal 16 warna dasar per adegan (hasil dithering tidak dihitung), dan palet dasarnya sama di satu cerita.
- Gradasi (langit, cahaya, kabut) memakai **dithering** pola catur, bukan gradien halus.
- Kamera dan gerakan hanya bergeser **dalam kelipatan pixel utuh** (tidak ada posisi setengah pixel).
- Latar tiga lapisan (depan, tengah, belakang) boleh bergeser dengan kecepatan beda (parallax) untuk kesan kedalaman.
- Efek horor: goyang layar (offset 1-2 pixel), kedip lampu, kabut dither, mata merah menyala 2 pixel.

### Mesin pembuat
- **Utama: kode** (Remotion, canvas, atau Python + Pillow). Hasilnya rapi, konsisten, murah, dan gerakannya bisa disinkronkan presisi dengan SFX.
- Kalau terpaksa memakai model gambar/video, tambahkan: "pixel art, crisp square pixels, limited palette, no anti-aliasing, no blur" dan cek hasilnya. Pixel sering berkedip atau melebur; kalau begitu pindah ke mesin kode.

### Prompt per adegan (untuk spesifikasi adegan atau model)
1. **CHARACTER**: blok dari `stickman-character`, persis sama.
2. **STYLE** (tetap):
   "Retro pixel art, 135x240 grid upscaled 8x, crisp square pixels, no anti-aliasing, limited palette with dithering, moody lighting, vertical 9:16. The stickman stays a simple line figure while the background is richly detailed."
3. **SCENE**: location bible dan palet dari `stickman-backgrounds`.
4. **ACTION BY TIME**: aksi dari detik ke detik, nama ekspresi dan pose dari pustaka karakter.

## Mode alternatif: SINEMATIK
Pakai kalau pengguna memintanya. STYLE: "Cinematic 2D illustration, richly detailed painterly background, moody lighting with strong rim light and soft volumetric haze, limited color palette, subtle film grain, vertical 9:16. The stickman stays a flat, simple line figure while the background is detailed."

## Kamera dan ritme (WAJIB, berlaku untuk setiap video)
- Sebelum merender, buat **shot list**: satu baris per adegan berisi jenis framing. Jangan merender sebelum shot list memenuhi aturan di bawah.
- Jenis framing: wide, medium, close-up wajah, close-up benda/detail (kaki, jejak, pintu, lampu), over-shoulder, low-angle (untuk hantu), top-down (untuk jejak atau benda di tanah).
- **Minimal 4 jenis framing berbeda** dalam satu video 40-55 detik, dengan **minimal 2 close-up**. Dua adegan berurutan tidak boleh memakai framing yang sama.
- **Satu shot lebar saja untuk seluruh video itu dilarang.**
- **Ukuran karakter:** di shot lebar tinggi stickman minimal 14% tinggi frame; di medium minimal 30%; di close-up wajah mengisi minimal 40% lebar frame.
- Close-up digambar ulang dengan lebih banyak pixel di grid yang sama. **Jangan memperbesar sprite** (ukuran pixel tidak boleh campur).
- Ritme: ada perubahan yang terlihat (shot berganti, lampu berkedip, bayangan bergeser, objek muncul) minimal tiap 3 detik.
- Tiap adegan 3-7 detik. Gerak kamera (push-in per langkah) dipakai di momen seram.

## Hook visual dan payoff (WAJIB)
- Detik 0-3: harus ada elemen janggal atau mengancam di layar, bukan hanya karakter berdiri.
- **Petunjuk pertama makhluk paling lambat detik 8-10** (siluet jauh, bayangan, mata merah kecil, kedip lampu). Wujud penuh tidak muncul sebelum sekitar 60% durasi.
- **Payoff/twist di akhir harus terbaca di layar:** pakai close-up atau insert shot, benda bukti minimal 8% tinggi frame, warna kontras tinggi, tahan minimal 2 detik. Jangan mengandalkan detail yang hanya beberapa pixel.

## Gerak latar halus (WAJIB)
- Minimal **2 elemen latar yang bergerak terus** supaya layar terasa hidup: bintang berkedip, kabut bergeser 1 pixel tiap 0.5 dtk, daun atau rumput bergoyang, lampu berkedip pelan, awan lewat, asap, debu.
- Animasi loop pendek (2-4 frame, 4-8 fps), gerak kecil (1 pixel), tidak boleh mengalihkan perhatian dari aksi utama atau menutupi area subtitle.
- Layar tidak boleh diam lebih dari 3 detik (dicek di laporan QA).
- Ciri khas channel (dead pixel merah dan sting audio) diatur di skill `stickman-channel-signature`.

## Kualitas visual (WAJIB)
1. **Close-up wajah** wajib punya leher, badan, dan lengan yang keluar dari satu titik di bawah leher, sama seperti di shot lain (tanpa garis bahu horizontal), terpotong tepi bawah frame (pakai `closeup()` di `stickman-character/scripts/sprites_reference.py`). Kepala tidak boleh melayang seperti balon. Latar close-up tidak boleh polos: tampilkan elemen latar (pagar, dinding, daun, lampu).
2. **Cahaya:** kerucut cahaya lampu selalu menempel pada lampunya dan lampunya terlihat. Tidak ada kerucut yang melayang sendirian.
3. **Aksi lengkap:** lengan, tangan, dan kaki terlihat penuh sesuai pose. Tangan tidak terpotong tepi frame. Aksi (membuka/menutup gerbang, memegang HP) digambar utuh dalam minimal 4 frame dan berada di tengah frame.
4. **Latar satu kanvas:** gambar latar sebagai satu kanvas besar, lalu geser atau potong dengan kelipatan pixel utuh. Dilarang menyambung potongan latar sehingga muncul kotak atau tepi keras.
5. **Tanpa artefak:** tidak ada garis titik-titik, pixel liar, atau objek terpotong tanpa alasan. Dithering hanya untuk gradasi (langit, cahaya, kabut), bukan untuk garis.
6. **Tinjauan visual:** sebelum menyerahkan, buat contact sheet 1 frame per detik (`qa_check.py --sheet`), tinjau satu per satu terhadap aturan 1-5, perbaiki, ulangi sampai bersih.

## Larangan
Tanpa gore atau kekerasan grafis, tanpa watermark, tanpa karakter/merek berhak cipta. Ambil gaya dari referensi, jangan meniru karakter atau kreasi spesifik orang lain.

## Cek akhir
Cek shot list: minimal 4 framing berbeda, minimal 2 close-up, tidak ada dua framing sama berurutan, petunjuk makhluk muncul sebelum detik 10, payoff akhir terbaca jelas. Ambil frame tiap adegan: pixel tajam (tidak blur/campur ukuran), palet konsisten, kamera bervariasi, area bawah bersih, urutan aksi benar. Cek karakter dengan `stickman-character` dan latar dengan `stickman-backgrounds`.
