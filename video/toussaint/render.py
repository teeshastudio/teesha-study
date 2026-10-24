"""Teesha Studio - Toussaint reel: zooms, animated captions, brand cards, transitions.

Usage: python3 render.py <work_dir> <fonts_dir> <src.mov> <out_video.mp4> [preview_seconds]
Reads graded frames from ffmpeg, composites overlays, writes video-only MP4.
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK, FONTS, SRC, OUT = sys.argv[1:5]
LIMIT = float(sys.argv[5]) if len(sys.argv) > 5 else None
W, H, FPS = 1080, 1920, 30
# KIT=<dir>: export an editable CapCut kit (PNGs, SRT, transitions) and render a
# clean base video (zooms only, original colours, no overlays)
KIT = os.environ.get("KIT")
GRADE = "null" if KIT else open(f"{WORK}/grade.txt").read().strip()

# Brand palette (charte Teesha Studio)
OFF = (250, 250, 247, 255)
BLACK = (0, 0, 0, 255)
LIME = (163, 230, 53, 255)
VIOLET = (76, 29, 149, 255)
WHITE = (255, 255, 255, 255)

ANTON = f"{FONTS}/Anton-Regular.ttf"          # stands in for Loubag
MONT = f"{FONTS}/Montserrat%5Bwght%5D.ttf"    # stands in for Kollektif Bold


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        f.set_variation_by_axes([weight])
    return f


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out_cubic(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_out_back(x, s=1.8):
    x = clamp(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def ease_in_out(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- words
raw = [w for seg in json.load(open(f"{WORK}/transcript.json")) for w in seg["words"]]
words = []
for w in raw:
    txt = w["w"].strip()
    if words and (txt.startswith("'") or txt.startswith("-") or txt in ("?", "!")):
        words[-1]["w"] += txt if txt not in ("?", "!") else " " + txt
        words[-1]["e"] = w["e"]
        continue
    words.append({"w": txt, "s": w["s"], "e": w["e"]})

# Fix mis-heard words ("Là, tout ça" == "La Toussaint")
FIX = []
i = 0
while i < len(words):
    a = words[i]["w"].lower().strip(",.")
    nxt = [x["w"].lower().strip(",.") for x in words[i + 1:i + 3]]
    if a in ("là", "la") and nxt == ["tout", "ça"]:
        FIX.append({"w": "La", "s": words[i]["s"], "e": words[i]["e"]})
        FIX.append({"w": "Toussaint", "s": words[i + 1]["s"], "e": words[i + 2]["e"]})
        i += 3
        continue
    FIX.append(words[i])
    i += 1
words = FIX
for w in words:
    if w["w"].startswith("réduites"):
        w["w"] = w["w"].replace("réduites", "réduits")

EMPH = {"TOUSSAINT", "TROIS", "IDÉES", "HORAIRES", "OUVERT", "FERMÉ", "RÉPONSE", "HOMMAGE",
        "BOUGIE", "BONS", "MAUVAIS", "PROMO", "OFFRES", "COMMERCIALE", "SERVICES",
        "FLEURISTE", "BOUGIES", "TOMBES", "MOMENT", "COMMANDER", "RAPIDEMENT", "BIENTÔT", "1", "3"}


def clean(t):
    return t.replace(",", "").replace(".", "").upper()


# Group into short punchy captions (<= 3 words / 16 chars, break on punctuation & pauses)
groups, cur = [], []
for k, w in enumerate(words):
    cur.append(w)
    txt = " ".join(clean(x["w"]) for x in cur)
    nxt = words[k + 1] if k + 1 < len(words) else None
    brk = (w["w"].endswith((",", ".", "?")) or len(cur) >= 3 or len(txt) >= 14
           or nxt is None or nxt["s"] - w["e"] > 0.25
           or (nxt and len(txt) + len(clean(nxt["w"])) + 1 > 17))
    if brk:
        groups.append(cur)
        cur = []
for gi, g in enumerate(groups):
    s, e = g[0]["s"], g[-1]["e"]
    if gi + 1 < len(groups) and groups[gi + 1][0]["s"] - e < 0.4:
        e = groups[gi + 1][0]["s"]
    else:
        e += 0.25
    groups[gi] = {"words": g, "s": s, "e": e}

CAP_FONT = font(MONT, 70, 850)
CAP_Y = 1430
_cap_cache = {}


def caption_img(gi, active):
    key = (gi, active)
    if key in _cap_cache:
        return _cap_cache[key]
    g = groups[gi]["words"]
    toks = [clean(x["w"]) for x in g]
    sp = CAP_FONT.getlength(" ")
    widths = [CAP_FONT.getlength(t) for t in toks]
    padx, pady = 16, 10
    total = sum(widths) + sp * (len(toks) - 1) + 2 * padx + 40
    asc, desc = CAP_FONT.getmetrics()
    hh = asc + desc + 2 * pady + 40
    im = Image.new("RGBA", (int(total), int(hh)), (0, 0, 0, 0))
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(shadow)
    x = 20 + padx
    y = 20 + pady
    for k, (tk, wd) in enumerate(zip(toks, widths)):
        base = tk.strip("?! ")
        if k == active:
            d.rounded_rectangle([x - padx, y - pady + 6, x + wd + padx, y + asc + desc + pady - 4],
                                radius=14, fill=LIME)
            d.text((x, y), tk, font=CAP_FONT, fill=BLACK)
        else:
            col = LIME if base in EMPH else WHITE
            ds.text((x, y + 5), tk, font=CAP_FONT, fill=(0, 0, 0, 200), stroke_width=7, stroke_fill=(0, 0, 0, 200))
            d.text((x, y), tk, font=CAP_FONT, fill=col, stroke_width=5, stroke_fill=BLACK)
        x += wd + sp
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    out = Image.alpha_composite(shadow, im)
    _cap_cache[key] = out
    return out


# ---------------------------------------------------------------- brand blocks
def block(text, fnt, fg, bg, padx=26, pady=14, radius=6):
    l, t, r, b = fnt.getbbox(text)
    im = Image.new("RGBA", (r - l + 2 * padx, b - t + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=radius, fill=bg)
    d.text((padx - l, pady - t), text, font=fnt, fill=fg)
    return im


def stack(blocks, gap=12, align="left"):
    w = max(b.width for b in blocks)
    h = sum(b.height for b in blocks) + gap * (len(blocks) - 1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    y = 0
    for b in blocks:
        x = 0 if align == "left" else (w - b.width) // 2
        im.alpha_composite(b, (x, y))
        y += b.height + gap
    return im


TAG = font(MONT, 40, 800)
TITLE = font(ANTON, 128)
TITLE_M = font(ANTON, 96)
CHIP = font(MONT, 46, 800)


def drop_shadow(im, r=14, a=110):
    pad = r * 2
    sh = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    alpha = im.getchannel("A").point(lambda v: v * a // 255)
    blk = Image.new("RGBA", im.size, (0, 0, 0, 255))
    blk.putalpha(alpha)
    sh.alpha_composite(blk, (pad, pad + 8))
    sh = sh.filter(ImageFilter.GaussianBlur(r))
    sh.alpha_composite(im, (pad, pad))
    return sh


def x_mark_chip(text):
    """Crossed-out card: 'pas de codes promo'."""
    return block(text, CHIP, BLACK, OFF, padx=30, pady=18, radius=10)


def check_chip(text):
    ic, padx, pady, gap = 46, 24, 18, 18
    l, t, r, b = CHIP.getbbox(text)
    im = Image.new("RGBA", (padx + ic + gap + (r - l) + padx, max(ic, b - t) + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=10, fill=BLACK)
    y0 = (im.height - ic) // 2
    d.rounded_rectangle([padx, y0, padx + ic, y0 + ic], radius=8, fill=LIME)
    d.line([(padx + 10, y0 + 24), (padx + 19, y0 + 33), (padx + 36, y0 + 13)], fill=BLACK, width=7)
    d.text((padx + ic + gap - l, (im.height - (b - t)) // 2 - t), text, font=CHIP, fill=WHITE)
    return im


# ---------------------------------------------------------------- timeline
SEC = [  # (start, end, tag, title, transition colour)
    (4.18, 7.6, "IDÉE 01", "TES HORAIRES", LIME),
    (12.36, 15.8, "IDÉE 02", "UN MESSAGE D'HOMMAGE", VIOLET),
    (27.52, 31.0, "IDÉE 03", "TES SERVICES", LIME),
]
TRANSITIONS = [(4.18, LIME), (12.36, VIOLET), (27.52, LIME), (40.54, BLACK)]

elements = []  # dicts: img, t0, t1, x, y, anim_in, anim_out


def add_el(img, t0, t1, x, y, a_in="wipe", a_out="wipe", shadow=True):
    if shadow:
        img = drop_shadow(img)
        x -= 28
        y -= 28
    elements.append(dict(img=img, t0=t0, t1=t1, x=x, y=y, a_in=a_in, a_out=a_out))


TOP = 250  # stays clear of the TikTok / Reels top bar
# Hook
hook = stack([block("3 IDÉES DE POSTS", TITLE, BLACK, LIME, padx=30, pady=18),
              block("SPÉCIAL TOUSSAINT · POUR TON BUSINESS", TAG, WHITE, BLACK)], gap=14)
add_el(hook, 0.05, 4.0, (W - hook.width) // 2, TOP, a_in="pop", a_out="wipe")

for s, e, tag, title, col in SEC:
    fnt = TITLE if TITLE.getlength(title) < 860 else TITLE_M
    tg = block(tag, TAG, BLACK if col == LIME else WHITE, col)
    card = stack([tg, block(title, fnt, WHITE, BLACK, padx=30, pady=18)], gap=12)
    add_el(card, s + 0.18, e, 70, TOP)

# "On n'est pas là pour..." crossed-out cards
for k, (txt, t0) in enumerate([("CODES PROMO", 21.72), ("OFFRES", 23.30), ("FÊTE COMMERCIALE", 24.68)]):
    c = x_mark_chip(txt)
    elements_idx = len(elements)
    add_el(c, t0, 27.3, 70, TOP + k * 118, a_in="pop", a_out="wipe")
    elements[elements_idx]["strike"] = t0 + 0.25
add_el(block("PAS LÀ POUR ÇA !", TITLE_M, WHITE, VIOLET, padx=30, pady=16), 25.84, 27.3,
       70, TOP + 3 * 118 + 10, a_in="pop")

# Idée 3: who is concerned
for k, (txt, t0) in enumerate([("FLEURISTE", 31.10), ("VENTE DE BOUGIES", 32.14), ("ENTRETIEN DE TOMBES", 33.42)]):
    add_el(check_chip(txt), t0, 36.8, 70, TOP + 40 + k * 112, a_in="pop")
deadline = stack([block("ASTUCE", TAG, BLACK, LIME),
                  block("DIS JUSQU'À QUAND", TITLE_M, WHITE, BLACK, padx=30, pady=16),
                  block("ON PEUT COMMANDER", TITLE_M, BLACK, LIME, padx=30, pady=16)], gap=12)
add_el(deadline, 37.45, 40.4, 70, TOP)

# Outro
outro = stack([block("À TOI DE JOUER", TITLE, BLACK, LIME, padx=30, pady=18),
               block("PUBLIE AVANT LE 1ER NOVEMBRE", TAG, WHITE, BLACK)], gap=14)
add_el(outro, 42.5, 45.2, (W - outro.width) // 2, TOP, a_in="pop")


def logo():
    t = block("TEESHA", font(ANTON, 150), LIME, BLACK, padx=40, pady=22, radius=4)
    sfont = font(MONT, 40, 700)
    label = "S T U D I O"
    s = Image.new("RGBA", (t.width, 70), (0, 0, 0, 0))
    ImageDraw.Draw(s).text(((t.width - sfont.getlength(label)) // 2, 10), label, font=sfont, fill=BLACK)
    bar_top = Image.new("RGBA", (int(t.width * 0.72), 26), BLACK)
    im = Image.new("RGBA", (t.width + 80, t.height + 150), (0, 0, 0, 0))
    plate = ImageDraw.Draw(im)
    plate.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=18, fill=OFF)
    im.alpha_composite(bar_top, (40, 22))
    im.alpha_composite(t, (40, 58))
    im.alpha_composite(s, (40, 58 + t.height + 6))
    return im


lg = logo()
add_el(lg, 45.35, 99, (W - lg.width) // 2, TOP + 40, a_in="pop", a_out="none")


def anim_frame(el, t):
    """Return (image, x, y) or None for an element at time t."""
    t0, t1 = el["t0"], el["t1"]
    if t < t0 or t > t1 + 0.3:
        return None
    img, x, y = el["img"], el["x"], el["y"]
    din, dout = 0.32, 0.22
    p_in = (t - t0) / din
    p_out = (t - t1) / dout if el["a_out"] != "none" else -1
    if "strike" in el and t >= el["strike"]:
        # animated violet strike line through the card
        p = ease_out_cubic((t - el["strike"]) / 0.25)
        img = img.copy()
        d = ImageDraw.Draw(img)
        x0, x1 = 28 + 20, img.width - 28 - 20
        ym = img.height // 2 - 4
        d.line([(x0, ym), (x0 + (x1 - x0) * p, ym)], fill=VIOLET, width=7)
    if p_in < 1:
        if el["a_in"] == "pop":
            sc = max(0.05, ease_out_back(p_in))
            nw, nh = max(1, int(img.width * sc)), max(1, int(img.height * sc))
            im2 = img.resize((nw, nh), Image.BILINEAR)
            a = clamp(p_in * 3)
            if a < 1:
                im2.putalpha(im2.getchannel("A").point(lambda v: int(v * a)))
            return im2, x + (img.width - nw) // 2, y + (img.height - nh) // 2
        # wipe from left, with a slide
        p = ease_out_cubic(p_in)
        cw = max(1, int(img.width * p))
        return img.crop((0, 0, cw, img.height)), x - int(40 * (1 - p)), y
    if p_out > 0:
        if p_out >= 1:
            return None
        p = ease_in_out(p_out)
        cw = max(1, int(img.width * (1 - p)))
        return img.crop((img.width - cw, 0, img.width, img.height)), x + img.width - cw, y
    return img, x, y


# ---------------------------------------------------------------- zoom curve
# (start, scale_at_start, scale_at_end); a new segment eases in over 0.12 s
Z = [
    (0.00, 1.06, 1.14), (3.46, 1.22, 1.24),
    (4.18, 1.00, 1.04), (6.26, 1.12, 1.13), (7.10, 1.02, 1.03), (8.18, 1.16, 1.17),
    (9.12, 1.04, 1.08), (11.42, 1.18, 1.19),
    (12.36, 1.00, 1.10),                      # hommage: slow, gentle push
    (16.76, 1.10, 1.16),
    (20.28, 1.06, 1.08), (21.72, 1.14, 1.15), (23.90, 1.04, 1.06), (24.68, 1.18, 1.19),
    (25.60, 1.08, 1.09), (26.74, 1.28, 1.30),
    (27.52, 1.00, 1.04), (31.10, 1.10, 1.11), (32.70, 1.03, 1.05), (33.64, 1.15, 1.16),
    (34.34, 1.04, 1.10), (37.20, 1.18, 1.20),
    (40.54, 1.00, 1.08), (44.50, 1.16, 1.18), (45.86, 1.08, 1.12), (46.50, 1.22, 1.26),
]


def seg_val(i, t):
    s, a, b = Z[i]
    e = Z[i + 1][0] if i + 1 < len(Z) else 47.6
    return a + (b - a) * clamp((t - s) / max(e - s, 1e-3))


def zoom_at(t):
    i = max(k for k in range(len(Z)) if Z[k][0] <= t)
    v = seg_val(i, t)
    if i > 0 and t - Z[i][0] < 0.12:
        prev = seg_val(i - 1, Z[i][0])
        v = prev + (v - prev) * ease_out_cubic((t - Z[i][0]) / 0.12)
    return v


CX, CY = 540, 820  # face anchor


def zoom_frame(img, s):
    if s <= 1.0005:
        return img
    cw, ch = W / s, H / s
    x0 = clamp(CX - cw / 2, 0, W - cw)
    y0 = clamp(CY - ch / 2, 0, H - ch)
    return img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))


# ---------------------------------------------------------------- transitions
def transition_overlay(t):
    for tc, col in TRANSITIONS:
        p = (t - (tc - 0.20)) / 0.40  # band sweeps across in 0.4 s, centred on the cut
        if 0 <= p <= 1:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            band = 1500
            skew = 420
            x = -band - skew + (W + band + 2 * skew) * ease_in_out(p)
            d.polygon([(x, 0), (x + band, 0), (x + band - skew, H), (x - skew, H)], fill=col)
            # thin accent stripe trailing the band
            acc = BLACK if col != BLACK else LIME
            d.polygon([(x - 40, 0), (x, 0), (x - skew, H), (x - skew - 40, H)], fill=acc)
            return ov
    return None


# ---------------------------------------------------------------- CapCut kit
def tc(t, sep=","):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}"


if KIT:
    names = ["accroche_3_idees", "idee_01_horaires", "idee_02_hommage", "idee_03_services",
             "barre_codes_promo", "barre_offres", "barre_fete_commerciale", "pas_la_pour_ca",
             "coche_fleuriste", "coche_bougies", "coche_tombes", "astuce_jusqua_quand",
             "a_toi_de_jouer", "logo_teesha_studio"]
    os.makedirs(f"{KIT}/elements", exist_ok=True)
    os.makedirs(f"{KIT}/transitions", exist_ok=True)
    rows = []
    for k, (el, name) in enumerate(zip(elements, names)):
        img = el["img"]
        if "strike" in el:
            img = img.copy()
            d = ImageDraw.Draw(img)
            ym = img.height // 2 - 4
            d.line([(48, ym), (img.width - 48, ym)], fill=VIOLET, width=7)
        fn = f"{k + 1:02d}_{name}.png"
        img.save(f"{KIT}/elements/{fn}")
        t1 = min(el["t1"], 47.6)
        rows.append(f"{fn:<34} {tc(el['t0'], '.')[3:]} -> {tc(t1, '.')[3:]}   position: x={el['x']} y={el['y']} (sur 1080x1920)")
    open(f"{KIT}/elements/TIMINGS.txt", "w").write(
        "Element                            Debut      -> Fin          Position\n" + "\n".join(rows) + "\n")
    with open(f"{KIT}/sous-titres.srt", "w") as f:
        for gi, g in enumerate(groups):
            txt = " ".join(clean(w["w"]) for w in g["words"])
            f.write(f"{gi + 1}\n{tc(g['s'])} --> {tc(g['e'])}\n{txt}\n\n")
    for k, (tcut, col) in enumerate(TRANSITIONS):
        frames = []
        for i in range(int(0.4 * FPS) + 1):
            ov = transition_overlay(tcut - 0.20 + i / FPS) or Image.new("RGBA", (W, H), (0, 0, 0, 0))
            frames.append(ov.tobytes())
        fn = f"{KIT}/transitions/transition_{k + 1}_{tc(tcut - 0.20, '.')[3:8].replace(':', 'm')}s.mov"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                        "-r", str(FPS), "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444",
                        "-pix_fmt", "yuva444p10le", fn], input=b"".join(frames), check=True)
    elements = []
    groups = []
    TRANSITIONS = []


# ---------------------------------------------------------------- main loop
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", GRADE, "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                        "-crf", "17", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                        "-color_trc", "bt709", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
fsz = W * H * 3
n = 0
total = 47.6
while True:
    buf = dec.stdout.read(fsz)
    if len(buf) < fsz:
        break
    t = n / FPS
    if LIMIT and t > LIMIT:
        break
    frame = Image.frombuffer("RGB", (W, H), buf).convert("RGBA")
    frame = zoom_frame(frame, zoom_at(t))

    # progress bar
    if not KIT:
        d = ImageDraw.Draw(frame)
        d.rectangle([0, 0, int(W * t / total), 9], fill=LIME)

    for el in elements:
        r = anim_frame(el, t)
        if r:
            im, x, y = r
            frame.alpha_composite(im, (int(x), int(y)))

    for gi, g in enumerate(groups):
        if g["s"] <= t < g["e"]:
            active = -1
            for k, w in enumerate(g["words"]):
                if w["s"] <= t:
                    active = k
            cap = caption_img(gi, active)
            p = (t - g["s"]) / 0.12
            sc = 0.82 + 0.18 * ease_out_back(p, 2.2) if p < 1 else 1.0
            if sc != 1.0:
                cap = cap.resize((max(1, int(cap.width * sc)), max(1, int(cap.height * sc))), Image.BILINEAR)
            frame.alpha_composite(cap, ((W - cap.width) // 2, CAP_Y - cap.height // 2))
            break

    ov = transition_overlay(t)
    if ov:
        frame.alpha_composite(ov)

    enc.stdin.write(frame.convert("RGB").tobytes())
    n += 1
    if n % 150 == 0:
        print(f"{t:5.1f}s", flush=True)
enc.stdin.close()
enc.wait()
dec.kill()
print("frames", n)
