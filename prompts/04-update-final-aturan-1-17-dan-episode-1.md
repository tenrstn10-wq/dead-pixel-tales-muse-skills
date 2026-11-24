# PROMPT FINAL untuk Muse

## Cara kirim (baca ini dulu)

**Kalau Muse-mu sudah pernah menerima skill stickman sebelumnya:** kirim prompt di bawah ini saja. Salin semua teks dari baris "MULAI" sampai "SELESAI", tempel ke Muse, lalu kirim. Satu pesan sudah cukup.

**Kalau percakapan Muse baru atau Muse belum menyimpan skill apa pun:** kirim dengan urutan ini:
1. File `SEMUA SKILL untuk paste` (tempel isinya).
2. `Prompt A` dari file `PROMPT untuk Muse`.
3. Prompt final di bawah ini.

**Lampiran opsional** (kalau Muse bisa menerima file): `lembar referensi sprite`, `lembar referensi hantu`, dan `sprites reference` (kodenya). Gambar-gambar itu hanya acuan bentuk, aturannya sudah lengkap di teks.

Setelah Muse menyerahkan hasilnya, kirim videonya ke sini untuk kuperiksa.

=============== MULAI ===============

Ini pembaruan aturan PERMANEN untuk skill-skill stickman (nomor 1 sampai 17), lalu perbaikan Episode 1. Aturan 1 sampai 17 berlaku untuk SEMUA konten, termasuk setiap konten baru ke depannya, bukan hanya satu episode. Kalau ada yang bertentangan dengan aturan lama, pakai aturan ini.

Simpan sebagai aturan tetap: kalau kamu bisa mengedit file skill-mu, perbarui SKILL.md yang terkait (visual-style, story-ideas, ghost-design, character, narration-timing, publish-metadata, audio-director) dan buat dua skill baru: stickman-qa-report dan stickman-channel-signature. Kalau tidak bisa, simpan sebagai aturan tetap di catatan/memorimu dan terapkan setiap kali saya minta konten baru. Sebelum menyerahkan tiap konten, cek sendiri semua aturan dan perbaiki yang belum terpenuhi.

## Aturan 1-7

**1. Kamera (skill visual-style)**
- Buat shot list dulu, satu baris per adegan berisi jenis framing. Jangan merender sebelum shot list memenuhi aturan ini.
- Jenis framing: wide, medium, close-up wajah, close-up benda/detail (kaki, jejak, pintu, lampu), over-shoulder, low-angle (untuk hantu), top-down.
- Minimal 4 jenis framing berbeda dalam satu video, minimal 2 close-up, dan dua adegan berurutan tidak boleh memakai framing yang sama. Satu shot lebar untuk seluruh video dilarang.
- Ukuran karakter: shot lebar minimal 14% tinggi frame, medium minimal 30%, close-up wajah minimal 40% lebar frame. Close-up digambar ulang dengan lebih banyak pixel di grid yang sama, jangan memperbesar sprite.
- Ada perubahan yang terlihat (shot berganti, lampu berkedip, bayangan bergeser) minimal tiap 3 detik.

**2. Hook dan petunjuk hantu (skill visual-style, story-ideas, ghost-design)**
- Detik 0-3 harus ada elemen janggal atau mengancam di layar.
- Petunjuk pertama makhluk muncul paling lambat detik 8-10. Wujud penuh tidak sebelum sekitar 60% durasi.

**3. Payoff akhir harus terbaca**
- Twist di akhir dibuat dengan close-up atau insert shot, benda bukti minimal 8% tinggi frame, kontras tinggi, ditahan minimal 2 detik. Jangan mengandalkan detail yang hanya beberapa pixel.

**4. Wajah stickman (skill character)**
- Kepala minimal 10 pixel dan mata selalu terlihat saat menghadap kamera. Jangan render kepala polos tanpa mata. Kalau terlalu kecil, ganti dengan shot yang lebih dekat.

**5. Konsistensi narasi (skill narration-timing)**
Sebelum menyerahkan narasi, periksa sendiri: (a) tidak ada kalimat yang bertentangan dengan urutan aksi, dan satu aturan legenda hanya dilanggar sekali, (b) POV sama di narasi, judul, dan deskripsi, (c) twist punya petunjuk yang cukup, (d) narasi cocok dengan visual tiap adegan.

**6. Cover (skill publish-metadata)**
- Frame cover: close-up wajah karakter yang ketakutan, atau teaser (siluet, mata merah) sebelum wujud penuh. Jangan memakai frame yang menampilkan twist atau lebih dari satu makhluk. Harus terbaca saat kecil.

**7. Naskah rekam berdurasi (skill narration-timing)**
- Setiap menyerahkan narasi, sertakan waktu tiap baris dalam format m:ss.d: waktu adegan (mulai-selesai), waktu mulai bicara (awal adegan + 0.3 dtk), estimasi selesai, dan batas akhir (akhir adegan - 0.2 dtk). Jeda dramatis ditulis sebagai baris sendiri dengan waktunya. Di akhir tulis total durasi video, total waktu bicara, dan sisa hening.

**8. Laporan QA di setiap penyerahan (skill stickman-qa-report)**
Sebelum menyerahkan konten, ukur hasilnya sendiri dan lampirkan laporan berformat tabel: Cek | Nilai | Aturan | PASS/FAIL. Perbaiki semua FAIL yang bisa diperbaiki, ukur ulang, baru serahkan. Jangan menulis PASS tanpa nilai. Hal yang tidak bisa diukur tulis "tidak diukur".
Yang diukur otomatis dari file video: resolusi 1080x1920, fps 30, durasi minimal 40 detik, durasi audio sama dengan video, peak audio maksimal -1.0 dBFS, loudness, jumlah perpindahan shot, layar diam terlama maksimal 3 detik, dan kerapian grid pixel (pixel kotak seragam, tidak blur).
Yang dilaporkan dari shot list: jumlah framing berbeda (minimal 4), jumlah close-up (minimal 2), tidak ada dua framing sama berurutan, detik petunjuk hantu pertama (maksimal detik 10), detik wujud penuh (minimal 60% durasi), payoff (detik mulai, ditahan minimal 2 detik, objek bukti minimal 8% tinggi frame), mata stickman terlihat, gerak latar ada, dead pixel (detik dan posisi), sting audio ada, narasi (semua status OK, POV konsisten, estimasi selesai tidak melewati batas akhir), metadata lengkap, cover tanpa spoiler.

**9. Gerak latar halus (skill visual-style)**
Minimal 2 elemen latar bergerak terus (bintang berkedip, kabut bergeser 1 pixel tiap 0.5 detik, daun atau rumput bergoyang, lampu berkedip pelan, awan, asap, debu). Loop pendek 2-4 frame di 4-8 fps, gerak kecil, tidak mengalihkan dari aksi utama atau menutupi area subtitle. Layar tidak boleh diam lebih dari 3 detik.

**10. Easter egg "dead pixel" (skill stickman-channel-signature)**
Setiap episode menyembunyikan satu dead pixel: kotak 2x2 pixel grid warna merah #ff2a4d (boleh berkedip 2 frame sekali). Terlihat minimal 1.5 detik total, tidak muncul di 3 detik pertama, tidak menutupi benda penting. Posisinya berbeda tiap episode (dinding, langit, tanah, pakaian hantu, jendela, bayangan); catat posisi dan detiknya di daftar ide terpakai dan di laporan QA, dan jangan mengulang posisi yang sama dalam 5 episode terakhir. Komentar sematan default: "Did you spot the dead pixel? Tell me where." (boleh ditambah satu pertanyaan cerita pendek di kalimat kedua, maksimal 2 kalimat).

**11. Sting audio khas (skill stickman-channel-signature dan audio-director)**
Di 1.5 detik terakhir setiap video, setelah payoff dan setelah narasi selesai, mainkan sting yang sama persis di setiap episode: tiga nada kotak menurun (A5 880 Hz, E5 659.3 Hz, A4 440 Hz, masing-masing 0.12 detik) diikuti semburan static pendek, dibuat kasar (bitcrush 3 bit). Total kurang dari 1.2 detik, peak maksimal -9 dBFS, tidak lebih keras dari SFX utama.

**12. Close-up wajah (skill character dan visual-style)**
Wajah di close-up wajib punya leher, badan, dan lengan yang keluar dari satu titik di bawah leher, sama persis seperti desain di shot lain. Dilarang menambah garis bahu horizontal (stickman klasik tidak punya bahu). Lengan turun sekitar 23 derajat sampai tepi bawah frame. Kepala tidak boleh melayang seperti balon. Latar close-up tidak boleh polos: tampilkan elemen latar (pagar, dinding, daun, lampu).

**13. Anatomi dan aksi (skill character)**
Proporsi stickman: kepala 29% tinggi, torso 40%, kaki 31%, tiap lengan 30% tinggi. Garis 1 pixel di shot lebar, 2 pixel di medium dan close-up. Lengan dan kaki selalu terlihat penuh sesuai pose (stand, walk, run, scared dengan tangan terangkat, reach dengan satu tangan ke depan). Tangan tidak terpotong tepi frame. Aksi (membuka atau menutup gerbang, memegang HP) digambar utuh dalam minimal 4 frame dan berada di tengah frame.

**14. Hantu (skill ghost-design)**
Di shot reveal, hantu minimal 40% tinggi frame dan ciri wajibnya terlihat. Pocong: wajah pucat abu, dua mata hitam cekung (3x4 pixel), hidung 1 pixel, mulut garis, ikatan kepala, leher, dan kaki terlihat jelas. Pocong harus bergerak: loop lompat 4 frame (tanah, udara, udara, tanah), naik 5 pixel, maju 3 pixel per lompatan, bayangan mengecil di udara. Dilarang memakai satu sprite statis. Makhluk gelap (genderuwo, sosok bayangan) wajib punya rim light 1 pixel ungu #7a63b8 di sekeliling siluet, mata merah 2x2 pixel dengan glow 1 pixel, dan ukuran lebih besar dari pocong. Semua hantu di pustaka (pocong, kuntilanak, genderuwo, tuyul, sosok bayangan, wanita berambut panjang, anak hantu, penunggu lorong) punya ciri wajib masing-masing di skill ghost-design; gambar sesuai ciri itu.

**15. Cahaya**
Kerucut cahaya lampu selalu menempel pada lampunya dan lampunya terlihat. Tidak boleh ada kerucut yang melayang sendirian.

**16. Latar satu kanvas dan tanpa artefak (skill visual-style dan backgrounds)**
Gambar latar sebagai satu kanvas besar lalu geser atau potong dengan kelipatan pixel utuh. Dilarang menyambung potongan latar sehingga muncul kotak atau tepi keras. Tidak ada garis titik-titik, pixel liar, atau objek terpotong tanpa alasan. Dithering hanya untuk gradasi (langit, cahaya, kabut), bukan untuk garis.

**17. Tinjauan visual (skill qa-report)**
Sebelum menyerahkan, buat contact sheet 1 frame per detik dan tinjau satu per satu terhadap aturan 12 sampai 16. Perbaiki dan ulangi sampai bersih. Masukkan temuan dan perbaikannya ke laporan QA.

## Urutan kerja sekarang
1. Simpan aturan 1 sampai 17, lalu balas SINGKAT: ringkasan aturan yang kamu simpan dan di mana kamu menyimpannya.
2. Setelah itu langsung kerjakan perbaikan Episode 1 di bawah memakai SEMUA aturan tadi, termasuk gerak latar, dead pixel, sting audio, dan laporan QA.

## Perbaikan Episode 1 "The Pocong on the Village Road"

Durasi total tetap 52 detik, format 1080x1920, tetap pixel art dengan latar jalan desa yang sama.

**Shot list baru**
| Adegan | Detik | Framing | Isi |
|---|---|---|---|
| 1 | 0-7 | wide, low-angle | jalan kosong, lampu berkedip di detik 1, siluet kecil pucat di ujung jauh jalan sekitar detik 5 |
| 2 | 7-13 | medium | stickman berjalan, memegang HP |
| 3 | 13-19 | close-up wajah | mata melebar mendengar bunyi |
| 4 | 19-26 | over-shoulder atau top-down | bayangan lompatan pocong makin besar di jalan di belakang stickman |
| 5 | 26-31 | close-up lampu | lampu berkedip, bunyi lompatan berhenti |
| 6 | 31-38 | close-up wajah | stickman menoleh pelan, mata ketakutan |
| 7 | 38-45 | low-angle wide | pocong besar di depan, genderuwo bermata merah di belakangnya, pocong melompat pergi melewati stickman |
| 8 | 45-52 | insert gerbang, lalu top-down | gerbang ditutup, lalu close-up jejak di debu: bekas lompatan kecil dan jejak kaki raksasa tiga jari, ditahan minimal 2 detik |

**Narasi baru** (sudut pandang "I", sudah dicek sesuai jatah kata; hitung ulang dengan skill dan perbaiki kalau ada yang lewat)
1. In Indonesia, they say: if you hear hopping behind you, never look back.
2. It was late. The road was empty. My phone had no signal.
3. Then I heard it. A soft thump. Behind me.
4. It came again. Closer now. I kept walking. I did not look.
5. Under the lamp, the light flickered. The hopping stopped.
6. Silence. Then it started again. So close. I couldn't help it. I looked.
7. A pocong. But it wasn't chasing me. It was running.
8. I shut my gate. In the dust: tiny hops, and giant footprints.

Durasi adegan untuk narasi (detik): 7, 6, 6, 7, 5, 7, 7, 7.

**Metadata baru**
- Judul rekomendasi tetap: "If You Hear Hopping, Don't Look Back". Opsi 3 diganti: "I Followed the Rule. Then I Broke It."
- Deskripsi: "I heard hopping behind me on an empty village road. The rule is simple: never look back." Lalu kalimat fiksi dan konteks pocong seperti sebelumnya.
- Cover: adegan 6 (sekitar detik 33), close-up wajah stickman ketakutan.

**Yang perlu dikerjakan ulang**
Video, tabel narasi (cek jatah kata), BGM dan SFX (karena waktu adegan berubah, buat ulang sesuai shot list baru), preview, dan metadata. Tetap tanpa voiceover dan subtitle (saya yang buat). Serahkan semuanya seperti biasa.

**Perbaikan visual khusus Episode 1** (temuan dari hasil sebelumnya, wajib dibereskan)
- Adegan 3 dan 6 (close-up wajah): tambahkan leher, badan, dan lengan (tanpa garis bahu, sama seperti desain di shot lain). Latar jangan polos: pakai pagar atau dinding rumah dengan lampu yang terlihat lengkap bersama kerucut cahayanya. Hapus kerucut cahaya yang melayang.
- Adegan 2 (medium): lengan penuh, memegang HP.
- Adegan 7 (reveal): pocong dengan wajah pucat dan mata cekung terlihat, melompat melewati stickman dengan loop 4 frame. Genderuwo di belakangnya diberi rim light ungu dan mata merah 2x2 pixel supaya terbaca. Perbaiki sambungan latar patah di kiri atas.
- Adegan 8: stickman memegang gerbang dengan lengan dan tangan lengkap di tengah frame, gerbang bergerak menutup minimal 4 frame, lalu jejak di debu seperti rencana. Hapus garis titik-titik kuning di dekat lampu dan di atas frame gerbang.
- Tambahkan gerak latar halus di semua adegan (termasuk close-up lampu) supaya tidak ada layar diam lebih dari 3 detik.

Serahkan Episode 1 yang sudah diperbaiki lengkap dengan: video (tanpa voiceover dan subtitle), naskah rekam berdurasi, audio (gabungan, BGM saja, SFX saja), preview, metadata, dan laporan QA (tabel PASS/FAIL, semua yang bisa diperbaiki sudah diperbaiki).

=============== SELESAI ===============
