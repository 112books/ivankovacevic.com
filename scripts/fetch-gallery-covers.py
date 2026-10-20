#!/usr/bin/env python3
"""
fetch-gallery-covers.py — Autoallotja les portades de la galeria.

Per què: les portades s'enllaçaven en calent des de blog.pocallum.cat, que respon
amb 'Cross-Origin-Resource-Policy: same-site'. El navegador bloqueja les imatges
encreuades (ERR_BLOCKED_BY_RESPONSE.NotSameSite) i les miniatures no es veien.
Ara es baixen a static/images/galleries/ i el camp 'cover' apunta a la ruta local.

Què fa, per a cada galeria de data/galleries.yaml:
  . cover amb URL externa  -> la baixa, l'optimitza (800 px, JPEG) i la fa local.
  . cover local            -> la conserva (si el fitxer falta, la torna a baixar
                              des de la font original quan és possible).
  . sense cover            -> intenta extreure og:image de la pàgina i la baixa.

Ús:
    python3 scripts/fetch-gallery-covers.py            # baixa i reescriu el YAML
    python3 scripts/fetch-gallery-covers.py --dry-run  # només mostra què faria
"""

import io
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
YAML = ROOT / "data" / "galleries.yaml"
OUT_DIR = ROOT / "static" / "images" / "galleries"
URL_PREFIX = "/images/galleries/"
MAX_W = 800          # les targetes fan ~322 px CSS; 800 px cobreix pantalles 2x
QUALITY = 76
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")
TIMEOUT = 60

OG_IMAGE = [
    r'<meta\s+property=["\']og:image["\']\s+content=["\'](https://[^"\']+)["\']',
    r'<meta\s+content=["\'](https://[^"\']+)["\']\s+property=["\']og:image["\']',
]

stats = {"baixades": 0, "locals": 0, "errors": 0}


def slug(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-").lower()


def fetch(url):
    req = Request(url, headers={"User-Agent": UA, "Referer": "https://ivankovacevic.com/"})
    with urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def optimize(raw, dest):
    """Redimensiona i comprimeix. Pillow (CI) o ImageMagick (local)."""
    try:
        from PIL import Image, ImageOps
    except ImportError:
        Image = None

    if Image is not None:
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw)))
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        return

    with tempfile.NamedTemporaryFile(suffix=".img", delete=False) as tmp:
        tmp.write(raw)
        src = Path(tmp.name)
    try:
        subprocess.run(
            ["magick", str(src), "-auto-orient", "-resize", f"{MAX_W}x>",
             "-strip", "-quality", str(QUALITY), "-interlace", "Plane", str(dest)],
            check=True, capture_output=True,
        )
    finally:
        src.unlink(missing_ok=True)


def og_image(page_url):
    try:
        html = fetch(page_url).decode("utf-8", "replace")
    except Exception as e:
        print(f"    avis: no s'ha pogut llegir {page_url[:60]} - {e}", file=sys.stderr)
        return None
    for pattern in OG_IMAGE:
        m = re.search(pattern, html)
        if m:
            return m.group(1)
    return None


def localize(gid, url, dry):
    """Baixa la portada (si cal) i retorna la ruta local, o None si falla."""
    name = slug(gid) + ".jpg"
    dest = OUT_DIR / name
    rel = URL_PREFIX + name
    if dry:
        print(f"  dry   {name}  <- {url[:70]}")
        return rel
    if dest.exists() and dest.stat().st_size > 0:
        stats["locals"] += 1
        return rel
    try:
        optimize(fetch(url), dest)
    except Exception as e:
        stats["errors"] += 1
        print(f"  FAIL  {name}: {e}", file=sys.stderr)
        return None
    stats["baixades"] += 1
    print(f"  ok    {name:58s} {dest.stat().st_size // 1024:5d} KB")
    return rel


def main():
    dry = "--dry-run" in sys.argv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = YAML.read_text(encoding="utf-8").splitlines(keepends=True)

    # Separa en blocs: preàmbul + un bloc per galeria (comença amb '- id:')
    preamble, blocks, current = [], [], None
    for line in lines:
        if re.match(r"^- id:", line):
            current = [line]
            blocks.append(current)
        elif current is None:
            preamble.append(line)
        else:
            current.append(line)

    for block in blocks:
        gid = re.match(r"^- id:\s*(\S+)", block[0]).group(1).strip("'\"")
        url = next((m.group(1) for l in block
                    if (m := re.match(r"^\s+url:\s*(\S.*?)\s*$", l))), None)
        url = url.strip("'\"") if url else None
        idx = next((i for i, l in enumerate(block) if re.match(r"^\s+cover:", l)), None)

        if idx is not None:
            cover = re.match(r"^\s+cover:\s*(\S.*?)\s*$", block[idx]).group(1).strip("'\"")
            indent = re.match(r"^(\s+)", block[idx]).group(1)
        else:
            cover, indent = None, "  "

        if cover and cover.startswith(URL_PREFIX):
            if dry:
                stats["locals"] += 1
                continue
            if (ROOT / "static" / cover.lstrip("/")).exists():
                stats["locals"] += 1
                continue
            # Falta el fitxer local: el tornem a baixar des de la font original
            cover = og_image(url)
            if not cover:
                stats["errors"] += 1
                print(f"  FAIL  {gid}: falta static{URL_PREFIX}{slug(gid)}.jpg i la font "
                      "externa no en dona cap (les de Google Photos no exposen og:image; "
                      "recupera-la amb 'git checkout -- static/images/galleries')",
                      file=sys.stderr)
                continue

        if not cover:
            if not url:
                continue
            print(f"  cercant og:image per {gid}")
            cover = og_image(url)
            if not cover:
                stats["errors"] += 1
                print(f"  FAIL  {gid}: sense coberta ni og:image", file=sys.stderr)
                continue

        rel = localize(gid, cover, dry)
        if not rel:
            continue
        newline = f"{indent}cover: {rel}\n"
        if idx is not None:
            block[idx] = newline
        else:
            block.append(newline)

    if not dry:
        YAML.write_text("".join(preamble + [l for b in blocks for l in b]), encoding="utf-8")

    total = sum(f.stat().st_size for f in OUT_DIR.glob("*") if f.is_file())
    print(f"\nBaixades: {stats['baixades']} · ja locals: {stats['locals']} · "
          f"errors: {stats['errors']}")
    print(f"Total a static/images/galleries/: {total / 1_048_576:.1f} MB")
    return 1 if stats["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
