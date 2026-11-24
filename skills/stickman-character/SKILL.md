---
name: stickman-character
description: Kunci desain karakter stickman klasik (gaya stickman asli) supaya bentuk dan ekspresinya identik di semua adegan dan episode. Pakai setiap kali menulis prompt visual atau menggambar adegan yang ada karakternya.
---

# Stickman Character (gaya klasik)

Satu-satunya sumber kebenaran untuk tampilan karakter. Skill lain (visual-style, backgrounds) tidak boleh mengubah desain di sini.

## Desain tokoh utama (gaya stickman asli, dikunci)
- Kepala: lingkaran putih polos dengan garis tepi tipis, proporsi normal (bukan kepala raksasa).
- Badan, tangan, kaki: garis lurus tipis. Tanpa jari, tanpa telapak detail.
- **Warna garis mengikuti kontras latar:** hitam di adegan terang, putih keputihan di adegan gelap. Bentuk tidak berubah, hanya warna garis.
- Tanpa pakaian, tanpa rambut, tanpa nama khusus.
- Wajah minimal: dua titik hitam sebagai mata, garis kecil sebagai mulut. Alis sederhana boleh dipakai untuk emosi.
- Ekspresi dibawa terutama oleh **pose tubuh**, posisi alis, dan bentuk mulut, bukan detail wajah.
- Aksesori per cerita (opsional, maksimal 1): senter, tas, kopi, dll. Aksesori hanya berlaku selama satu cerita.
- Karakter tetap sederhana dan datar. Yang kaya detail adalah latar belakangnya.

## Proporsi dan sprite referensi (WAJIB)
- Proporsi: kepala 29% tinggi, torso 40%, kaki 31%, tiap lengan 30% tinggi. Garis 1 pixel di shot lebar, 2 pixel di medium dan close-up.
- Lengan dan kaki selalu terlihat penuh sesuai pose: stand, walk, run, scared (tangan terangkat), reach (satu tangan ke depan).
- Close-up: wajib leher, badan, dan lengan yang keluar dari satu titik di bawah leher, **sama seperti shot lain**. Dilarang menambah garis bahu horizontal (stickman klasik tidak punya bahu). Lengan turun sekitar 23 derajat (seperti pose stand) sampai tepi bawah frame. Jangan gambar kepala melayang.
- Kode referensi: `scripts/sprites_reference.py` (fungsi `stickman`, `closeup`, `pocong`, `genderuwo`) dan gambar `references/sprites_reference_sheet.png`. Pakai fungsinya atau tiru proporsinya persis.

## Aturan wajah dan ukuran
- Kepala minimal diameter 10 pixel dan **mata selalu terlihat** (1 pixel gelap kontras) kecuali karakter jelas membelakangi kamera.
- Jangan pernah merender kepala polos tanpa mata saat karakter menghadap kamera. Kalau kepala terlalu kecil untuk wajah, ganti dengan shot yang lebih dekat.
- Di close-up, wajah digambar ulang dengan lebih banyak pixel (alis, mulut, keringat) di grid yang sama.

## Versi pixel art (mode default)
- Tinggi total sekitar **34 pixel** di grid 135x240: kepala diameter 10 pixel, badan 14 pixel, kaki 10 pixel, garis tebal 1 pixel.
- Mata: 1 pixel hitam masing-masing. Mulut: 1-3 pixel.
- Animasi per langkah (12 fps): jalan 4 frame, lari 6 frame, diam 2 frame (napas), kaget 2 frame (goyang).
- Bayangan di tanah: garis gelap 1 pixel di bawah kaki.

## Blok prompt karakter (tempel PERSIS sama di setiap adegan)
"A classic stickman in pixel art: a plain white circle head, two single-pixel dot eyes and a minimal line mouth, and a body, arms and legs drawn as one-pixel straight lines (black on light scenes, white on dark scenes). No clothes, no hair, flat simple line figure."
Jangan diparafrase, jangan dipersingkat, jangan ditambah kata sifat baru. Aksesori cerita ditambahkan sebagai kalimat terpisah setelah blok ini, bukan di dalamnya.

## Pustaka ekspresi (pakai nama ini di prompt)
neutral, sleepy, curious, worried, scared (alis naik, mulut kecil terbuka), shocked (mulut bulat, tangan terangkat), terrified (tubuh gemetar, keringat), relieved (bahu turun), smiling, deadpan.

## Pustaka pose
berdiri, berjalan, berlari, mengintip, membeku di tempat, menunjuk, menutup mulut, jatuh/terduduk, menoleh pelan, menggenggam benda.

## Tokoh pendukung
- Dibuat berbeda jelas dari tokoh utama agar tidak tertukar: warna kepala, bentuk kepala, atau siluet berbeda (mis. kepala hitam solid, atau tanpa wajah).
- Makhluk/hantu: desainnya diatur di skill `stickman-ghost-design` (setia pada penampakan legenda, tanpa gore).
- Setiap tokoh pendukung punya blok prompt sendiri, ditulis sekali dan dipakai persis sama.
- Maksimal 2 tokoh pendukung per cerita 40-55 detik supaya jelas.

## Referensi karakter
Di awal proyek, buat satu lembar referensi (tokoh utama: depan, samping, 3 ekspresi). Kalau mesin video mendukung gambar referensi, lampirkan di setiap adegan.

## Cek konsistensi (tiap adegan)
Bentuk kepala dan ketebalan garis sama, tidak ada pakaian atau rambut yang muncul sendiri, jumlah anggota badan benar, tidak berubah jadi karakter realistis atau 3D. Kalau melenceng, buat ulang adegan itu.
