import os, json, subprocess
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

# Output goes next to this script's parent folder, wherever the kit lives.
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for d in ("svg", "png", "favicon"): os.makedirs(f"{OUT}/{d}", exist_ok=True)

DARK = dict(bg="#272e3d", chev="#98c379", e="#61afef", cur="#e5c07b", text="#e6e9ef", sub="#9aa3b2")
LIGHT = dict(bg="#ffffff", chev="#50a14f", e="#4078f2", cur="#c18401", text="#1f2430", sub="#5c6370")

font = next(f for f in TTCollection("/System/Library/Fonts/Menlo.ttc").fonts
            if f["name"].getDebugName(2) == "Bold")
gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
adv = font["hmtx"].metrics[cmap[ord("e")]][0]

def glyph(ch, x, baseline, size):
    """SVG path and bbox of one Menlo Bold glyph."""
    name, s = cmap[ord(ch)], size / upm
    t = (s, 0, 0, -s, x, baseline)
    pen = SVGPathPen(gs); gs[name].draw(TransformPen(pen, t))
    bp = BoundsPen(gs); gs[name].draw(TransformPen(bp, t))
    return pen.getCommands(), bp.bounds

def mark(c, mono=None, scale=1.0):
    """The ❯e_ mark in a 400x400 box, optically centred. Returns (svg body, bbox)."""
    ch, ec, cc = (mono,)*3 if mono else (c["chev"], c["e"], c["cur"])
    epath, (ex0, ey0, ex1, ey1) = glyph("e", 150, 262, 190)
    # chevron stroke width 26 → visual extent from 65 to 136; cursor 272..320
    x0, x1 = 65, 320
    y0, y1 = min(137, ey0), max(263, ey1)
    dx, dy = 200 - (x0 + x1) / 2, 200 - (y0 + y1) / 2
    body = (f'<g transform="translate(200 200) scale({scale}) translate(-200 -200) translate({dx:.1f} {dy:.1f})">'
            f'<path d="M78 150 L123 200 L78 250" fill="none" stroke="{ch}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{epath}" fill="{ec}"/>'
            f'<rect x="272" y="232" width="48" height="24" rx="4" fill="{cc}"/></g>')
    return body

def text_paths(s, x, baseline, size, fill):
    out, step = [], adv * size / upm
    for i, ch in enumerate(s):
        if ch != " ":
            d, _ = glyph(ch, x + i * step, baseline, size); out.append(f'<path d="{d}" fill="{fill}"/>')
    return "".join(out), len(s) * step

def svg(w, h, body, name):
    p = f"{OUT}/svg/{name}.svg"
    open(p, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>\n')
    return p

def png(src, size, dst, h=None):
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(h or size), src, "-o", dst], check=True)

# --- square marks (400 box)
files = {
 "avatar":          f'<rect width="400" height="400" fill="{DARK["bg"]}"/>' + mark(DARK, scale=0.86),
 "icon-rounded":    f'<rect width="400" height="400" rx="88" fill="{DARK["bg"]}"/>' + mark(DARK, scale=0.86),
 "icon-light":      f'<rect width="400" height="400" rx="88" fill="{LIGHT["bg"]}"/>' + mark(LIGHT, scale=0.86),
 "mark-on-dark":    mark(DARK),
 "mark-on-light":   mark(LIGHT),
 "mark-mono-dark":  mark(None, mono=DARK["bg"]),
 "mark-mono-white": mark(None, mono="#ffffff"),
}
paths = {n: svg(400, 400, b, n) for n, b in files.items()}

# --- wordmark: ❯ eizedev_  (chevron drawn, text as paths)
def wordmark(c, name, size=120):
    h = int(size * 1.5); base = int(size * 1.08)
    s = size / 190  # scale chevron/cursor to text size
    chev = (f'<path d="M{20} {base-size*0.58:.1f} L{20+45*s:.1f} {base-size*0.32:.1f} L20 {base-size*0.06:.1f}" fill="none" '
            f'stroke="{c["chev"]}" stroke-width="{26*s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    txt, tw = text_paths("eizedev", 20 + 80*s, base, size, c["e"])
    cx = 20 + 80*s + tw + 8*s
    cur = f'<rect x="{cx:.1f}" y="{base-30*s:.1f}" width="{48*s:.1f}" height="{24*s:.1f}" rx="{4*s:.1f}" fill="{c["cur"]}"/>'
    w = int(cx + 48*s + 20)
    return svg(w, h, chev + txt + cur, name), w, h
wm_dark = wordmark(DARK, "wordmark-on-dark"); wm_light = wordmark(LIGHT, "wordmark-on-light")

# --- social / Open Graph preview 1280x640: centred wordmark + tagline
def wm_body(c, size, ox, base):
    k = size / 190
    chev = (f'<path d="M{ox} {base-size*0.58:.1f} L{ox+45*k:.1f} {base-size*0.32:.1f} L{ox} {base-size*0.06:.1f}" fill="none" '
            f'stroke="{c["chev"]}" stroke-width="{26*k:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    txt, tw = text_paths("eizedev", ox + 80*k, base, size, c["e"])
    cx = ox + 80*k + tw + 8*k
    return chev + txt + f'<rect x="{cx:.1f}" y="{base-30*k:.1f}" width="{48*k:.1f}" height="{24*k:.1f}" rx="{4*k:.1f}" fill="{c["cur"]}"/>', cx + 48*k - ox
size = 150
_, ww = wm_body(DARK, size, 0, 0)
wm, _ = wm_body(DARK, size, (1280 - ww) / 2, 330)
tagline = "Automation, self-hosting & PowerShell"
_, tgw = text_paths(tagline, 0, 0, 34, DARK["sub"])
tg, _ = text_paths(tagline, (1280 - tgw) / 2, 420, 34, DARK["sub"])
paths["social-preview"] = svg(1280, 640, f'<rect width="1280" height="640" fill="{DARK["bg"]}"/>' + wm + tg, "social-preview")

# --- PNG exports
for sz in (500, 1000): png(paths["avatar"], sz, f"{OUT}/png/avatar-{sz}.png")
for sz in (512, 1024): png(paths["icon-rounded"], sz, f"{OUT}/png/icon-rounded-{sz}.png")
for sz in (256, 512, 1024):
    png(paths["mark-on-dark"], sz, f"{OUT}/png/mark-on-dark-{sz}.png")
    png(paths["mark-on-light"], sz, f"{OUT}/png/mark-on-light-{sz}.png")
png(paths["social-preview"], 1280, f"{OUT}/png/social-preview-1280x640.png", 640)
for src, w, h in (wm_dark, wm_light):
    n = os.path.basename(src)[:-4]; png(src, w*2, f"{OUT}/png/{n}@2x.png", h*2)

# --- favicons
import shutil
shutil.copy(paths["icon-rounded"], f"{OUT}/favicon/favicon.svg")
png(paths["avatar"], 180, f"{OUT}/favicon/apple-touch-icon.png")   # iOS rounds corners itself
for sz in (192, 512): png(paths["icon-rounded"], sz, f"{OUT}/favicon/icon-{sz}.png")
from PIL import Image
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    png(paths["icon-rounded"], 256, f"{tmp}/ico.png")
    Image.open(f"{tmp}/ico.png").save(f"{OUT}/favicon/favicon.ico", sizes=[(16,16),(32,32),(48,48)])
json.dump({"name": "eizedev", "short_name": "eizedev",
           "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
           "theme_color": DARK["bg"], "background_color": DARK["bg"], "display": "standalone"},
          open(f"{OUT}/favicon/site.webmanifest", "w"), indent=2)
print("done")
