"""Endpoint Vercel: kalender kontribusi 3D bergaya coretan, dibuat saat diminta.

GET /api/contrib?theme=dark|light  ->  image/svg+xml

Butuh environment variable GITHUB_TOKEN di Vercel (personal access token,
cukup akses baca publik). Username diambil dari profile.json, jadi endpoint ini
tidak bisa dipakai untuk akun lain.
"""
import datetime
import json
import pathlib
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402  (generator yang sama dengan aset di repo)

# max-age=0: browser & cache gambar GitHub (camo) selalu cek ulang;
# s-maxage=300: CDN Vercel menyimpan 5 menit, jadi GitHub API dipanggil paling sering ~12x/jam.
CACHE_OK = "public, max-age=0, must-revalidate, s-maxage=300, stale-while-revalidate=60"
CACHE_ERR = "public, max-age=0, must-revalidate, s-maxage=60"


def render(theme):
    p = json.loads((ROOT / "profile.json").read_text(encoding="utf-8"))
    c = build.themes(p["accent"])[theme]
    weeks = build.fetch_contributions(p["github_user"])
    style = {"3d": build.calendar_sketch, "3d-solid": build.calendar_3d,
             "flat": build.calendar_flat}[p.get("calendar_style", "3d")]
    if weeks:
        today = datetime.datetime.now(datetime.timezone.utc).strftime("%d %b %Y")
        foot = f"live from GitHub · updated {today}"
        kw = {"foot": foot} if style is build.calendar_sketch else {}
        return style(p, c, weeks, **kw), True
    kw = ({"foot": "live from GitHub", "empty_note": "couldn't reach GitHub right now..."}
          if style is build.calendar_sketch else {})
    return style(p, c, None, **kw), False


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        theme = q.get("theme", ["dark"])[0]
        if theme not in ("dark", "light"):
            theme = "dark"
        try:
            svg, ok = render(theme)
        except Exception as exc:  # jangan pernah kirim gambar rusak ke README
            print("contrib error:", exc)
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", CACHE_ERR)
            self.end_headers()
            self.wfile.write(b"calendar render failed")
            return
        body = svg.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
        self.send_header("Cache-Control", CACHE_OK if ok else CACHE_ERR)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
