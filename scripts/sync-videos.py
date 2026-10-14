#!/usr/bin/env python3
"""
sync-videos.py
Agrega els canals de YouTube definits a data/sources.yaml i genera
static/data/videos.json, etiquetant cada vídeo amb el canal d'origen.

Reutilitza yt-dlp (mateixa eina que el workflow original).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError as e:
    print(f"Falta dependència: {e}. Instal·la requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "data" / "sources.yaml"
OUT = ROOT / "static" / "data" / "videos.json"
PER_CHANNEL = 50


def fetch_channel(channel_id):
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    proc = subprocess.run(
        [
            "yt-dlp",
            "--flat-playlist",
            "--dump-single-json",
            "--no-warnings",
            "--playlist-end",
            str(PER_CHANNEL),
            url,
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip()[-300:] or "yt-dlp va fallar")
    return json.loads(proc.stdout)


def normalize(entry, channel_name):
    if not entry:
        return None
    video_id = entry.get("id") or entry.get("url", "").split("v=")[-1]
    if not video_id:
        return None
    title = entry.get("title", "")
    if re.search(r"#[Ss]horts?", title):
        return None
    url = entry.get("url") or entry.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}"
    if "/shorts/" in url:
        return None

    upload_date = entry.get("upload_date", "")
    if len(upload_date) == 8:
        published = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
    else:
        published = upload_date[:10] if upload_date else ""

    thumbnails = entry.get("thumbnails", [])
    thumb = thumbnails[-1].get("url") if thumbnails else f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

    return {
        "id": video_id,
        "title": title,
        "published": published,
        "thumb": thumb,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "embed": f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1",
        "channel": channel_name,
    }


def main():
    sources = yaml.safe_load(SOURCES.read_text(encoding="utf-8")) or {}
    channels = sources.get("videos") or []
    if not channels:
        print("Cap canal de vídeo a data/sources.yaml", file=sys.stderr)
        sys.exit(1)

    existing = {}
    if OUT.exists():
        try:
            for v in json.loads(OUT.read_text(encoding="utf-8")):
                existing[v["id"]] = v
        except Exception:
            pass

    merged = {}
    report = []
    for src in channels:
        name, channel_id = src.get("name", "?"), src.get("channel")
        if not channel_id:
            continue
        try:
            data = fetch_channel(channel_id)
        except Exception as e:
            print(f"AVÍS: canal «{name}» ha fallat: {e}", file=sys.stderr)
            continue
        count = 0
        for entry in data.get("entries", []):
            video = normalize(entry, name)
            if video:
                merged[video["id"]] = video
                count += 1
        report.append(f"  {name}: {count} vídeos")

    for vid_id, v in existing.items():
        merged.setdefault(vid_id, v)

    videos = sorted(merged.values(), key=lambda v: v.get("published", ""), reverse=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(videos, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Vídeos sincronitzats:")
    print("\n".join(report))
    print(f"Total: {len(videos)} vídeos de {len(channels)} canals")


if __name__ == "__main__":
    main()
