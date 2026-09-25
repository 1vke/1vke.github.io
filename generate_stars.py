#!/usr/bin/env python3
"""
Generates the star field for the website (Hugo partial + background images).

History, for future me:
  v1 (stars.js, RIP): ~1000 box-shadow "stars" (squares!) animated by a
     requestAnimationFrame loop. Laggy, and box-shadows are square.
  v2 (pattern SVG + SMIL): round stars, zero JS, but Firefox runs SMIL
     on the main thread AND re-rasterizes pattern content every frame
     when opacity animates inside it. SMIL's clock also pauses on hidden
     tabs, so stars jumped when switching tabs.
  v3 (CSS animations + SVG backgrounds): composited and wall-clock
     synced, but Firefox re-rasterizes SVG background images while their
     element's transform animates — still main-thread work.
  v4 (PNG tiles + 12 opacity-animated divs): no rasterization left, but
     12 oversized layers (viewport + 2 tiles) each re-blended every
     frame is a classic layer explosion — Firefox's GPU helper pinned.
  v5 (this): 3 layers total, one animation each:
     - 2 static parallax layers (small + medium stars), transform-only.
     - 1 parallax layer whose big stars twinkle via a pre-rendered
       sprite strip: 12 frames stacked in ONE PNG, animated with
       `steps(12)` on background-position. The star layout is identical
       in every frame, so stepping by one frame-height changes only the
       twinkle phase, never the positions — and it repaints 12 times
       per cycle instead of blending layers at 60fps. The sprite lives
       on a child element so the parent's transform animation stays
       unambiguously compositor-eligible in Firefox.
     Wall-clock sync: a one-shot inline script sets animation-delay to
     -(Date.now()/1000 % duration) per element, so star state is a pure
     function of absolute time — identical across page navigations,
     reloads, and tab switches (this is what the old stars.js did with
     Date.now(), and what SMIL could not).
  v6 (+ DRIFT_STEP): drift animations use steps() instead of
     linear — "temporal quantization". The drift is so slow (4-12 px/s)
     that 0.6px steps are visually identical to continuous motion, but
     the transform VALUE only changes when a step fires, so the
     compositor produces ~20 distinct frames/s for the fastest layer
     instead of 60 (WebRender's design goal: no render when nothing
     changed). Scroll-driven animations (animation-timeline: scroll())
     would be the only true zero-idle-cost approach, but Firefox still
     doesn't support them as of this writing.
  v7 (this): smooth twinkle. The sprite strip alone stepped between
     12 brightness levels (a ~20% jump every 750ms on bright stars).
     Two copies of the strip now crossfade: copy X holds frame k while
     fading 1->0 across each frame interval, copy Y holds frame k+1
     while fading 0->1, so displayed brightness = w*b_k + (1-w)*b_{k+1}
     — a genuine linear fade between levels. The opacity glides are
     quantized with steps(SUB) (8 updates/s) to keep the v6 GPU win,
     and each element carries exactly ONE animation (opacity on .cw
     wrappers, background on .tw inners) so Firefox keeps the opacity
     animations on the compositor.

Output:
  layouts/partials/stars.html       (the divs + <style> + sync script)
  static/img/stars/l{0,1,2}-{theme}.png   (l2 = 12-frame sprite strip)

Regenerate with: python3 generate_stars.py
"""

import math
import os
import shutil
import struct
import zlib

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static", "img", "stars")
PARTIAL = os.path.join(BASE, "layouts", "partials", "stars.html")

TW, TH = 480, 600        # background tile (CSS px)
SS = 2                   # PNG supersample factor (crisp on retina)
SEED = 42069             # same seed as the old stars.js, lol
FRAMES = 12              # twinkle frames in the l2 sprite strip
CYCLE = 9                # seconds for a full twinkle cycle (wall-clock synced)
SUB = 10                 # crossfade sub-steps per frame interval — smoothness
                         # dial. Updates/sec = FRAMES*SUB/CYCLE; keep at or
                         # below the drift's step rate so the GPU win holds.
DRIFT_STEP = 0.6         # px per drift step — the GPU dial. Each layer's
                         # transform only *changes* when it steps, so fewer
                         # distinct frames are produced than with `linear`.
                         # 0.6px is visually indistinguishable at these speeds.

# (name, base radius, star count per tile, drift duration in seconds,
#  twinkle?) — counts keep the old site's 7:2:1 layer ratio.
LAYERS = [
    ("l0", 0.7, 78, 50, False),
    ("l1", 1.2, 22, 100, False),
    ("l2", 1.8, 11, 150, True),
]

# The old --star-color values, baked into the PNGs as gray + alpha.
# (gray value, alpha) — light: black @ 0x7a, dark: white @ 0x7a
THEMES = {"light": (0, 0x7A), "dark": (255, 0x7A)}

PNG_SIG = b"\x89PNG\r\n\x1a\n"


# LCG stands for "Linear Congruential Generator". ✨ The more you know ✨
def lcg(seed):
    state = seed
    while True:
        state = (1103515245 * state + 12345) % 2147483648
        yield state / 2147483648


def paint_star(buf, w, cx, cy, r, alpha):
    """Anti-aliased disc into a gray/alpha interleaved buffer (2x units)."""
    x0, x1 = max(0, int(cx - r - 1)), min(w - 1, int(cx + r + 1))
    y0, y1 = max(0, int(cy - r - 1)), int(cy + r + 1)
    for y in range(y0, y1 + 1):
        row = y * w
        for x in range(x0, x1 + 1):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            coverage = max(0.0, min(1.0, r - d + 0.5))
            a = int(alpha * coverage)
            if a:
                i = (row + x) * 2 + 1
                if a > buf[i]:
                    buf[i] = a


def write_png(path, gray, plane_h, stars_by_frame):
    """Minimal grayscale+alpha PNG; stars_by_frame is a list of frames,
    each a list of (cx, cy, r, alpha) in supersampled tile units."""
    w = TW * SS
    h = plane_h * SS
    buf = bytearray(bytes((gray, 0)) * (w * h))
    frame_h = TH * SS
    for k, stars in enumerate(stars_by_frame):
        off = k * frame_h
        for cx, cy, r, alpha in stars:
            paint_star(buf, w, cx, cy + off, r, alpha)

    raw = bytearray()
    stride = w * 2
    for y in range(h):
        raw.append(0)  # filter: none
        raw += buf[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 4, 0, 0, 0)  # 8-bit, gray+alpha
    png = PNG_SIG + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def make():
    gen = lcg(SEED)
    rnd = lambda: next(gen)

    if os.path.isdir(STATIC):
        shutil.rmtree(STATIC)   # drop stale tiles from previous versions
    os.makedirs(STATIC)

    rules_light, rules_dark, divs = [], [], []
    steps = round(TH / DRIFT_STEP)  # travel is exactly TH, so this is universal
    for name, base_r, count, drift, twinkles in LAYERS:
        stars = [(rnd() * TW * SS, rnd() * TH * SS, base_r * (0.75 + rnd() * 0.5) * SS)
                 for _ in range(count)]
        for theme, (gray, alpha) in THEMES.items():
            path = os.path.join(STATIC, f"{name}-{theme}.png")
            if not twinkles:
                write_png(path, gray, TH, [[(cx, cy, r, alpha) for cx, cy, r in stars]])
            else:
                # Per-star twinkle: a SUM OF HARMONICS of the frame cycle
                # (each multiple divides FRAMES, so the strip stays exactly
                # periodic and loops cleanly). A pure single-frequency fade
                # reads as a metronome — every star pulsing the same 9s
                # sine — while harmonic sums give each star an irregular,
                # unique light curve, like real atmospheric twinkling.
                params = []
                for _ in stars:
                    w = (1.0, 0.2 + rnd() * 0.3, 0.1 + rnd() * 0.2)  # weights
                    p = (rnd(), rnd(), rnd())                        # phases
                    params.append((w, p, 25 + rnd() * 40, 170 + rnd() * 85))
                frames = []
                for k in range(FRAMES):
                    u = k / FRAMES
                    frame = []
                    for (cx, cy, r), (w, p, a_min, a_max) in zip(stars, params):
                        f = sum(w[i] * math.cos(2 * math.pi * ((i + 1) * u + p[i]))
                                 for i in range(len(w)))
                        a = a_min + (a_max - a_min) * (1 + f / sum(w)) / 2
                        frame.append((cx, cy, r, a))
                    frames.append(frame)
                write_png(path, gray, TH * FRAMES, frames)

        css_h = TH * (FRAMES if twinkles else 1)
        size = f"background-size:{TW}px {css_h}px"
        # Static layers paint their own background; the twinkle layer's
        # sprite goes ONLY on the child (.tw), so the transform-animated
        # parent stays a bare composited layer with nothing to repaint.
        sel = f".tw.{name}" if twinkles else f".sk.{name}"
        rules_light.append(f'{sel}{{background-image:url(/img/stars/{name}-light.png);{size}}}')
        rules_dark.append(f'{sel}{{background-image:url(/img/stars/{name}-dark.png);{size}}}')

        anim = f'animation:sk-drift {drift}s steps({steps},end) infinite'
        divs.append(f'<div class="sk {name}" style="{anim}" data-dur="{drift}"></div>')
        if twinkles:
            # Smooth twinkle via crossfade interpolation: two copies of the
            # strip stepped one frame apart, one fading out while the other
            # fades in. Displayed brightness = w*b_k + (1-w)*b_{k+1}: a true
            # linear fade between the 12 raster levels. The opacity glides
            # are quantized (steps(SUB)) so they don't restore 60fps blends.
            # Wrappers (.cw) carry only the opacity animation and inners
            # (.tw) only the background one, so Firefox keeps the opacity
            # compositor-eligible instead of falling back to repaints.
            iv = CYCLE / FRAMES
            divs[-1] = (
                f'<div class="sk {name}" style="{anim}" data-dur="{drift}">'
                f'<div class="cw" style="animation:sk-fx {iv}s steps({SUB},end) infinite" data-dur="{iv}">'
                f'<div class="tw {name}" style="animation:sk-tw {CYCLE}s steps({FRAMES},end) infinite" data-dur="{CYCLE}"></div>'
                f'</div>'
                f'<div class="cw" style="animation:sk-fi {iv}s steps({SUB},end) infinite" data-dur="{iv}">'
                f'<div class="tw {name}" style="animation:sk-tw {CYCLE}s steps({FRAMES},end) -{iv}s infinite" data-dur="{CYCLE}" data-off="{iv}"></div>'
                f'</div></div>'
            )

    style = (
        "/* Generated by generate_stars.py — do not edit by hand */\n"
        "#star-container .sk{position:absolute;left:0;top:-600px;width:100%;"
        f"height:calc(100% + {2 * TH}px);background-repeat:repeat;will-change:transform;}}\n"
        "#star-container .cw{position:absolute;inset:0;will-change:opacity}\n"
        "#star-container .tw{position:absolute;inset:0;background-repeat:repeat}\n"
        f"@keyframes sk-drift{{to{{transform:translateY(-{TH}px)}}}}\n"
        f"@keyframes sk-tw{{to{{background-position:0 -{TH * FRAMES}px}}}}\n"
        "@keyframes sk-fx{from{opacity:1}to{opacity:0}}\n"
        "@keyframes sk-fi{from{opacity:0}to{opacity:1}}\n"
        + "\n".join(rules_light) + "\n"
        + "@media (prefers-color-scheme: dark){\n" + "\n".join(rules_dark) + "\n}\n"
    )

    # One-shot wall-clock sync: phase = f(Date.now()), exactly like the old
    # stars.js. Runs once at parse time (no loop, no rAF), before first
    # paint, so there is no flash of phase-zero stars. Elements can carry
    # comma-separated durations/offsets when they have several animations.
    script = (
        "<script>"
        "(function(){var n=Date.now()/1e3;"
        "document.querySelectorAll('#star-container [data-dur]').forEach(function(e){"
        "var D=e.dataset.dur.split(','),O=(e.dataset.off||'0').split(',');"
        "e.style.animationDelay=D.map(function(d,i){"
        "return -((n+(+O[i]||0))%d)+'s'}).join(',');});})();"
        "</script>"
    )

    return (
        '<div id="star-container" class="DO_NOT_OPEN_VERY_LAGGY" aria-hidden="true">\n'
        '<style>\n' + style + '</style>\n'
        + "\n".join(divs) + '\n'
        + script + '\n</div>\n'
    )


if __name__ == "__main__":
    partial = make()
    with open(PARTIAL, "w") as f:
        f.write(partial)
    tiles = sorted(os.listdir(STATIC))
    print(f"wrote {PARTIAL} ({os.path.getsize(PARTIAL)} bytes)")
    print(f"wrote {len(tiles)} PNGs to {STATIC}: {', '.join(tiles)}")
