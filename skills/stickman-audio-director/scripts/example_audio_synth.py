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
