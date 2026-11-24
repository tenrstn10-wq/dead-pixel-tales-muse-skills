---
name: stickman-audio-director
description: Buat BGM dan efek suara (SFX) yang sesuai isi video stickman: sinkron dengan aksi per detik, mengikuti genre dan alur emosi cerita, volume aman untuk voiceover yang direkam pengguna. Pakai setiap kali sebuah video stickman selesai atau rencana adegannya sudah ada. Muse tidak membuat voiceover atau subtitle.
---

# Stickman Audio Director

Muse hanya membuat **BGM + SFX**. Voiceover dan subtitle dikerjakan pengguna sendiri.

## Mesin (hybrid)
- **BGM**: lewat model musik kalau tersedia dan lisensinya mengizinkan pemakaian komersial/YouTube. Kalau tidak, sintesis dengan kode (lihat `scripts/example_audio_synth.py`).
- **SFX**: tempel lewat kode di detik yang tepat. Suara bisa sintesis kode (gaya kartun, gratis) atau klip pendek dari model.
- **Gabung, atur volume, pasang ke video**: selalu lewat kode (ffmpeg).
- Jangan pakai lagu/sample berhak cipta (bisa kena klaim Content ID).

## Langkah
1. **Daftar aksi (cue sheet)**. Kalau Muse yang membuat video, ambil dari rencana adegan. Kalau video dari luar, deteksi dari gerakan antar-frame (selisih frame per 0.1 dtk) dan lihat frame kunci. Format:
   `detik | aksi | jenis suara | intensitas (1-3)`
2. **Struktur musik mengikuti adegan.** Ganti bagian musik tepat di pergantian adegan (potong di batas adegan, bukan di tengah). Gunakan tempo tetap (mis. 120 BPM) supaya batas adegan jatuh di hitungan.
3. **Pasang SFX** dari kamus di bawah pada detik di cue sheet.
4. **Atur volume.** Lihat bagian Mixing.
5. **Keluarkan file** dan preview.
6. **Cek.**

## Musik per genre
| Genre | BGM |
|---|---|
| everyday-horror / rules-horror | drone rendah + nada tunggal jarang, banyak ruang kosong, riser sebelum kejutan, kejutan (stinger) tepat di momen muncul |
| twist-reveal | datar dan tenang, lalu berhenti sesaat sebelum twist, baru masuk bagian baru |
| wholesome-scary | seram di awal, lalu melodi hangat (marimba/piano) di penutup |
| dark-comedy | pizzicato / marimba ringan, tempo naik di bagian panik |
| local-legend | tambah instrumen etnik halus (kendang/gamelan sintetis) di bawah drone |

**Mode pixel art (default): gaya audio retro.** BGM berupa synth gelap/chiptune (gelombang kotak dan segitiga, arpeggio lambat untuk horor, lebih cepat untuk komedi). SFX gaya 8-bit untuk aksi (blip, noise pendek, sapuan nada), dipadukan dengan stinger horor yang lebih "dalam". Tetap ikuti tabel di atas untuk strukturnya.

Horor: **diam adalah alat**. Beri jeda tanpa musik 0.5-1 dtk sebelum kejutan. Jangan isi semua detik.

## Kamus aksi -> suara
| Aksi | Suara |
|---|---|
| memukul / mengetuk | benturan pendek (thump + klik), nada turun cepat |
| pintu / lift | gesekan + klik, dentang lift (ding) |
| langkah kaki | thump pendek bergantian kiri-kanan, tempo mengikuti kecepatan gerak |
| lari | langkah rapat + napas kecil (bukan suara orang) |
| loncat / terbang | whoosh naik, boing |
| jatuh / benda jatuh | thump + denting |
| kaget | stinger pendek + getaran (tremolo) |
| keringat / gugup | plip kecil |
| alarm / telepon | bip berulang pola 4 |
| lompatan waktu | whoosh naik + lonceng |
| sosok muncul | riser, diam 0.3 dtk, lalu stinger |
| ruangan sepi | room tone sangat halus |

## Sting khas channel
Setiap video diakhiri sting khas yang sama persis (lihat skill `stickman-channel-signature`, ada contoh kodenya). Taruh di 1.5 detik terakhir setelah payoff dan setelah narasi selesai.

## Mixing
- BGM kecil (sekitar -26 LUFS integrated) supaya voiceover pengguna jelas. Kalau tabel narasi tersedia (skill stickman-narration-timing), turunkan BGM tambahan 4-6 dB di jendela narasi, dan jangan menaruh SFX panjang di bawah kalimat penting.
- SFX peak sekitar -6 dBFS. Peak mix akhir tidak melebihi -1 dBFS.
- Durasi audio **sama persis** dengan durasi video. Fade-out halus di akhir.
- Stereo 44.1 kHz. Langkah kaki dan benda bergerak boleh di-pan kiri-kanan tipis.

## Keluaran
- `bgm_sfx_mix.wav` (gabungan), `bgm_saja.wav`, `sfx_saja.wav`
- `preview_bgm_sfx.mp4` (video + audio baru, tanpa voiceover)
- Daftar cue (detik dan aksi) supaya pengguna bisa meminta geser waktu

## Cek akhir
- Durasi audio = durasi video (ffprobe).
- Tidak ada clipping, tidak ada klik di sambungan.
- Setiap aksi besar di video punya suara; tidak ada SFX di momen tanpa aksi.
- Jujur soal batas: waktu SFX dari analisis gerakan bisa meleset sekitar 0.5 dtk. Tawarkan penyesuaian.

## Referensi kode
`scripts/example_audio_synth.py` adalah contoh lengkap untuk video 15 detik (BGM 3 bagian, SFX, mix, stem). Timeline-nya hanya contoh; ganti dengan cue sheet video yang sedang dikerjakan.
