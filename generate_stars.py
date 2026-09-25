#!/usr/bin/env python3
"""
Generates the star field for the website as an inline SVG (Hugo partial).

Replaces the old box-shadow + requestAnimationFrame approach
(static/js/stars.js, RIP) with the same pattern-tiled SMIL animation used
by the GitHub profile README:

- Stars are real circles (box-shadows are squares)
- Zero JavaScript — no rAF loop, nothing to lag the profiler
- The drift loop is free: patterns tile infinitely, so no duplicated
  star markup and it fills any viewport size
- Fills inherit --star-color from custom_style.html, so light/dark
  theming keeps working exactly as before
- Twinkles: stars fade in groups sharing one <animate> each (random
  membership + random phase/duration keeps it looking organic)

Output: layouts/partials/stars.html
Regenerate with: python3 generate_stars.py
"""

import os

TW, TH = 480, 600        # pattern tile (px): userSpaceOnUse units
SEED = 42069             # same seed as the old stars.js, lol
OUT = os.path.join(os.path.dirname(__file__), "layouts", "partials", "stars.html")

# (base radius, star count per tile, drift duration in seconds)
# Counts keep the old site's 7:2:1 layer ratio (700/200/100).
LAYERS = [
    (0.7, 78, 50),
    (1.2, 22, 100),
    (1.8, 11, 150),
]

TWINKLE_GROUPS = 6  # fade groups per layer; more = more organic, more markup


# LCG stands for "Linear Congruential Generator". ✨ The more you know ✨
def lcg(seed):
    state = seed
    while True:
        state = (1103515245 * state + 12345) % 2147483648
        yield state / 2147483648


def make_partial():
    gen = lcg(SEED)
    rnd = lambda: next(gen)
    patterns = []

    for base_r, count, drift in LAYERS:
        # Split this layer's stars into twinkle groups. Each group gets
        # ONE shared fade animation; stars are assigned randomly so the
        # groups aren't spatially clumped.
        groups = [[] for _ in range(TWINKLE_GROUPS)]
        for _ in range(count):
            groups[int(rnd() * TWINKLE_GROUPS)].append(
                f'<circle cx="{rnd() * TW:.0f}" cy="{rnd() * TH:.0f}" '
                f'r="{base_r * (0.75 + rnd() * 0.5):.1f}"/>'
            )

        group_markup = ""
        for stars in groups:
            if not stars:
                continue
            dur = 2 + rnd() * 4
            begin = -rnd() * dur
            o_min = 0.08 + rnd() * 0.17
            # Peak is 1.0 because --star-color already carries its own
            # alpha (#0000007a / #ffffff7a), matching the old look.
            group_markup += (
                f'<g opacity="{o_min:.2f}">'
                f'<animate attributeName="opacity" values="{o_min:.2f};1;{o_min:.2f}" '
                f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
                + "".join(stars) + '</g>'
            )

        patterns.append(group_markup)

    defs = "".join(
        f'<pattern id="stars-{i}" width="{TW}" height="{TH}" patternUnits="userSpaceOnUse">'
        + p + '</pattern>'
        for i, p in enumerate(patterns)
    )

    # One rect per layer, painted with that layer's pattern. Each rect is
    # tall enough that translating it up by one tile-height (the pattern
    # period) loops seamlessly while always covering the viewport.
    rects = "".join(
        f'<rect x="0" y="-{TH}" width="100%" height="500%" fill="url(#stars-{i})">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 0" to="0 -{TH}" dur="{LAYERS[i][2]}s" repeatCount="indefinite"/></rect>'
        for i in range(len(LAYERS))
    )

    # No viewBox: user units are CSS pixels, so the pattern tiles in real
    # screen space and fills any viewport. fill on the root is inherited
    # by every circle; rects override it with their pattern.
    return (
        '<svg id="star-container" class="DO_NOT_OPEN_VERY_LAGGY" '
        'xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" '
        'fill="var(--star-color)" aria-hidden="true">\n'
        f'<defs>{defs}</defs>\n{rects}\n</svg>\n'
    )


if __name__ == "__main__":
    with open(OUT, "w") as f:
        f.write(make_partial())
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
