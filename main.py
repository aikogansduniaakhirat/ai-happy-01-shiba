import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageOps

OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output") + "/entry.png"
SS = 3          # supersample factor
W = H = 1024    # final size
S = W * SS      # render size

def canvas():
    img = Image.new("RGB", (S, S), (255, 140, 120))
    return img, ImageDraw.Draw(img)

def grad_bg(d, top, bottom):
    for y in range(S):
        t = y / S
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (S, y)], fill=c)

def glow(d, cx, cy, r, color, steps=14):
    for i in range(steps, 0, -1):
        rr = r * (i / steps)
        a = int(60 * (i / steps))
        c = color + (a,)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=c)

def star_pts(cx, cy, R, r, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        ang = rot + i * math.pi / n
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts

def rounded_rect(d, box, rad, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)

def main():
    img, d = canvas()
    grad_bg(d, (255, 205, 120), (255, 140, 110))
    glow(d, S * 0.5, S * 0.42, S * 0.55, (255, 235, 170), steps=16)

    scx, scy = S * 0.5, S * 0.52
    star_R, star_r = S * 0.30, S * 0.13
    glow(d, scx, scy, star_R * 1.4, (255, 240, 150), steps=18)
    d.polygon(star_pts(scx, scy, star_R, star_r), fill=(255, 214, 90))
    d.polygon(star_pts(scx, scy, star_R * 0.82, star_r * 0.82), fill=(255, 228, 130))
    eye_r = S * 0.018
    d.ellipse([scx - S * 0.07 - eye_r, scy - S * 0.02 - eye_r,
               scx - S * 0.07 + eye_r, scy - S * 0.02 + eye_r], fill=(120, 80, 30))
    d.ellipse([scx + S * 0.07 - eye_r, scy - S * 0.02 - eye_r,
               scx + S * 0.07 + eye_r, scy - S * 0.02 + eye_r], fill=(120, 80, 30))
    d.arc([scx - S * 0.04, scy + S * 0.01, scx + S * 0.04, scy + S * 0.06],
          start=10, end=170, fill=(120, 80, 30), width=max(2, S // 300))

    hx, hy = S * 0.5, S * 0.38
    hr = S * 0.22
    d.ellipse([hx - hr * 0.72, hy + hr * 0.18, hx - hr * 0.28, hy + hr * 0.62], fill=(250, 205, 150))
    d.ellipse([hx + hr * 0.28, hy + hr * 0.18, hx + hr * 0.72, hy + hr * 0.62], fill=(250, 205, 150))
    d.polygon([(hx - hr * 0.85, hy - hr * 0.55), (hx - hr * 0.45, hy - hr * 1.15), (hx - hr * 0.15, hy - hr * 0.55)],
              fill=(222, 150, 80))
    d.polygon([(hx + hr * 0.85, hy - hr * 0.55), (hx + hr * 0.45, hy - hr * 1.15), (hx + hr * 0.15, hy - hr * 0.55)],
              fill=(222, 150, 80))
    d.polygon([(hx - hr * 0.72, hy - hr * 0.62), (hx - hr * 0.5, hy - hr * 0.95), (hx - hr * 0.3, hy - hr * 0.62)],
              fill=(255, 190, 130))
    d.polygon([(hx + hr * 0.72, hy - hr * 0.62), (hx + hr * 0.5, hy - hr * 0.95), (hx + hr * 0.3, hy - hr * 0.62)],
              fill=(255, 190, 130))
    d.ellipse([hx - hr * 0.60, hy + hr * 0.05, hx + hr * 0.60, hy + hr * 0.85], fill=(255, 245, 230))
    er = S * 0.028
    for ex in (hx - hr * 0.35, hx + hr * 0.35):
        ey = hy - hr * 0.05
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(40, 30, 20))
        d.ellipse([ex - er * 0.55, ey - er * 0.55, ex - er * 0.1, ey - er * 0.1], fill=(255, 255, 255))
    d.ellipse([hx - S * 0.022, hy + hr * 0.30, hx + S * 0.022, hy + hr * 0.30 + S * 0.028], fill=(60, 40, 30))
    d.arc([hx - hr * 0.30, hy + hr * 0.30, hx + hr * 0.30, hy + hr * 0.85], start=20, end=160,
          fill=(60, 40, 30), width=max(2, S // 260))
    d.ellipse([hx - S * 0.02, hy + hr * 0.52, hx + S * 0.02, hy + hr * 0.52 + S * 0.035], fill=(255, 120, 130))
    for ex in (hx - hr * 0.62, hx + hr * 0.62):
        d.ellipse([ex - S * 0.03, hy + hr * 0.18, ex + S * 0.03, hy + hr * 0.18 + S * 0.03], fill=(255, 150, 130))

    for px in (hx - hr * 0.42, hx + hr * 0.42):
        d.ellipse([px - S * 0.035, scy - S * 0.16, px + S * 0.035, scy - S * 0.16 + S * 0.07], fill=(245, 185, 120))

    # happy sparkles around with golden tints
    sparkles = [(0.2, 0.2), (0.8, 0.22), (0.15, 0.6), (0.85, 0.58), (0.5, 0.12), (0.3, 0.85), (0.7, 0.85)]
    for sx, sy in sparkles:
        glow(d, S * sx, S * sy, S * 0.045, (255, 255, 210), steps=7)

    img = img.resize((W, H), Image.LANCZOS)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    main()
