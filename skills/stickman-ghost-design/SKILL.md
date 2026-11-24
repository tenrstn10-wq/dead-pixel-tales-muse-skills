---
name: stickman-ghost-design
description: Desain visual hantu dan makhluk seram yang setia pada penampakan aslinya di legenda (pocong, kuntilanak, genderuwo, tuyul, dan hantu universal), digambar dalam pixel art tanpa gore. Pakai setiap kali ada hantu atau makhluk seram di cerita.
---

# Stickman Ghost Design

Tujuan: hantu langsung dikenali penonton karena ciri khas aslinya, bukan bentuk karangan. Karakter stickman tetap sederhana; hantu boleh lebih detail supaya jadi pusat perhatian. Contoh sprite: `references/ghost_sprites_sample.png`, kode: `scripts/ghost_sprites_example.py`.

## Prinsip
- **Setia pada legenda.** Ambil 2-4 ciri khas yang paling ikonik dan wajib ada. Tambahan lain opsional.
- **Siluet dulu.** Hantu harus terbaca dari bentuk bayangannya saja.
- **Seram dari suasana, bukan gore.** Tanpa darah, luka terbuka, organ, atau kekerasan grafis. Wajah boleh pucat, kosong, atau tertutup.
- **Satu hantu utama per cerita** (maksimal dua makhluk), dengan blok prompt sendiri yang ditulis sekali dan dipakai persis sama.
- **Reveal bertahap:** siluet jauh -> bagian kecil (mata, tangan) -> wujud penuh di puncak. Petunjuk pertama paling lambat detik 8-10; wujud penuh tidak sebelum sekitar 60% durasi. Jangan tampilkan wujud penuh di awal.
- Tanpa tokoh nyata, tanpa kejadian tragis nyata, tanpa merek atau karakter berhak cipta (hindari karakter creepypasta yang punya pemilik/ikon spesifik).
- Perlakukan legenda dengan hormat; jangan mengolok ritual keagamaan.

## Pustaka hantu Indonesia (local-legend)
Untuk penonton luar negeri, beri 1 kalimat pengantar di narasi ("In Indonesia, people say...").

| Hantu | Ciri khas WAJIB | Opsional | Gerak | Suara/SFX |
|---|---|---|---|---|
| **Pocong** | tubuh terbungkus kain kafan putih, ikatan di atas kepala, leher, dan kaki; wajah pucat dengan mata hitam cekung | kain kusam, noda tanah samar | melompat-lompat tegak, atau diam berdiri | lompatan "thump" berat berulang, gesekan kain |
| **Kuntilanak** | wanita bergaun putih panjang, rambut hitam sangat panjang menutupi wajah, kulit pucat | celah wajah pucat, tangan menggantung, sering di dekat pohon besar | melayang pelan, menoleh pelan | desis angin, nada tinggi tipis (tanpa tawa suara manusia) |
| **Genderuwo** | tubuh besar tinggi berbulu gelap, bahu lebar, lengan panjang, mata merah menyala | bayangan besar di pintu/pohon | langkah berat, berdiri menutup jalan | napas berat rendah, langkah menggelegar |
| **Tuyul** | sosok anak kecil botak berukuran mungil, mata besar, tanpa pakaian atau kain minimal | membawa uang receh | berlari kecil, mengendap | tawa kecil dari efek, langkah ringan |

## Pustaka hantu universal
| Hantu | Ciri khas WAJIB | Gerak |
|---|---|---|
| Wanita berambut panjang (gaya onryo) | gaun putih, rambut hitam panjang menutupi wajah, merangkak/berjalan patah-patah | gerak kaku, muncul dekat layar |
| Sosok bayangan | siluet hitam pekat, mata merah/putih menyala, tanpa wajah | berdiri diam di ujung ruang, bergeser tiap kedip lampu |
| Anak hantu | anak kecil pucat, mata hitam | berdiri membelakangi, menoleh |
| Penunggu lorong/lift | tinggi, kurus, bayangan memanjang | muncul di pantulan atau di lampu berkedip |

## Sprite referensi semua hantu
Semua hantu di pustaka ini punya fungsi gambar di `stickman-character/scripts/sprites_reference.py` (kamus `GHOSTS`), dan gambarnya ada di `stickman-character/references/ghosts_reference_sheet.png` (lengkap dengan stickman sebagai pembanding ukuran):
| Hantu | Fungsi |
|---|---|
| Pocong | `pocong()` |
| Kuntilanak | `kuntilanak()` |
| Genderuwo | `genderuwo()` |
| Tuyul | `tuyul()` |
| Sosok bayangan | `shadow_figure()` |
| Wanita berambut panjang | `long_hair_woman()` |
| Anak hantu | `child_ghost()` |
| Penunggu lorong | `corridor_thing()` |
Pakai fungsinya atau tiru proporsi dan ciri khasnya persis. Hantu baru di luar daftar ini boleh dibuat dengan aturan yang sama (ciri wajib, siluet jelas, rim light untuk makhluk gelap) dan ditambahkan ke pustaka.

## Aturan kualitas hantu (WAJIB)
- Di shot reveal, hantu minimal 40% tinggi frame dan ciri wajibnya terlihat jelas.
- **Pocong:** wajah pucat abu, dua mata hitam cekung (3x4 pixel), hidung 1 pixel, mulut garis, dan ikatan kepala, leher, serta kaki terlihat jelas. Pocong **harus bergerak** saat melompat: loop 4 frame (tanah, udara, udara, tanah), naik 5 pixel, maju 3 pixel per lompatan, bayangan mengecil di udara. Dilarang memakai satu sprite statis.
- **Makhluk gelap** (genderuwo, sosok bayangan): wajib rim light 1 pixel ungu `#7a63b8` di sekeliling siluet, mata merah 2x2 pixel dengan glow 1 pixel, dan ukuran lebih besar dari pocong. Kontras terhadap latar harus jelas.
- Kode referensi: `stickman-character/scripts/sprites_reference.py` (`pocong`, `genderuwo`).

## Cara menggambar dalam pixel art
- Skala hantu: tinggi 55-64 pixel di grid 135x240 (lebih tinggi dari stickman yang 34 pixel) supaya terasa mengancam.
- Palet hantu kontras dengan latar: hantu putih di latar gelap, hantu gelap (genderuwo, bayangan) dengan mata menyala (merah 2 pixel).
- Detail lewat tekstur dither (lipatan kain, rambut, bulu), bukan garis tipis.
- Animasi per langkah 8-12 fps: napas/goyang 2 frame, melayang naik-turun 1-2 pixel, lompat pocong 4 frame.
- Kedip lampu atau layar sebelum hantu muncul (1-3 frame gelap).

## Blok prompt (tempel persis di adegan yang ada hantunya)
- Pocong: "A pocong in pixel art: a corpse wrapped in a white burial shroud, tied with knots above the head, at the neck and at the feet, pale face with hollow black eyes, no gore."
- Kuntilanak: "A kuntilanak in pixel art: a woman in a long white dress with very long black hair covering most of her pale face, arms hanging, no gore."
- Genderuwo: "A genderuwo in pixel art: a tall bulky dark hairy creature with broad shoulders, long arms and glowing red eyes, no gore."
- Tuyul: "A tuyul in pixel art: a tiny bald child-like creature with large eyes, mischievous, no gore."
- Bayangan: "A shadow figure in pixel art: a tall pitch-black humanoid silhouette with two glowing eyes, no face, no gore."

## Cek
Ciri khas wajib ada semua, siluet terbaca, tidak ada gore, ukuran lebih besar dari stickman, dan blok prompt tidak diubah antar adegan.
