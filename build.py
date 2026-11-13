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


BUILDERS = {
    "hero": hero,
}


def main():
    p = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    ASSETS.mkdir(exist_ok=True)
    for theme_name, c in themes(p["accent"]).items():
        for name, fn in BUILDERS.items():
            out = ASSETS / f"{name}-{theme_name}.svg"
            out.write_text(fn(p, c), encoding="utf-8")
            print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
