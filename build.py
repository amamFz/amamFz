#!/usr/bin/env python3
"""Generator aset README profil.

Semua data diambil dari profile.json. Jalankan:
    python3 build.py
Hasilnya ditulis ke folder assets/ (versi -dark dan -light untuk tiap aset).
Tanpa dependensi luar, cukup Python 3.8+.
"""
import json
import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

SANS = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Consolas, 'DejaVu Sans Mono', monospace"


def themes(accent):
    return {
        "dark": {
            "bg": "#0d1117", "surface": "#161b22", "border": "#30363d",
            "text": "#e6edf3", "muted": "#8b949e", "faint": "#21262d",
            "accent": accent, "accent_text": accent,
        },
        "light": {
            "bg": "#ffffff", "surface": "#f6f8fa", "border": "#d0d7de",
            "text": "#1f2328", "muted": "#59636e", "faint": "#eaeef2",
            "accent": accent, "accent_text": shade(accent, 0.62),
        },
    }


def shade(hex_color, factor):
    """Gelapkan warna (factor < 1) agar teks aksen tetap terbaca di tema terang."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(c * factor) for c in (r, g, b))


def t(s):
    return escape(str(s))


# ─────────────────────────────── HERO ───────────────────────────────
def hero(p, c):
    W, H = 1200, 320
    user = t(p["github_user"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{t(p["name"])} — {t(p["tagline"])}">
  <title>{t(p["name"])} — {t(p["tagline"])}</title>
  <defs>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{c["border"]}"/>
    </pattern>
    <radialGradient id="glow" cx="82%" cy="20%" r="60%">
      <stop offset="0" stop-color="{c["accent"]}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bar" x1="0" x2="1">
      <stop offset="0" stop-color="{c["accent"]}"/>
      <stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    <style>
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      .float {{ animation: float 6s ease-in-out infinite; }}
      @keyframes float {{ 50% {{ transform: translateY(-6px); }} }}
      @media (prefers-reduced-motion: reduce) {{ .cursor, .float {{ animation: none; }} }}
    </style>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{c["bg"]}"/>
    <rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.55"/>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{c["border"]}"/>

  <!-- kiri: identitas -->
  <text x="72" y="96" font-family="{MONO}" font-size="20" fill="{c["accent_text"]}">~/{user} $ whoami<tspan class="cursor" fill="{c["accent"]}"> ▍</tspan></text>
  <text x="68" y="186" font-family="{SANS}" font-size="84" font-weight="800" letter-spacing="3" fill="{c["text"]}">{t(p["name"])}</text>
  <rect x="72" y="208" width="320" height="5" rx="2.5" fill="url(#bar)"/>
  <text x="72" y="254" font-family="{SANS}" font-size="26" font-weight="500" fill="{c["muted"]}">{t(p["tagline"])}</text>
  <circle cx="79" cy="281" r="5" fill="{c["accent"]}"/>
  <text x="94" y="287" font-family="{MONO}" font-size="16" fill="{c["muted"]}">based in {t(p["location"])}</text>

  <!-- kanan: jendela wireframe (UI designer + developer) -->
  <g class="float">
    <g transform="translate(850 70)">
      <rect width="280" height="190" rx="14" fill="{c["surface"]}" stroke="{c["border"]}"/>
      <path d="M0 14a14 14 0 0 1 14-14h252a14 14 0 0 1 14 14v22H0z" fill="{c["faint"]}"/>
      <circle cx="20" cy="18" r="5" fill="#ff5f57"/>
      <circle cx="38" cy="18" r="5" fill="#febc2e"/>
      <circle cx="56" cy="18" r="5" fill="#28c840"/>
      <rect x="20" y="56" width="110" height="74" rx="8" fill="{c["accent"]}" opacity="0.18"/>
      <path d="M48 104l18-20 14 14 10-8 14 14" fill="none" stroke="{c["accent"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="146" y="58" width="112" height="10" rx="5" fill="{c["text"]}" opacity="0.75"/>
      <rect x="146" y="78" width="88" height="8" rx="4" fill="{c["muted"]}" opacity="0.6"/>
      <rect x="146" y="94" width="100" height="8" rx="4" fill="{c["muted"]}" opacity="0.6"/>
      <rect x="146" y="114" width="64" height="18" rx="9" fill="{c["accent"]}"/>
      <text x="20" y="166" font-family="{MONO}" font-size="15" fill="{c["muted"]}">&lt;<tspan fill="{c["accent_text"]}">Design</tspan> to=<tspan fill="{c["text"]}">"code"</tspan> /&gt;</text>
    </g>
  </g>
</svg>
'''


# ────────────────────────────── TOMBOL ──────────────────────────────
# Ikon digambar sendiri (stroke 24x24), bukan logo merek.
ICONS = {
    # globe
    "portfolio": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.8 3.8 5.8 3.8 9s-1.2 6.2-3.8 9c-2.6-2.8-3.8-5.8-3.8-9S9.4 5.8 12 3z"/>',
    # tas kerja
    "linkedin": '<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M8.5 7V5.5A1.5 1.5 0 0 1 10 4h4a1.5 1.5 0 0 1 1.5 1.5V7M3 12.5h18"/>',
    # amplop
    "email": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.8 6.5 12 13l8.2-6.5"/>',
    # branch
    "github": '<circle cx="6" cy="5.5" r="2.2"/><circle cx="6" cy="18.5" r="2.2"/><circle cx="18" cy="8" r="2.2"/><path d="M6 7.7v8.6M18 10.2c0 4-6 3.2-11 6.5"/>',
}
BUTTON_LABELS = {"portfolio": "Portfolio", "linkedin": "LinkedIn", "email": "Email", "github": "GitHub"}


def button(key, c):
    W, H = 220, 60
    label = BUTTON_LABELS[key]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
  <title>{label}</title>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{c["surface"]}" stroke="{c["border"]}" stroke-width="1.5"/>
  <rect x="12" y="12" width="36" height="36" rx="10" fill="{c["accent"]}" fill-opacity="0.16"/>
  <g transform="translate(18 18)" fill="none" stroke="{c["accent_text"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</g>
  <text x="62" y="37" font-family="{SANS}" font-size="19" font-weight="600" fill="{c["text"]}">{label}</text>
  <path d="M188 36l10-10M190 26h8v8" fill="none" stroke="{c["muted"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''


def buttons(p, c):
    return {f"btn-{k}": button(k, c) for k in BUTTON_LABELS}


# ──────────────────────────── TECH STACK ────────────────────────────
# Titik warna khas tiap teknologi (hanya kode warna, bukan logo). Fallback: aksen.
TECH_COLORS = {
    "HTML": "#E34F26", "CSS": "#663399", "JavaScript": "#F7DF1E", "TypeScript": "#3178C6",
    "React": "#61DAFB", "Next.js": "#888888", "Vue": "#42B883", "Material UI": "#007FFF",
    "Tailwind CSS": "#38BDF8", "Sass": "#CC6699", "MySQL": "#4479A1", "Figma": "#F24E1E",
    "Illustrator": "#FF9A00", "Git": "#F05032", "GitHub": "#8B949E", "VS Code": "#007ACC",
}


def text_width(s, size):
    """Perkiraan lebar teks sans-serif semibold (cukup akurat untuk ukuran pill)."""
    w = 0.0
    for ch in s:
        if ch in "il.,:;|!'I j": w += 0.30
        elif ch in "ft()r-": w += 0.38
        elif ch in "mwMW": w += 0.88
        elif ch.isupper(): w += 0.68
        else: w += 0.56
    return w * size


def stack(p, c):
    W, PAD, LABEL_W = 900, 36, 200
    PILL_H, GAP_X, GAP_Y, FS = 40, 12, 14, 17
    rows, y = [], 92
    for group, items in p["stack"].items():
        x, row_y = PAD + LABEL_W, y
        pills = []
        for name in items:
            pw = int(text_width(name, FS)) + 58
            if x + pw > W - PAD:              # bungkus ke baris berikutnya
                x, y = PAD + LABEL_W, y + PILL_H + GAP_Y
            dot = TECH_COLORS.get(name, c["accent"])
            pills.append(
                f'<g transform="translate({x} {y})">'
                f'<rect width="{pw}" height="{PILL_H}" rx="{PILL_H // 2}" fill="{c["surface"]}" stroke="{c["border"]}"/>'
                f'<circle cx="22" cy="20" r="6" fill="{dot}"/>'
                f'<text x="38" y="26" font-family="{SANS}" font-size="{FS}" font-weight="600" fill="{c["text"]}">{t(name)}</text></g>')
            x += pw + GAP_X
        rows.append(
            f'<text x="{PAD}" y="{row_y + 26}" font-family="{MONO}" font-size="16" fill="{c["muted"]}">'
            f'<tspan fill="{c["accent_text"]}">//</tspan> {t(group.lower())}</text>' + "".join(pills))
        y += PILL_H + 26
    H = y + 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">
  <title>Tech stack: {t(", ".join(n for g in p["stack"].values() for n in g))}</title>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}"/>
  <text x="{PAD}" y="52" font-family="{SANS}" font-size="24" font-weight="700" fill="{c["text"]}">Tech Stack</text>
  <rect x="{PAD}" y="64" width="44" height="4" rx="2" fill="{c["accent"]}"/>
  {"".join(rows)}
</svg>
'''


# Tiap builder mengembalikan {nama_file_tanpa_tema: isi_svg}.
BUILDERS = [
    lambda p, c: {"hero": hero(p, c)},
    buttons,
    lambda p, c: {"stack": stack(p, c)},
]


# ────────────────────────────── README ──────────────────────────────
def picture(name, alt, width=None, height=None):
    size = (f' width="{width}"' if width else "") + (f' height="{height}"' if height else "")
    return (f'<picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">'
            f'<img src="assets/{name}-dark.svg" alt="{t(alt)}"{size}>'
            f'</picture>')


def readme(p):
    L = p["links"]
    hrefs = {"portfolio": L["portfolio"], "linkedin": L["linkedin"],
             "email": "mailto:" + L["email"], "github": L["github"]}
    btns = "\n  ".join(
        f'<a href="{t(hrefs[k])}">{picture("btn-" + k, BUTTON_LABELS[k], height=52)}</a>'
        for k in BUTTON_LABELS)
    e = p["education"]
    return f'''<!-- File ini dibuat oleh build.py dari profile.json. Edit data di sana, lalu jalankan: python3 build.py -->
<div align="center">

<p>{picture("hero", p["name"] + " — " + p["tagline"], width="100%")}</p>

<p>
  {btns}
</p>

</div>

### About me

{t(p["bio"])}

🎓 **{t(e["school"])}** — {t(e["major"])} ({t(e["years"])})

<br/>

<div align="center">

{picture("stack", "Tech stack", width="100%")}

</div>
'''


def write_readme(p):
    (ROOT / "README.md").write_text(readme(p), encoding="utf-8")
    print("wrote README.md")


def main():
    p = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    ASSETS.mkdir(exist_ok=True)
    for theme_name, c in themes(p["accent"]).items():
        for fn in BUILDERS:
            for name, svg in fn(p, c).items():
                out = ASSETS / f"{name}-{theme_name}.svg"
                out.write_text(svg, encoding="utf-8")
                print("wrote", out.relative_to(ROOT))
    write_readme(p)


if __name__ == "__main__":
    main()
