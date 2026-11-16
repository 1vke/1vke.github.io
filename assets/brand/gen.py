from PIL import Image, ImageDraw, ImageFont

BG = (19, 18, 23)        # #131217
TEXT = (216, 214, 222)   # #d8d6de
ACCENT = (164, 134, 252) # #a486fc
MUTED = (125, 123, 136) # #7d7b88

ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
MENLO = "/System/Library/Fonts/Menlo.ttc"


def tracked(draw, xy, text, font, fill, tracking):
    """Draw text with per-character tracking, centered on x."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, xy[1]), ch, font=font, fill=fill, anchor="lm")
        x += w + tracking


# ---- share.png: 1200x630 OG card -------------------------------------
share = Image.new("RGB", (1200, 630), BG)
d = ImageDraw.Draw(share)
d.text((600, 240), "Lucas Lowe", font=ImageFont.truetype(ARIAL_BOLD, 130), fill=TEXT, anchor="mm")
tracked(d, (600, 358), "SOFTWARE ENGINEER", ImageFont.truetype(ARIAL, 44), ACCENT, 10)
d.rounded_rectangle((540, 424, 660, 428), radius=2, fill=ACCENT)
d.text((600, 555), "lucaslowe.com", font=ImageFont.truetype(MENLO, 26), fill=MUTED, anchor="mm")
share.save("static/images/share.png", optimize=True)

# ---- favicon.png: 512x512, rounded square with alpha -----------------
fav = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
d = ImageDraw.Draw(fav)
d.rounded_rectangle((0, 0, 511, 511), radius=96, fill=BG + (255,))
d.text((256, 262), "LL", font=ImageFont.truetype(ARIAL_BOLD, 230), fill=ACCENT + (255,), anchor="mm")
fav.save("static/images/favicon.png", optimize=True)

print("written")
