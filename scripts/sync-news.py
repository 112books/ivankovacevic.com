#!/usr/bin/env python3
"""
sync-news.py
Agrega les mencions d'Ivan Kovačević a partir dels feeds RSS/Atom
definits a data/sources.yaml (Google Alerts, blogs de projectes, premsa...).

Genera static/data/news.json amb els elements més recents, deduplicats per URL.
"""
import json
import sys
import re
import html
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import yaml
    import requests
except ImportError as e:
    print(f"Falta dependència: {e}. Instal·la requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "data" / "sources.yaml"
OUT = ROOT / "static" / "data" / "news.json"
MAX_ITEMS = 100

ATOM = "{http://www.w3.org/2005/Atom}"
DC = "{http://purl.org/dc/elements/1.1/}"


def text(el):
    return html.unescape("".join(el.itertext()).strip()) if el is not None else ""


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def parse_feed(content, source_name):
    items = []
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return items

    nodes = root.iter("item")
    is_atom = root.tag == f"{ATOM}feed"
    if is_atom:
        nodes = root.iter(f"{ATOM}entry")

    for node in nodes:
        if node.tag in ("item", f"{ATOM}entry"):
            title = text(node.find("title")) if not is_atom else text(node.find(f"{ATOM}title"))
            if is_atom:
                link_el = node.find(f"{ATOM}link")
                link = link_el.get("href") if link_el is not None else ""
                date = text(node.find(f"{ATOM}updated")) or text(node.find(f"{ATOM}published"))
            else:
                link = text(node.find("link")) or text(node.find("guid"))
                date = text(node.find("pubDate")) or text(node.find(DC + "date"))
            summary = strip_tags(text(node.find("description"))) or strip_tags(
                text(node.find(f"{ATOM}summary"))
            )
            if not link:
                continue
            items.append(
                {
                    "title": title,
                    "link": link,
                    "source": source_name,
                    "published": date,
                    "summary": summary[:280],
                }
            )
    return items


def main():
    sources = yaml.safe_load(SOURCES.read_text(encoding="utf-8")) or {}
    feeds = sources.get("news") or []
    if not feeds:
        print("Cap font de notícies a data/sources.yaml — res a fer.")
        return

    seen, items = set(), []
    for src in feeds:
        name, rss = src.get("name", "?"), src.get("rss")
        if not rss:
            continue
        try:
            resp = requests.get(rss, timeout=30, headers={"User-Agent": "ivankovacevic.com/1.0"})
            resp.raise_for_status()
        except Exception as e:
            print(f"AVÍS: feed «{name}» ha fallat: {e}", file=sys.stderr)
            continue
        for item in parse_feed(resp.text, name):
            if item["link"] in seen:
                continue
            seen.add(item["link"])
            items.append(item)

    items = items[:MAX_ITEMS]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "items": items},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Notícies sincronitzades: {len(items)} mencions de {len(feeds)} fonts")


if __name__ == "__main__":
    main()
