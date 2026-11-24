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
