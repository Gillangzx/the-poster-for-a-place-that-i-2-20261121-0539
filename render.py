#!/usr/bin/env python3
"""LUMARIS — a travel poster for a place that isn't there.

Drawn by hand with Pillow. One invented lakeside town at dusk: a cyan-glowing
lagoon, a single white stone arch bridge as the signature landmark, warm-lit
houses on the far shore, a dark mountain ridge, and the name LUMARIS set large
in the empty sky. No other text anywhere in the picture.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
OUT = "entry.png"

SKY_TOP = (27, 42, 94)        # indigo
SKY_MID = (92, 74, 122)       # dusty violet
SKY_LOW = (232, 162, 76)      # amber band at the horizon
RIDGE_FAR = (38, 44, 84)
RIDGE_NEAR = (14, 19, 34)
LAKE_TOP = (11, 74, 90)
LAKE_BOT = (7, 30, 43)
GLOW = (53, 230, 224)         # bioluminescent cyan
STONE = (242, 239, 230)       # white stone of the bridge
STONE_SHADE = (205, 198, 182)
RIM = (255, 217, 160)         # warm rim light on the bridge
HOUSE = (42, 31, 46)
WINDOW = (255, 178, 94)
NAME_INK = (247, 243, 232)
RULE_INK = (232, 162, 76)
ROCK = (6, 16, 24)          # dark rocks at the water's edge
REED = (18, 48, 52)         # dark reeds at the water's edge

HORIZON = 532                 # 52% of the height
BRIDGE_CX = 560               # bridge centre x (central, dominant)
BRIDGE_HALF = 210             # half span of the arch
BRIDGE_DECK = 615             # deck height at the feet
BRIDGE_APEX = 520             # deck height at the apex
GLOW_C = (560, 648)           # brightest point of the lagoon, under the bridge

rng = random.Random(20261121)


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def pick_font(size):
    for path in (
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def vertical_gradient(img, top_y, bot_y, stops):
    """Paint a vertical gradient between (y, colour) stops onto img."""
    d = ImageDraw.Draw(img)
    span = bot_y - top_y
    for y in range(top_y, bot_y):
        t = (y - top_y) / span
        for i in range(len(stops) - 1):
            y0, c0 = stops[i]
            y1, c1 = stops[i + 1]
            if y0 <= t <= y1:
                f = (t - y0) / (y1 - y0) if y1 > y0 else 0.0
                d.line([(0, y), (W, y)], fill=mix(c0, c1, f))
                break


def soft_blob(img, centre, radii, colour, blur, alpha=255):
    """A soft elliptical bloom: concentric ellipses on a layer, blurred."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = centre
    rx, ry = radii
    steps = 24
    for i in range(steps, 0, -1):
        f = i / steps
        a = int(alpha * (1 - f) * 0.55)
        d.ellipse(
            [cx - rx * f, cy - ry * f, cx + rx * f, cy + ry * f],
            fill=colour + (a,),
        )
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(layer)


def jagged_ridge(base_y, low, high, step, seed_jitter):
    """A mountain silhouette: jagged polyline from x=0 to x=W, closed at base."""
    pts = []
    x = -10
    while x <= W + 10:
        pts.append((x, base_y - rng.uniform(low, high) * seed_jitter))
        x += step
    pts.append((W + 10, base_y + 60))
    pts.append((-10, base_y + 60))
    return pts


def arch_y(x):
    """Parabola of the bridge deck: apex at BRIDGE_CX, feet at BRIDGE_DECK."""
    u = (x - BRIDGE_CX) / BRIDGE_HALF
    return BRIDGE_DECK - (BRIDGE_DECK - BRIDGE_APEX) * (1 - u * u)


def smooth_polyline(pts, iterations=1):
    """Round a jagged polyline's corners (Chaikin cuts): peaks become soft curves."""
    for _ in range(iterations):
        out = [pts[0]]
        for i in range(len(pts) - 1):
            p0, p1 = pts[i], pts[i + 1]
            out.append((p0[0] + 0.25 * (p1[0] - p0[0]), p0[1] + 0.25 * (p1[1] - p0[1])))
            out.append((p0[0] + 0.75 * (p1[0] - p0[0]), p0[1] + 0.75 * (p1[1] - p0[1])))
        out.append(pts[-1])
        pts = out
    return pts


def main():
    img = Image.new("RGBA", (W, H), SKY_TOP + (255,))
    draw = ImageDraw.Draw(img)

    # --- sky: indigo -> violet -> amber band at the horizon ---
    vertical_gradient(img, 0, HORIZON, [(0.0, SKY_TOP), (0.55, SKY_MID), (0.92, SKY_LOW), (1.0, SKY_LOW)])

    # --- one soft warm bloom, low centre-left in the sky ---
    soft_blob(img, (380, 430), (260, 120), (240, 178, 92), 70, alpha=150)

    # --- far ridge (taller, more varied peaks), then near ridge with a dip where the bridge lands ---
    far_pts = smooth_polyline(jagged_ridge(HORIZON, 50, 190, 46, 1.0))
    draw.polygon(far_pts, fill=RIDGE_FAR + (255,))
    near = []
    x = -10
    while x <= W + 10:
        dip = 1.0
        if 380 <= x <= 740:
            dip = 0.25  # the ridge dips where the bridge meets the far shore
        near.append((x, HORIZON - rng.uniform(15, 120) * dip))
        x += 38
    near.append((W + 10, HORIZON + 40))
    near.append((-10, HORIZON + 40))
    near = smooth_polyline(near)
    draw.polygon(near, fill=RIDGE_NEAR + (255,))

    # --- the lake: dark teal, deepening toward the bottom ---
    vertical_gradient(img, HORIZON, H, [(0.0, LAKE_TOP), (1.0, LAKE_BOT)])

    # --- the glow: brightest directly beneath the bridge ---
    soft_blob(img, GLOW_C, (600, 260), GLOW, 90, alpha=110)
    soft_blob(img, GLOW_C, (420, 200), GLOW, 60, alpha=235)
    soft_blob(img, GLOW_C, (200, 90), (120, 210, 90), 40, alpha=200)
    # a faint second glow echo, deep in the lower water
    soft_blob(img, (560, 880), (380, 130), GLOW, 80, alpha=55)

    # --- ripples: horizontal dashes, denser and brighter near the glow ---
    draw = ImageDraw.Draw(img)
    for y in range(HORIZON + 18, H - 12, 13):
        n = rng.randint(2, 6)
        for _ in range(n):
            x = rng.randint(20, W - 120)
            ln = rng.randint(22, 95)
            dist = math.hypot(x + ln / 2 - GLOW_C[0], y - GLOW_C[1]) / 420.0
            bright = max(0.0, 1.0 - dist)
            col = mix((16, 60, 74), (150, 240, 235), bright * 0.85)
            a = int(60 + 150 * bright)
            draw.line([(x, y), (x + ln, y)], fill=col + (a,), width=2)

    # --- far shore: a dark land strip along the waterline that both piers stand on ---
    # deterministic undulation (no rng) so the houses and ripples keep their exact places
    shore_top = []
    x = -10
    while x <= W + 10:
        shore_top.append((x, HORIZON - 14 - 4 * math.sin(x / 90.0) - 3 * math.sin(x / 47.0)))
        x += 34
    draw.polygon(shore_top + [(W + 10, HORIZON + 18), (-10, HORIZON + 18)], fill=RIDGE_NEAR + (255,))
    draw.line(shore_top, fill=RIDGE_FAR + (255,), width=2)
    # two rocky banks descending from the strip to each pier base
    for fx in (BRIDGE_CX - BRIDGE_HALF, BRIDGE_CX + BRIDGE_HALF - 18):
        cx = fx + 9
        draw.polygon(
            [(cx - 34, HORIZON + 10), (cx + 34, HORIZON + 10),
             (cx + 16, BRIDGE_DECK + 56), (cx - 16, BRIDGE_DECK + 56)],
            fill=RIDGE_NEAR + (255,),
        )

    # --- houses on the far shore, left: dark bodies, warm windows ---
    shore_y = HORIZON - 6
    for i in range(8):
        hx = 60 + i * 32 + rng.randint(-6, 6)
        hw = rng.randint(24, 40)
        hh = rng.randint(26, 52)
        draw.rectangle([hx, shore_y - hh, hx + hw, shore_y], fill=HOUSE + (255,))
        draw.polygon(
            [(hx - 3, shore_y - hh), (hx + hw / 2, shore_y - hh - 12), (hx + hw + 3, shore_y - hh)],
            fill=(30, 22, 34, 255),
        )
        for _ in range(rng.randint(1, 3)):
            wx = hx + rng.randint(4, hw - 10)
            wy = shore_y - rng.randint(8, hh - 8)
            draw.rectangle([wx, wy, wx + 5, wy + 7], fill=WINDOW + (255,))

    # --- the bridge: one white stone arch, off-centre right ---
    xs = list(range(BRIDGE_CX - BRIDGE_HALF, BRIDGE_CX + BRIDGE_HALF + 1, 6))
    top = [(x, arch_y(x)) for x in xs]
    band = 40
    bot = [(x, arch_y(x) + band) for x in reversed(xs)]
    draw.polygon(top + bot, fill=STONE + (255,))
    # warm rim light along the left half of the deck
    rim_pts = [(x, arch_y(x) - 2) for x in xs if x <= BRIDGE_CX + 20]
    draw.line(rim_pts, fill=RIM + (255,), width=4)
    # piers at both feet
    for fx in (BRIDGE_CX - BRIDGE_HALF, BRIDGE_CX + BRIDGE_HALF - 18):
        draw.rectangle([fx, BRIDGE_DECK, fx + 18, BRIDGE_DECK + 52], fill=STONE_SHADE + (255,))
    # no solid fill under the arch: the glowing lagoon shows through the opening

    # --- reflection of the arch, broken by ripples ---
    refl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(refl)
    mirror = 2 * (BRIDGE_DECK + 30)
    rtop = [(x, mirror - arch_y(x)) for x in xs]
    rbot = [(x, mirror - arch_y(x) - band) for x in reversed(xs)]
    rd.polygon(rtop + rbot, fill=STONE + (110,))
    refl = refl.filter(ImageFilter.GaussianBlur(3))
    img.alpha_composite(refl)
    draw = ImageDraw.Draw(img)
    for _ in range(46):
        y = rng.randint(BRIDGE_DECK + 34, BRIDGE_DECK + 150)
        x = rng.randint(BRIDGE_CX - BRIDGE_HALF - 20, BRIDGE_CX + BRIDGE_HALF + 20)
        ln = rng.randint(18, 70)
        draw.line([(x, y), (x + ln, y)], fill=LAKE_TOP + (170,), width=3)

    # --- denser ripple texture in the lower water, concentrated near the glow ---
    for y in range(700, H - 12, 10):
        n = rng.randint(4, 9)
        for _ in range(n):
            x = int(rng.gauss(GLOW_C[0], 260))
            x = max(20, min(W - 140, x))
            ln = rng.randint(18, 80)
            dist = math.hypot(x + ln / 2 - GLOW_C[0], y - GLOW_C[1]) / 420.0
            bright = max(0.0, 1.0 - dist)
            col = mix((16, 60, 74), (150, 240, 235), bright * 0.85)
            a = int(50 + 130 * bright)
            draw.line([(x, y), (x + ln, y)], fill=col + (a,), width=2)

    # --- a few small dark rocks and reeds at the bottom corners: water texture only ---
    for (bx, by, s) in ((30, 1006, 1.0), (72, 1014, 0.7), (986, 1004, 1.0), (944, 1016, 0.7)):
        draw.polygon([(bx - 34 * s, by), (bx - 12 * s, by - 26 * s), (bx + 10 * s, by - 30 * s),
                      (bx + 30 * s, by - 8 * s), (bx + 34 * s, by)], fill=ROCK + (255,))
        for _ in range(3):
            rx = bx + rng.randint(-24, 24)
            draw.line([(rx, by - 4), (rx + rng.randint(-6, 6), by - 34 - rng.randint(0, 18))],
                      fill=REED + (255,), width=2)

    # --- the name, GIANT across the full width at the top: the biggest element ---
    word = "LUMARIS"
    tracking = 28
    size = 220
    while size > 60:
        font = pick_font(size)
        total = sum(font.getlength(ch) + tracking for ch in word) - tracking
        if total <= 896:
            break
        size -= 4
    widths = [font.getlength(ch) for ch in word]
    ascent, descent = font.getmetrics()
    x = (W - total) // 2
    y = 44
    # soft shadow so the letters sit on the sky
    sx = x
    for i, ch in enumerate(word):
        draw.text((sx + 3, y + 4), ch, font=font, fill=(10, 14, 30, 160))
        sx += widths[i] + tracking
    sx = x
    for i, ch in enumerate(word):
        draw.text((sx, y), ch, font=font, fill=NAME_INK + (255,))
        sx += widths[i] + tracking
    # thin amber rule under the name, spanning its full width
    draw.line([(x, y + ascent + 16), (x + total, y + ascent + 16)], fill=RULE_INK + (255,), width=4)

    img.convert("RGB").save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
