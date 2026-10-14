#!/usr/bin/env python3
"""
sync-agenda.py
Agrega els calendaris iCal definits a data/sources.yaml i genera:
  - static/data/concerts.txt          (un sol VCALENDAR vàlid, per al JS client)
  - data/concerts-schema.json         (JSON-LD MusicEvent, per a Hugo)

Cada esdeveniment porta el nom del projecte (font) com a artista/origen.
"""
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
    import requests
except ImportError as e:
    print(f"Falta dependència: {e}. Instal·la requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "data" / "sources.yaml"
ICAL_OUT = ROOT / "static" / "data" / "concerts.txt"
SCHEMA_OUT = ROOT / "data" / "concerts-schema.json"
BASE_URL = "https://ivankovacevic.com"


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def unescape_ical(text):
    text = text.replace("\\n", "\n").replace("\\,", ",")
    text = text.replace("\\;", ";").replace("\\\\", "\\")
    return text.strip()


def unfold_ical(lines):
    result = []
    for line in lines:
        if line.startswith((" ", "\t")) and result:
            result[-1] = result[-1].rstrip("\r\n") + line.lstrip()
        else:
            result.append(line)
    return result


def parse_ical(content):
    lines = unfold_ical(content.splitlines(keepends=True))
    events, current, in_event = [], {}, False
    for line in lines:
        line = line.rstrip("\r\n")
        if line == "BEGIN:VEVENT":
            in_event, current = True, {}
        elif line == "END:VEVENT":
            in_event = False
            if current:
                events.append(current)
        elif in_event and ":" in line:
            key, _, value = line.partition(":")
            key = key.split(";")[0].strip()
            current[key] = unescape_ical(value)
    return events


def parse_ical_date(dtstr):
    dtstr = dtstr.strip()
    try:
        if "T" in dtstr:
            if dtstr.endswith("Z"):
                dt = datetime.strptime(dtstr, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
            else:
                dt = datetime.strptime(dtstr, "%Y%m%dT%H%M%S")
        else:
            dt = datetime.strptime(dtstr, "%Y%m%d")
        return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    except ValueError:
        return dtstr


def to_schema(event, performer, base_url=BASE_URL):
    summary = event.get("SUMMARY", "")
    location = event.get("LOCATION", "")
    dtstart = event.get("DTSTART", "")
    dtend = event.get("DTEND", "")
    desc = event.get("DESCRIPTION", "")
    url = event.get("URL", base_url)

    schema = {
        "@type": "MusicEvent",
        "name": summary,
        "startDate": parse_ical_date(dtstart),
        "performer": {"@type": "MusicGroup", "name": performer},
    }
    if dtend:
        schema["endDate"] = parse_ical_date(dtend)

    if location:
        parts = [p.strip() for p in location.split(",")]
        schema["location"] = {
            "@type": "Place",
            "name": parts[0],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": parts[1] if len(parts) > 1 else "",
                "addressLocality": parts[-1] if len(parts) > 1 else parts[0],
                "addressCountry": "ES",
            },
        }
    else:
        schema["location"] = {
            "@type": "Place",
            "name": "Barcelona",
            "address": {"@type": "PostalAddress", "addressLocality": "Barcelona", "addressCountry": "ES"},
        }

    if desc:
        schema["description"] = desc[:200]
    if url and url != base_url:
        schema["url"] = url
    schema["eventStatus"] = "https://schema.org/EventScheduled"
    schema["organizer"] = {"@type": "MusicGroup", "name": performer}
    return schema


def fetch(url):
    resp = requests.get(url, timeout=30, headers={"User-Agent": "ivankovacevic.com/1.0"})
    resp.raise_for_status()
    return resp.text


def escape_ical(text):
    return text.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def main():
    sources = yaml.safe_load(SOURCES.read_text(encoding="utf-8")) or {}
    gigs = sources.get("gigs") or []
    if not gigs:
        print("Cap font de gigs a data/sources.yaml", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(timezone.utc)
    vervevents = []
    schema_events = []
    report = []

    for src in gigs:
        name, ical_url = src.get("name", "?"), src.get("ical")
        if not ical_url:
            continue
        try:
            content = fetch(ical_url)
        except Exception as e:
            print(f"AVÍS: no s'ha pogut descarregar «{name}»: {e}", file=sys.stderr)
            continue

        events = parse_ical(content)
        kept = 0
        for ev in events:
            dtstart = ev.get("DTSTART", "")
            if not dtstart:
                continue
            try:
                iso = parse_ical_date(dtstart)
                dt = datetime.fromisoformat(iso)
                if dt.timestamp() <= now.timestamp() - 86400:
                    continue
            except Exception:
                pass
            ev["X-PERFORMER"] = name
            vervevents.append(ev)
            schema_events.append(to_schema(ev, name))
            kept += 1
        report.append(f"  {name}: {kept} esdeveniments propers")

    schema_events.sort(key=lambda x: x.get("startDate", ""))
    SCHEMA_OUT.write_text(
        json.dumps({"generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "events": schema_events}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ivankovacevic.com//agenda//CA",
        "CALSCALE:GREGORIAN",
        "X-WR-CALNAME:Ivan Kovačević",
    ]
    for ev in vervevents:
        lines.append("BEGIN:VEVENT")
        for key in ("SUMMARY", "DTSTART", "DTEND", "LOCATION", "DESCRIPTION", "URL", "X-PERFORMER"):
            if ev.get(key):
                lines.append(f"{key}:{escape_ical(ev[key])}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    ICAL_OUT.parent.mkdir(parents=True, exist_ok=True)
    ICAL_OUT.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")

    print("Agenda sincronitzada:")
    print("\n".join(report))
    print(f"Total: {len(schema_events)} esdeveniments propers de {len(gigs)} fonts")


if __name__ == "__main__":
    main()
