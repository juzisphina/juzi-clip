"""Draw the 橘子存片 / JuziClip icon.

  python tools/build_icon.py a      # the user's X + loop logo, white, on a peach→orange tile
  python tools/build_icon.py b      # a cute orange with a leaf and a download arrow
  python tools/build_icon.py a --final   # also writes art/ + docs/ + app logo files

Needs Pillow. The user's logo design is art/logo-design.png.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
S = 1024
INSET = 100
TILE = S - 2 * INSET
RAD = int(TILE * 0.225)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def gradient(size, c1, c2):
    """Diagonal gradient, top-left c1 → bottom-right c2."""
    w, h = size
    g = Image.new('RGB', (w, h))
    px = g.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = lerp(c1, c2, (x + y) / (w + h - 2))
    return g


def tile_base(fill_img):
    canvas = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    shadow = Image.new('L', (S, S), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((INSET, INSET + 14, S - INSET, S - INSET + 14), RAD, fill=70)
    canvas.paste(Image.new('RGBA', (S, S), (160, 70, 20, 255)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(20)))
    mask = Image.new('L', (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle((INSET, INSET, S - INSET, S - INSET), RAD, fill=255)
    full = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    full.paste(fill_img.convert('RGBA'), (INSET, INSET))
    canvas.paste(full, (0, 0), mask)
    return canvas


def arrow_layer(cx, top, bottom, width, tray_w, tray_drop, color, k=4):
    """Round-capped download arrow + smile tray, drawn 4x then scaled down (smooth)."""
    layer = Image.new('L', (S * k, S * k), 0)
    d = ImageDraw.Draw(layer)
    w = width * k

    def seg(a, b):
        d.line([(a[0] * k, a[1] * k), (b[0] * k, b[1] * k)], fill=255, width=int(w))
        for x, y in (a, b):
            d.ellipse((x * k - w / 2, y * k - w / 2, x * k + w / 2, y * k + w / 2), fill=255)

    head = (bottom - top) * 0.42
    seg((cx, top), (cx, bottom))
    seg((cx - head, bottom - head), (cx, bottom))
    seg((cx + head, bottom - head), (cx, bottom))
    y0 = bottom + width * 1.7
    pts = [(cx - tray_w / 2 + t / 60 * tray_w, y0 + tray_drop * math.sin(math.pi * t / 60)) for t in range(61)]
    for a, b in zip(pts, pts[1:]):
        seg(a, b)
    layer = layer.resize((S, S), Image.LANCZOS)
    out = Image.new('RGBA', (S, S), color + (0,))
    out.putalpha(layer)
    return out


# ---------------------------------------------------------------- option A

def option_a():
    """The user's own X + loop logo in white on a peach → coral tile, cream arrow."""
    tile = tile_base(gradient((TILE, TILE), (255, 204, 140), (255, 128, 96)))
    src = Image.open(ROOT / 'art' / 'logo-design.png').convert('RGB')
    box = (412 - 24, 386 - 24, 1048 + 24, 828)            # only the X + loop (arrow redrawn below)
    mark = src.crop(box)
    w, h = mark.size
    mark = mark.resize((w * 2, h * 2), Image.LANCZOS)
    alpha = Image.new('L', mark.size, 0)
    mp, ap = mark.load(), alpha.load()
    for y in range(mark.size[1]):
        for x in range(mark.size[0]):
            r, g, b = mp[x, y]
            if g > 120 and g - r > 50:      # leftover of the green arrow
                continue
            ap[x, y] = max(0, min(255, int((235 - min(r, g, b)) * 255 / 200)))
    white = Image.new('RGBA', mark.size, (255, 255, 255, 255))
    white.putalpha(alpha)
    mw = int(TILE * 0.66)
    mh = int(white.size[1] * mw / white.size[0])
    white = white.resize((mw, mh), Image.LANCZOS)
    top = INSET + int(TILE * 0.17)
    # soft shadow under the white mark so it reads on light peach too
    sh = Image.new('RGBA', white.size, (190, 80, 30, 0))
    sh.putalpha(white.getchannel('A').point(lambda v: v * 0.35))
    tile.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), ((S - mw) // 2, top + 8))
    tile.alpha_composite(white, ((S - mw) // 2, top))
    a_top = top + mh + 34
    tile.alpha_composite(arrow_layer(S // 2, a_top, a_top + 128, 34, 220, 30, (255, 246, 222)))
    return tile


# ---------------------------------------------------------------- option B

def option_b():
    """A cute orange (with leaf) holding a white download arrow, on a cream tile."""
    tile = tile_base(gradient((TILE, TILE), (255, 248, 238), (255, 232, 214)))
    k = 4
    big = Image.new('RGBA', (S * k, S * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    cx, cy, r = S // 2, int(S * 0.55), int(TILE * 0.33)
    # fruit with a simple radial shading
    fruit = Image.new('RGBA', (2 * r * k, 2 * r * k), (0, 0, 0, 0))
    fp = fruit.load()
    for y in range(2 * r * k):
        for x in range(2 * r * k):
            dx, dy = x / (r * k) - 1, y / (r * k) - 1
            dist = math.hypot(dx, dy)
            if dist <= 1:
                light = math.hypot(dx + 0.38, dy + 0.42)
                fp[x, y] = lerp((255, 178, 92), (247, 106, 45), min(1, light / 1.5)) + (255,)
    big.alpha_composite(fruit, ((cx - r) * k, (cy - r) * k))
    # leaf + stem
    d.line([(cx * k, (cy - r + 6) * k), ((cx + 6) * k, (cy - r - 34) * k)], fill=(122, 82, 50, 255), width=14 * k)
    # leaf: two curved edges between its base and tip
    bx, by, tx, ty = cx + 6, cy - r - 30, cx + 140, cy - r - 70
    ang = math.atan2(ty - by, tx - bx)
    nx, ny = -math.sin(ang), math.cos(ang)
    pts = []
    for side in (1, -1):
        rng = range(0, 41) if side == 1 else range(40, -1, -1)
        for i in rng:
            t = i / 40
            bulge = math.sin(math.pi * t) * 34 * side
            pts.append(((bx + (tx - bx) * t + nx * bulge) * k, (by + (ty - by) * t + ny * bulge) * k))
    d.polygon(pts, fill=(118, 196, 112, 255))
    d.line([((bx + 8) * k, (by - 2) * k), ((tx - 18) * k, (ty + 5) * k)], fill=(86, 160, 88, 255), width=5 * k)
    # little highlight
    d.ellipse(((cx - r * 0.62) * k, (cy - r * 0.62) * k, (cx - r * 0.30) * k, (cy - r * 0.38) * k), fill=(255, 236, 205, 170))
    big = big.resize((S, S), Image.LANCZOS)
    tile.alpha_composite(big)
    tile.alpha_composite(arrow_layer(cx, cy - int(r * 0.42), cy + int(r * 0.22), 34, 200, 26, (255, 255, 255)))
    return tile


def write_final(img):
    img.save(ROOT / 'art' / 'icon-1024.png')
    img.save(ROOT / 'art' / 'ClipSaver.icns')
    img.save(ROOT / 'art' / 'ClipSaver.ico', sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    img.resize((256, 256), Image.LANCZOS).save(ROOT / 'docs' / 'assets' / 'icon.png')
    img.resize((128, 128), Image.LANCZOS).save(ROOT / 'clipsaver' / 'logo.png')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'a'
    img = option_a() if which == 'a' else option_b()
    out = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else ROOT / f'icon-{which}.png'
    img.save(out)
    if '--final' in sys.argv:
        write_final(img)
    print('saved', out)
