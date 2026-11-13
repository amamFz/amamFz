"""Toolkit gaya "coretan tangan" untuk aset SVG.

Semua bentuk dibuat secara deterministik (seed tetap), jadi build ulang dengan
data yang sama menghasilkan file yang sama persis (tidak ada diff palsu di git).

Isi:
  Fonts   - menanam font tulisan tangan (subset, base64) ke dalam SVG + ukur lebar teks
  Pen     - garis goyang, kotak/elips coretan, arsiran, stabilo, doodle
  icon()  - logo Simple Icons (CC0) atau ikon doodle buatan sendiri
"""
import base64
import io
import json
import math
import pathlib
import random

SRC = pathlib.Path(__file__).resolve().parent / "src"

FONT_FILES = {
    "hand": SRC / "fonts" / "Caveat-Bold.woff2",          # judul & label (Caveat, OFL)
    "note": SRC / "fonts" / "PatrickHand-Regular.woff2",  # teks kecil (Patrick Hand, OFL)
}
FONT_FAMILY = {"hand": "SketchHand", "note": "SketchNote"}
FALLBACK = "'Comic Sans MS', 'Segoe Print', cursive"


# ───────────────────────────── FONT ─────────────────────────────
class Fonts:
    """Kumpulkan karakter yang dipakai per font, lalu tanam subset-nya sebagai @font-face."""
    _cache = {}

    def __init__(self):
        self.used = {k: set() for k in FONT_FILES}

    @classmethod
    def _font(cls, key):
        if key not in cls._cache:
            from fontTools.ttLib import TTFont
            cls._cache[key] = TTFont(str(FONT_FILES[key]))
        return cls._cache[key]

    def family(self, key):
        return f"{FONT_FAMILY[key]}, {FALLBACK}"

    def width(self, key, text, size):
        f = self._font(key)
        cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
        return sum(hmtx[cmap.get(ord(ch), cmap.get(ord("?")))][0] for ch in text) * size / upm

    def text(self, key, s, x, y, size, fill, anchor="start", extra=""):
        from xml.sax.saxutils import escape
        self.used[key].update(s)
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{self.family(key)}" font-size="{size}"'
                f' fill="{fill}"{a}{extra}>{escape(s)}</text>')

    def css(self):
        from fontTools import subset
        rules = []
        for key, chars in self.used.items():
            if not chars:
                continue
            opts = subset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["kern"]
            font = subset.load_font(str(FONT_FILES[key]), opts)
            sub = subset.Subsetter(opts)
            sub.populate(text="".join(sorted(chars)) + " ")
            sub.subset(font)
            buf = io.BytesIO()
            subset.save_font(font, buf, opts)
            b64 = base64.b64encode(buf.getvalue()).decode()
            rules.append(f"@font-face{{font-family:{FONT_FAMILY[key]};"
                         f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
        return "".join(rules)


# ───────────────────────────── PENA ─────────────────────────────
def _catmull(points, closed):
    """Catmull-Rom → path cubic halus melalui titik-titik."""
    points = [(round(px, 1), round(py, 1)) for px, py in points]
    pts = points + points[:3] if closed else [points[0]] + points + [points[-1]]
    d = f"M{pts[1][0]:.1f} {pts[1][1]:.1f}" if closed else f"M{points[0][0]:.1f} {points[0][1]:.1f}"
    rng = range(1, len(pts) - 2)
    for i in rng:
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


class Pen:
    def __init__(self, seed, ink, width=1.6, rough=1.0):
        self.r = random.Random(seed)
        self.ink, self.w, self.rough = ink, width, rough

    def j(self, amount=1.0):
        return self.r.uniform(-amount, amount) * self.rough

    def _stroke(self, d, color=None, width=None, opacity=1.0, extra=""):
        op = f' stroke-opacity="{opacity}"' if opacity != 1 else ""
        return (f'<path d="{d}" fill="none" stroke="{color or self.ink}" stroke-width="{width or self.w}"'
                f' stroke-linecap="round" stroke-linejoin="round"{op}{extra}/>')

    def line(self, x1, y1, x2, y2, passes=2, color=None, width=None, bow=1.5):
        out = []
        for _ in range(passes):
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L, dx / L
            b1, b2 = self.j(bow), self.j(bow)
            a = (x1 + self.j(1.2), y1 + self.j(1.2))
            b = (x2 + self.j(1.2), y2 + self.j(1.2))
            c1 = (x1 + dx * 0.3 + nx * b1, y1 + dy * 0.3 + ny * b1)
            c2 = (x1 + dx * 0.7 + nx * b2, y1 + dy * 0.7 + ny * b2)
            out.append(self._stroke(f"M{a[0]:.1f} {a[1]:.1f}C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {b[0]:.1f} {b[1]:.1f}",
                                    color, width, opacity=1 if _ == 0 else 0.55))
        return "".join(out)

    def _round_rect_pts(self, x, y, w, h, r, step=30):
        pts = []
        r = min(r, w / 2, h / 2)
        segs = [((x + r, y), (x + w - r, y)), ((x + w, y + r), (x + w, y + h - r)),
                ((x + w - r, y + h), (x + r, y + h)), ((x, y + h - r), (x, y + r))]
        centers = [(x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)]
        for (s, e), (cx, cy, a0) in zip(segs, centers):
            n = max(1, int(math.hypot(e[0] - s[0], e[1] - s[1]) / step))
            for i in range(n):
                pts.append((s[0] + (e[0] - s[0]) * i / n, s[1] + (e[1] - s[1]) * i / n))
            for k in range(3):
                a = math.radians(a0 + 30 * k)
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        return pts

    def box(self, x, y, w, h, r=10, passes=2, color=None, width=None, fill=None, wobble=1.3):
        out = []
        base = self._round_rect_pts(x, y, w, h, r)
        if fill:
            out.append(f'<path d="{_catmull(base, True)}Z" fill="{fill}"/>')
        for p in range(passes):
            pts = [(px + self.j(wobble), py + self.j(wobble)) for px, py in base]
            # coretan tidak tertutup sempurna: mulai & selesai sedikit melewati
            k = self.r.randrange(len(pts))
            pts = pts[k:] + pts[:k]
            pts.append((pts[0][0] + self.j(3) + 4, pts[0][1] + self.j(2)))
            out.append(self._stroke(_catmull(pts, False), color, width, opacity=1 if p == 0 else 0.5))
        return "".join(out)

    def ellipse(self, cx, cy, rx, ry, passes=2, color=None, width=None, overshoot=0.18):
        out = []
        for p in range(passes):
            a0 = self.r.uniform(0, math.tau)
            n = 14
            pts = []
            for i in range(n + 2):
                a = a0 + (math.tau * (1 + overshoot)) * i / (n + 1)
                f = 1 + self.j(0.06)
                pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
            out.append(self._stroke(_catmull(pts, False), color, width, opacity=1 if p == 0 else 0.5))
        return "".join(out)

    def hachure(self, x, y, w, h, color, gap=6, angle=-35, width=1.2, opacity=0.6, clip_id=None):
        """Arsiran diagonal di dalam kotak (dipotong clipPath bila clip_id diberikan)."""
        out = []
        t = math.tan(math.radians(angle))
        span = w + abs(t) * h
        i = -abs(t) * h
        while i < span:
            x1, y1 = x + i, y + h
            x2, y2 = x + i - t * h, y
            out.append(f"M{x1 + self.j(1):.1f} {y1:.1f}L{x2 + self.j(1):.1f} {y2:.1f}")
            i += gap + self.j(1.2)
        clip = f' clip-path="url(#{clip_id})"' if clip_id else ""
        return (f'<path d="{"".join(out)}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"'
                f' stroke-opacity="{opacity}" fill="none"{clip}/>')

    def highlight(self, x, y, w, h, color, opacity=0.35):
        """Sapuan stabilo miring di belakang teks."""
        y1, y2 = y + self.j(2), y + self.j(3) - 2
        d = f"M{x:.1f} {y1:.1f}C{x + w * 0.3:.1f} {y1 + self.j(2):.1f} {x + w * 0.7:.1f} {y2 + self.j(2):.1f} {x + w:.1f} {y2:.1f}"
        return self._stroke(d, color, h, opacity=opacity)

    def underline(self, x, y, w, color=None, width=2.2, loops=False):
        """Garis bawah tangan: satu sapuan, atau dua sapuan bolak-balik."""
        d = (f"M{x:.1f} {y + self.j(1):.1f}C{x + w * 0.35:.1f} {y + 3 + self.j(2):.1f} "
             f"{x + w * 0.7:.1f} {y - 2 + self.j(2):.1f} {x + w:.1f} {y + self.j(1):.1f}")
        if loops:
            d += (f"C{x + w * 0.7:.1f} {y + 5 + self.j(1):.1f} {x + w * 0.3:.1f} {y + 3 + self.j(1):.1f} "
                  f"{x + 8:.1f} {y + 7 + self.j(1):.1f}")
        return self._stroke(d, color, width)

    def squiggle(self, x, y, w, amp=4, waves=4, color=None, width=2.0):
        d, n = f"M{x:.1f} {y:.1f}", waves * 2
        for i in range(1, n + 1):
            xx = x + w * i / n
            yy = y + (amp if i % 2 else -amp) + self.j(1)
            d += f"Q{x + w * (i - 0.5) / n:.1f} {yy:.1f} {xx:.1f} {y:.1f}"
        return self._stroke(d, color, width)

    def star(self, cx, cy, r, color=None, width=1.8):
        pts = []
        for i in range(11):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(a) + self.j(0.8), cy + rr * math.sin(a) + self.j(0.8)))
        return self._stroke("M" + "L".join(f"{px:.1f} {py:.1f}" for px, py in pts), color, width)

    def sparkle(self, cx, cy, r, color=None, width=1.8):
        d = (f"M{cx:.1f} {cy - r:.1f}V{cy + r:.1f}M{cx - r:.1f} {cy:.1f}H{cx + r:.1f}"
             f"M{cx - r * .55:.1f} {cy - r * .55:.1f}L{cx - r * .3:.1f} {cy - r * .3:.1f}"
             f"M{cx + r * .55:.1f} {cy + r * .55:.1f}L{cx + r * .3:.1f} {cy + r * .3:.1f}")
        return self._stroke(d, color, width)

    def arrow(self, x1, y1, x2, y2, curve=30, color=None, width=2.0, head=9):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / L * curve, my + dx / L * curve
        body = f"M{x1:.1f} {y1:.1f}Q{cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}"
        ang = math.atan2(y2 - cy, x2 - cx)
        h1 = (x2 - head * math.cos(ang - 0.5), y2 - head * math.sin(ang - 0.5))
        h2 = (x2 - head * math.cos(ang + 0.5), y2 - head * math.sin(ang + 0.5))
        heads = f"M{h1[0]:.1f} {h1[1]:.1f}L{x2:.1f} {y2:.1f}L{h2[0]:.1f} {h2[1]:.1f}"
        return self._stroke(body, color, width) + self._stroke(heads, color, width)

    def spiral(self, cx, cy, r, turns=2.5, color=None, width=1.8):
        pts = []
        for i in range(int(turns * 16)):
            a = i / 16 * math.tau
            rr = r * i / (turns * 16)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        return self._stroke(_catmull(pts, False), color, width)


# ───────────────────────────── IKON ─────────────────────────────
# Nama teknologi di profile.json → slug Simple Icons (src/icons, lisensi CC0).
ICON_SLUG = {
    "HTML": "html5", "CSS": "css", "JavaScript": "javascript", "TypeScript": "typescript",
    "React": "react", "Next.js": "nextdotjs", "Vue": "vuedotjs", "Material UI": "mui",
    "Tailwind CSS": "tailwindcss", "Sass": "sass", "MySQL": "mysql", "Figma": "figma",
    "Git": "git", "GitHub": "github",
}
# Ikon doodle buatan sendiri (stroke, 24x24) untuk logo yang tidak tersedia di Simple Icons.
DOODLE_ICONS = {
    "Illustrator": ("#FF9A00", '<path d="M12 2.5 5.5 9.5 8 19h8l2.5-9.5z"/><path d="M12 2.5v9"/><circle cx="12" cy="13" r="1.8"/><path d="M8 21.5h8"/>'),
    "VS Code": ("#2F80ED", '<rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path d="M2.5 8h19"/><path d="m9.5 11.5-3 2.75 3 2.75M14.5 11.5l3 2.75-3 2.75"/>'),
}
_BRANDS = None


def brand(name):
    """(warna_hex, isi_svg_24x24, mode) — mode 'fill' (Simple Icons) atau 'stroke' (doodle)."""
    global _BRANDS
    if name in DOODLE_ICONS:
        hex_, body = DOODLE_ICONS[name]
        return hex_, body, "stroke"
    slug = ICON_SLUG.get(name)
    if not slug:
        return None
    if _BRANDS is None:
        _BRANDS = json.loads((SRC / "icons" / "brands.json").read_text())
    svg = (SRC / "icons" / f"{slug}.svg").read_text()
    d = svg.split(' d="', 1)[1].split('"', 1)[0]
    return _BRANDS[slug]["hex"], f'<path d="{d}"/>', "fill"


def luminance(hex_):
    r, g, b = (int(hex_.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def icon(name, x, y, size, ink, dark):
    """Logo pada posisi (x, y). Logo yang terlalu gelap/terang untuk latar diganti warna tinta."""
    b = brand(name)
    if not b:
        return ""
    hex_, body, mode = b
    lum = luminance(hex_)
    color = hex_
    if (dark and lum < 0.18) or (not dark and lum > 0.8):
        color = ink
    s = size / 24
    if mode == "fill":
        return f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.3f})" fill="{color}">{body}</g>'
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.3f})" fill="none" stroke="{color}" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{body}</g>')
