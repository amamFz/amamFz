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
        raise SystemExit(f"GraphQL error: {data['errors']}")
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


# Tiap builder mengembalikan {nama_file_tanpa_tema: isi_svg}.
BUILDERS = [
    lambda p, c: {"hero": hero(p, c)},
    buttons,
    lambda p, c: {"stack": stack(p, c)},
    lambda p, c: {"footer": footer(p, c)},
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

<br/><br/>

{picture("calendar", "Contribution calendar", width="100%")}

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
            style = calendar_3d if p.get("calendar_style", "3d") == "3d" else calendar_flat
            out.write_text(style(p, c, weeks), encoding="utf-8")
            print("wrote", out, "(data)" if weeks else "(placeholder)")
        else:
            print("kept", out.relative_to(ROOT), "(tidak ada data baru)")
    write_readme(p)


if __name__ == "__main__":
    main()
