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
