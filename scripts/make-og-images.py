#!/usr/bin/env python3
"""
Genera imatges de previsualització social (OpenGraph / Twitter / Telegram).

    python3 scripts/make-og-images.py            # genera i escriu data/og-images.json
    python3 scripts/make-og-images.py --dry-run  # només informe
    python3 scripts/make-og-images.py --check    # exit 1 si hi ha deriva (CI)

Per què existeix:
  · Telegram, WhatsApp, Facebook, X, LinkedIn i Slack rebutgen imatges de
    previsualització de més de 5 MB i les retallen a ~1.91:1 (1200×630).
  · Algunes imatges del web (portades de disc, fotos de projecte) pesen 7-11 MB
    o són quadrades, i el preview queda buit o retallat de manera lletja.

Què fa:
  1. Llegeix els camps d'imatge del front matter (og_image, cover, photo, image)
     de totes les llengües + la imatge per defecte de hugo.toml.
  2. Si la imatge ja és lleugera i amb una proporció raonable, la deixa tal qual.
  3. Si no, en crea una variant 1200×630 a static/images/og/:
       - proporció entre 1.5 i 2.3 → retall centrat (crop)
       - qualsevol altra proporció   → imatge sencera sobre fons desenfocat
  4. Escriu data/og-images.json, que layouts/partials/seo.html utilitza per
     publicar l'URL final i les mides exactes (og:image:width/height/type).

Els fitxers generats es poden esborrar i regenerar sempre que calgui; si
data/og-images.json no existeix, el web fa fallback a la imatge original.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageOps
except ImportError:  # pragma: no cover
    sys.exit("Cal Pillow: pip install Pillow")

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
CONTENT = ROOT / "content"
OUT_DIR = STATIC / "images" / "og"
DATA_FILE = ROOT / "data" / "og-images.json"

TARGET = (1200, 630)
MAX_BYTES = 400 * 1024      # per sobre, es regenera
MAX_SIDE = 1600             # per sobre, es regenera
# Marge de proporció acceptable per a una targeta social (1.91:1 ≈ 1200×630).
# Dins d'aquest marge es retalla; fora, es compon sobre fons desenfocat.
MIN_RATIO, MAX_RATIO = 1.5, 2.3

FM_KEYS = ("og_image", "cover", "photo", "image")


def site_default_image() -> str | None:
    """Llegeix params.og_image de hugo.toml."""
    cfg = (ROOT / "hugo.toml").read_text(encoding="utf-8")
    m = re.search(r'^\s*og_image\s*=\s*"([^"]+)"', cfg, re.M)
    return m.group(1) if m else None


def front_matter_images() -> dict[str, set[str]]:
    """Retorna {ruta_imatge: {fitxers que la referencien}}."""
    found: dict[str, set[str]] = {}
    for md in sorted(CONTENT.rglob("*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            continue
        for line in m.group(1).split("\n"):
            km = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
            if not km or km.group(1) not in FM_KEYS:
                continue
            raw = km.group(2).strip()
            if not raw.startswith(("'", '"')):
                continue
            val = raw.strip("'\"")
            if not val.startswith("/") and not val.startswith("images/"):
                continue  # URLs externes o relatives a la pàgina
            found.setdefault(val.lstrip("/"), set()).add(str(md.relative_to(ROOT)))
    return found


def slug(path: str) -> str:
    stem = re.sub(r"\.[^.]+$", "", path)
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")


def to_rgb(im: Image.Image) -> Image.Image:
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (17, 17, 17))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def compose(im: Image.Image) -> Image.Image:
    """Retalla o composa la imatge a 1200×630."""
    ratio = im.width / im.height
    if MIN_RATIO <= ratio <= MAX_RATIO:
        return ImageOps.fit(im, TARGET, method=Image.LANCZOS, centering=(0.5, 0.4))

    # Proporcions allunyades (portades quadrades, fotos molt amples):
    # fons desenfocat i la imatge sencera al damunt, sense retallar res.
    bg = ImageOps.fit(im, TARGET, method=Image.LANCZOS, centering=(0.5, 0.5))
    bg = bg.filter(ImageFilter.GaussianBlur(48))
    bg = bg.point(lambda p: int(p * 0.55))
    fg = ImageOps.contain(im, TARGET, method=Image.LANCZOS)
    out = bg.copy()
    out.paste(fg, ((TARGET[0] - fg.width) // 2, (TARGET[1] - fg.height) // 2))
    return out


def plan(images: dict[str, set[str]]) -> tuple[dict[str, dict], list[tuple[str, str, Image.Image]]]:
    """Decideix què cal generar. Retorna (entrades, [(clau, nom_fitxer, imatge)])."""
    entries: dict[str, dict] = {}
    todo: list[tuple[str, str, Image.Image]] = []
    for path in sorted(images):
        src = STATIC / path
        if not src.is_file():
            print(f"  ! no trobada: static/{path}", file=sys.stderr)
            continue
        try:
            im = to_rgb(Image.open(src))
        except Exception as exc:  # imatge corrupta
            print(f"  ! no llegible: static/{path} ({exc})", file=sys.stderr)
            continue

        size = src.stat().st_size
        ratio = im.width / im.height
        needs = (size > MAX_BYTES or max(im.size) > MAX_SIDE
                 or not (MIN_RATIO <= ratio <= MAX_RATIO))

        if not needs:
            entries[path] = {
                "url": path,
                "w": im.width,
                "h": im.height,
                "type": ("image/jpeg" if path.lower().endswith((".jpg", ".jpeg"))
                         else f"image/{path.rsplit('.', 1)[-1].lower()}"),
                "generated": False,
            }
        else:
            out_name = slug(path) + ".jpg"
            entries[path] = {
                "url": f"images/og/{out_name}",
                "w": TARGET[0],
                "h": TARGET[1],
                "type": "image/jpeg",
                "generated": True,
                "source": path,
                "sourceBytes": size,
            }
            todo.append((path, out_name, im))
    return entries, todo


def check(entries: dict[str, dict]) -> int:
    """Compara el pla amb data/og-images.json. Retorna codi de sortida."""
    if not DATA_FILE.is_file():
        print("data/og-images.json no existeix: executa scripts/make-og-images.py")
        return 1

    current: dict[str, dict] = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    problems: list[str] = []

    for path, entry in entries.items():
        old = current.get(path)
        if old is None:
            problems.append(f"imatge nova sense variant: {path}")
        elif old.get("url") != entry["url"]:
            problems.append(f"URL desactualitzada: {path} ({old.get('url')} → {entry['url']})")
        elif entry["generated"] and not (STATIC / entry["url"]).is_file():
            problems.append(f"falta el fitxer generat: static/{entry['url']}")

    for path in current:
        if path not in entries:
            problems.append(f"entrada òrfena a data/og-images.json: {path}")

    if problems:
        print("Miniatures socials desactualitzades:")
        for p in problems:
            print(f"  · {p}")
        print("\nArregla-ho amb: python3 scripts/make-og-images.py")
        return 1

    print(f"Miniatures socials al dia ({len(entries)} imatges).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="no escriu res")
    ap.add_argument("--check", action="store_true",
                    help="no escriu res; exit 1 si data/og-images.json o les variants no estan al dia")
    args = ap.parse_args()

    images = front_matter_images()
    default = site_default_image()
    if default:
        images.setdefault(default.lstrip("/"), set()).add("hugo.toml (params.og_image)")

    if not images:
        print("Cap imatge al front matter; no es fa res.")
        return 1

    entries, todo = plan(images)

    if args.check:
        return check(entries)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = 0
    for key, out_name, im in todo:
        out_file = OUT_DIR / out_name
        out = compose(im)
        if not args.dry_run:
            out.save(out_file, "JPEG", quality=82, optimize=True, progressive=True)
            entries[key]["outBytes"] = out_file.stat().st_size
        generated += 1
        print(f"  + {out_name}")

    if not args.dry_run:
        DATA_FILE.write_text(
            json.dumps(dict(sorted(entries.items())), ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )

    kept = len(entries) - generated
    print(f"\n{len(entries)} imatges: {generated} variants 1200×630, {kept} ja òptimes")
    print(f"data/og-images.json {'(dry-run, no escrit)' if args.dry_run else 'escrit'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
