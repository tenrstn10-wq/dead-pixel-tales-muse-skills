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
