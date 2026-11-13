#!/usr/bin/env python3
"""Generator aset README profil.

Semua data diambil dari profile.json. Jalankan:
    python3 build.py
Hasilnya ditulis ke folder assets/ (versi -dark dan -light untuk tiap aset).
Tanpa dependensi luar, cukup Python 3.8+.
"""
import json
import pathlib

import sketch
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
            "paper": "#0d1117", "grid": "#1a2029", "ink": "#e6edf3", "ink2": "#9da7b3", "dark": True,
        },
        "light": {
            "bg": "#ffffff", "surface": "#f6f8fa", "border": "#d0d7de",
            "text": "#1f2328", "muted": "#59636e", "faint": "#eaeef2",
            "accent": accent, "accent_text": shade(accent, 0.62),
            "paper": "#fffcf5", "grid": "#efe9dc", "ink": "#2b2f36", "ink2": "#5d6570", "dark": False,
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


# ──────────────────────── KALENDER KONTRIBUSI ───────────────────────
GQL = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch_contributions(user):
    """Ambil kalender dari GitHub GraphQL API. Butuh env GITHUB_TOKEN.
    Mengembalikan list minggu; tiap minggu = list hari {date, count, level}."""
    import os
    import urllib.request
    token = os.environ.get("GITHUB_TOKEN")
    if os.environ.get("CALENDAR_SAMPLE"):           # hanya untuk preview lokal
        return sample_contributions()
    if not token:
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": GQL, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-readme-build"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
    except Exception as exc:
        if os.environ.get("CI"):
            raise
        print(f"warning: gagal mengambil kontribusi ({exc}); kalender tidak diubah")
        return None
    if "errors" in data:
        if os.environ.get("CI"):
            raise SystemExit(f"GraphQL error: {data['errors']}")
        print(f"warning: GraphQL error ({data['errors']}); kalender tidak diubah")
        return None
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [[{"date": d["date"], "count": d["contributionCount"],
              "level": LEVELS.get(d["contributionLevel"], 0)} for d in w["contributionDays"]]
            for w in weeks]


def sample_contributions():
    """Data contoh deterministik untuk preview; tidak pernah di-commit."""
    import datetime
    import random
    rnd = random.Random(7)
    end = datetime.date.today()
    start = end - datetime.timedelta(days=364 + (end.weekday() + 1) % 7)
    weeks, day = [], start
    while day <= end:
        if not weeks or day.weekday() == 6:
            weeks.append([])
        n = 0 if rnd.random() < 0.35 else int(rnd.expovariate(0.25))
        weeks[-1].append({"date": day.isoformat(), "count": n,
                          "level": 0 if n == 0 else min(4, 1 + n // 4)})
        day += datetime.timedelta(days=1)
    return weeks


def streaks(days):
    cur = best = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        best = max(best, run)
    for d in reversed(days):                         # hari ini boleh masih 0
        if d["count"]:
            cur += 1
        elif d is not days[-1]:
            break
    return cur, best


def calendar_flat(p, c, weeks):
    import datetime
    W, PAD = 900, 36
    CELL, STEP = 12, 15
    GX, GY = PAD + 30, 132                              # pojok kiri-atas grid
    lv = [c["faint"], c["accent"], c["accent"], c["accent"], c["accent"]]
    op = [1, 0.3, 0.5, 0.75, 1]
    H = GY + 7 * STEP + 52
    parts = []

    if weeks:
        days = [d for w in weeks for d in w]
        total = sum(d["count"] for d in days)
        cur, best = streaks(days)
        top = max(days, key=lambda d: d["count"])
        stats = [(f"{total:,}", "contributions in the last year"),
                 (f"{cur}", "day current streak"), (f"{best}", "day longest streak")]
        # sel
        for wi, w in enumerate(weeks[-53:]):
            for d in w:
                wd = (datetime.date.fromisoformat(d["date"]).weekday() + 1) % 7   # Minggu = 0
                parts.append(f'<rect x="{GX + wi * STEP}" y="{GY + wd * STEP}" width="{CELL}" height="{CELL}" rx="3" '
                             f'fill="{lv[d["level"]]}" fill-opacity="{op[d["level"]]}"><title>{d["date"]}: {d["count"]}</title></rect>')
        # label bulan
        last = None
        for wi, w in enumerate(weeks[-53:]):
            m = datetime.date.fromisoformat(w[0]["date"]).strftime("%b")
            if m != last and wi < 51:
                parts.append(f'<text x="{GX + wi * STEP}" y="{GY - 10}" font-family="{MONO}" font-size="12" fill="{c["muted"]}">{m}</text>')
                last = m
        foot = f'Most active: {datetime.date.fromisoformat(top["date"]).strftime("%d %b %Y")} · {top["count"]} contributions'
    else:
        stats = [("—", "waiting for first sync"), ("—", "day current streak"), ("—", "day longest streak")]
        for wi in range(53):
            for wd in range(7):
                parts.append(f'<rect x="{GX + wi * STEP}" y="{GY + wd * STEP}" width="{CELL}" height="{CELL}" rx="3" fill="{c["faint"]}"/>')
        foot = "Updated automatically by GitHub Actions"

    for i, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        parts.append(f'<text x="{PAD}" y="{GY + i * STEP + 10}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">{name}</text>')
    # statistik di header
    sx = PAD
    head = []
    for num, label in stats:
        head.append(f'<text x="{sx}" y="88" font-family="{SANS}" font-size="15" fill="{c["muted"]}">'
                    f'<tspan font-size="22" font-weight="700" fill="{c["accent_text"]}">{t(num)}</tspan> {t(label)}</text>')
        sx += int(text_width(num, 22) + text_width(label, 15)) + 48
    # legenda
    ly = H - 30
    legend = [f'<text x="{W - PAD - 150}" y="{ly + 10}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">Less</text>']
    for i in range(5):
        legend.append(f'<rect x="{W - PAD - 114 + i * 16}" y="{ly}" width="{CELL}" height="{CELL}" rx="3" fill="{lv[i]}" fill-opacity="{op[i]}"/>')
    legend.append(f'<text x="{W - PAD - 30}" y="{ly + 10}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">More</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Contribution calendar">
  <title>Contribution calendar for {t(p["github_user"])}</title>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}"/>
  <text x="{PAD}" y="52" font-family="{SANS}" font-size="24" font-weight="700" fill="{c["text"]}">Contributions</text>
  <rect x="{PAD}" y="64" width="44" height="4" rx="2" fill="{c["accent"]}"/>
  {"".join(head)}
  {"".join(parts)}
  <text x="{PAD}" y="{ly + 10}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">{t(foot)}</text>
  {"".join(legend)}
</svg>
'''


def mix(a, b, k):
    """Campur warna hex a→b dengan rasio k (0..1)."""
    pa = [int(a.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * k) for x, y in zip(pa, pb))


def calendar_3d(p, c, weeks):
    """Kalender kontribusi isometrik: tiap hari = balok, tinggi ~ jumlah kontribusi."""
    import datetime
    W, H, PAD = 900, 450, 36
    UX, UY = 13.0, -4.0          # sumbu minggu (ke kanan-atas)
    VX, VY = 10.0, 6.5           # sumbu hari (ke kanan-bawah)
    OX, OY = 66.0, 332.0         # titik asal (minggu 0, Minggu)
    FILL, HMAX = 0.78, 62.0      # ukuran balok di dalam sel, tinggi maksimum
    dark = c["bg"] == "#0d1117"
    empty = "#1c2128" if dark else "#e4e8ec"
    lv = [empty] + [mix(empty, c["accent"], k) for k in (0.38, 0.6, 0.8, 1.0)]
    side_l, side_r = (0.72, 0.52) if dark else (0.86, 0.70)
    shade = lambda col, k: mix("#000000", col, k)

    def pt(w, d, z=0.0):
        return OX + w * UX + d * VX, OY + w * UY + d * VY - z

    def poly(points, fill):
        return '<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in points) + f'Z" fill="{fill}"/>'

    if weeks:
        weeks = weeks[-53:]
        days = [d for w in weeks for d in w]
        counts = sorted(d["count"] for d in days if d["count"])
        cap = counts[int(len(counts) * 0.95) - 1] if counts else 1
        total = sum(d["count"] for d in days)
        cur, best = streaks(days)
        top = max(days, key=lambda d: d["count"])
        stats = [(f"{total:,}", "contributions"), (str(cur), "day current streak"), (str(best), "day longest streak")]
        foot = f'Most active: {datetime.date.fromisoformat(top["date"]).strftime("%d %b %Y")} · {top["count"]} contributions'
    else:
        days = None
        cap = 1
        stats = [("—", "waiting for first sync"), ("—", "day current streak"), ("—", "day longest streak")]
        foot = "Updated automatically by GitHub Actions"

    cells = []                                   # (w, d, level, count, date)
    if weeks:
        for wi, w in enumerate(weeks):
            for d in w:
                wd = (datetime.date.fromisoformat(d["date"]).weekday() + 1) % 7
                cells.append((wi, wd, d["level"], d["count"], d["date"]))
    else:
        cells = [(wi, wd, 0, 0, None) for wi in range(53) for wd in range(7)]

    # gambar dari belakang ke depan (painter's algorithm)
    cells.sort(key=lambda e: (UY * e[0] + VY * e[1], e[0]))
    m = (1 - FILL) / 2
    blocks = []
    for w, d, level, count, date in cells:
        h = 2.5 if not count else 5 + HMAX * min(count, cap) / cap
        a, b = w + m, w + 1 - m
        e, f = d + m, d + 1 - m
        col = lv[level]
        top_face = poly([pt(a, e, h), pt(b, e, h), pt(b, f, h), pt(a, f, h)], col)
        left = poly([pt(a, e), pt(a, f), pt(a, f, h), pt(a, e, h)], shade(col, side_l))
        front = poly([pt(a, f), pt(b, f), pt(b, f, h), pt(a, f, h)], shade(col, side_r))
        tip = f"<title>{date}: {count}</title>" if date else ""
        blocks.append(f"<g>{tip}{left}{front}{top_face}</g>")

    # label bulan di sepanjang tepi depan
    months = []
    if weeks:
        last = None
        for wi, w in enumerate(weeks):
            mname = datetime.date.fromisoformat(w[0]["date"]).strftime("%b")
            if mname != last and wi < 51:
                x, y = pt(wi + 0.2, 7.6)
                months.append(f'<text transform="translate({x:.1f} {y + 12:.1f}) rotate(-17.1)" font-family="{MONO}" '
                              f'font-size="11" fill="{c["muted"]}">{mname}</text>')
                last = mname

    head = []
    for i, (num, label) in enumerate(stats):
        y = 112 + i * 40
        head.append(f'<text x="{PAD}" y="{y}" font-family="{SANS}" font-size="15" fill="{c["muted"]}">'
                    f'<tspan font-size="24" font-weight="700" fill="{c["accent_text"]}">{t(num)}</tspan> {t(label)}</text>')

    ly = H - 32
    legend = [f'<text x="{W - PAD - 150}" y="{ly + 10}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">Less</text>']
    for i in range(5):
        legend.append(f'<rect x="{W - PAD - 114 + i * 16}" y="{ly}" width="12" height="12" rx="3" fill="{lv[i]}"/>')
    legend.append(f'<text x="{W - PAD - 30}" y="{ly + 10}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">More</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="3D contribution calendar">
  <title>3D contribution calendar for {t(p["github_user"])}</title>
  <defs>
    <radialGradient id="cal-glow" cx="70%" cy="45%" r="55%">
      <stop offset="0" stop-color="{c["accent"]}" stop-opacity="{0.14 if dark else 0.10}"/>
      <stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#cal-glow)"/>
  <text x="{PAD}" y="52" font-family="{SANS}" font-size="24" font-weight="700" fill="{c["text"]}">Contributions</text>
  <rect x="{PAD}" y="64" width="44" height="4" rx="2" fill="{c["accent"]}"/>
  {"".join(head)}
  {"".join(blocks)}
  {"".join(months)}
  <text x="{PAD}" y="{ly + 10}" font-family="{MONO}" font-size="11" fill="{c["muted"]}">{t(foot)}</text>
  {"".join(legend)}
</svg>
'''


# ────────────────────────────── FOOTER ──────────────────────────────
def footer(p, c):
    W, H, PAD = 900, 230, 44
    email = p["links"]["email"]
    ew = int(len(email) * 17 * 0.62) + 68          # font mono: lebar per huruf ~0.6em
    dark = c["bg"] == "#0d1117"

    def cube(x, y, s, k):
        """Kubus isometrik kecil sebagai dekorasi (senada dengan kalender 3D)."""
        top = mix(c["bg"], c["accent"], k)
        l, r = mix("#000000", top, 0.72 if dark else 0.86), mix("#000000", top, 0.52 if dark else 0.70)
        h = s * 0.58
        return (f'<path d="M{x} {y}l{s} {-h}l{s} {h}l{-s} {h}z" fill="{top}"/>'
                f'<path d="M{x} {y}l{s} {h}v{s * 1.15}l{-s} {-h}z" fill="{l}"/>'
                f'<path d="M{x + s} {y + h}l{s} {-h}v{s * 1.15}l{-s} {h}z" fill="{r}"/>')

    cubes = "".join([cube(700, 86, 26, 1.0), cube(752, 116, 20, 0.6), cube(668, 140, 16, 0.4),
                     cube(790, 64, 14, 0.8)])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{t(p["footer"]["cta"])} {t(email)}">
  <title>{t(p["footer"]["cta"])} — {t(email)}</title>
  <defs>
    <radialGradient id="ft-glow" cx="82%" cy="50%" r="50%">
      <stop offset="0" stop-color="{c["accent"]}" stop-opacity="{0.20 if dark else 0.14}"/>
      <stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/>
    </radialGradient>
    <style>
      .bob {{ animation: bob 5s ease-in-out infinite; }}
      @keyframes bob {{ 50% {{ transform: translateY(-5px); }} }}
      @media (prefers-reduced-motion: reduce) {{ .bob {{ animation: none; }} }}
    </style>
  </defs>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#ft-glow)"/>
  <text x="{PAD}" y="66" font-family="{MONO}" font-size="15" fill="{c["accent_text"]}">// get in touch</text>
  <text x="{PAD}" y="106" font-family="{SANS}" font-size="30" font-weight="800" fill="{c["text"]}">{t(p["footer"]["cta"])}</text>
  <text x="{PAD}" y="136" font-family="{SANS}" font-size="16" fill="{c["muted"]}">{t(p["footer"]["sub"])}</text>
  <g transform="translate({PAD} 156)">
    <rect width="{ew}" height="44" rx="22" fill="{c["accent"]}" fill-opacity="0.14" stroke="{c["accent"]}" stroke-opacity="0.55"/>
    <g transform="translate(16 10)" fill="none" stroke="{c["accent_text"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS["email"]}</g>
    <text x="50" y="28" font-family="{MONO}" font-size="17" font-weight="600" fill="{c["text"]}">{t(email)}</text>
  </g>
  <g class="bob">{cubes}</g>
</svg>
'''


# ──────────────────────── TEMA SKETSA (coretan) ──────────────────────
def paper(W, H, c, pen, fonts, seed_note=""):
    """Kertas: latar, kotak-kotak buku tulis tipis, bingkai coretan. Mengembalikan (defs, body)."""
    defs = (f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<path d="M24 0H0V24" fill="none" stroke="{c["grid"]}" stroke-width="1"/></pattern>')
    body = (f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="16" fill="{c["paper"]}"/>'
            f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="16" fill="url(#grid)"/>'
            + pen.box(6, 6, W - 12, H - 12, r=16, color=c["ink2"], width=1.6, wobble=1.6))
    return defs, body


def svg_doc(W, H, label, fonts, defs, body, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{t(label)}">
  <title>{t(label)}</title>
  <defs>{defs}<style>{fonts.css()}{extra_css}</style></defs>
  {body}
</svg>
'''


def stack_sketch(p, c):
    W, PAD, LABEL_W = 900, 40, 168
    PILL_H, GAP_X, GAP_Y, FS, ICON = 46, 11, 16, 25, 22
    fonts = sketch.Fonts()
    pen = sketch.Pen(seed=11, ink=c["ink"])
    parts = []

    # judul + stabilo + doodle
    title = "Tech Stack"
    tw = fonts.width("hand", title, 46)
    parts.append(pen.highlight(PAD - 6, 62, tw + 14, 18, c["accent"], opacity=0.38 if c["dark"] else 0.32))
    parts.append(fonts.text("hand", title, PAD, 72, 46, c["ink"]))
    parts.append(pen.star(PAD + tw + 26, 46, 11, color=c["accent_text"]))
    parts.append(pen.sparkle(PAD + tw + 52, 66, 6, color=c["ink2"], width=1.5))
    note = "my everyday toolkit"
    nw = fonts.width("note", note, 20)
    parts.append(fonts.text("note", note, W - PAD - nw, 50, 20, c["ink2"]))
    parts.append(pen.arrow(W - PAD - nw * 0.55, 60, W - PAD - nw * 0.85, 98, curve=-18, color=c["ink2"], width=1.6))

    y = 118
    for gi, (group, items) in enumerate(p["stack"].items()):
        lw = fonts.width("hand", group, 26)
        parts.append(fonts.text("hand", group, PAD, y + 31, 26, c["accent_text"]))
        parts.append(pen.squiggle(PAD, y + 42, min(lw, LABEL_W - 30), amp=2.5, waves=3, color=c["accent_text"], width=1.6))
        x = PAD + LABEL_W
        for name in items:
            pw = int(fonts.width("hand", name, FS)) + ICON + 36
            if x + pw > W - PAD:
                x, y = PAD + LABEL_W, y + PILL_H + GAP_Y
            rot = pen.r.uniform(-1.4, 1.4)
            cx, cy = x + pw / 2, y + PILL_H / 2
            hex_ = (sketch.brand(name) or (c["accent"],))[0]
            blob = f'<circle cx="{x + 12 + ICON / 2:.1f}" cy="{cy:.1f}" r="{ICON / 2 + 5}" fill="{hex_}" fill-opacity="{0.22 if c["dark"] else 0.16}"/>'
            parts.append(
                f'<g transform="rotate({rot:.2f} {cx:.1f} {cy:.1f})">'
                + pen.box(x, y, pw, PILL_H, r=14, color=c["ink"], width=1.5, fill=c["paper"], wobble=1.1)
                + blob
                + sketch.icon(name, x + 12, cy - ICON / 2, ICON, c["ink"], c["dark"])
                + fonts.text("hand", name, x + 12 + ICON + 10, cy + 8.5, FS, c["ink"])
                + "</g>")
            x += pw + GAP_X
        y += PILL_H + 30

    # doodle penutup di pojok kanan bawah
    parts.append(pen.spiral(W - PAD - 14, y - 6, 12, color=c["ink2"], width=1.4))
    H = y + 24
    defs, bg = paper(W, H, c, pen, fonts)
    label = "Tech stack: " + ", ".join(n for g in p["stack"].values() for n in g)
    return svg_doc(W, H, label, fonts, defs, bg + "".join(parts))


def hero_sketch(p, c):
    W, H = 1200, 340
    fonts = sketch.Fonts()
    pen = sketch.Pen(seed=5, ink=c["ink"])
    parts = []
    X = 70

    # sapaan kecil + ombak
    hi = "hi there, I'm"
    parts.append(fonts.text("note", hi, X + 4, 84, 26, c["ink2"]))
    parts.append(pen.squiggle(X + 8 + fonts.width("note", hi, 26) + 10, 76, 34, amp=4, waves=2, color=c["accent_text"], width=2))

    # nama besar dengan stabilo + garis bawah yang "digambar"
    name = p["name"]
    nw = fonts.width("hand", name, 104)
    parts.append(pen.highlight(X - 8, 160, nw + 18, 34, c["accent"], opacity=0.36 if c["dark"] else 0.30))
    parts.append(fonts.text("hand", name, X, 176, 104, c["ink"]))
    parts.append(f'<g class="draw">{pen.underline(X + 4, 198, nw * 0.62, color=c["accent_text"], width=3, loops=True)}</g>')
    parts.append(pen.star(X + nw + 30, 104, 14, color=c["accent_text"], width=2.2))
    parts.append(pen.sparkle(X + nw + 58, 136, 8, color=c["ink2"]))

    # tagline + lokasi
    parts.append(fonts.text("hand", p["tagline"], X + 2, 256, 36, c["ink2"]))
    pin_x, pin_y = X + 10, 294
    parts.append(pen.ellipse(pin_x, pin_y - 4, 6, 6, passes=1, color=c["accent_text"], width=2))
    parts.append(pen.line(pin_x, pin_y + 2, pin_x, pin_y + 10, passes=1, color=c["accent_text"], width=2))
    parts.append(fonts.text("note", f'based in {p["location"]}', pin_x + 16, pin_y + 6, 22, c["ink2"]))

    # kanan: wireframe coretan → kode
    gx, gy, gw, gh = 860, 66, 280, 200
    wf = [pen.box(gx, gy, gw, gh, r=12, color=c["ink"], width=1.8, fill=c["paper"]),
          pen.line(gx + 4, gy + 32, gx + gw - 4, gy + 32, color=c["ink"], width=1.5)]
    for i, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        wf.append(f'<circle cx="{gx + 20 + i * 17}" cy="{gy + 17}" r="5" fill="{col}"/>')
        wf.append(pen.ellipse(gx + 20 + i * 17, gy + 17, 5.5, 5.5, passes=1, color=c["ink"], width=1.1))
    # gambar placeholder dengan arsiran + gunung
    ix, iy, iw, ih = gx + 20, gy + 50, 104, 80
    wf.append(f'<clipPath id="img"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="6"/></clipPath>')
    wf.append(pen.hachure(ix, iy, iw, ih, c["accent"], gap=7, opacity=0.55, clip_id="img"))
    wf.append(pen.box(ix, iy, iw, ih, r=6, color=c["ink"], width=1.5))
    wf.append(f'<path d="M{ix + 18} {iy + 62}l22-26 16 16 12-10 20 20" fill="none" stroke="{c["ink"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    wf.append(pen.ellipse(ix + 80, iy + 22, 7, 7, passes=1, color=c["ink"], width=1.6))
    # baris teks sebagai coretan + tombol
    tx = gx + 142
    wf.append(pen.line(tx, gy + 60, tx + 112, gy + 60, color=c["ink"], width=3))
    wf.append(pen.squiggle(tx, gy + 82, 90, amp=2, waves=4, color=c["ink2"], width=1.6))
    wf.append(pen.squiggle(tx, gy + 100, 104, amp=2, waves=5, color=c["ink2"], width=1.6))
    bx, by = tx, gy + 116
    wf.append(f'<clipPath id="btn"><rect x="{bx}" y="{by}" width="74" height="26" rx="13"/></clipPath>')
    wf.append(pen.hachure(bx, by, 74, 26, c["accent"], gap=4, width=1.6, opacity=0.9, clip_id="btn"))
    wf.append(pen.box(bx, by, 74, 26, r=13, color=c["ink"], width=1.5))
    wf.append(fonts.text("note", "</> code", gx + 22, gy + 170, 22, c["accent_text"]))
    wf.append(pen.squiggle(gx + 120, gy + 164, 130, amp=2, waves=6, color=c["ink2"], width=1.4))
    parts.append(f'<g class="float">{"".join(wf)}</g>')

    # anotasi tangan
    parts.append(fonts.text("hand", "design", 748, 92, 30, c["accent_text"]))
    parts.append(pen.arrow(790, 102, 852, 130, curve=-22, color=c["accent_text"], width=2))
    parts.append(fonts.text("note", "pixels -> code", 726, 300, 22, c["ink2"]))
    parts.append(pen.arrow(840, 290, 900, 272, curve=14, color=c["ink2"], width=1.6))
    parts.append(pen.spiral(1150, 300, 11, color=c["ink2"], width=1.4))

    # tanpa animasi pun garis tetap tampil; efek "digambar" hanya lewat keyframes
    css = (".draw path{animation:draw 1.8s .3s ease-out backwards}"
           "@keyframes draw{from{stroke-dasharray:900;stroke-dashoffset:900}to{stroke-dasharray:900;stroke-dashoffset:0}}"
           ".float{animation:float 6s ease-in-out infinite}@keyframes float{50%{transform:translateY(-6px)}}"
           "@media (prefers-reduced-motion:reduce){.draw path,.float{animation:none}}")
    defs, bg = paper(W, H, c, pen, fonts)
    return svg_doc(W, H, f'{p["name"]} — {p["tagline"]}', fonts, defs, bg + "".join(parts), css)


def button_sketch(key, c):
    W, H = 232, 72
    fonts = sketch.Fonts()
    pen = sketch.Pen(seed=sum(map(ord, key)), ink=c["ink"])
    label = BUTTON_LABELS[key]
    rot = pen.r.uniform(-1.6, 1.6)
    bx, by, bw, bh = 8, 9, W - 16, H - 18
    ix, iy = bx + 16, by + (bh - 26) / 2
    body = [
        pen.box(bx, by, bw, bh, r=14, color=c["ink"], width=1.7, fill=c["paper"], wobble=1.2),
        f'<clipPath id="hb"><circle cx="{ix + 13}" cy="{iy + 13}" r="17"/></clipPath>',
        pen.hachure(ix - 6, iy - 6, 38, 38, c["accent"], gap=4.5, width=1.4, opacity=0.55, clip_id="hb"),
        f'<g transform="translate({ix + 1} {iy + 1})" fill="none" stroke="{c["ink"]}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</g>',
        fonts.text("hand", label, ix + 40, by + bh / 2 + 9, 28, c["ink"]),
        pen.arrow(W - 50, by + bh / 2 + 7, W - 30, by + bh / 2 - 9, curve=-6, color=c["accent_text"], width=2, head=7),
    ]
    g = f'<g transform="rotate({rot:.2f} {W / 2} {H / 2})">{"".join(body)}</g>'
    return svg_doc(W, H, label, fonts, "", g)


def buttons_sketch(p, c):
    return {f"btn-{k}": button_sketch(k, c) for k in BUTTON_LABELS}


def calendar_sketch(p, c, weeks, foot=None, empty_note=None):
    """Kalender isometrik 3D bergaya coretan: balok bergaris tinta di atas kertas."""
    import datetime
    W, H, PAD = 900, 470, 40
    UX, UY = 13.0, -4.0
    VX, VY = 10.0, 6.5
    OX, OY = 92.0, 346.0
    FILL, HMAX = 0.80, 64.0
    fonts = sketch.Fonts()
    pen = sketch.Pen(seed=3, ink=c["ink"])
    dark = c["dark"]
    empty = mix(c["paper"], c["ink"], 0.10 if dark else 0.07)
    lv = [empty] + [mix(c["paper"], c["accent"], k) for k in (0.40, 0.62, 0.82, 1.0)]
    side_l, side_r = (0.70, 0.50) if dark else (0.86, 0.70)
    outline = mix(c["paper"], c["ink"], 0.55 if dark else 0.75)

    def pt(w, d, z=0.0):
        return OX + w * UX + d * VX, OY + w * UY + d * VY - z

    def face(points, fill, stroke=True):
        d = "M" + "L".join(f"{x + pen.j(0.35):.1f} {y + pen.j(0.35):.1f}" for x, y in points) + "Z"
        st = f' stroke="{outline}" stroke-width="0.9" stroke-linejoin="round"' if stroke else ""
        return f'<path d="{d}" fill="{fill}"{st}/>'

    cells, stats, peak = [], None, None
    if weeks:
        weeks = weeks[-53:]
        days = [d for w in weeks for d in w]
        counts = sorted(d["count"] for d in days if d["count"])
        cap = counts[int(len(counts) * 0.95) - 1] if counts else 1
        cur, best = streaks(days)
        stats = (sum(d["count"] for d in days), cur, best)
        for wi, w in enumerate(weeks):
            for d in w:
                wd = (datetime.date.fromisoformat(d["date"]).weekday() + 1) % 7
                cells.append((wi, wd, d["level"], d["count"], d["date"]))
        top = max(cells, key=lambda e: e[3])
        peak = top
    else:
        cap = 1
        cells = [(wi, wd, 0, 0, None) for wi in range(53) for wd in range(7)]

    cells.sort(key=lambda e: (UY * e[0] + VY * e[1], e[0]))
    m = (1 - FILL) / 2
    animate = p.get("calendar_animate", True)
    # tata letak 2D (grid datar seperti kalender GitHub) untuk animasi 3D <-> 2D
    S2, GX, GY = 15.0, (W - 53 * 15) / 2, 262.0

    def p2(w, d):
        return GX + w * S2, GY + d * S2

    def num(v):
        return str(round(v))

    def path_d(points):
        return "M" + "L".join(f"{num(x)} {num(y)}" for x, y in points) + "Z"

    # animasi "to" dari bentuk sekarang; dipicu jam bersama #g (ke 2D) / #b (ke 3D)
    EASE = 'calcMode="spline" keyTimes="0;1" keySplines=".6 0 .3 1"'

    def face(points, flat_pts, fill, stroke=True):
        a = path_d([(x + pen.j(0.5), y + pen.j(0.5)) for x, y in points])
        st = f' stroke="{outline}" stroke-width="0.9" stroke-linejoin="round"' if stroke else ""
        if not animate:
            return f'<path d="{a}" fill="{fill}"{st}/>'
        return (f'<path d="{a}" fill="{fill}"{st}>'
                f'<animate attributeName="d" to="{path_d(flat_pts)}" begin="g.begin" dur="1.2s" fill="freeze"/>'
                f'<animate attributeName="d" to="{a}" begin="b.begin" dur="1.2s" fill="freeze"/></path>')

    blocks = []
    for w, d, level, count, date in cells:
        h = 2.0 if not count else 5 + HMAX * min(count, cap) / cap
        a, b, e, f = w + m, w + 1 - m, d + m, d + 1 - m
        col = lv[level]
        tip = f"<title>{date}: {count}</title>" if date else ""
        top3 = [pt(a, e, h), pt(b, e, h), pt(b, f, h), pt(a, f, h)]
        top2 = [p2(a, e), p2(b, e), p2(b, f), p2(a, f)]
        if not count:
            blocks.append(face(top3, top2, col, stroke=False))
            continue
        blocks.append("<g>" + tip
                      + face([pt(a, e), pt(a, f), pt(a, f, h), pt(a, e, h)],
                             [p2(a, e), p2(a, f), p2(a, f), p2(a, e)], mix("#000000", col, side_l))
                      + face([pt(a, f), pt(b, f), pt(b, f, h), pt(a, f, h)],
                             [p2(a, f), p2(b, f), p2(b, f), p2(a, f)], mix("#000000", col, side_r))
                      + face(top3, top2, col) + "</g>")

    def fade(show_in_3d=True):
        """Opacity: tampil di 3D lalu hilang di 2D (True), atau sebaliknya (False)."""
        if not animate:
            return ""
        # yang akan hilang memudar cepat di awal transisi; yang akan muncul menyusul di akhir
        if show_in_3d:
            return ('<animate attributeName="opacity" to="0" begin="g.begin" dur=".4s" fill="freeze"/>'
                    '<animate attributeName="opacity" to="1" begin="b.begin+.8s" dur=".4s" fill="freeze"/>')
        return ('<animate attributeName="opacity" to="1" begin="g.begin+.8s" dur=".4s" fill="freeze"/>'
                '<animate attributeName="opacity" to="0" begin="b.begin" dur=".4s" fill="freeze"/>')

    parts = []
    # judul
    title = "Contributions"
    tw = fonts.width("hand", title, 44)
    parts.append(pen.highlight(PAD - 6, 58, tw + 14, 18, c["accent"], opacity=0.38 if dark else 0.32))
    parts.append(fonts.text("hand", title, PAD, 68, 44, c["ink"]))
    parts.append(pen.sparkle(PAD + tw + 22, 44, 8, color=c["accent_text"]))
    if animate:
        mx = PAD + tw + 44
        parts.append(f'<g>{fonts.text("note", "(3D view)", mx, 62, 20, c["ink2"])}{fade(True)}</g>')
        parts.append(f'<g opacity="0">{fonts.text("note", "(2D view)", mx, 62, 20, c["ink2"])}{fade(False)}</g>')

    # statistik sebagai catatan tangan
    if stats:
        total, cur, best = stats
        num = f"{total:,}"
        nw = fonts.width("hand", num, 46)
        parts.append(fonts.text("hand", num, PAD + 4, 134, 46, c["accent_text"]))
        parts.append(pen.ellipse(PAD + 4 + nw / 2, 120, nw / 2 + 16, 26, color=c["accent_text"], width=1.8))
        parts.append(fonts.text("note", "contributions this year", PAD + nw + 30, 128, 21, c["ink2"]))
        parts.append(fonts.text("hand", f"{cur} day streak", PAD + 4, 182, 30, c["ink"]))
        parts.append(pen.squiggle(PAD + 4, 192, fonts.width("hand", f"{cur} day streak", 30), amp=2, waves=4,
                                  color=c["accent_text"], width=1.6))
        parts.append(fonts.text("note", f"longest: {best} days", PAD + 4, 222, 21, c["ink2"]))
        # anotasi hari terbaik
        w, d, _, count, date = peak
        h = 5 + HMAX * min(count, cap) / cap
        tx, ty = pt(w + 0.5, d + 0.5, h)
        label = f"best day! ({count})"
        lw = fonts.width("note", label, 21)
        parts.append("<g>")
        ly0 = max(ty - 44, 34)
        if tx + 30 + lw < W - PAD:          # label di kanan atas balok
            lx = tx + 30
            parts.append(pen.arrow(lx - 2, ly0 + 2, tx + 4, ty - 6, curve=10, color=c["accent_text"], width=1.8, head=8))
        else:                               # tidak muat: di kiri atas balok
            lx = tx - 30 - lw
            parts.append(pen.arrow(lx + lw + 2, ly0 + 2, tx - 4, ty - 6, curve=-10, color=c["accent_text"], width=1.8, head=8))
        parts.append(fonts.text("note", label, lx, ly0 + 6, 21, c["accent_text"]))
        parts.append(fade(True) + "</g>")
        # label bulan
        last = None
        for wi, wk in enumerate(weeks):
            mname = datetime.date.fromisoformat(wk[0]["date"]).strftime("%b")
            if mname != last and wi < 51:
                x, y = pt(wi + 0.2, 7.7)
                x2, y2 = p2(wi + 0.1, 0)
                tr = ro = ""
                if animate:
                    at = 'attributeName="transform" dur="1.2s" fill="freeze" ' + EASE
                    tr = (f'<animateTransform {at} type="translate" to="{x2:.1f} {y2 - 8:.1f}" begin="g.begin"/>'
                          f'<animateTransform {at} type="translate" to="{x:.1f} {y + 14:.1f}" begin="b.begin"/>')
                    ro = (f'<animateTransform {at} type="rotate" to="0" begin="g.begin"/>'
                          f'<animateTransform {at} type="rotate" to="-17.1" begin="b.begin"/>')
                parts.append(f'<g transform="translate({x:.1f} {y + 14:.1f})">{tr}<g transform="rotate(-17.1)">{ro}'
                             + fonts.text("note", mname, 0, 0, 16, c["ink2"]) + "</g></g>")
                last = mname
        foot = foot or "drawn fresh every day by GitHub Actions"
    else:
        parts.append(fonts.text("hand", empty_note or "waiting for the first sync...", PAD + 4, 134, 32, c["ink2"]))
        parts.append(pen.arrow(PAD + 120, 150, PAD + 170, 230, curve=20, color=c["ink2"], width=1.8))
        foot = foot or "updated automatically by GitHub Actions"

    if animate:
        for i, dname in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
            parts.append(f'<g opacity="0">{fonts.text("note", dname, GX - 34, GY + i * S2 + 11, 14, c["ink2"])}{fade(False)}</g>')
        # jam bersama: 3D ditahan ~5 dtk -> berubah 1.2 dtk -> 2D ditahan 5 dtk -> kembali
        parts.append('<rect width="0" height="0">'
                     '<animate id="g" attributeName="x" from="0" to="0" begin="4s;b.end+5s" dur="1.2s"/>'
                     '<animate id="b" attributeName="x" from="0" to="0" begin="g.end+5s" dur="1.2s"/></rect>')

    ly = H - 34
    parts.append(fonts.text("note", foot, PAD, ly + 12, 18, c["ink2"]))
    lx0 = W - PAD - 150
    parts.append(fonts.text("note", "less", lx0, ly + 12, 18, c["ink2"]))
    for i in range(5):
        parts.append(pen.box(lx0 + 34 + i * 18, ly, 13, 13, r=3, passes=1, color=outline, width=1, fill=lv[i], wobble=0.5))
    parts.append(fonts.text("note", "more", lx0 + 128, ly + 12, 18, c["ink2"]))

    defs, bg = paper(W, H, c, pen, fonts)
    return svg_doc(W, H, f'3D contribution calendar for {p["github_user"]}', fonts, defs,
                   bg + "".join(blocks) + "".join(parts))


def footer_sketch(p, c):
    W, H, PAD = 900, 260, 44
    fonts = sketch.Fonts()
    pen = sketch.Pen(seed=21, ink=c["ink"])
    email = p["links"]["email"]
    parts = [fonts.text("note", "// get in touch", PAD, 62, 22, c["accent_text"])]

    cta = p["footer"]["cta"]
    cw = fonts.width("hand", cta, 42)
    parts.append(pen.highlight(PAD - 6, 102, cw + 12, 16, c["accent"], opacity=0.36 if c["dark"] else 0.30))
    parts.append(fonts.text("hand", cta, PAD, 110, 42, c["ink"]))
    parts.append(fonts.text("note", p["footer"]["sub"], PAD, 146, 20, c["ink2"]))

    # email dalam pill coretan berarsir
    ew = fonts.width("hand", email, 28)
    bx, by, bw, bh = PAD, 170, ew + 72, 50
    parts.append(f'<clipPath id="mail"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="25"/></clipPath>')
    parts.append(pen.box(bx, by, bw, bh, r=25, passes=0, fill=c["paper"]))
    parts.append(pen.hachure(bx, by, bw, bh, c["accent"], gap=7, width=1.2, opacity=0.35, clip_id="mail"))
    parts.append(pen.box(bx, by, bw, bh, r=25, color=c["ink"], width=1.7))
    parts.append(f'<g transform="translate({bx + 18} {by + 13})" fill="none" stroke="{c["ink"]}" stroke-width="2" '
                 f'stroke-linecap="round" stroke-linejoin="round">{ICONS["email"]}</g>')
    parts.append(fonts.text("hand", email, bx + 54, by + 34, 28, c["ink"]))
    parts.append(fonts.text("note", "say hi!", bx + bw + 52, by + 33, 20, c["ink2"]))
    parts.append(pen.arrow(bx + bw + 46, by + 27, bx + bw + 12, by + 24, curve=6, color=c["ink2"], width=1.6, head=7))

    # pesawat kertas + jejak putus-putus
    trail = (f'<path d="M560 214C610 226 640 190 616 168C596 150 572 178 600 190C650 212 700 150 738 94" fill="none" '
             f'stroke="{c["ink2"]}" stroke-width="1.8" stroke-dasharray="6 8" stroke-linecap="round"/>')
    px, py = 742, 58
    plane = [f'<path d="M{px} {py + 30}L{px + 86} {py}L{px + 58} {py + 74}L{px + 38} {py + 48}Z" fill="{c["paper"]}"/>',
             f'<path d="M{px + 38} {py + 48}L{px + 86} {py}L{px + 34} {py + 64}Z" fill="{c["accent"]}" fill-opacity="0.45"/>']
    for a, b in [((0, 30), (86, 0)), ((86, 0), (58, 74)), ((58, 74), (38, 48)), ((38, 48), (0, 30)),
                 ((38, 48), (86, 0)), ((38, 48), (34, 64)), ((34, 64), (46, 54))]:
        plane.append(pen.line(px + a[0], py + a[1], px + b[0], py + b[1], color=c["ink"], width=1.8, bow=0.8))
    parts.append(trail)
    parts.append(f'<g class="fly">{"".join(plane)}</g>')
    parts.append(pen.sparkle(706, 70, 7, color=c["accent_text"]))
    parts.append(pen.star(850, 180, 9, color=c["accent_text"]))
    parts.append(pen.sparkle(820, 222, 5, color=c["ink2"], width=1.4))

    css = (".fly{animation:fly 5s ease-in-out infinite}"
           "@keyframes fly{50%{transform:translate(4px,-6px)}}"
           "@media (prefers-reduced-motion:reduce){.fly{animation:none}}")
    defs, bg = paper(W, H, c, pen, fonts)
    return svg_doc(W, H, f'{cta} {email}', fonts, defs, bg + "".join(parts), css)


def wrap(fonts, key, text, size, max_w):
    """Pecah teks jadi baris berdasarkan lebar font sebenarnya."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and fonts.width(key, trial, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + ([cur] if cur else [])


def about_sketch(p, c):
    W, PAD = 900, 44
    fonts = sketch.Fonts()
    pen = sketch.Pen(seed=13, ink=c["ink"])
    parts = []

    title = "About me"
    tw = fonts.width("hand", title, 44)
    parts.append(pen.highlight(PAD - 6, 60, tw + 14, 18, c["accent"], opacity=0.38 if c["dark"] else 0.32))
    parts.append(fonts.text("hand", title, PAD, 70, 44, c["ink"]))
    parts.append(pen.squiggle(PAD + tw + 18, 56, 30, amp=4, waves=2, color=c["accent_text"], width=2))

    # bio
    y = 116
    for line in wrap(fonts, "note", p["bio"], 22, 520):
        parts.append(fonts.text("note", line, PAD, y, 22, c["ink"]))
        y += 32

    # pendidikan dengan topi wisuda
    e = p["education"]
    y += 20
    cx, cy = PAD + 18, y - 8
    cap = (f'<path d="M{cx - 18} {cy}L{cx} {cy - 9}L{cx + 18} {cy}L{cx} {cy + 9}Z" fill="{c["accent"]}" fill-opacity="0.35"/>'
           + pen.line(cx - 18, cy, cx, cy - 9, passes=1, width=1.8) + pen.line(cx, cy - 9, cx + 18, cy, passes=1, width=1.8)
           + pen.line(cx + 18, cy, cx, cy + 9, passes=1, width=1.8) + pen.line(cx, cy + 9, cx - 18, cy, passes=1, width=1.8)
           + f'<path d="M{cx - 10} {cy + 5}v8c6 5 14 5 20 0v-8" fill="none" stroke="{c["ink"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
           + f'<path d="M{cx + 14} {cy + 2}v12" stroke="{c["accent_text"]}" stroke-width="1.8" stroke-linecap="round"/>'
           + f'<circle cx="{cx + 14}" cy="{cy + 16}" r="2.2" fill="{c["accent_text"]}"/>')
    parts.append(cap)
    parts.append(fonts.text("hand", e["school"], PAD + 48, y, 32, c["ink"]))
    sw = fonts.width("hand", e["school"], 32)
    parts.append(pen.underline(PAD + 48, y + 9, sw, color=c["accent_text"], width=2))
    parts.append(fonts.text("note", f'{e["major"]}  ·  {e["years"]}', PAD + 48, y + 38, 21, c["ink2"]))
    H = int(y + 76)

    # catatan tempel "currently"
    nx, ny, nw, nh = 618, 70, 236, 160
    note_bg = mix(c["paper"], c["accent"], 0.22 if c["dark"] else 0.16)
    note = [pen.box(nx, ny, nw, nh, r=6, color=c["ink"], width=1.6, fill=note_bg, wobble=1.0),
            f'<rect x="{nx + nw / 2 - 34}" y="{ny - 10}" width="68" height="22" rx="2" fill="{c["ink2"]}" fill-opacity="0.35" transform="rotate(-4 {nx + nw / 2} {ny})"/>',
            fonts.text("hand", "currently:", nx + 20, ny + 44, 28, c["accent_text"])]
    yy = ny + 80
    for line in wrap(fonts, "hand", p["currently"], 25, nw - 40):
        note.append(fonts.text("hand", line, nx + 20, yy, 25, c["ink"]))
        yy += 30
    note.append(pen.star(nx + nw - 26, ny + nh - 24, 9, color=c["accent_text"]))
    parts.append(f'<g transform="rotate(3 {nx + nw / 2} {ny + nh / 2})">{"".join(note)}</g>')
    parts.append(pen.sparkle(nx - 26, ny + 20, 7, color=c["ink2"]))
    H = max(H, ny + nh + 50)

    defs, bg = paper(W, H, c, pen, fonts)
    return svg_doc(W, H, f'About me: {p["bio"]} Education: {e["school"]}, {e["major"]} ({e["years"]})',
                   fonts, defs, bg + "".join(parts))


# Tiap builder mengembalikan {nama_file_tanpa_tema: isi_svg}.
BUILDERS = [
    lambda p, c: {"hero": hero_sketch(p, c)},
    buttons_sketch,
    lambda p, c: {"about": about_sketch(p, c)},
    lambda p, c: {"stack": stack_sketch(p, c)},
    lambda p, c: {"footer": footer_sketch(p, c)},
]


# ────────────────────────────── README ──────────────────────────────
def picture(name, alt, width=None, height=None, url=None):
    """<picture> gelap/terang. `url` (opsional) = endpoint luar yang menerima ?theme=dark|light."""
    size = (f' width="{width}"' if width else "") + (f' height="{height}"' if height else "")
    src = (lambda th: f"{url}?theme={th}") if url else (lambda th: f"assets/{name}-{th}.svg")
    return (f'<picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="{t(src("dark"))}">'
            f'<source media="(prefers-color-scheme: light)" srcset="{t(src("light"))}">'
            f'<img src="{t(src("dark"))}" alt="{t(alt)}"{size}>'
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

<div align="center">

{picture("about", "About me: " + p["bio"] + " Education: " + e["school"] + ", " + e["major"] + " (" + e["years"] + ")", width="100%")}

<br/><br/>

{picture("stack", "Tech stack", width="100%")}

<br/><br/>

{picture("calendar", "Contribution calendar", width="100%", url=p.get("calendar_url") or None)}

<br/><br/>

<a href="mailto:{t(L["email"])}">{picture("footer", p["footer"]["cta"] + " " + L["email"], width="100%")}</a>

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

    # Kalender: hanya ditulis ulang bila ada data (token tersedia), supaya build lokal
    # tanpa token tidak menimpa kalender asli. Jika belum ada, buat placeholder.
    import os
    weeks = fetch_contributions(p["github_user"])
    cal_dir = pathlib.Path(os.environ.get("CALENDAR_OUT", ASSETS))
    for theme_name, c in themes(p["accent"]).items():
        out = cal_dir / f"calendar-{theme_name}.svg"
        if weeks or not out.exists():
            style = {"3d": calendar_sketch, "3d-solid": calendar_3d, "flat": calendar_flat}[p.get("calendar_style", "3d")]
            out.write_text(style(p, c, weeks), encoding="utf-8")
            print("wrote", out, "(data)" if weeks else "(placeholder)")
        else:
            print("kept", out.relative_to(ROOT), "(tidak ada data baru)")
    write_readme(p)


if __name__ == "__main__":
    main()
