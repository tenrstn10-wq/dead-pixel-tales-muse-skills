# Dead Pixel Tales: Muse Skills

Kumpulan **10 skill** dan **prompt** untuk membuat YouTube Shorts storytelling horor stickman pixel art lewat Muse. Target penonton internasional, video vertikal 9:16 berdurasi minimal 40 detik, dengan BGM dan SFX buatan Muse. Voiceover dan subtitle dikerjakan sendiri oleh pembuat konten.

Channel: **Dead Pixel Tales** (`@TheDeadPixelTales`)

## Isi repo

```
dead-pixel-tales-muse-skills/
├── README.md
├── skills/                      10 skill (tiap folder berisi SKILL.md)
│   ├── stickman-story-ideas/        ide cerita, genre acak, aturan variasi
│   ├── stickman-narration-timing/   narasi English dengan jatah kata dan naskah rekam berdurasi
│   ├── stickman-character/          desain stickman klasik, proporsi, sprite referensi
│   ├── stickman-ghost-design/       8 hantu setia legenda, tanpa gore
│   ├── stickman-backgrounds/        latar, palet, location bible
│   ├── stickman-visual-style/       pixel art 9:16, kamera, kualitas visual
│   ├── stickman-audio-director/     BGM + SFX retro, mixing
│   ├── stickman-publish-metadata/   judul, deskripsi, hashtag, cover
│   ├── stickman-channel-signature/  dead pixel dan sting audio khas
│   └── stickman-qa-report/          laporan QA otomatis sebelum serah terima
├── prompts/                     prompt yang dikirim ke Muse (urut nomor)
├── docs/                        alur kerja, catatan perubahan, gambar contoh
└── install/                     installer satu file dan file gabungan untuk ditempel
```

## Alur kerja

1. **Ide:** Muse mengajukan 3-5 ide (genre diputar acak, dengan hook, premis, twist).
2. **Rencana adegan:** setelah ide dipilih, Muse membuat shot list, location bible, dan desain karakter/hantu.
3. **Narasi:** teks English dengan jatah kata per adegan dan naskah rekam berdurasi.
4. **Visual:** video pixel art 9:16 dirender lewat kode.
5. **QA visual:** contact sheet, pemeriksaan semua aturan, perbaikan.
6. **Audio:** BGM + SFX retro sesuai aksi per detik, plus sting khas channel.
7. **Serah terima:** video tanpa audio, naskah rekam, audio (gabungan, BGM saja, SFX saja), preview, metadata, laporan QA.

Setelah itu: rekam voiceover, buat subtitle, gabungkan di editor, upload.

## Cara memasang skill

**A. Salin folder (paling gampang)**
Salin semua folder di `skills/` ke folder skills Muse, misalnya `~/.claude/skills/`, sehingga hasilnya `.../skills/stickman-story-ideas/SKILL.md`, dan seterusnya.

**B. Pakai installer**
```bash
python install/install_skills.py ~/.claude/skills
```
(ganti path dengan folder skills Muse; tanpa argumen dipakai `~/.claude/skills`). Installer hanya menulis file teks, dan membuat gambar contoh bila Pillow terpasang.

**C. Tempel manual**
Buka `install/semua-skill-untuk-paste.md`, tempel isinya ke Muse. Penanda `==== SKILL n/10: nama ====` di dalamnya memudahkan Muse memecahnya per skill.

## Untuk Muse (agen)

Kalau kamu agen yang membaca repo ini: salin tiap folder di `skills/` ke folder skills-mu, lalu baca `prompts/01-setup-prompt-A.md` untuk aturan kerja tetap. Kamu tidak membuat voiceover dan subtitle. Kamu membuat ide, narasi bertimestamp, video, BGM, SFX, metadata, dan laporan QA.

## Cara pakai

1. Pasang skill (di atas).
2. Kirim `prompts/01-setup-prompt-A.md` sekali.
3. Tes pertama: `prompts/03-tes-pertama-prompt-C.md`.
4. Untuk memperbarui Muse yang sudah punya skill versi lama: `prompts/04-update-final-aturan-1-17-dan-episode-1.md`.
5. Konten berikutnya: `prompts/02-konten-baru-prompt-B.md`.

## Aturan utama (ringkas)

- Minimal 40 detik, vertikal 1080x1920, 30 fps, pixel art tajam tanpa blur.
- Shot list wajib: minimal 4 framing berbeda dan 2 close-up; petunjuk hantu sebelum detik 10; payoff akhir terbaca jelas.
- Stickman klasik (tanpa bahu, tanpa pakaian), proporsi tetap, mata selalu terlihat.
- Hantu setia legenda, tanpa gore, dengan ciri wajib dan gerak.
- Narasi English pas dengan durasi, dengan waktu per baris.
- Setiap episode: satu dead pixel merah tersembunyi dan sting audio yang sama di akhir.
- Setiap penyerahan disertai laporan QA PASS/FAIL.

## Skrip

- `skills/stickman-qa-report/scripts/qa_check.py`: pengukuran otomatis video (butuh ffmpeg, numpy, pillow).
- `skills/stickman-character/scripts/sprites_reference.py`: sprite referensi stickman dan 8 hantu.
- `skills/stickman-visual-style/scripts/pixel_scene_example.py`, `skills/stickman-ghost-design/scripts/ghost_sprites_example.py`, `skills/stickman-audio-director/scripts/example_audio_synth.py`: contoh render.

## Lisensi

Belum ditentukan. Tambahkan file `LICENSE` sesuai kebutuhan sebelum repo dipublikasikan.
