"""Burn Teesha Studio captions onto an edited video and export an overlay track.

Style: white text with black outline; the word being spoken sits on a lime box
in black. Captions move up while a CapCut card occupies the caption zone.

Usage: python3 captions.py <transcript.json> <font.ttf> <src.mp4> <out_dir>
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TRANSCRIPT, FONT, SRC, OUT = sys.argv[1:5]
W, H, FPS = 2160, 3840, 30
K = W / 1080  # layout was designed at 1080 wide
DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "default=nw=1:nk=1", SRC]))

WHITE, BLACK, LIME = (255, 255, 255, 255), (0, 0, 0, 255), (163, 230, 53, 255)
CAP_Y = int(1430 * K)        # normal position (caption centre)
DODGE_Y = int(1150 * K)      # while a card sits in the caption zone
DODGE = [(4.35, 6.20), (12.55, 14.75), (25.30, 30.10)]
STRIP_Y, STRIP_H = int(980 * K), int(620 * K)  # only this band is rendered

# ---------------------------------------------------------------- words
raw = [w for seg in json.load(open(TRANSCRIPT)) for w in seg["words"]]
words = []
for w in raw:
    txt = w["w"].strip()
    if words and (txt.startswith("'") or txt.startswith("-") or txt in ("?", "!")):
        words[-1]["w"] += txt if txt not in ("?", "!") else " " + txt
        words[-1]["e"] = w["e"]
        continue
    words.append({"w": txt, "s": w["s"], "e": w["e"]})

fixed, i = [], 0
while i < len(words):
    a = words[i]["w"].lower().strip(",.")
    nxt = [x["w"].lower().strip(",.") for x in words[i + 1:i + 3]]
    if a in ("là", "la") and nxt == ["tout", "ça"]:      # "La Toussaint"
        fixed.append({"w": "La", "s": words[i]["s"], "e": words[i]["e"]})
        fixed.append({"w": "Toussaint" + words[i + 2]["w"][2:], "s": words[i + 1]["s"], "e": words[i + 2]["e"]})
        i += 3
        continue
    if a == "deux" and nxt[:1] == ["trois"]:              # "Et de 3"
        words[i]["w"] = "de"
    fixed.append(words[i])
    i += 1
words = fixed


def clean(t):
    return t.replace(",", "").replace(".", "").upper()


groups, cur = [], []
for k, w in enumerate(words):
    cur.append(w)
    txt = " ".join(clean(x["w"]) for x in cur)
    nxt = words[k + 1] if k + 1 < len(words) else None
    if (w["w"].endswith((",", ".", "?")) or len(cur) >= 3 or len(txt) >= 14 or nxt is None
            or nxt["s"] - w["e"] > 0.25 or len(txt) + len(clean(nxt["w"])) + 1 > 17):
        groups.append(cur)
        cur = []
for gi, g in enumerate(groups):
    s, e = g[0]["s"], g[-1]["e"]
    if gi + 1 < len(groups) and groups[gi + 1][0]["s"] - e < 0.4:
        e = groups[gi + 1][0]["s"]
    else:
        e += 0.25
    groups[gi] = {"words": g, "s": s, "e": e}

# ---------------------------------------------------------------- drawing
F = ImageFont.truetype(FONT, int(60 * K))
F.set_variation_by_axes([850])
_cache = {}


def caption_img(gi, active):
    if (gi, active) in _cache:
        return _cache[(gi, active)]
    toks = [clean(x["w"]) for x in groups[gi]["words"]]
    sp = F.getlength(" ")
    widths = [F.getlength(t) for t in toks]
    padx, pady, m = int(16 * K), int(10 * K), int(20 * K)
    asc, desc = F.getmetrics()
    im = Image.new("RGBA", (int(sum(widths) + sp * (len(toks) - 1) + 2 * padx + 2 * m),
                            asc + desc + 2 * pady + 2 * m), (0, 0, 0, 0))
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(shadow)
    x, y = m + padx, m + pady
    for k, (tk, wd) in enumerate(zip(toks, widths)):
        if k == active:
            d.rounded_rectangle([x - padx, y - pady + 6 * K, x + wd + padx, y + asc + desc + pady - 4 * K],
                                radius=int(14 * K), fill=LIME)
            d.text((x, y), tk, font=F, fill=BLACK)
        else:
            ds.text((x, y + 5 * K), tk, font=F, fill=(0, 0, 0, 200), stroke_width=int(7 * K), stroke_fill=(0, 0, 0, 200))
            d.text((x, y), tk, font=F, fill=WHITE, stroke_width=int(5 * K), stroke_fill=BLACK)
        x += wd + sp
    out = Image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(6 * K)), im)
    _cache[(gi, active)] = out
    return out


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ease_out_back(x, s=2.2):
    x = max(0.0, min(1.0, x))
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def caption_y(t):
    """Glide between the normal and dodge positions over 0.2 s."""
    v = 0.0
    for a, b in DODGE:
        v = max(v, min(ease((t - a + 0.2) / 0.2), ease((b + 0.2 - t) / 0.2)))
    return CAP_Y + (DODGE_Y - CAP_Y) * v


# ---------------------------------------------------------------- render
os.makedirs(OUT, exist_ok=True)
burn = subprocess.Popen([
    "ffmpeg", "-v", "error", "-y", "-i", SRC,
    "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{STRIP_H}", "-r", str(FPS), "-i", "-",
    "-filter_complex", f"[0:v][1:v]overlay=0:{STRIP_Y}:eof_action=pass[v]",
    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "copy", "-movflags", "+faststart", f"{OUT}/video_sous-titree.mp4"], stdin=subprocess.PIPE)
track = subprocess.Popen([
    "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{STRIP_H}",
    "-r", str(FPS), "-i", "-",
    "-vf", f"pad={W}:{H}:0:{STRIP_Y}:color=black@0,scale=1080:1920",
    "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
    f"{OUT}/piste_sous-titres_transparente.mov"], stdin=subprocess.PIPE)

n = 0
while n / FPS < DUR:
    t = n / FPS
    strip = Image.new("RGBA", (W, STRIP_H), (0, 0, 0, 0))
    for gi, g in enumerate(groups):
        if g["s"] <= t < g["e"]:
            active = max([k for k, w in enumerate(g["words"]) if w["s"] <= t], default=-1)
            cap = caption_img(gi, active)
            p = (t - g["s"]) / 0.12
            if p < 1:
                sc = 0.82 + 0.18 * ease_out_back(p)
                cap = cap.resize((max(1, int(cap.width * sc)), max(1, int(cap.height * sc))), Image.BILINEAR)
            strip.alpha_composite(cap, ((W - cap.width) // 2, int(caption_y(t) - STRIP_Y - cap.height / 2)))
            break
    data = strip.tobytes()
    burn.stdin.write(data)
    track.stdin.write(data)
    n += 1
for p in (burn, track):
    p.stdin.close()
    p.wait()


# Editable caption text (SRT) for later tweaks
def tc(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


with open(f"{OUT}/sous-titres_modifiables.srt", "w") as f:
    for gi, g in enumerate(groups):
        f.write(f"{gi + 1}\n{tc(g['s'])} --> {tc(g['e'])}\n{' '.join(clean(w['w']) for w in g['words'])}\n\n")
print("frames", n, "groups", len(groups))
