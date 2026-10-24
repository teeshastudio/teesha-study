"""Compose a royalty-free lo-fi bed + SFX for the Toussaint reel."""
import sys, wave
import numpy as np

SR = 48000
DUR = 48.2
BPM = 88
BEAT = 60 / BPM
rng = np.random.default_rng(7)
N = int(SR * DUR)
t_all = np.arange(N) / SR

# Section times (seconds) taken from the transcript
SECTIONS = [0.0, 4.18, 12.36, 27.52, 40.54]
HOMMAGE = (12.36, 20.2)
TRANSITIONS = [4.18, 12.36, 27.52, 40.54]
POPS = [0.15, 0.55, 21.72, 23.30, 24.70, 31.10, 32.14, 33.42, 37.58, 42.64, 45.40]


def note(f):
    return 440 * 2 ** ((f - 69) / 12)


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    # vectorised one-pole via lfilter-like loop in chunks
    from itertools import accumulate  # noqa: F401
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def lp_fast(x, cutoff):
    # FFT brick-ish lowpass with soft roll-off (fast for long buffers)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def hp_fast(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 - 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def add(buf, sig, start):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


# Chords: Am9 - Fmaj7 - Cmaj7 - Gsus/E  (warm, respectful, a bit of groove)
CHORDS = [[57, 60, 64, 67, 71], [53, 57, 60, 64, 67], [48, 55, 59, 64, 67], [52, 55, 59, 62, 67]]
BASS = [45, 41, 48, 40]
BAR = BEAT * 4

keys = np.zeros(N)
pad = np.zeros(N)
bass = np.zeros(N)
drums = np.zeros(N)


def rhodes(f, dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.exp(-tt * 2.2) * np.minimum(1, tt * 200)
    s = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 6)
         + 0.12 * np.sin(2 * np.pi * 3 * f * tt) * np.exp(-tt * 9))
    return s * env * (1 + 0.08 * np.sin(2 * np.pi * 4.5 * tt))


def padtone(f, dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * d * tt + rng.uniform(0, 6)) for d in (0.996, 1.0, 1.004))
    s += 0.3 * np.sin(2 * np.pi * 2 * f * tt)
    att = np.minimum(1, tt / 0.6)
    rel = np.minimum(1, (dur - tt) / 0.6).clip(0)
    return s * att * rel


bar = 0
t = 0.0
while t < DUR:
    c = CHORDS[bar % 4]
    for k, m in enumerate(c):
        add(keys, rhodes(note(m + 12), BAR) * 0.16, t + k * 0.012)          # strum
        add(keys, rhodes(note(m + 12), BEAT * 1.5) * 0.08, t + BEAT * 2.5)  # off-beat re-hit
    for m in c[:3]:
        add(pad, padtone(note(m), BAR + 0.6) * 0.05, t)
    bt = np.arange(int(BAR * SR)) / SR
    b = np.sin(2 * np.pi * note(BASS[bar % 4]) * bt) * np.exp(-bt * 0.9) * np.minimum(1, bt * 300)
    add(bass, b * 0.32, t)
    bar += 1
    t += BAR


def kick():
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    f = 45 + 90 * np.exp(-tt * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)


def snare():
    n = int(0.25 * SR)
    tt = np.arange(n) / SR
    nz = hp_fast(rng.standard_normal(n), 1500)
    return (nz * 0.5 + np.sin(2 * np.pi * 190 * tt) * 0.4) * np.exp(-tt * 18)


def hat():
    n = int(0.06 * SR)
    tt = np.arange(n) / SR
    return hp_fast(rng.standard_normal(n), 7000) * np.exp(-tt * 70)


K, Sn, H = kick(), snare(), hat()
beat_i = 0
t = 0.0
while t < DUR:
    drums_on = 4.0 <= t < HOMMAGE[0] - 0.2 or HOMMAGE[1] <= t < 47.3
    if drums_on:
        pos = beat_i % 4
        if pos in (0, 2) or (pos == 3 and (beat_i // 4) % 2 == 1):
            add(drums, K * 0.55, t + (BEAT / 2 if pos == 3 else 0))
        if pos in (1, 3):
            add(drums, Sn * 0.22, t)
        add(drums, H * 0.10, t)
        add(drums, H * 0.06, t + BEAT * 0.58)  # swung 8th
    beat_i += 1
    t += BEAT

keys = lp_fast(keys, 3200)
pad = lp_fast(pad, 1800)
# intro filter sweep on keys (opens up into the first idea)
sweep = np.clip(t_all / 4.18, 0, 1)
keys = keys * (0.55 + 0.45 * sweep) + lp_fast(keys, 700) * (1 - sweep) * 0.6

# hommage: soften everything
soft = np.ones(N)
a, b = HOMMAGE
soft[(t_all > a) & (t_all < b)] = 0.75
music = keys + pad + bass + drums
music *= soft
# vinyl-ish noise bed
music += lp_fast(rng.standard_normal(N), 4000) * 0.004
fade = np.clip((DUR - t_all) / 1.2, 0, 1) * np.clip(t_all / 0.3, 0, 1)
music *= fade
music /= np.abs(music).max() + 1e-9
music *= 0.8

# Stereo widen: tiny delay on right channel
d = int(0.012 * SR)
L = music
R = np.concatenate([np.zeros(d), music[:-d]]) * 0.9 + music * 0.1

# SFX
sfx = np.zeros(N)
for tr in TRANSITIONS:
    n = int(0.55 * SR)
    tt = np.arange(n) / SR
    nz = rng.standard_normal(n)
    env = np.sin(np.pi * tt / tt[-1]) ** 2
    lo = lp_fast(nz, 2500) - lp_fast(nz, 300)
    hi = hp_fast(nz, 3000) * 0.4
    w = (lo + hi * np.sin(np.pi * tt / tt[-1])) * env
    add(sfx, w * 0.35 / (np.abs(w).max() + 1e-9), tr - 0.30)
for p in POPS:
    n = int(0.09 * SR)
    tt = np.arange(n) / SR
    f = 1100 * np.exp(-tt * 18) + 380
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 45)
    add(sfx, s * 0.28, p)


def write(path, chans):
    x = np.stack(chans, 1)
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


out = sys.argv[1]
write(f"{out}/music.wav", [L, R])
write(f"{out}/sfx.wav", [sfx, sfx])
print("ok")
