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
