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
