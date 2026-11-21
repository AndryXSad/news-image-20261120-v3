#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page (1024x1024 PNG).

A newspaper front page drawn from scratch with PIL and DejaVu fonts:
a dark masthead with a DATE CHECK box, three illustrated leads (the
overnight barrage on Kyiv, Anthropic's second-day slide, Cyclone
Akvan's landfall), a dark world map with eight numbered pins and a
stippled ocean, a UTC timeline of five moments, a day-in-figures
strip, one top story from each of seven regions, a twenty-four-item
grid and an "Also today" ticker. 45 stories in all; every one was
checked against reporting dated Friday 20 November 2026 before it
was drawn (see STORIES.md).

Deterministic output: no timestamps, no unseeded randomness, fixed
font paths, fixed story order. The same run always produces the same
bytes. A seeded generator (seed 20261120) places the map stipple, so
it is identical on every run.

Run locally:  python3 main.py            (writes entry.png next to main.py)
Grader mode:  MAKEFUN_OUTPUT_DIR=out python3 main.py
              (writes entry.png into out/ and nowhere else)
If PIL is unavailable, main.py falls back to copying the pre-rendered
entry.png shipped in this repository into the output directory.
"""
import math
import os
import random
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_NAME = "entry.png"
W, H = 1024, 1024
SEED = 20261120

try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except Exception:  # pragma: no cover - grader without PIL
    HAVE_PIL = False

PAPER = (247, 243, 232)
PANEL = (255, 255, 255)
INK = (17, 17, 17)
RED = (176, 42, 42)
DARKRED = (140, 28, 28)
BLUE = (31, 78, 121)
STEEL = (58, 110, 150)
GRAY = (102, 102, 102)
GOLD = (201, 162, 39)
DARK = (20, 20, 20)
MAPBG = (24, 40, 56)
MAPLINE = (52, 76, 98)
LANDC = (216, 210, 189)
LANDLINE = (138, 132, 116)
NIGHT = (16, 24, 44)
SKYLINE = (38, 48, 70)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_FILES = {
    "serif_b": "DejaVuSerif-Bold.ttf",
    "serif": "DejaVuSerif.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
    "sans": "DejaVuSans.ttf",
}


def font(kind, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, FONT_FILES[kind]),
                               size)


def wrap_lines(dr, text, fnt, max_width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if dr.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(dr, x, y, text, fnt, max_width, color, leading=None, center=False):
    leading = leading or int(fnt.size * 1.28)
    for line in wrap_lines(dr, text, fnt, max_width):
        if center:
            dr.text((x + max_width / 2, y), line, font=fnt, fill=color,
                    anchor="ma")
        else:
            dr.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(dr, x0, x1, y, width=2, color=INK):
    dr.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker(dr, x, y, text, size=12):
    dr.text((x, y), text, font=font("sans_b", size), fill=RED)


def burst(dr, cx, cy, r, color):
    """A small explosion starburst: 8 spikes around a core."""
    pts = []
    for i in range(16):
        ang = -math.pi / 2 + i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    dr.polygon(pts, fill=color)


# ---------------- the stories (all verified 20 Nov 2026) ----------------
LEADS = [
    ("LEAD  \u2022  UKRAINE",
     "Russia's biggest barrage hits three Kyiv bridges",
     "110+ missiles and 400+ drones overnight: three bridges "
     "damaged, 9 killed, power and heat cut.",
     "Reuters, CNN, BBC  \u2022  20 Nov",
     "kyiv"),
    ("LEAD  \u2022  MARKETS",
     "Anthropic slides 8.5% on day two as AI rout deepens",
     "ANT closes at $88.91, down from the $97.17 debut close; "
     "Nasdaq \u22125.3%, S&P \u22123.7%.",
     "Reuters, Investopedia, BBC  \u2022  20 Nov",
     "markets"),
    ("LEAD  \u2022  WEATHER",
     "Cyclone Akvan makes landfall at Gopalpur",
     "Crosses the Odisha coast at 70\u201380 km/h, gusting 90, after "
     "300,000+ were moved to shelters.",
     "IMD, The Hindu BusinessLine  \u2022  20 Nov",
     "cyclone"),
]

# Simplified continent outlines (lon, lat), hand-approximated.
NORTH_AMERICA = [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73),
                 (-65, 60), (-55, 47), (-70, 42), (-76, 35), (-81, 26),
                 (-90, 21), (-97, 16), (-92, 15), (-83, 9), (-79, 9),
                 (-86, 12), (-94, 17), (-102, 18), (-110, 24), (-117, 33),
                 (-124, 40), (-124, 48), (-132, 56), (-150, 61), (-162, 58)]
SOUTH_AMERICA = [(-79, 9), (-70, 11), (-60, 8), (-52, 4), (-50, 0),
                 (-42, -4), (-35, -8), (-39, -17), (-48, -26), (-57, -38),
                 (-66, -47), (-70, -54), (-73, -50), (-73, -37), (-71, -19),
                 (-77, -12), (-81, -4), (-80, 1)]
AFRICA = [(-17, 15), (-11, 28), (-6, 35), (9, 37), (20, 32), (32, 31),
          (36, 27), (40, 15), (43, 11), (51, 11), (45, 2), (40, -8),
          (36, -18), (32, -29), (25, -34), (18, -33), (13, -18), (9, -4),
          (9, 4), (-8, 5), (-14, 8)]
EURASIA = [(-10, 36), (-9, 43), (-3, 48), (2, 51), (7, 55), (10, 59),
           (18, 56), (23, 58), (29, 61), (40, 67), (55, 69), (70, 72),
           (85, 74), (100, 76), (115, 73), (130, 72), (145, 72), (160, 70),
           (178, 65), (170, 60), (162, 56), (156, 52), (142, 55), (140, 48),
           (134, 43), (128, 38), (122, 38), (118, 30), (110, 20), (106, 10),
           (100, 8), (96, 14), (90, 22), (86, 20), (80, 14), (76, 9),
           (72, 20), (65, 25), (58, 26), (52, 28), (48, 30), (42, 31),
           (36, 36), (30, 36), (24, 38), (20, 41), (14, 44), (8, 44),
           (2, 43), (-2, 37), (-9, 37)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 57), (-3, 58), (0, 53), (-1, 51)]
JAPAN = [(130, 31), (133, 34), (136, 35), (139, 37), (141, 41), (143, 44),
         (141, 45), (139, 40), (136, 36), (132, 33)]
SE_ASIA = [(95, 5), (99, 2), (102, -3), (106, -6), (110, -7), (114, -8),
           (118, -9), (120, -6), (117, -1), (114, 3), (110, 5), (105, 2),
           (100, 5)]
AUSTRALIA = [(113, -22), (115, -32), (120, -34), (128, -32), (135, -35),
             (141, -38), (147, -39), (151, -37), (153, -30), (151, -24),
             (146, -19), (142, -13), (140, -17), (136, -12), (132, -12),
             (128, -14), (123, -17), (118, -20)]
NEW_ZEALAND = [(167, -45), (170, -43), (174, -41), (177, -38), (175, -37),
               (172, -41), (169, -44)]
GREENLAND = [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68),
             (-25, 70), (-20, 74), (-25, 78), (-35, 80), (-50, 80),
             (-58, 76), (-62, 72), (-60, 68)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (48, -20), (46, -24),
              (44, -25), (43, -21), (44, -18)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4),
          (110, -3), (109, -1)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9),
              (147, -9), (142, -8), (137, -6), (132, -4)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5),
           (100, -1), (97, 3)]
CUBA = [(-85, 22), (-80, 23), (-75, 21), (-74, 20), (-78, 21), (-83, 22)]
ICELAND = [(-22, 64), (-18, 63), (-14, 64), (-15, 66), (-19, 66),
           (-22, 65)]
LAND = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA, BRITAIN, JAPAN,
        SE_ASIA, AUSTRALIA, NEW_ZEALAND, GREENLAND, MADAGASCAR, BORNEO,
        NEW_GUINEA, SUMATRA, CUBA, ICELAND]

# (number, lon, lat, nudge_x, nudge_y)
PINS = [("1", 30.5, 50.4, 0, -6), ("2", 23.5, 53.9, -20, -2),
        ("3", 46.7, 24.7, 12, 2), ("4", 30.7, 36.9, 18, 2),
        ("5", 4.35, 50.85, -12, 4), ("6", 34.5, 31.5, -8, 6),
        ("7", 56.3, 26.6, 14, -4), ("8", 84.9, 19.3, 0, 0)]
KEY = ["1  KYIV \u2014 3 bridges hit in the overnight barrage; 9 killed",
       "2  POLAND \u2014 Russian Kh-101 missile crashes in Poland",
       "3  RIYADH \u2014 Houthi missile damages the PIF tower",
       "4  ANTALYA \u2014 COP31 slips into overtime with no deal",
       "5  BRUSSELS \u2014 UK\u2013EU summit: youth visas, 100,000 a year",
       "6  GAZA \u2014 Israeli forces cross the Yellow Line",
       "7  HORMUZ \u2014 Tanker on fire after hitting a mine",
       "8  GOPALPUR \u2014 Cyclone Akvan landfall; 300,000+ evacuated"]

TIMES = [("00:49 UTC", "M5.6 quake south-east of the Loyalty Islands"),
         ("02:00 UTC", "Cyclone Akvan crosses the coast at Gopalpur"),
         ("14:00 UTC", "BBC: Anthropic shares fall after the debut"),
         ("21:00 UTC", "US markets close: Nasdaq \u22125.3%, S&P \u22123.7%"),
         ("EVENING", "COP31 slips into overtime with no deal in sight")]

FIGS = [("110+", "missiles fired at Ukraine overnight"),
        ("$88.91", "Anthropic close, day two, \u22128.5%"),
        ("300,000+", "evacuated ahead of Cyclone Akvan"),
        ("100,000", "UK\u2013EU youth visas a year")]

REGIONS = [("NORTH AMERICA", "Army delays Iowa explosives blast"),
           ("SOUTH AMERICA", "Argentina backs disability law"),
           ("EUROPE", "Cost-of-living protests sweep Europe"),
           ("AFRICA", "Kenya discharges last Ebola patient"),
           ("MIDDLE EAST", "Israel crosses Yellow Line in Gaza"),
           ("ASIA", "Japan core CPI 2.2%; Dec hike eyed"),
           ("OCEANIA", "M5.6 quake off New Caledonia")]

GRID = [("BRUSSELS", "EU adopts \u20ac1bn in military aid for Ukraine"),
        ("LONDON", "UK pledges 1,000+ drones for Ukraine, \u00a3260m"),
        ("BERLIN", "Europe ready for talks with Russia, leaders say"),
        ("BERLIN", "Merz: Europe will not accept a new Yalta"),
        ("PARIS", "Depardieu and Houellebecq face sex inquiries"),
        ("TBILISI", "Georgia declares 22 Nov a day of mourning"),
        ("KHARKIV", "Russian drone hits a hospital; four hurt"),
        ("WASHINGTON", "Trump confirms he fired cyber chief Cairncross"),
        ("WASHINGTON", "Trump threatens ban on AI data centres abroad"),
        ("WASHINGTON", "Trump announces posthumous pardon for Pete Rose"),
        ("USA", "Sanctions hit Comancheros and 'Ndrangheta"),
        ("USA", "Court limits agriculture chief's emails"),
        ("TEXAS", "Execution takes more than an hour"),
        ("ANTALYA", "Panama threatens to block a weak COP31 deal"),
        ("SUDAN", "Drone strike kills 10 at a gold mine"),
        ("HAITI", "34 suspected gang members killed, police say"),
        ("NIGERIA", "Moves to end jail terms for attempted suicide"),
        ("SOUTH AFRICA", "Nearly 600 women killed in three months"),
        ("SEOUL", "111 students caught cheating in Suneung exam"),
        ("NEW DELHI", "Indian man jailed 19+ years in Sikh plot"),
        ("TURIN", "Alcaraz beats Cobolli; unbeaten at ATP Finals"),
        ("LAS VEGAS", "Rain washes out F1 first practice"),
        ("GTA VI", "Sales top $2.3bn in a record launch"),
        ("ROME", "Italy fines Meta \u20ac805m over photo access")]

TICKER = ("F1 to use full-time race stewards from 2027  \u2022  Tom Brady "
          "could buy a Chelsea stake  \u2022  England fined for fans' "
          "anti-Catholic chants in Spain")

# ---------------- illustrations ----------------
def art_kyiv(dr, x, y):
    """Night over the Dnipro: skyline, two bridge spans, one hit."""
    w, h = 312, 62
    dr.rectangle([x, y, x + w, y + h], fill=NIGHT)
    # stars
    rng = random.Random(SEED + 1)
    for _ in range(14):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(2, 18)
        dr.ellipse([sx, sy, sx + 1, sy + 1], fill=(247, 243, 232))
    # skyline silhouette
    for bx, bh in ((0, 22), (26, 34), (58, 26), (92, 40), (128, 30),
                   (164, 36), (200, 24), (238, 32), (276, 26)):
        dr.rectangle([x + bx, y + h - 18 - bh, x + bx + 30, y + h - 18],
                     fill=SKYLINE)
    # river
    dr.rectangle([x, y + h - 18, x + w, y + h], fill=STEEL)
    # bridge: deck + two arches, middle span broken by a blast
    dr.line([(x + 8, y + 44), (x + 150, y + 44)], fill=(247, 243, 232),
            width=3)
    dr.arc([x + 8, y + 26, x + 76, y + 46], 180, 360,
           fill=(247, 243, 232), width=2)
    dr.line([(x + 168, y + 44), (x + 304, y + 44)], fill=(247, 243, 232),
            width=3)
    dr.arc([x + 172, y + 26, x + 240, y + 46], 180, 360,
           fill=(247, 243, 232), width=2)
    dr.arc([x + 244, y + 26, x + 304, y + 46], 180, 360,
           fill=(247, 243, 232), width=2)
    # blast where the middle span was
    burst(dr, x + 159, y + 30, 13, GOLD)
    burst(dr, x + 159, y + 30, 7, RED)
    dr.text((x, y + h + 4), "The Dnipro at night: three spans hit",
            font=font("sans", 10), fill=GRAY)


def art_markets(dr, x, y):
    """A falling line: $111.50 open, $97.17 close, $88.91 day two."""
    w, h = 312, 62
    dr.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    # gridlines
    for gy in (y + 14, y + 30, y + 46):
        dr.line([(x + 8, gy), (x + w - 8, gy)], fill=(226, 222, 210),
                width=1)
    pts = [(x + 18, y + 12), (x + 92, y + 34), (x + 166, y + 30),
           (x + 240, y + 50), (x + 294, y + 54)]
    dr.line(pts, fill=RED, width=3)
    for px, py in pts:
        dr.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
                   outline=PANEL, width=1)
    dr.text((x + 92, y + 38), "$97.17", font=font("sans_b", 10), fill=INK)
    dr.text((x + 236, y + 16), "$88.91", font=font("sans_b", 11), fill=RED)
    dr.text((x, y + h + 4), "ANT: open $111.50 \u2192 day-two close $88.91",
            font=font("sans", 10), fill=GRAY)


def art_cyclone(dr, x, y):
    """Spiral storm over a coastline, with wind arrows."""
    w, h = 312, 62
    dr.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    # coastline
    dr.polygon([(x + 210, y), (x + 236, y + 20), (x + 224, y + 42),
                (x + 248, y + h), (x + w, y + h), (x + w, y)],
               fill=(216, 210, 189), outline=LANDLINE)
    dr.text((x + 252, y + 8), "ODISHA", font=font("sans_b", 10), fill=INK)
    # spiral arms
    cx, cy = x + 96, y + 32
    for r, a0, a1 in ((34, 20, 300), (26, 60, 330), (18, 100, 350),
                      (10, 140, 380)):
        dr.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=BLUE, width=4)
    dr.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    # wind arrows
    for ax, ay, dx in ((x + 150, y + 12, 18), (x + 158, y + 50, 18),
                       (x + 40, y + 52, -14)):
        dr.line([(ax, ay), (ax + dx, ay)], fill=BLUE, width=2)
        dr.polygon([(ax + dx, ay), (ax + dx - 6, ay - 3),
                    (ax + dx - 6, ay + 3)], fill=BLUE)
    dr.text((x, y + h + 4), "Landfall 07:30 IST \u2022 70\u201380 km/h, gusts 90",
            font=font("sans", 10), fill=GRAY)


ART = {"kyiv": art_kyiv, "markets": art_markets, "cyclone": art_cyclone}

MX, MY, MW, MH = 28, 358, 556, 118


def project(lon, lat):
    px = MX + (lon + 180.0) / 360.0 * MW
    py = MY + (78.0 - lat) / 136.0 * MH
    return (px, py)


# ---------------- render ----------------
def render(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)

    # faint paper grain (seeded: identical every run), under everything
    grain = random.Random(SEED + 7)
    for _ in range(2400):
        gx = grain.randint(0, W - 1)
        gy = grain.randint(96, H - 1)
        dr.point((gx, gy), fill=(238, 233, 220))

    # ---------- masthead ----------
    dr.rectangle([0, 0, W, 94], fill=DARK)
    dr.text((W / 2, 6), "THE DAILY GLOBE", font=font("serif_b", 50),
            fill=(247, 243, 232), anchor="ma")
    para(dr, 28, 68,
         "FRIDAY 20 NOVEMBER 2026  \u2022  45 STORIES  \u2022  SEVEN "
         "REGIONS  \u2022  FIVE MOMENTS IN UTC",
         font("sans_b", 13), 968, (247, 243, 232), center=True)
    dr.rectangle([858, 12, 996, 54], fill=RED, outline=(247, 243, 232),
                 width=1)
    dr.text((927, 16), "DATE CHECK", font=font("sans_b", 11),
            fill=(247, 243, 232), anchor="ma")
    dr.text((927, 32), "FRI 20 NOV 2026", font=font("sans_b", 11),
            fill=(247, 243, 232), anchor="ma")

    # ---------- three leads ----------
    colx = [28, 356, 684]
    colw = 312
    for (kick, head, deck, src, art), x in zip(LEADS, colx):
        kicker(dr, x, 102, kick)
        para(dr, x, 122, head, font("serif_b", 21), colw, INK, leading=24)
        ART[art](dr, x, 196)
        para(dr, x, 278, deck, font("sans", 12), colw, INK, leading=15)
        dr.text((x, 324), src, font=font("sans", 11), fill=GRAY)
    rule(dr, 28, 996, 336, 2)

    # ---------- dark world map + key ----------
    kicker(dr, 28, 342, "THE WORLD \u2014 EIGHT PLACES IN THE NEWS", 13)
    dr.rectangle([MX, MY, MX + MW, MY + MH], fill=MAPBG, outline=INK,
                 width=1)
    # stippled ocean (seeded: identical every run), drawn before land
    rng = random.Random(SEED)
    for _ in range(260):
        dx = MX + rng.randint(3, MW - 3)
        dy = MY + rng.randint(3, MH - 3)
        dr.ellipse([dx, dy, dx + 1, dy + 1], fill=MAPLINE)
    # graticule
    for lon in range(-150, 181, 30):
        gx = MX + (lon + 180.0) / 360.0 * MW
        dr.line([(gx, MY), (gx, MY + MH)], fill=MAPLINE, width=1)
    for lat in (-60, -30, 0, 30, 60):
        gy = MY + (78.0 - lat) / 136.0 * MH
        dr.line([(MX, gy), (MX + MW, gy)], fill=MAPLINE, width=1)
    for poly in LAND:
        pts = [project(lon, lat) for lon, lat in poly]
        dr.polygon(pts, fill=LANDC, outline=LANDLINE)
    for num, lon, lat, nx, ny in PINS:
        px, py = project(lon, lat)
        px, py = px + nx, py + ny
        dr.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                   outline=(247, 243, 232), width=2)
        dr.text((px, py - 1), num, font=font("sans_b", 9),
                fill=(247, 243, 232), anchor="mm")
    ky = 360
    for line in KEY:
        dr.text((600, ky), line, font=font("sans", 11), fill=INK)
        ky += 15
    rule(dr, 28, 996, 486, 1)

    # ---------- UTC timeline ----------
    kicker(dr, 28, 494, "THE DAY IN UTC \u2014 FIVE MOMENTS", 13)
    for i, (t, txt) in enumerate(TIMES):
        x = 28 + i * 194
        dr.text((x, 512), t, font=font("sans_b", 12), fill=RED)
        para(dr, x, 528, txt, font("sans", 11), 184, INK, leading=13)
    rule(dr, 28, 996, 560, 1)

    # ---------- day in figures ----------
    for i, (num, lab) in enumerate(FIGS):
        x = 28 + i * 242
        dr.rectangle([x, 568, x + 232, 614], fill=PANEL, outline=INK,
                     width=1)
        dr.line([(x, 568), (x + 232, 568)], fill=RED, width=3)
        dr.text((x + 10, 574), num, font=font("serif_b", 20), fill=INK)
        dr.text((x + 10, 596), lab, font=font("sans", 10), fill=GRAY)

    # ---------- seven regions ----------
    kicker(dr, 28, 622, "SEVEN REGIONS \u2014 ONE TOP STORY FROM EACH", 13)
    for i, (region, head) in enumerate(REGIONS):
        x = 28 + i * 139
        dr.rectangle([x, 640, x + 134, 694], fill=PANEL, outline=INK,
                     width=1)
        dr.line([(x, 640), (x + 134, 640)], fill=RED, width=3)
        dr.text((x + 6, 644), region, font=font("sans_b", 10), fill=RED)
        para(dr, x + 6, 658, head, font("sans", 11), 122, INK, leading=13)

    # ---------- grid: 24 stories ----------
    kicker(dr, 28, 700, "AROUND THE WORLD", 13)
    rule(dr, 28, 996, 718, 1)
    for i, (place, head) in enumerate(GRID):
        col, row = i % 4, i // 4
        x, y = 28 + col * 242, 726 + row * 39
        dr.text((x, y), place, font=font("sans_b", 10), fill=RED)
        para(dr, x, y + 13, head, font("sans", 11), 230, INK, leading=13)

    # ---------- ticker + footer ----------
    rule(dr, 28, 996, 966, 2)
    dr.text((28, 972), "ALSO TODAY", font=font("sans_b", 12), fill=RED)
    dr.text((150, 972), TICKER, font=font("sans", 11), fill=INK)
    rule(dr, 28, 996, 990, 1)
    para(dr, 28, 996,
         "The Daily Globe  \u2022  Friday 20 November 2026  \u2022  45 "
         "stories  \u2022  Sources: Reuters, AP, BBC, CNN, IMD, UN News, "
         "Le Monde, WSJ, USA Today, Ukrinform",
         font("sans", 11), 968, GRAY, center=True)
    dr.rectangle([0, 1016, W, H], fill=RED)

    img.save(out_path, "PNG", optimize=True)
    print("saved", out_path, os.path.getsize(out_path), "bytes")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or HERE
    out_path = os.path.join(out_dir, OUT_NAME)
    if HAVE_PIL:
        os.makedirs(out_dir, exist_ok=True)
        render(out_path)
        return 0
    src = os.path.join(HERE, OUT_NAME)
    if not os.path.exists(src):
        print("PIL is not available and no pre-rendered entry.png exists",
              file=sys.stderr)
        return 1
    if os.path.abspath(src) != os.path.abspath(out_path):
        os.makedirs(out_dir, exist_ok=True)
        shutil.copyfile(src, out_path)
    print("copied", out_path, os.path.getsize(out_path), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
