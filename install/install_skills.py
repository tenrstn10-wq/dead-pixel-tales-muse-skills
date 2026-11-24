#!/usr/bin/env python3
"""
Installer 8 skill stickman untuk Muse.
Cara pakai:  python install_skills.py [folder_skills]
Default folder_skills: ~/.claude/skills  (ganti dengan folder skills Muse kalau beda)
Skrip ini hanya menulis file teks (SKILL.md dan skrip contoh) ke folder tujuan.
Tidak menjalankan perintah lain, kecuali membuat 2 gambar contoh bila Pillow tersedia.
"""
import os, sys, subprocess, shutil

DATA = r'''
<<<FILE stickman-audio-director/SKILL.md>>>
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
<<<FILE stickman-audio-director/scripts/example_audio_synth.py>>>
# CONTOH: timeline di bawah hanya contoh untuk video 15 detik. Ganti cue/durasi sesuai video yang sedang dikerjakan.
# Butuh: numpy, scipy, ffmpeg (untuk memasang audio ke video).
import numpy as np, wave
from scipy.signal import butter, sosfilt

sr = 44100
DUR = 15.0
N = int(sr * DUR)
B = 0.5  # 120 BPM
rng = np.random.default_rng(7)

def buf(): return np.zeros((N, 2))
def tt(d): return np.arange(int(d * sr)) / sr
def noise(d): return rng.standard_normal(int(d * sr))
def hp(x, f): return sosfilt(butter(2, f, 'hp', fs=sr, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'lp', fs=sr, output='sos'), x)
def bp(x, f1, f2): return sosfilt(butter(2, [f1, f2], 'bp', fs=sr, output='sos'), x)
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def sec(b): return b * B

def fade(x, a=0.003, r=0.01):
    n = len(x); na = int(a * sr); nr = int(r * sr)
    e = np.ones(n); e[:na] = np.linspace(0, 1, na); e[-nr:] = np.linspace(1, 0, nr)
    return x * e

def add(b, sig, t, g=1.0, pan=0.0):
    i = int(t * sr)
    if i >= N or i < 0: return
    j = min(N, i + len(sig))
    ang = (pan + 1) * np.pi / 4
    seg = sig[:j - i] * g
    b[i:j, 0] += seg * np.cos(ang)
    b[i:j, 1] += seg * np.sin(ang)

# ---------- instruments ----------
def marimba(f, d=0.5):
    t = tt(d)
    s = (np.sin(2*np.pi*f*t) * np.exp(-t*7) + 0.3*np.sin(2*np.pi*f*4*t) * np.exp(-t*22)
         + 0.1*np.sin(2*np.pi*f*10*t) * np.exp(-t*40))
    return fade(s, 0.002, 0.02)

def bassn(f, d=0.45):
    t = tt(d)
    s = np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t)
    return fade(s * np.exp(-t*4), 0.004, 0.03)

def pad(freqs, d):
    t = tt(d)
    s = sum(np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*f*2.005*t) for f in freqs) / len(freqs)
    return s * np.minimum(1, t/0.8) * np.minimum(1, (d - t)/0.8)

def kick():
    t = tt(0.25); f = 45 + 90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/sr) * np.exp(-t*14)

def snare():
    t = tt(0.2)
    return hp(noise(0.2), 1500) * np.exp(-t*22) * 0.8 + np.sin(2*np.pi*190*t) * np.exp(-t*25) * 0.4

def hat(o=False):
    d = 0.12 if o else 0.04
    return hp(noise(d), 7000) * np.exp(-tt(d) * (25 if o else 90))

# ---------- BGM ----------
bgm = buf()

# A (0-5s): sleepy
for st, ch in [(0, [48, 52, 55]), (2.5, [53, 57, 60])]:
    add(bgm, pad([hz(n) for n in ch], 2.7), st, 0.10)
for b, n in [(0, 64), (1, 67), (2, 69), (3, 67), (4.5, 64), (6, 62), (7, 64), (8, 60)]:
    add(bgm, marimba(hz(n), 0.9), sec(b), 0.35)
for b, n in [(0, 36), (3, 36), (5, 41), (8, 43)]:
    add(bgm, bassn(hz(n), 1.2), sec(b), 0.45)

# B (5-10s): panic build
chords = [(10, 14, 57, [57, 60, 64, 60]), (14, 16, 53, [53, 57, 60, 57]),
          (16, 18, 55, [55, 59, 62, 59]), (18, 20, 52, [52, 56, 59, 56])]
for b0, b1, root, arp in chords:
    k = 0; b = b0
    while b < b1 - 1e-9:
        add(bgm, marimba(hz(arp[k % 4]), 0.35), sec(b), 0.35)
        add(bgm, bassn(hz(root - 12), 0.3), sec(b), 0.40)
        b += 0.5; k += 1
for b in range(10, 20):
    add(bgm, kick(), sec(b), 0.55)
    if b % 2 == 1 and b < 18:
        add(bgm, snare(), sec(b), 0.30)
b = 10.0
while b < 20:
    add(bgm, hat(), sec(b), 0.07 + 0.10 * (b - 10) / 10)
    b += 0.25
b = 18.0
while b < 20:
    add(bgm, snare(), sec(b), 0.18 + 0.35 * (b - 18) / 2)
    b += 0.25
d = 2.0; t = tt(d)
add(bgm, hp(noise(d), 2500) * (t / d) ** 2, sec(16), 0.18)
f = 300 + 1500 * (t / d) ** 2
add(bgm, np.sin(2*np.pi*np.cumsum(f)/sr) * (t / d) ** 2, sec(16), 0.06)

# C (10-14s): run groove
bars = [(20, 36, 43, [72, 76, 79, 76, 72, 79, 76, 72]),
        (24, 43, 50, [71, 74, 79, 74, 71, 74, 79, 74])]
for b0, root, five, pat in bars:
    for i, n in enumerate(pat):
        add(bgm, marimba(hz(n), 0.3), sec(b0 + i * 0.5), 0.30)
        add(bgm, hat(), sec(b0 + i * 0.5), 0.07 if i % 2 == 0 else 0.13)
    for j in range(4):
        add(bgm, bassn(hz(root if j % 2 == 0 else five), 0.4), sec(b0 + j), 0.5)
        if j % 2 == 0: add(bgm, kick(), sec(b0 + j), 0.5)
        else: add(bgm, snare(), sec(b0 + j), 0.35)
# end hit at 14.0s
for n in [60, 64, 67, 72]:
    add(bgm, marimba(hz(n), 1.0), sec(28), 0.35)
add(bgm, bassn(hz(36), 1.0), sec(28), 0.6)
add(bgm, kick(), sec(28), 0.6)
add(bgm, hp(noise(1.0), 5000) * np.exp(-tt(1.0) * 5), sec(28), 0.22)
add(bgm, pad([hz(48), hz(52), hz(55)], 1.0), sec(28), 0.10)

rms = np.sqrt((bgm ** 2).mean())
bgm *= 0.07 / rms

# ---------- SFX ----------
sfx = buf()

def hit():
    t = tt(0.25); f = 170 * np.exp(-t*18) + 50
    return (np.sin(2*np.pi*np.cumsum(f)/sr) * np.exp(-t*16) * 0.9
            + hp(noise(0.25), 1800) * np.exp(-t*60) * 0.5)

def click():
    t = tt(0.05)
    return bp(noise(0.05), 2000, 5000) * np.exp(-t*80)

def beep(d=0.08):
    t = tt(d)
    return fade(np.sin(2*np.pi*2400*t) + 0.3*np.sin(2*np.pi*4800*t), 0.004, 0.008) * 0.6

def snore(d=1.1):
    t = tt(d)
    saw = 2 * ((75 * t * (1 + 0.02*np.sin(2*np.pi*5*t))) % 1) - 1
    s = lp(saw, 350) + 0.5 * lp(noise(d), 600)
    return s * np.sin(np.pi * t / d) ** 2

def whoosh(d, up=True):
    t = tt(d)
    env = np.sin(np.pi * (t / d) ** (0.6 if up else 1.6)) ** 2
    n = bp(noise(d), 600, 6000) * env * 0.6
    f = (400 + 1600 * t / d) if up else (2000 - 1600 * t / d)
    return n + np.sin(2*np.pi*np.cumsum(f)/sr) * env * 0.12

def boing(d=0.5):
    t = tt(d)
    f = 350 + 250 * np.exp(-t*6) * np.sin(2*np.pi*7*t)
    ph = 2*np.pi*np.cumsum(f)/sr
    return (np.sin(ph) + 0.3*np.sin(2*ph)) * np.exp(-t*5) * 0.6

def stab(d=0.5):
    t = tt(d)
    s = 0
    for f0 in [110, 164.8, 220]:
        s = s + (2 * ((f0 * t) % 1) - 1)
    return lp(s, 1200) * np.exp(-t*7) * 0.5

def step():
    t = tt(0.12)
    return np.sin(2*np.pi*95*t) * np.exp(-t*40) * 0.8 + lp(noise(0.12), 1500) * np.exp(-t*50) * 0.4

def plip():
    t = tt(0.1); f = 1400 - 900 * t / 0.1
    return np.sin(2*np.pi*np.cumsum(f)/sr) * np.exp(-t*35)

def clink(f0, d=0.25):
    t = tt(d)
    return np.sin(2*np.pi*f0*t) * np.exp(-t*30) + 0.3*np.sin(2*np.pi*f0*2.7*t) * np.exp(-t*50)

def bell(f0=1568, d=1.0):
    t = tt(d)
    return (np.sin(2*np.pi*f0*t) + 0.4*np.sin(2*np.pi*f0*2.76*t)) * np.exp(-t*5)

# adegan diam (napas/ngorok)
add(sfx, snore(1.1), 0.1, 0.25)
# bunyi bip berulang
for g0 in [1.6, 2.3]:
    for k in range(4):
        add(sfx, beep(), g0 + 0.15 * k, 0.35)
# pukulan/ketukan ke benda
add(sfx, hit(), 3.0, 0.9)
add(sfx, click(), 3.0, 0.5)
# adegan diam (napas/ngorok) lagi
add(sfx, snore(1.0), 3.7, 0.2)
# transisi waktu (whoosh + lonceng)
add(sfx, whoosh(0.35, True), 4.65, 0.6)
add(sfx, bell(1568), 5.0, 0.30)
add(sfx, bell(1175), 5.15, 0.22)
# kaget (stinger + getaran)
add(sfx, stab(), 5.7, 0.7)
add(sfx, boing(), 5.75, 0.6)
t = tt(1.05)
f = 700 + 200 * t
trem = np.sin(2*np.pi*np.cumsum(f)/sr) * (0.5 + 0.5*np.sin(2*np.pi*22*t))
add(sfx, trem * np.minimum(1, t/0.2) * np.minimum(1, (1.05 - t)/0.1), 5.85, 0.12)
# melompat
add(sfx, whoosh(0.3, True), 6.9, 0.5)
add(sfx, boing(), 6.95, 0.6)
add(sfx, step(), 7.25, 0.8)
# gugup (plip)
add(sfx, plip(), 7.5, 0.25, 0.4)
add(sfx, plip(), 8.4, 0.25, -0.4)
# ancang-ancang lalu kabur (whoosh)
add(sfx, whoosh(0.65, True), 9.3, 0.7)
add(sfx, whoosh(0.25, False), 9.95, 0.5)
# berlari (langkah kaki)
for k in range(12):
    add(sfx, step(), 10.05 + 0.29 * k, 0.6 + 0.1 * (k % 2), -0.3 if k % 2 == 0 else 0.3)
for t0 in [11.0, 12.2]:
    add(sfx, bp(noise(0.15), 500, 3000) * np.exp(-tt(0.15) * 20), t0, 0.2)
# rem lalu berhenti
t = tt(0.45)
add(sfx, bp(noise(0.45), 1200, 5000) * np.exp(-t*6) * np.minimum(1, t/0.03), 13.4, 0.5)
add(sfx, step(), 13.9, 1.0)
# benda kecil jatuh
add(sfx, clink(2300), 14.1, 0.3, 0.4)
add(sfx, clink(1800), 14.22, 0.25, 0.5)

peak = np.abs(sfx).max()
sfx *= 0.5 / peak

# ---------- mix & save ----------
mix = bgm + sfx
mp = np.abs(mix).max()
if mp > 0.9:
    mix *= 0.9 / mp

def save(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(pcm.tobytes())

import os
os.makedirs('./output', exist_ok=True)
save('./output/bgm_sfx_mix.wav', mix)
save('./output/bgm_saja.wav', bgm)
save('./output/sfx_saja.wav', sfx)
print('bgm rms', np.sqrt((bgm**2).mean()), 'sfx peak', np.abs(sfx).max(), 'mix peak', np.abs(mix).max())
<<<FILE stickman-backgrounds/SKILL.md>>>
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
<<<FILE stickman-channel-signature/SKILL.md>>>
---
name: stickman-channel-signature
description: Ciri khas channel Dead Pixel Tales yang konsisten di setiap episode: easter egg "dead pixel" merah tersembunyi dan sting audio pendek di akhir. Pakai di setiap episode baru.
---

# Channel Signature (Dead Pixel Tales)

Dua ciri khas yang selalu ada supaya penonton mengenali channel dan punya alasan menonton ulang.

## 1. Easter egg "dead pixel"
- Setiap episode menyembunyikan **satu dead pixel**: kotak 2x2 pixel grid warna merah `#ff2a4d` (boleh berkedip 2 frame sekali).
- Terlihat minimal **1.5 detik** total, tidak muncul di 3 detik pertama, dan tidak menutupi benda penting cerita.
- **Posisi berbeda di setiap episode** (dinding, langit, tanah, pakaian hantu, jendela, bayangan). Catat posisi dan detiknya di `used_ideas.md` dan di laporan QA. Jangan mengulang posisi yang sama dalam 5 episode terakhir.
- Jangan terlalu mencolok, tapi bisa ditemukan oleh penonton yang mencari.
- Komentar sematan default: "Did you spot the dead pixel? Tell me where." (lihat skill publish-metadata).

## 2. Sting audio khas
- Di **1.5 detik terakhir** video, setelah payoff, mainkan sting yang **sama persis** di setiap episode: tiga nada kotak menurun (A5, E5, A4, masing-masing 0.12 dtk) diikuti semburan static pendek, dibuat kasar (bitcrush). Total kurang dari 1.2 detik.
- Peak sting maksimal -9 dBFS, tidak lebih keras dari SFX utama, dan tidak menutupi kalimat narasi terakhir (taruh setelah estimasi selesai narasi).
- Contoh kode:
```python
import numpy as np
def channel_sting(sr=44100):
    out = []
    for f in (880, 659.3, 440):
        t = np.arange(int(0.12 * sr)) / sr
        out.append(np.sign(np.sin(2 * np.pi * f * t)) * 0.5 * np.linspace(1, 0.6, len(t)))
    n = np.random.default_rng(1).standard_normal(int(0.25 * sr)) * np.linspace(0.4, 0, int(0.25 * sr))
    s = np.concatenate(out + [n])
    return np.round(s * 8) / 8  # bitcrush
```

## Aturan
- Kedua ciri khas ini tidak boleh dihapus untuk alasan apa pun kecuali pengguna memintanya.
- Keduanya dicek di laporan QA.
<<<FILE stickman-character/SKILL.md>>>
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
<<<FILE stickman-character/scripts/sprites_reference.py>>>
"""
Sprite referensi pixel art (stickman, pocong, genderuwo) di grid yang sama.
Tujuan: bentuk benar dan konsisten di semua shot. Pakai fungsi ini (atau tiru proporsinya persis).
Butuh: pillow. Jalankan file ini untuk membuat lembar referensi: python sprites_reference.py
Semua gambar memakai pixel kotak tanpa anti-aliasing. Jangan memperbesar sprite; gambar ulang dengan pixel lebih banyak.
"""
import math, random
from PIL import Image, ImageDraw, ImageFont

INK = '#0a0a1a'

def _end(x, y, ang, ln):
    r = math.radians(ang)
    return (round(x + ln * math.sin(r)), round(y + ln * math.cos(r)))

# ---------- STICKMAN: wide (h~34), medium (h~68), close-up lewat closeup() ----------
POSES = {  # sudut dari lurus ke bawah; negatif = ke kiri, positif = ke kanan
    'stand':  dict(la=-24, ra=24, ll=-12, rl=12),
    'walk':   dict(la=30, ra=-30, ll=-24, rl=22),
    'run':    dict(la=60, ra=-60, ll=-45, rl=40),
    'scared': dict(la=-130, ra=130, ll=-16, rl=16),   # tangan terangkat
    'reach':  dict(la=-20, ra=85, ll=-12, rl=12),     # satu tangan ke depan (gerbang, pintu)
}

def stickman(d, cx, feet_y, h, pose='stand', expr='neutral', col='#f0eeff', head_col='#ffffff', outline='#8f89d6'):
    p = POSES[pose]
    head_d = max(10, round(h * 0.29)); r = head_d // 2
    w = 1 if h < 50 else 2
    leg = round(h * 0.31); torso = round(h * 0.40)
    hip_y = feet_y - leg; neck_y = hip_y - torso; hy = neck_y - r
    d.line([(cx, neck_y), (cx, hip_y)], fill=col, width=w)
    sh = neck_y + max(2, round(torso * 0.12)); al = round(h * 0.30)
    for ang in (p['la'], p['ra']): d.line([(cx, sh), _end(cx, sh, ang, al)], fill=col, width=w)
    for ang in (p['ll'], p['rl']): d.line([(cx, hip_y), _end(cx, hip_y, ang, leg)], fill=col, width=w)
    d.ellipse([cx - r, hy - r, cx + r, hy + r], fill=head_col, outline=outline)
    _face(d, cx, hy, head_d, expr)

def _face(d, cx, cy, head_d, expr):
    ex = max(1, round(head_d / 9)); dx = max(2, round(head_d * 0.22)); ey = cy - round(head_d * 0.04)
    for s in (-1, 1):
        x = cx + s * dx
        d.rectangle([x - ex // 2, ey - ex // 2, x - ex // 2 + ex - 1, ey - ex // 2 + ex - 1], fill=INK)
        if head_d >= 16:   # alis
            lift = 3 if expr in ('scared', 'worried') else 2
            inner = (cx + s * (dx - ex), ey - ex * lift - 1); outer = (cx + s * (dx + ex * 2), ey - ex * 2 - 1)
            d.line([inner, outer], fill=INK, width=1)
    my = cy + round(head_d * 0.28)
    if expr in ('scared', 'shocked'):
        d.ellipse([cx - ex, my - ex, cx + ex, my + ex], outline=INK)
    else:
        d.line([(cx - ex * 2, my), (cx + ex * 2, my)], fill=INK, width=1)

def closeup(d, cx, cy, head_d=44, expr='scared', bottom=96, col='#f0eeff', head_col='#ffffff', outline='#8f89d6'):
    """Close-up wajah: WAJIB punya leher, badan, dan lengan yang keluar dari satu titik di bawah leher, sama seperti shot lain (tanpa garis bahu horizontal)."""
    r = head_d // 2
    neck = cy + r; sh = neck + 8                       # titik lengan keluar, sama seperti di shot lain (TANPA garis bahu datar)
    dx = round((bottom - sh) * 0.42)                   # lengan keluar sekitar 23 derajat (sama seperti pose stand)
    d.line([(cx, neck), (cx, bottom)], fill=col, width=2)
    d.line([(cx, sh), (cx - dx, bottom)], fill=col, width=2)
    d.line([(cx, sh), (cx + dx, bottom)], fill=col, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=head_col, outline=outline)
    _face(d, cx, cy, head_d, expr)
    if expr in ('scared', 'terrified'):   # keringat
        for (x, y) in [(cx + r - 4, cy - r + 6), (cx + r - 4, cy - r + 7), (cx + r - 5, cy - r + 8)]:
            d.point((x, y), fill='#7ad7ff')

# ---------- POCONG: wajah pucat + mata hitam cekung + 3 ikatan (WAJIB terlihat) ----------
def pocong(d, cx, feet_y, h=62, air=False):
    fy = feet_y - (5 if air else 0)
    SH, SH2, OUT, FACE = '#ece8d6', '#c8c3ac', '#2a2740', '#b9b8a8'
    hw = round(h * 0.17); bw = round(h * 0.19)
    neck = fy - round(h * 0.64); head_top = fy - h + 6
    d.ellipse([cx - (9 if air else 12), feet_y + 1, cx + (9 if air else 12), feet_y + 3], fill='#07071a')  # bayangan
    d.polygon([(cx - 6, neck), (cx + 6, neck), (cx + bw - 1, neck + 8), (cx + bw, fy - round(h * 0.30)),
               (cx + 7, fy - 4), (cx - 7, fy - 4), (cx - bw, fy - round(h * 0.30)), (cx - bw + 1, neck + 8)], fill=SH, outline=OUT)
    for yy in range(neck + 12, fy - 10, 6):
        d.line([(cx - bw + 3, yy), (cx - bw + 5, yy + 2)], fill=SH2); d.line([(cx + bw - 5, yy + 1), (cx + bw - 3, yy + 3)], fill=SH2)
    d.rectangle([cx + bw - 4, neck + 10, cx + bw - 3, fy - 14], fill=SH2)
    d.ellipse([cx - hw, head_top, cx + hw, neck + 4], fill=SH, outline=OUT)
    d.polygon([(cx - 3, head_top + 1), (cx, head_top - 6), (cx + 3, head_top + 1)], fill=SH, outline=OUT)   # ikatan kepala
    d.line([(cx - 7, neck + 2), (cx + 7, neck + 2)], fill=OUT, width=2)                                       # ikatan leher
    d.line([(cx - bw + 3, fy - 9), (cx + bw - 3, fy - 9)], fill=OUT, width=2)                                 # ikatan kaki
    d.polygon([(cx - 5, fy - 4), (cx, fy + 2), (cx + 5, fy - 4)], fill=SH, outline=OUT)
    d.ellipse([cx - hw + 3, head_top + 5, cx + hw - 3, neck + 1], fill=FACE)                                  # wajah pucat
    d.rectangle([cx + 4, head_top + 8, cx + 6, head_top + 11], fill='#07070f')   # mata cekung kanan
    d.rectangle([cx - 6, head_top + 8, cx - 4, head_top + 11], fill='#07070f')   # mata cekung kiri
    d.point((cx, head_top + 13), fill='#5e5e52')
    d.line([(cx - 3, head_top + 15), (cx + 3, head_top + 15)], fill='#07070f')

# ---------- GENDERUWO: kontras tinggi dengan rim light ungu + mata merah ----------
def genderuwo(d, cx, feet_y, h=72, seed=2):
    rnd = random.Random(seed)
    FUR, FUR2, RIM = '#2b1d1a', '#3f2e28', '#7a63b8'
    top = feet_y - h
    d.polygon([(cx - 10, top + 20), (cx + 10, top + 20), (cx + 18, top + 32), (cx + 16, feet_y - 4), (cx + 7, feet_y),
               (cx - 7, feet_y), (cx - 16, feet_y - 4), (cx - 18, top + 32)], fill=FUR, outline=RIM)
    d.polygon([(cx - 18, top + 30), (cx - 25, top + 52), (cx - 22, feet_y - 2), (cx - 16, top + 46)], fill=FUR, outline=RIM)
    d.polygon([(cx + 18, top + 30), (cx + 25, top + 52), (cx + 22, feet_y - 2), (cx + 16, top + 46)], fill=FUR, outline=RIM)
    d.ellipse([cx - 8, top + 4, cx + 8, top + 24], fill=FUR, outline=RIM)
    for _ in range(70):
        x = rnd.randint(cx - 22, cx + 22); y = rnd.randint(top + 20, feet_y - 3)
        d.point((x, y), fill=FUR2)
    for s in (-1, 1):
        x = cx + s * 4
        d.rectangle([x - 1, top + 12, x, top + 13], fill='#ff2a4d')
        for gx, gy in [(x - 2, top + 12), (x + 1, top + 12), (x - 1, top + 11), (x - 1, top + 14)]:
            d.point((gx, gy), fill='#9c1d3a')
    d.line([(cx - 3, top + 18), (cx + 3, top + 18)], fill='#0a0505')
    d.point((cx - 3, top + 19), fill='#e8e0d0'); d.point((cx + 3, top + 19), fill='#e8e0d0')

# ---------- HANTU LAIN (semua di pustaka stickman-ghost-design) ----------
OUTL = '#2a2740'

def kuntilanak(d, cx, feet_y, h=62):
    fy = feet_y - 3; top = fy - h   # melayang 3 pixel
    HAIR, DRESS, SKIN = '#0b0b14', '#f2efe4', '#cfcab8'
    d.ellipse([cx - 8, feet_y, cx + 8, feet_y + 2], fill='#07071a')
    d.polygon([(cx - 5, top + 22), (cx + 5, top + 22), (cx + 12, fy - 6), (cx + 9, fy), (cx + 5, fy - 4), (cx + 1, fy),
               (cx - 3, fy - 4), (cx - 7, fy), (cx - 12, fy - 6)], fill=DRESS, outline=OUTL)
    d.line([(cx, top + 30), (cx, fy - 6)], fill=SKIN)
    d.line([(cx - 5, top + 24), (cx - 9, top + 46)], fill=SKIN); d.line([(cx + 5, top + 24), (cx + 9, top + 46)], fill=SKIN)
    d.polygon([(cx - 8, top + 8), (cx - 13, fy - 10), (cx - 8, fy - 16), (cx - 5, top + 22)], fill=HAIR)
    d.polygon([(cx + 8, top + 8), (cx + 13, fy - 10), (cx + 8, fy - 16), (cx + 5, top + 22)], fill=HAIR)
    d.ellipse([cx - 7, top + 2, cx + 7, top + 22], fill=HAIR)
    d.rectangle([cx - 2, top + 10, cx + 2, top + 19], fill=SKIN)
    d.point((cx - 1, top + 13), fill='#07070f'); d.point((cx + 1, top + 13), fill='#07070f'); d.point((cx - 1, top + 14), fill='#07070f'); d.point((cx + 1, top + 14), fill='#07070f')

def tuyul(d, cx, feet_y, h=30):
    SK = '#a9b89a'; top = feet_y - h
    d.ellipse([cx - 5, feet_y, cx + 5, feet_y + 2], fill='#07071a')
    d.line([(cx - 2, top + 22), (cx - 3, feet_y)], fill=SK); d.line([(cx + 2, top + 22), (cx + 3, feet_y)], fill=SK)
    d.polygon([(cx - 4, top + 13), (cx + 4, top + 13), (cx + 5, top + 23), (cx - 5, top + 23)], fill=SK, outline=OUTL)
    d.rectangle([cx - 5, top + 21, cx + 5, top + 24], fill='#8c3b3b')
    d.line([(cx - 4, top + 15), (cx - 8, top + 21)], fill=SK); d.line([(cx + 4, top + 15), (cx + 8, top + 20)], fill=SK)
    d.rectangle([cx + 8, top + 19, cx + 9, top + 20], fill='#f2c46d')   # uang receh
    d.polygon([(cx - 7, top + 6), (cx - 11, top + 3), (cx - 7, top + 10)], fill=SK, outline=OUTL)
    d.polygon([(cx + 7, top + 6), (cx + 11, top + 3), (cx + 7, top + 10)], fill=SK, outline=OUTL)
    d.ellipse([cx - 7, top, cx + 7, top + 13], fill=SK, outline=OUTL)
    for s_ in (-1, 1):
        x = cx + s_ * 3
        d.rectangle([x - 1, top + 5, x + 1, top + 8], fill='#07070f'); d.point((x - 1, top + 5), fill='#ffffff')
    d.line([(cx - 2, top + 10), (cx + 2, top + 10)], fill='#07070f')

def shadow_figure(d, cx, feet_y, h=70):
    BLK, RIM = '#05050f', '#7a63b8'; top = feet_y - h
    d.polygon([(cx - 9, top + 14), (cx + 9, top + 14), (cx + 11, top + 40), (cx + 7, feet_y), (cx - 7, feet_y), (cx - 11, top + 40)], fill=BLK, outline=RIM)
    d.line([(cx - 10, top + 16), (cx - 15, feet_y - 12)], fill=RIM); d.line([(cx - 9, top + 16), (cx - 14, feet_y - 12)], fill=BLK, width=3)
    d.line([(cx + 10, top + 16), (cx + 15, feet_y - 12)], fill=RIM); d.line([(cx + 9, top + 16), (cx + 14, feet_y - 12)], fill=BLK, width=3)
    d.ellipse([cx - 6, top, cx + 6, top + 14], fill=BLK, outline=RIM)
    for s_ in (-1, 1):
        d.rectangle([cx + s_ * 3 - 1, top + 6, cx + s_ * 3, top + 7], fill='#f5f5ff')
        d.point((cx + s_ * 3 - 2, top + 6), fill='#6a5aa8'); d.point((cx + s_ * 3 + 1, top + 6), fill='#6a5aa8')

def long_hair_woman(d, cx, feet_y, h=62):
    GOWN, RIM, HAIR, SKIN = '#1a1a26', '#7a63b8', '#07070f', '#cfcab8'; top = feet_y - h
    d.polygon([(cx - 6, top + 22), (cx + 6, top + 22), (cx + 13, feet_y - 3), (cx + 6, feet_y), (cx - 6, feet_y), (cx - 13, feet_y - 3)], fill=GOWN, outline=RIM)
    d.line([(cx + 5, top + 24), (cx + 15, top + 12)], fill=SKIN, width=1); d.rectangle([cx + 15, top + 9, cx + 17, top + 12], fill=SKIN)   # tangan terangkat
    d.line([(cx - 5, top + 24), (cx - 9, top + 46)], fill=SKIN)
    d.ellipse([cx - 9, top + 4, cx + 7, top + 26], fill=HAIR, outline=RIM)           # kepala miring tertutup rambut
    d.polygon([(cx - 9, top + 12), (cx - 12, feet_y - 14), (cx - 6, feet_y - 20), (cx - 5, top + 24)], fill=HAIR)
    d.polygon([(cx + 7, top + 12), (cx + 10, feet_y - 18), (cx + 4, feet_y - 22), (cx + 3, top + 24)], fill=HAIR)
    d.point((cx - 2, top + 14), fill='#cfcab8'); d.point((cx + 1, top + 14), fill='#cfcab8')

def child_ghost(d, cx, feet_y, h=40):
    fy = feet_y - 4; top = fy - h; GOWN, SK = '#e8e8f4', '#d8d8e8'
    d.ellipse([cx - 6, feet_y, cx + 6, feet_y + 2], fill='#07071a')
    d.polygon([(cx - 5, top + 12), (cx + 5, top + 12), (cx + 9, fy - 3), (cx + 6, fy), (cx + 3, fy - 3), (cx, fy), (cx - 3, fy - 3), (cx - 6, fy), (cx - 9, fy - 3)], fill=GOWN, outline=OUTL)
    d.line([(cx - 5, top + 14), (cx - 8, top + 26)], fill=SK); d.line([(cx + 5, top + 14), (cx + 8, top + 26)], fill=SK)
    d.ellipse([cx - 6, top, cx + 6, top + 12], fill=SK, outline=OUTL)
    d.rectangle([cx - 4, top + 4, cx - 2, top + 7], fill='#07070f'); d.rectangle([cx + 2, top + 4, cx + 4, top + 7], fill='#07070f')
    d.line([(cx - 1, top + 10), (cx + 1, top + 10)], fill='#07070f')

def corridor_thing(d, cx, feet_y, h=88):
    """Penunggu lorong: kurus, bungkuk, leher panjang, kepala miring, lutut tertekuk (bukan berjas, bukan tegak lurus)."""
    BLK, RIM = '#0a0a16', '#7a63b8'; top = feet_y - h
    for s_ in (-1, 1):
        d.line([(cx + s_ * 2, top + 50), (cx + s_ * 8, top + 70), (cx + s_ * 4, feet_y)], fill=BLK, width=2)           # kaki tertekuk
        d.line([(cx + s_ * 5, top + 20), (cx + s_ * 14, top + 44), (cx + s_ * 12, feet_y - 6)], fill=BLK, width=2)    # lengan panjang menekuk
    d.polygon([(cx - 5, top + 18), (cx + 5, top + 18), (cx + 4, top + 50), (cx - 4, top + 50)], fill=BLK, outline=RIM)
    d.line([(cx, top + 18), (cx + 5, top + 9)], fill=BLK, width=2)                                                       # leher panjang
    d.ellipse([cx + 1, top, cx + 10, top + 10], fill=BLK, outline=RIM)                                                   # kepala miring
    d.line([(cx + 3, top + 5), (cx + 4, top + 5)], fill='#f5f5ff'); d.line([(cx + 7, top + 5), (cx + 8, top + 5)], fill='#f5f5ff')

GHOSTS = {'pocong': pocong, 'kuntilanak': kuntilanak, 'genderuwo': genderuwo, 'tuyul': tuyul, 'bayangan': shadow_figure,
          'wanita_rambut_panjang': long_hair_woman, 'anak_hantu': child_ghost, 'penunggu_lorong': corridor_thing}

if __name__ == '__main__':
    W, H, S = 300, 100, 4
    img = Image.new('RGB', (W, H), '#141233'); d = ImageDraw.Draw(img)
    d.rectangle([0, 90, W, H], fill='#10122a'); d.line([0, 90, W, 90], fill='#1f1a45')
    stickman(d, 14, 88, 34, 'walk')
    stickman(d, 46, 88, 68, 'reach', 'worried')
    stickman(d, 82, 88, 68, 'scared', 'scared')
    closeup(d, 135, 36, 40, 'scared', bottom=99)
    pocong(d, 188, 88); pocong(d, 218, 88, air=True)
    genderuwo(d, 266, 88)
    big = img.resize((W * S, H * S), Image.NEAREST)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 14)
        bd = ImageDraw.Draw(big)
        for t, x in [('WIDE', 14), ('MEDIUM', 46), ('SCARED', 82), ('CLOSE-UP', 135), ('POCONG', 203), ('GENDERUWO', 266)]:
            w = bd.textlength(t, font=f); bd.text((min(max(x * S - w / 2, 2), W * S - w - 2), 4), t, fill='#8f89d6', font=f)
    except Exception:
        pass
    big.save('sprites_reference_sheet.png'); print('ok')

    # ---- lembar semua hantu (skala dengan stickman) ----
    W2, H2, S2 = 330, 108, 4
    im2 = Image.new('RGB', (W2, H2), '#141233'); g = ImageDraw.Draw(im2)
    g.rectangle([0, 100, W2, H2], fill='#10122a'); g.line([0, 100, W2, 100], fill='#1f1a45')
    placed = [('POCONG', pocong, 20), ('KUNTILANAK', kuntilanak, 52), ('GENDERUWO', genderuwo, 92), ('TUYUL', tuyul, 132),
              ('BAYANGAN', shadow_figure, 164), ('RAMBUT', long_hair_woman, 198), ('ANAK', child_ghost, 232), ('LORONG', corridor_thing, 262)]
    for name, fn, x in placed: fn(g, x, 98)
    stickman(g, 306, 98, 34, 'stand')
    big2 = im2.resize((W2 * S2, H2 * S2), Image.NEAREST)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 12)
        bd = ImageDraw.Draw(big2)
        for i, (name, fn, x) in enumerate(placed + [('STICKMAN', None, 306)]):
            w = bd.textlength(name, font=f); bd.text((min(max(x * S2 - w / 2, 2), W2 * S2 - w - 2), 101 * S2 + 8), name, fill='#8f89d6', font=f)
    except Exception:
        pass
    big2.save('ghosts_reference_sheet.png'); print('ok2')
<<<FILE stickman-ghost-design/SKILL.md>>>
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
<<<FILE stickman-ghost-design/scripts/ghost_sprites_example.py>>>
# Contoh sprite hantu pixel art (pocong, kuntilanak, genderuwo). Butuh: pillow.
import random
from PIL import Image, ImageDraw, ImageFont

random.seed(5)
GW, GH, S = 108, 66, 8
img = Image.new('RGB', (GW, GH), '#0b0d24')
d = ImageDraw.Draw(img)
for y in range(GH):
    for x in range(GW):
        if y > 10 and (x + y) % 2 == 0 and y % 9 == 0:
            img.putpixel((x, y), (16, 18, 44))
d.rectangle([0, 58, GW, GH], fill='#10122a')
d.line([0, 58, GW, 58], fill='#1f1a45')
for _ in range(25):
    img.putpixel((random.randrange(GW), random.randrange(0, 20)), (150, 146, 210))

OUT = '#23202e'
def ox(o): return o  # offset x panel

# ---------- POCONG (panel 1) ----------
o = 0; cx = o + 18
SHROUD, SH2, FACE = '#ece8d6', '#c8c3ac', '#a9a89a'
d.polygon([(cx-6,26),(cx+6,26),(cx+10,32),(cx+11,44),(cx+7,55),(cx-7,55),(cx-11,44),(cx-10,32)], fill=SHROUD, outline=OUT)
d.ellipse([cx-8, 8, cx+8, 28], fill=SHROUD, outline=OUT)
d.polygon([(cx-3,8),(cx,2),(cx+3,8)], fill=SHROUD, outline=OUT)          # simpul kepala
d.line([cx-7,27,cx+7,27], fill=OUT)                                       # ikatan leher
d.polygon([(cx-6,55),(cx,60),(cx+6,55)], fill=SHROUD, outline=OUT)       # simpul kaki
d.line([cx-7,53,cx+7,53], fill=OUT)                                       # ikatan kaki
d.ellipse([cx-5, 13, cx+5, 25], fill=FACE)                                # wajah pucat
d.rectangle([cx-4, 17, cx-2, 19], fill='#07070f'); d.rectangle([cx+2, 17, cx+4, 19], fill='#07070f')
d.line([cx-2,23,cx+2,23], fill='#07070f')
for yy in range(31, 52, 5):                                               # lipatan kain
    d.line([cx-8, yy, cx-6, yy+2], fill=SH2); d.line([cx+6, yy+1, cx+8, yy+3], fill=SH2)
d.rectangle([cx-9, 33, cx-8, 50], fill=SH2)
d.line([cx-9,59,cx+9,59], fill='#07071a')

# ---------- KUNTILANAK (panel 2) ----------
cx = 54
d.polygon([(cx-6,26),(cx+6,26),(cx+13,56),(cx-13,56)], fill='#f2efe4', outline=OUT)   # gaun putih
d.line([cx-9,50,cx-8,56], fill='#cfcab8'); d.line([cx+8,46,cx+10,56], fill='#cfcab8'); d.line([cx,40,cx,56], fill='#dedacb')
d.line([cx-6,28,cx-9,46], fill='#d9d5c4'); d.line([cx+6,28,cx+9,46], fill='#d9d5c4')    # lengan pucat
d.ellipse([cx-8, 8, cx+8, 27], fill='#0b0b14')                                          # rambut
for hx in range(cx-11, cx+12, 2):                                                       # rambut panjang
    d.line([hx, 12, hx + random.choice([-1,0,1]), random.randint(44,54)], fill='#0b0b14')
d.rectangle([cx-9, 20, cx-5, 50], fill='#0b0b14'); d.rectangle([cx+5, 20, cx+9, 50], fill='#0b0b14')
d.rectangle([cx-3, 14, cx+3, 22], fill='#cfcab8')                                       # celah wajah pucat
d.point((cx-2,17), fill='#07070f'); d.point((cx+2,17), fill='#07070f')
d.rectangle([cx-14, 56, cx+14, 56], fill='#e4e0d0')

# ---------- GENDERUWO (panel 3) ----------
cx = 90
FUR, FUR2 = '#2b1d1a', '#3b2a24'
d.polygon([(cx-9,22),(cx+9,22),(cx+15,34),(cx+13,54),(cx+6,58),(cx-6,58),(cx-13,54),(cx-15,34)], fill=FUR)
d.ellipse([cx-6, 8, cx+6, 22], fill=FUR)
d.polygon([(cx-15,30),(cx-20,48),(cx-17,57),(cx-13,52)], fill=FUR)                     # lengan kiri
d.polygon([(cx+15,30),(cx+20,48),(cx+17,57),(cx+13,52)], fill=FUR)                     # lengan kanan
for _ in range(60):                                                                    # bulu kasar
    x = random.randint(cx-19, min(cx+17, GW-3)); y = random.randint(10, 58)
    if img.getpixel((x, y)) == (43, 29, 26): d.point((x + random.choice([-1,1]), y + random.choice([-1,0])), fill=FUR2)
d.rectangle([cx-4, 13, cx-2, 14], fill='#ff2a4d'); d.rectangle([cx+2, 13, cx+4, 14], fill='#ff2a4d')
d.line([cx-3,18,cx+3,18], fill='#0a0505')

big = img.resize((GW*S, GH*S), Image.NEAREST)
try:
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 22)
    bd = ImageDraw.Draw(big)
    for name, cxp in [('POCONG', 18), ('KUNTILANAK', 54), ('GENDERUWO', 90)]:
        w = bd.textlength(name, font=f)
        bd.text((cxp*S - w/2, (GH-5)*S), name, fill='#8f89d6', font=f)
except Exception as e:
    pass
big.save('ghost_sprites_sample.png')
print('ok')
<<<FILE stickman-narration-timing/SKILL.md>>>
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
<<<FILE stickman-publish-metadata/SKILL.md>>>
---
name: stickman-publish-metadata
description: Siapkan metadata upload YouTube Shorts dalam bahasa Inggris untuk video stickman: judul, deskripsi, hashtag, komentar sematan, dan saran frame cover. Pakai setelah video dan narasi selesai, tiap kali satu episode siap diunggah.
---

# Stickman Publish Metadata

Tugas: setelah satu episode selesai, Muse menyiapkan semua teks untuk upload. Semua dalam **bahasa Inggris sederhana** (penonton internasional).

## Judul
- Maksimal 60 karakter (judul Shorts mudah terpotong).
- Memancing rasa penasaran dan sesuai isi video. Jangan menjanjikan sesuatu yang tidak ada di video.
- Beri 3 pilihan, tandai satu yang direkomendasikan. POV judul sama dengan narasi.
- **Variasikan pola judul** antar-episode (pertanyaan, pernyataan janggal, "aturan", dll). Jangan memakai satu template judul yang sama terus.

## Deskripsi
- 1-2 kalimat teaser tanpa membocorkan twist. **POV harus sama dengan narasi** (kalau narasi pakai "I", deskripsi dan judul juga memakai "I", bukan "He").
- Tambahkan kalimat penanda fiksi: "This is a fictional story." Jangan pernah mengklaim "kisah nyata" atau "true story" kalau tidak benar.
- Untuk hantu lokal, tambahkan 1 kalimat konteks budaya singkat.
- Hashtag 3-5 saja, mis. #shorts #horror #scarystory #pixelart #stickman. Tiga hashtag pertama tampil di atas judul, jadi urutkan dari yang paling relevan.

## Komentar sematan
Default (ciri khas channel): "Did you spot the dead pixel? Tell me where." Boleh ditambah satu pertanyaan cerita pendek di kalimat kedua (mis. "Would you have looked back?"). Maksimal 2 kalimat.

## Frame cover
Sebutkan detik frame untuk cover/thumbnail Shorts:
- Pilih close-up wajah karakter yang ketakutan, atau teaser (siluet, mata merah, bayangan) **sebelum wujud penuh**.
- **Jangan** memakai frame yang menampilkan twist atau lebih dari satu makhluk.
- Harus tetap terbaca saat kecil (thumbnail sekitar 150 px): kontras tinggi, satu fokus.

## Pengingat untuk pengguna
- Cek di YouTube Studio opsi pengungkapan konten buatan/AI, dan ikuti aturan terbaru yang berlaku. Muse tidak memutuskan ini untuk pengguna.
- Tidak memakai musik atau suara berhak cipta.

## Output (satu blok rapi)
Judul (3 pilihan + rekomendasi) | Deskripsi | Hashtag | Komentar sematan | Frame cover (detik) | Pengingat
<<<FILE stickman-qa-report/SKILL.md>>>
---
name: stickman-qa-report
description: Laporan QA wajib di setiap penyerahan konten stickman. Muse mengukur hasil video dan audio, memeriksa semua aturan, memperbaiki yang gagal, lalu menyerahkan laporan singkat bersama hasilnya. Pakai sebelum menyerahkan episode apa pun.
---

# Stickman QA Report

Sebelum menyerahkan konten ke pengguna, Muse memeriksa hasilnya sendiri dan melampirkan laporan. Yang gagal diperbaiki dulu.

## Langkah
1. **Ukur otomatis.** Jalankan `scripts/qa_check.py video.mp4` (atau buat pengukuran setara kalau skrip tidak bisa dijalankan). Skrip mengukur: resolusi (1080x1920), fps (30), durasi (minimal 40 dtk), durasi audio sama dengan video, peak audio (maks -1.0 dBFS), loudness, jumlah perpindahan shot, layar diam terlama (maks 3 dtk), dan kerapian grid pixel.
2. **Periksa dari shot list dan rencana** (hal yang tidak bisa diukur mesin). Laporkan nilainya, jangan hanya "OK":
   - jumlah jenis framing berbeda (minimal 4), jumlah close-up (minimal 2), tidak ada dua framing sama berurutan
   - detik petunjuk hantu pertama (maksimal detik 10) dan detik wujud penuh (minimal 60% durasi)
   - payoff akhir: detik mulai, lama ditahan (minimal 2 dtk), tinggi objek bukti (minimal 8% tinggi frame)
   - mata stickman terlihat di semua shot yang menghadap kamera
   - gerak latar halus ada (minimal 2 elemen)
   - dead pixel: detik dan posisinya (terlihat minimal 1.5 dtk)
   - sting audio khas ada di akhir
   - narasi: semua status OK, POV konsisten, estimasi selesai tidak melewati batas akhir
   - metadata lengkap dan frame cover tidak membocorkan twist
   - **kualitas visual (tinjau contact sheet `qa_check.py --sheet sheet.jpg`):** close-up punya leher, badan, dan lengan (tanpa garis bahu), lengan dan tangan lengkap, tidak ada kerucut cahaya melayang, tidak ada sambungan latar patah, tidak ada garis titik-titik atau pixel liar, pocong berwajah dan bergerak, makhluk gelap punya rim light
3. **Tulis laporan** berformat tabel: Cek | Nilai | Aturan | PASS/FAIL.
4. **Perbaiki semua FAIL yang bisa diperbaiki**, ukur ulang, lalu perbarui laporan. Jangan menyerahkan dengan FAIL yang masih bisa diperbaiki. Kalau ada FAIL yang tidak bisa diperbaiki, jelaskan alasannya dengan jujur.
5. **Serahkan** hasil beserta laporan akhir (maksimal sekitar 15 baris) dan satu kalimat daftar apa yang diperbaiki.

## Kejujuran laporan
- Hanya laporkan yang benar-benar diukur atau dibaca dari shot list. Hal yang tidak bisa dinilai mesin (mis. enak tidaknya suara) tulis "tidak diukur".
- Jangan menulis PASS tanpa nilai.
<<<FILE stickman-qa-report/scripts/qa_check.py>>>
#!/usr/bin/env python3
"""
QA otomatis untuk video Shorts stickman pixel art.
Pakai:  python qa_check.py video.mp4 [--min-duration 40] [--grid-scale 8]
Butuh: ffmpeg, ffprobe, numpy, pillow.
Mengukur hal yang bisa diukur mesin. Hal yang butuh shot list (jenis framing, waktu petunjuk hantu,
posisi dead pixel) dilaporkan sendiri oleh Muse dari shot list-nya.
"""
import argparse, json, re, subprocess, sys
import numpy as np
from PIL import Image

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate,duration",
             "-of", "json", path])
    j = json.loads(r.stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    num, den = v["r_frame_rate"].split("/")
    return {"w": int(v["width"]), "h": int(v["height"]), "fps": float(num) / float(den),
            "dur": float(j["format"]["duration"]), "has_audio": a is not None,
            "audio_dur": float(a["duration"]) if a and a.get("duration") else None}

def loudness(path):
    r = run(["ffmpeg", "-i", path, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"])
    txt = r.stderr
    tail = txt[txt.rfind("Summary:"):] if "Summary:" in txt else txt
    I = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    P = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return (float(I.group(1)) if I else None, float(P.group(1)) if P else None)

def small_frames(path, fps=4, w=135, h=240):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h},format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w).astype(float)

def grid_diff(path, dur, scale):
    diffs = []
    for t in np.linspace(1, max(1, dur - 1), 5):
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        import io
        im = Image.open(io.BytesIO(r.stdout)).convert("RGB")
        a = np.asarray(im).astype(int)
        sm = im.resize((im.width // scale, im.height // scale), Image.NEAREST).resize(im.size, Image.NEAREST)
        diffs.append(np.abs(a - np.asarray(sm).astype(int)).mean())
    return float(np.mean(diffs))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--min-duration", type=float, default=40)
    ap.add_argument("--grid-scale", type=int, default=8)
    ap.add_argument("--sheet", default=None, help="simpan contact sheet 1 frame/detik ke file ini (mis. sheet.jpg)")
    a = ap.parse_args()
    if a.sheet:
        d0 = probe(a.video)['dur']; cols = 6; rows_n = int(-(-d0 // cols))
        run(['ffmpeg','-v','error','-y','-i',a.video,'-vf',f'fps=1,scale=180:-1,tile={cols}x{rows_n}','-frames:v','1',a.sheet])
        print('Contact sheet disimpan:', a.sheet)
    rows = []
    def add(name, value, ok, rule): rows.append((name, value, "PASS" if ok else "FAIL", rule))

    p = probe(a.video)
    add("Resolusi", f"{p['w']}x{p['h']}", (p['w'], p['h']) == (1080, 1920), "1080x1920 (9:16)")
    add("FPS", f"{p['fps']:.0f}", abs(p['fps'] - 30) < 0.5, "30")
    add("Durasi video", f"{p['dur']:.1f} dtk", p['dur'] >= a.min_duration, f">= {a.min_duration:.0f} dtk")
    if p["has_audio"]:
        if p["audio_dur"]:
            add("Durasi audio = video", f"{p['audio_dur']:.1f} vs {p['dur']:.1f}", abs(p['audio_dur'] - p['dur']) < 0.3, "selisih < 0.3 dtk")
        I, pk = loudness(a.video)
        if pk is not None: add("Peak audio", f"{pk:.1f} dBFS", pk <= -1.0, "<= -1.0 dBFS")
        if I is not None: add("Loudness", f"{I:.1f} LUFS", -30 <= I <= -14, "-30 s/d -14 LUFS")
    else:
        add("Audio", "tidak ada", False, "harus ada BGM + SFX")

    fr = small_frames(a.video)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))          # per 0.25 dtk
    cuts = int((d > 8).sum())
    add("Perpindahan shot (cut)", f"{cuts}", cuts >= 5, ">= 5 untuk 4+ framing (cek shot list)")
    still, longest = 0, 0
    for x in d:
        still = still + 1 if x < 0.02 else 0
        longest = max(longest, still)
    add("Layar diam terlama", f"{longest * 0.25:.1f} dtk", longest * 0.25 <= 3.0, "<= 3 dtk (harus ada gerak/perubahan)")
    gd = grid_diff(a.video, p["dur"], a.grid_scale)
    add("Kerapian grid pixel", f"selisih {gd:.2f}", gd < 0.5, "< 0.5 (pixel kotak seragam)")

    w = max(len(r[0]) for r in rows)
    print("LAPORAN QA OTOMATIS")
    for n, v, s, rule in rows:
        print(f"{s:4} | {n:<{w}} | {v:<18} | {rule}")
    fails = [r for r in rows if r[2] == "FAIL"]
    print("\nHASIL:", "SEMUA LOLOS" if not fails else f"{len(fails)} GAGAL: " + ", ".join(r[0] for r in fails))
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
<<<FILE stickman-story-ideas/SKILL.md>>>
---
name: stickman-story-ideas
description: Cari ide cerita storytelling stickman untuk YouTube Shorts (penonton internasional, 40 detik ke atas). Pakai setiap kali pengguna minta ide/konten baru. Genre diputar acak, ada hook kuat, twist, dan daftar ide terpakai supaya tidak berulang.
---

# Stickman Story Ideas

Tugas: tiap kali pengguna mau bikin konten baru, Muse yang mencari idenya.

## Aturan dasar
- Penonton: orang luar negeri. Judul, hook, dan narasi dalam **bahasa Inggris sederhana** (level B1, kalimat pendek).
- Format: YouTube Shorts vertikal, **minimal 40 detik** (target 40-55 detik, menyesuaikan cerita), 7-9 adegan.
- Cerita **orisinal**. Jangan menyalin creepypasta, film, atau cerita yang sudah ada.
- Tanpa gore, kekerasan grafis, atau konten seksual. Seram lewat suasana, suara, dan twist.
- Setting harus dikenal semua orang (lift, hotel, shift malam, rumah kosong, pesan dari nomor asing, dll). Horor lokal Indonesia boleh sesekali, dengan 1 kalimat pengantar untuk penonton luar.

## Alur
1. Baca `used_ideas.md` (daftar ide terpakai). Kalau belum ada, buat file kosong.
2. Pilih genre secara acak dari putaran ini, dan jangan genre yang sama dua kali berturut-turut:
   - everyday-horror (tempat sehari-hari jadi seram)
   - rules-horror (cerita "aturan": "if you hear X, never do Y")
   - twist-reveal (yang disangka hantu ternyata manusia, atau sebaliknya)
   - wholesome-scary (seram di awal, hangat di akhir)
   - dark-comedy (seram tapi lucu)
   - local-legend (legenda Indonesia + 1 kalimat pengantar; sesekali saja)
3. Ajukan **3-5 ide**. Untuk tiap ide tulis:
   - Judul (English)
   - Genre
   - Hook: kalimat 3 detik pertama (English, maks 12 kata, memicu pertanyaan)
   - Premis: 1 kalimat
   - Twist / ending
   - Setting
   - Perkiraan jumlah adegan dan durasi
   - Kenapa orang nonton sampai habis atau mengulang
4. Ide yang tidak lolos saringan di bawah jangan diajukan.
5. Setelah pengguna memilih (atau bilang "pilih sendiri" -> pilih yang paling kuat), catat ke `used_ideas.md`: tanggal, judul, genre, hook, dan lima atribut variasi: lokasi, jenis hantu/makhluk, pola twist, tempo, palet warna, plus posisi dead pixel (lihat skill stickman-channel-signature).

## Saringan kualitas (semua harus lolos)
- Hook memicu rasa penasaran dalam 3 detik.
- Ada twist atau belokan yang jelas.
- Muat di 40-55 detik tanpa terasa dipadatkan.
- Tidak mirip ide di `used_ideas.md` (judul, premis, maupun pola twist).
- Lolos aturan variasi di bawah.
- Punya alur cerita yang jelas (setup, eskalasi, twist), bukan sekadar rangkaian adegan seram acak.
- Tidak memakai tokoh nyata, merek, atau karakter berhak cipta.
- Bisa dipahami tanpa budaya tertentu.

## Aturan variasi antar-episode
Tujuannya supaya channel tidak terlihat seperti video berbasis template yang berulang.
- Bandingkan ide baru dengan 5 episode terakhir di `used_ideas.md`.
- Ide baru harus berbeda minimal **3 dari 5** atribut: lokasi, jenis hantu/makhluk, pola twist, tempo (gaya hook dan akhir), palet warna.
- Pola twist yang sama tidak boleh dipakai di 3 episode berturut-turut.
- Boleh tetap sama: karakter stickman, gaya pixel art, dan format. Itu identitas channel.
- Tandai cerita sebagai fiksi. Jangan mengklaim kisah nyata.

## Struktur cerita 40-55 detik
- 0-3 dtk: hook
- 3-12 dtk: setup (siapa, di mana, apa yang normal)
- 12-30 dtk: eskalasi (2-3 kejadian yang makin aneh)
- 30-42 dtk: puncak
- 42-50 dtk: twist / penutup
- Kalimat terakhir sebaiknya nyambung ke hook supaya penonton mengulang.

## Aturan visual hook dan payoff
- Hook harus punya sisi visual, bukan hanya kalimat: elemen janggal di layar pada detik 0-3.
- Petunjuk pertama makhluk muncul paling lambat detik 8-10. Wujud penuh tidak sebelum sekitar 60% durasi.
- Twist harus bisa **dilihat**: rancang satu gambar bukti yang jelas dan besar di akhir (mis. jejak, benda, bayangan), bukan detail kecil.
- Satu aturan legenda dilanggar tepat satu kali, dan pelanggarannya terjadi di puncak, bukan di tengah.

## Tren
Boleh cek format horor pendek yang sedang ramai lewat pencarian, tapi hanya untuk mengambil pola/format, bukan ceritanya.
<<<FILE stickman-visual-style/SKILL.md>>>
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
<<<FILE stickman-visual-style/scripts/pixel_scene_example.py>>>
# Contoh render pixel art 9:16 lewat kode. Grid 135x240, diperbesar 8x (nearest neighbor) jadi 1080x1920.
# Butuh: pillow. Jalankan: python pixel_scene_example.py
import random
from PIL import Image, ImageDraw

W, H, S = 135, 240, 8
random.seed(3)
img = Image.new('RGB', (W, H), '#0b0d24')
d = ImageDraw.Draw(img)

def hexrgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

# --- langit: pita warna + dithering di perbatasan ---
sky = ['#0b0d24', '#141233', '#1f1a45', '#2d2259', '#3f2c6b']
horizon = 150
band = horizon / len(sky)
for y in range(horizon):
    i = min(len(sky) - 1, int(y / band))
    frac = (y / band) - i
    for x in range(W):
        c = sky[i]
        if i + 1 < len(sky) and frac > 0.75 and (x + y) % 2 == 0:
            c = sky[i + 1]
        img.putpixel((x, y), hexrgb(c))

# bintang
for _ in range(45):
    x, y = random.randrange(W), random.randrange(0, 90)
    img.putpixel((x, y), hexrgb(random.choice(['#c9c3ff', '#8f89d6', '#ffffff'])))

# bulan
d.ellipse([92, 22, 110, 40], fill='#f4e9b8')
for p in [(98, 28), (103, 33), (100, 36), (105, 27)]:
    img.putpixel(p, hexrgb('#d9c98f'))

# --- gedung belakang (siluet) ---
x = 0
while x < W:
    bw = random.randint(10, 18); bh = random.randint(30, 70)
    d.rectangle([x, horizon + 14 - bh, x + bw, horizon + 14], fill='#171230')
    for wy in range(horizon + 14 - bh + 4, horizon + 10, 6):
        for wx in range(x + 2, x + bw - 2, 4):
            if random.random() < 0.18:
                d.rectangle([wx, wy, wx + 1, wy + 2], fill='#f2c46d')
    x += bw + 1

# gedung kiri dengan papan neon (tanpa teks)
d.rectangle([0, 112, 46, 170], fill='#1b1538')
d.rectangle([0, 112, 46, 114], fill='#2a2050')
for wy in range(122, 165, 12):
    for wx in range(5, 42, 12):
        lit = random.random() < 0.3
        d.rectangle([wx, wy, wx + 7, wy + 7], fill='#f2c46d' if lit else '#262050')
d.rectangle([8, 98, 38, 108], fill='#120e2b', outline='#ff4f9a')
d.line([10, 103, 36, 103], fill='#4fe3ff')
d.line([10, 100, 22, 100], fill='#ff4f9a')

# --- tanah ---
d.rectangle([0, 170, W, H], fill='#10122a')
d.rectangle([0, 170, W, 172], fill='#1a1b3d')
for y in range(180, H, 10):
    d.line([0, y, W, y], fill='#13152f')

# --- cahaya lampu jalan (dither) ---
lx, ly = 52, 176
for y in range(120, 215):
    for x in range(14, 100):
        dist = ((x - lx) ** 2 + ((y - 128) * 0.7) ** 2) ** 0.5
        if dist < 36 and (x + y) % 2 == 0 and y > 128:
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (min(255, r + 38), min(255, g + 32), min(255, b + 10)))
d.line([lx, 128, lx, 176], fill='#0a0a1a')
d.rectangle([lx - 3, 124, lx + 3, 128], fill='#f7d98b')

# --- kabut tipis ---
for y in range(150, 200, 7):
    for x in range(W):
        if (x + y // 7) % 3 == 0 and (x + y) % 2 == 0:
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (min(255, r + 22), min(255, g + 20), min(255, b + 34)))

# --- stickman klasik (pixel) ---
sx, sy = 72, 172  # titik kaki (garis terang di adegan gelap, hitam di adegan terang)
d.ellipse([sx - 5, sy - 34, sx + 4, sy - 25], fill='#ffffff', outline='#8f89d6')
img.putpixel((sx - 2, sy - 30), hexrgb('#0a0a1a')); img.putpixel((sx + 1, sy - 30), hexrgb('#0a0a1a'))
d.line([sx, sy - 24, sx, sy - 10], fill='#f0eeff')            # badan
d.line([sx, sy - 22, sx - 7, sy - 15], fill='#f0eeff')        # tangan kiri
d.line([sx, sy - 22, sx + 7, sy - 16], fill='#f0eeff')        # tangan kanan
d.line([sx, sy - 10, sx - 5, sy], fill='#f0eeff')             # kaki kiri
d.line([sx, sy - 10, sx + 5, sy], fill='#f0eeff')             # kaki kanan
d.line([sx - 8, sy + 1, sx + 8, sy + 1], fill='#07071a')      # bayangan

# --- sosok bayangan di ujung jalan ---
fx, fy = 112, 170
d.rectangle([fx - 4, fy - 44, fx + 4, fy], fill='#05050f')
d.ellipse([fx - 5, fy - 54, fx + 5, fy - 43], fill='#05050f')
img.putpixel((fx - 2, fy - 49), hexrgb('#ff2a4d')); img.putpixel((fx + 2, fy - 49), hexrgb('#ff2a4d'))

img.resize((W * S, H * S), Image.NEAREST).save('pixel_style_sample.png')
print('ok')
'''

def main():
    dest = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/.claude/skills")
    os.makedirs(dest, exist_ok=True)
    parts = DATA.split("<<<FILE ")[1:]
    written = []
    for part in parts:
        path, rest = part.split(">>>\n", 1)
        path = path.strip()
        if path.startswith("/") or ".." in path.split("/"):
            continue
        out = os.path.join(dest, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(rest.rstrip() + "\n")
        written.append(path)
    skills = sorted({p.split("/")[0] for p in written})
    print("Terpasang", len(skills), "skill di", dest)
    for s in skills:
        ok = os.path.exists(os.path.join(dest, s, "SKILL.md"))
        print(" -", s, "OK" if ok else "SKILL.md TIDAK ADA")
    # gambar contoh (opsional, butuh Pillow)
    jobs = [("stickman-visual-style", "pixel_scene_example.py", "pixel_style_sample.png", "pixel-style-sample.png"),
            ("stickman-ghost-design", "ghost_sprites_example.py", "ghost_sprites_sample.png", "ghost_sprites_sample.png"),
            ("stickman-character", "sprites_reference.py", "sprites_reference_sheet.png", "sprites_reference_sheet.png"),
            ("stickman-character", "sprites_reference.py", "ghosts_reference_sheet.png", "ghosts_reference_sheet.png")]
    for skill, script, made, final in jobs:
        sdir = os.path.join(dest, skill, "scripts")
        rdir = os.path.join(dest, skill, "references")
        try:
            os.makedirs(rdir, exist_ok=True)
            subprocess.run([sys.executable, script], cwd=sdir, check=True, capture_output=True, timeout=60)
            shutil.move(os.path.join(sdir, made), os.path.join(rdir, final))
            print("Gambar contoh dibuat:", skill + "/references/" + final)
        except Exception:
            print("Gambar contoh dilewati (butuh Pillow):", skill)

if __name__ == "__main__":
    main()
