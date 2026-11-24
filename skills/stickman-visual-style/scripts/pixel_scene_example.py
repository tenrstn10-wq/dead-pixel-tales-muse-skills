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
