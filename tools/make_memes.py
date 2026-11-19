#!/usr/bin/env python3
"""Build the three gta6-meme-x-01 meme variants (1200x675 PNG).

Every variant is drawn with PIL from scratch: gradient scene, simple vector
shapes, big stroked headline text, and the real make.fun ghost mascot
(assets/mark-1024.png, the official press-kit mark) composited INTO the
scene as a character -- never a corner sticker.

Run:  python3 tools/make_memes.py
Out:  meme-a-price.png  meme-b-waiting.png  meme-c-download.png
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
ROOT = __file__.rsplit("/", 2)[0] if "/" in __file__ else "."
GHOST = f"{ROOT}/assets/mark-1024.png"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MAGENTA = (196, 28, 131)
PINK = (255, 77, 168)
WHITE = (255, 255, 255)
BLACK = (10, 10, 14)


def font(size, path=BOLD):
    return ImageFont.truetype(path, size)


def vgrad(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def fit_text(draw, text, max_w, start, path=BOLD, min_size=40):
    """Largest font size (<= start) whose text fits max_w."""
    size = start
    while size > min_size:
        f = font(size, path)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return font(min_size, path)


def text_center(draw, cx, y, text, f, fill=WHITE, stroke=BLACK, sw=6):
    draw.text((cx, y), text, font=f, fill=fill, anchor="ma",
              stroke_width=sw, stroke_fill=stroke)


def ghost(size, tilt=0):
    g = Image.open(GHOST).convert("RGBA")
    g = g.resize((size, size), Image.LANCZOS)
    if tilt:
        g = g.rotate(tilt, resample=Image.BICUBIC, expand=False)
    return g


def sun(draw, cx, cy, r, color=(255, 190, 80)):
    for i in range(3, 0, -1):
        draw.ellipse([cx - r * i, cy - r * i, cx + r * i, cy + r * i],
                     fill=tuple(min(255, c + 30 * (3 - i)) for c in color))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def palm(draw, x, base_y, h, lean=0, color=(16, 10, 26)):
    """A simple palm silhouette: curved trunk + 6 fronds."""
    top_x, top_y = x + lean, base_y - h
    pts = []
    for t in [i / 12 for i in range(13)]:
        px = x + lean * t * t + math.sin(t * 1.2) * 6
        py = base_y - h * t
        pts.append((px, py))
    draw.line(pts, fill=color, width=max(8, h // 22), joint="curve")
    for ang in (-150, -120, -95, -70, -40, -15):
        a = math.radians(ang)
        ex = top_x + math.cos(a) * h * 0.52
        ey = top_y + math.sin(a) * h * 0.42 + h * 0.10
        mx = top_x + math.cos(a) * h * 0.30
        my = top_y + math.sin(a) * h * 0.18 - h * 0.06
        draw.line([(top_x, top_y), (mx, my), (ex, ey)], fill=color,
                  width=max(6, h // 30), joint="curve")


def brand_strip(draw, y, label="make.fun"):
    """Magenta pill with the make.fun name, bottom centre."""
    f = font(44)
    tw = draw.textlength(label, font=f)
    bw, bh = int(tw) + 56, 64
    x0 = (W - bw) // 2
    draw.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=32, fill=MAGENTA,
                           outline=BLACK, width=4)
    draw.text((W // 2, y + bh // 2), label, font=f, fill=WHITE, anchor="mm",
              stroke_width=2, stroke_fill=BLACK)


def save(img, name):
    img.save(name, "PNG")
    print("wrote", name, img.size)


# ---------------------------------------------------------------- variant A
# "GTA 6 COSTS $100" / ghost holding its coin on a Vice City sunset street.
def variant_a():
    img = vgrad((W, H), (58, 8, 72), (255, 92, 140))
    d = ImageDraw.Draw(img, "RGBA")
    sun(d, 600, 300, 110)
    # skyline
    for x0, w2, h2 in [(40, 130, 150), (200, 90, 210), (880, 110, 180),
                       (1020, 140, 240), (320, 70, 120)]:
        d.rectangle([x0, 470 - h2, x0 + w2, 470], fill=(24, 8, 34))
        for wy in range(470 - h2 + 18, 460, 34):
            for wx in range(x0 + 14, x0 + w2 - 10, 28):
                d.rectangle([wx, wy, wx + 12, wy + 16], fill=(255, 214, 120))
    # road (kept plain so the punchline stays clean)
    d.rectangle([0, 470, W, H], fill=(18, 8, 26))
    d.rectangle([0, 470, W, 482], fill=(255, 214, 120))
    palm(d, 90, 480, 260, lean=30)
    palm(d, 1120, 480, 300, lean=-35)
    # headline
    f = fit_text(d, "GTA 6 COSTS $100", W - 80, 118)
    text_center(d, W // 2, 28, "GTA 6 COSTS $100", f, sw=8)
    # ghost as the hero, standing on the road holding its coin
    g = ghost(360)
    img.paste(g, (430, 210), g)
    # punchline
    f2 = fit_text(d, "GOOD THING MY AI AGENT", W - 80, 64)
    text_center(d, W // 2, 520, "GOOD THING MY AI AGENT", f2, sw=6)
    f3 = fit_text(d, "ALREADY WON IT ON make.fun", W - 80, 64)
    text_center(d, W // 2, 588, "ALREADY WON IT ON make.fun", f3,
                fill=(255, 214, 120), sw=6)
    save(img, "meme-a-price.png")


# ---------------------------------------------------------------- variant B
# "ME WAITING FOR GTA 6 SINCE 2013" / ghost on the couch, TV glowing GTA VI.
def variant_b():
    img = vgrad((W, H), (14, 16, 34), (38, 30, 58))
    d = ImageDraw.Draw(img, "RGBA")
    # cobweb, top-left corner
    for i in range(5):
        d.line([(0, 40 + i * 34), (40 + i * 34, 0)], fill=(200, 200, 220),
               width=2)
    for r in (50, 95, 140):
        d.arc([0 - r, 0 - r, r, r], 0, 90, fill=(200, 200, 220), width=2)
    # TV on the wall, glowing "GTA VI" (sun kept small, inside the screen)
    d.rounded_rectangle([380, 90, 820, 300], radius=18, fill=(8, 8, 14),
                        outline=(90, 90, 120), width=6)
    d.rectangle([400, 110, 800, 280], fill=(255, 92, 140))
    sun(d, 600, 175, 34, color=(255, 220, 130))
    d.rectangle([400, 235, 800, 280], fill=(24, 10, 40))
    f = fit_text(d, "GTA VI", 380, 92)
    text_center(d, 600, 118, "GTA VI", f, sw=7)
    d.rectangle([560, 310, 640, 330], fill=(40, 40, 56))
    # floor + couch
    d.rectangle([0, 520, W, H], fill=(22, 18, 34))
    d.rounded_rectangle([180, 400, 1020, 560], radius=46, fill=(96, 24, 84))
    d.rounded_rectangle([210, 340, 990, 430], radius=40, fill=(120, 32, 104))
    d.rounded_rectangle([180, 470, 1020, 560], radius=30, fill=(76, 18, 66))
    # ghost slumped on the couch, waiting since 2013 (clear of the TV)
    g = ghost(260, tilt=-6)
    img.paste(g, (470, 300), g)
    # headline + punchline
    f1 = fit_text(d, "ME WAITING FOR GTA 6", W - 80, 84)
    text_center(d, W // 2, 8, "ME WAITING FOR GTA 6", f1, sw=7)
    f2 = fit_text(d, "SINCE 2013", W - 80, 76)
    text_center(d, W // 2, 566, "SINCE 2013", f2, fill=(255, 214, 120), sw=7)
    f3 = fit_text(d, "MY AGENT WON $100 ON make.fun", W - 80, 40)
    text_center(d, W // 2, 636, "MY AGENT WON $100 ON make.fun", f3, sw=4)
    save(img, "meme-b-waiting.png")


# ---------------------------------------------------------------- variant C
# "DOWNLOADING GTA 6... 200 GB" / progress bar at 99%, ghost watching.
def variant_c():
    img = vgrad((W, H), (10, 12, 30), (30, 16, 52))
    d = ImageDraw.Draw(img, "RGBA")
    # giant monitor frame
    d.rounded_rectangle([90, 150, 1110, 520], radius=26, fill=(6, 6, 12),
                        outline=(120, 120, 150), width=6)
    # progress bar inside the monitor
    d.rounded_rectangle([150, 300, 1050, 372], radius=30, fill=(40, 40, 60),
                        outline=BLACK, width=4)
    d.rounded_rectangle([150, 300, 1041, 372], radius=30, fill=MAGENTA)
    for x in range(170, 1040, 46):
        d.line([(x, 306), (x - 18, 366)], fill=(255, 120, 200), width=8)
    f = fit_text(d, "99%", 200, 96)
    text_center(d, 600, 196, "99%", f, fill=(255, 214, 120), sw=7)
    f2 = fit_text(d, "13 YEARS OF WAITING. 4 MORE MINUTES.", 760, 48)
    # shrink further if the line is still too wide for the ghost's corner
    while d.textlength("13 YEARS OF WAITING. 4 MORE MINUTES.", font=f2) > 800:
        f2 = font(f2.size - 2)
    text_center(d, 600, 396, "13 YEARS OF WAITING. 4 MORE MINUTES.", f2, sw=5)
    # ghost peeking in at the monitor's bottom-right, clear of every line
    g = ghost(140, tilt=5)
    img.paste(g, (1040, 385), g)
    # headline + punchline
    f1 = fit_text(d, "DOWNLOADING GTA 6... 200 GB", W - 80, 82)
    text_center(d, W // 2, 16, "DOWNLOADING GTA 6... 200 GB", f1, sw=7)
    # punchline kept left of the ghost (ghost owns the bottom-right corner)
    f3 = fit_text(d, "MY AGENT WON $100 ON make.fun", W - 80, 56)
    text_center(d, W // 2, 556, "MY AGENT WON $100 ON make.fun",
                f3, fill=(255, 214, 120), sw=5)
    save(img, "meme-c-download.png")


if __name__ == "__main__":
    variant_a()
    variant_b()
    variant_c()
