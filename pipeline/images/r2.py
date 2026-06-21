"""
R2-Upload (P9, SPEC E43/E44). S3-kompatibel via boto3.

Pro Bild zwei Objekte:
  <prefix>/<artnr>-<N>.jpg              verarbeitetes Shop-Bild
  originals/<prefix>/<artnr>-<N>.<ext>  Original (Magic-Byte-Extension)
Public-URL = R2_PUBLIC_BASE/<prefix>/<artnr>-<N>.jpg.
Idempotent: gleicher Key wird überschrieben (kein Duplikat). 3 Retries.

Credentials: config.r2_credentials() (env oder pipeline/.secrets/...), nie geloggt.
"""
from __future__ import annotations

import json
import re
import time

import boto3
from botocore.config import Config as BotoConfig

from .. import config
from .process import ProcessedImage

_CONTENT_TYPE = {"jpg": "image/jpeg", "png": "image/png", "webp": "image/webp",
                 "gif": "image/gif", "heic": "image/heic", "bin": "application/octet-stream"}
_CACHE = "public, max-age=2592000"


def _client():
    creds = config.r2_credentials()
    return boto3.client("s3", config=BotoConfig(retries={"max_attempts": 3, "mode": "standard"}),
                        **creds)


def _put(client, key: str, body: bytes, content_type: str):
    for attempt in range(3):
        try:
            client.put_object(Bucket=config.R2_BUCKET, Key=key, Body=body,
                              ContentType=content_type, CacheControl=_CACHE)
            return
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def upload_vater(client, prefix: str, artnr: str, images: list[ProcessedImage]) -> list[str]:
    """Lädt verarbeitete + Original-Bilder hoch. Gibt Public-URLs (verarbeitet) zurück."""
    urls = []
    for pi in images:
        fname = f"{artnr}-{pi.index}"
        _put(client, f"{prefix}/{fname}.jpg", pi.jpg_bytes, "image/jpeg")
        _put(client, f"originals/{prefix}/{fname}.{pi.orig_ext}", pi.orig_bytes,
             _CONTENT_TYPE.get(pi.orig_ext, "application/octet-stream"))
        urls.append(f"{config.R2_PUBLIC_BASE}/{prefix}/{fname}.jpg")
    return urls


def make_client():
    return _client()


# --- A-Nummern-Index pro Kollektion (für Galerie-Artikelnummern-Spanne) -----
# originals/<prefix>/_artikel_index.json = {semantischer_artnr: A-Nummer}.
# Beim Upload gemerged, damit die Galerie zeigen kann, welche WaWi-Artikelnummern
# eine Kollektion umfasst (Wunsch für Sarahs Bilder-Galerie).
_ARTIKEL_INDEX = "_artikel_index.json"


def _read_artikel_index(client, prefix: str) -> dict:
    try:
        obj = client.get_object(Bucket=config.R2_BUCKET, Key=f"originals/{prefix}/{_ARTIKEL_INDEX}")
        return json.loads(obj["Body"].read().decode("utf-8"))
    except Exception:
        return {}


def update_artikel_index(client, prefix: str, mapping: dict) -> dict:
    """{semantischer_artnr: A-Nummer} mergen + nach R2 schreiben. Aufruf beim Upload."""
    idx = _read_artikel_index(client, prefix)
    idx.update({k: v for k, v in mapping.items() if k and v})
    _put(client, f"originals/{prefix}/{_ARTIKEL_INDEX}",
         json.dumps(idx, ensure_ascii=False).encode("utf-8"), "application/json")
    return idx


def _artikel_span(client, prefix: str):
    """(min_A, max_A) als String aus dem Index, oder None."""
    idx = _read_artikel_index(client, prefix)
    nums = [(int(m.group(1)), a) for a in idx.values()
            if a and (m := re.search(r"(\d+)", a))]
    return (min(nums)[1], max(nums)[1]) if nums else None


def _discover_prefixes(client) -> list:
    """Alle originals/<prefix>/-Kollektionsordner via Delimiter entdecken."""
    prefixes, token = [], None
    while True:
        kw = {"Bucket": config.R2_BUCKET, "Prefix": "originals/", "Delimiter": "/"}
        if token:
            kw["ContinuationToken"] = token
        resp = client.list_objects_v2(**kw)
        for cp in resp.get("CommonPrefixes", []):
            seg = cp["Prefix"][len("originals/"):].strip("/")
            if seg:
                prefixes.append(seg)
        if not resp.get("IsTruncated"):
            break
        token = resp.get("NextContinuationToken")
    return prefixes


def _collection_descriptor(client, prefix: str):
    """(rang, marker 'YYYY-MM', span) der Kollektion — wie auf der Master-Karte.
    rang = chronologischer Rang über ALLE Kollektionen (ältester = #1)."""
    dated = []
    for p in _discover_prefixes(client):
        dts = [_latest(v) for v in _list_originals(client, p).values() if _latest(v)]
        dated.append((p, max(dts) if dts else None))
    dated.sort(key=lambda e: e[1].timestamp() if e[1] else 0)
    rank = next((i + 1 for i, (p, _) in enumerate(dated) if p == prefix), None)
    latest = next((d for p, d in dated if p == prefix), None)
    marker = latest.strftime("%Y-%m") if latest else ""
    return rank, marker, _artikel_span(client, prefix)


# --- Originale-Galerie (B34): öffentliche index.html für Social-Media -----
def _list_originals(client, prefix: str) -> dict[str, list[tuple]]:
    """{artnr: [(idx, public_url, last_modified), ...]} aus originals/<prefix>/.
    last_modified (R2-Upload-Zeit) trägt die Chronologie für die Galerie-Sortierung."""
    import re
    from collections import defaultdict
    out = defaultdict(list)
    token = None
    base = f"originals/{prefix}/"
    while True:
        kw = {"Bucket": config.R2_BUCKET, "Prefix": base}
        if token:
            kw["ContinuationToken"] = token
        resp = client.list_objects_v2(**kw)
        for obj in resp.get("Contents", []):
            key = obj["Key"]
            fname = key[len(base):]
            # Aktuelles Schema: <artnr>-<N>.<ext>, artnr enthält NIE '_'. Alte
            # Cowork-Trial-Originale (..._NN_HOTCAKES_YYYY-MM-...) ausfiltern.
            if not fname or fname.endswith(".html") or "_" in fname or "/" in fname:
                continue
            m = re.match(r"^(.*)-(\d+)\.[^.]+$", fname)  # <artnr>-<N>.<ext>
            artnr = m.group(1) if m else fname
            idx = int(m.group(2)) if m else 0
            out[artnr].append((idx, f"{config.R2_PUBLIC_BASE}/{key}", obj.get("LastModified")))
        if not resp.get("IsTruncated"):
            break
        token = resp.get("NextContinuationToken")
    return {a: sorted(v) for a, v in out.items()}


def _urls(items: list) -> list[str]:
    return [u for _, u, _ in items]


def _latest(items: list):
    """Jüngste R2-Upload-Zeit einer Bildgruppe (für Chronologie); None wenn unbekannt."""
    ds = [d for _, _, d in items if d]
    return max(ds) if ds else None


def _safe(s: str) -> str:
    """Dateinamen-tauglich machen (verbotene Zeichen raus, Whitespace normalisieren)."""
    return re.sub(r"\s+", " ", re.sub(r'[\\/:*?"<>|]+', "", s)).strip()


def build_originals_index(client, prefix: str, name_map: dict | None = None,
                          titel: str = "Originalbilder") -> str:
    """Galerie-HTML aller Originale generieren + nach originals/<prefix>/index.html
    hochladen. Gibt die Public-URL der Galerie zurück."""
    groups = _list_originals(client, prefix)
    name_map = name_map or {}
    aidx = _read_artikel_index(client, prefix)

    def _anum(artnr):
        m = re.search(r"(\d+)", aidx.get(artnr, "") or "")
        return int(m.group(1)) if m else 10 ** 12  # ohne A-Nummer ans Ende

    # Aufsteigend nach Artikelnummer (übersichtlich); #1 = niedrigste ArtNr.
    ordered = sorted(groups.items(), key=lambda kv: _anum(kv[0]))
    cards = []
    for i, (artnr, items) in enumerate(ordered):
        num = i + 1
        head = name_map.get(artnr, artnr)
        a = aidx.get(artnr, "")
        # A-Nummer VOR dem Artikelnamen, mit Bindestrich (Wunsch: Sarah sieht sofort die ArtNr).
        title = f'<span class="artnr">{a}</span> - {head}' if a else head
        # Lesbarer Dateiname: A-Nummer + Hersteller/Modell, z.B. „A1009303 Pole Addict Top Goddess Schwarz".
        filebase = _safe(f"{a} {head}")
        dt = _latest(items)
        marker = dt.strftime("%Y-%m") if dt else ""
        thumbs = "".join(
            f'<a class="dl" href="{u}" target="_blank" download="{filebase}-{j+1}.{u.rsplit(".", 1)[-1].split("?")[0]}">'
            f'<img loading="lazy" src="{u}" alt="{filebase}-{j+1}"></a>'
            for j, u in enumerate(_urls(items)))
        cards.append(
            f'<section><h2>{title} <span class="badge">{marker} · #{num}</span>'
            f'<button class="dlall" data-name="{filebase}" onclick="zipDownload(this)">⬇ Alle herunterladen</button>'
            f'</h2><div class="g">{thumbs}</div></section>')

    # Kollektions-ZIP-Name wie die Galerie-Kachel: Marke + Datums-Marker (#Rang) + ArtNr-Spanne.
    marke = titel.replace(" Originalbilder", "").strip()
    _rank, _marker, _span = _collection_descriptor(client, prefix)
    _parts = [marke]
    if _marker:
        _parts.append(_marker)
    if _rank:
        _parts.append(f"#{_rank}")
    if _span:
        _parts.append(_span[0] if _span[0] == _span[1] else f"{_span[0]}-{_span[1]}")
    collname = _safe(" ".join(_parts))

    html = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{titel}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
<style>body{{font-family:system-ui,sans-serif;margin:0;background:#faf7f5;color:#222}}
header{{padding:24px;background:#fff;border-bottom:1px solid #eee}}h1{{margin:0;font-size:20px}}
.crumbs{{font-size:13px;margin-bottom:10px}}.crumbs a{{color:#a0508c;text-decoration:none}}.crumbs a:hover{{text-decoration:underline}}
.sub{{color:#888;font-size:13px;margin-top:4px}}section{{padding:16px 24px}}
h2{{font-size:15px;color:#444;margin:8px 0;display:flex;align-items:center;flex-wrap:wrap;gap:8px}}
.badge{{color:#a0508c;font-size:12px;font-weight:600}}.artnr{{color:#555;font-size:12px;font-weight:600;margin-left:4px}}
.dlall{{margin-left:auto;background:#a0508c;color:#fff;border:0;border-radius:6px;padding:6px 12px;font-size:13px;cursor:pointer}}.dlall:disabled{{opacity:.6;cursor:default}}
.collbtn{{margin-top:12px;background:#7a2f66;color:#fff;border:0;border-radius:6px;padding:9px 16px;font-size:14px;font-weight:600;cursor:pointer}}.collbtn:disabled{{opacity:.6;cursor:default}}
.g{{display:flex;flex-wrap:wrap;gap:10px}}
.g img{{height:220px;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.12);object-fit:cover}}
.g a{{display:inline-block}}</style></head><body>
<header><div class="crumbs"><a href="../index.html">&larr; Alle Kollektionen</a></div><h1>{titel}</h1>
<div class="sub">Klick auf ein Bild = Original in voller Auflösung. „Alle herunterladen" = ein Artikel als ZIP. {sum(len(u) for u in groups.values())} Bilder, {len(groups)} Artikel.</div>
<button class="collbtn" data-name="{collname}" onclick="zipAll(this)">⬇ Ganze Kollektion als ZIP</button></header>
{''.join(cards)}
<script>
async function zipDownload(btn){{
  const sec=btn.closest('section'), links=[...sec.querySelectorAll('a.dl')], name=btn.dataset.name||'bilder';
  const orig=btn.textContent; btn.disabled=true; btn.textContent='Lädt…';
  try{{
    const zip=new JSZip();
    for(let i=0;i<links.length;i++){{
      const u=links[i].href, r=await fetch(u), b=await r.blob();
      const ext=(u.split('.').pop()||'jpg').split('?')[0];
      zip.file(name+'-'+(i+1)+'.'+ext, b);
    }}
    saveAs(await zip.generateAsync({{type:'blob'}}), name+'.zip');
  }}catch(e){{alert('Download fehlgeschlagen: '+e);}}
  btn.disabled=false; btn.textContent=orig;
}}
async function zipAll(btn){{
  const secs=[...document.querySelectorAll('section')], orig=btn.textContent;
  btn.disabled=true; btn.textContent='Lädt…';
  try{{
    const zip=new JSZip();
    for(const sec of secs){{
      const b=sec.querySelector('.dlall'), folder=(b&&b.dataset.name)||'artikel';
      const links=[...sec.querySelectorAll('a.dl')];
      for(let i=0;i<links.length;i++){{
        const u=links[i].href, r=await fetch(u), bl=await r.blob();
        const ext=(u.split('.').pop()||'jpg').split('?')[0];
        zip.folder(folder).file(folder+'-'+(i+1)+'.'+ext, bl);
      }}
    }}
    saveAs(await zip.generateAsync({{type:'blob'}}), (btn.dataset.name||'kollektion')+'.zip');
  }}catch(e){{alert('Download fehlgeschlagen: '+e);}}
  btn.disabled=false; btn.textContent=orig;
}}
</script>
</body></html>"""
    _put(client, f"originals/{prefix}/index.html", html.encode("utf-8"), "text/html; charset=utf-8")
    return f"{config.R2_PUBLIC_BASE}/originals/{prefix}/index.html"


def build_master_index(client, titel: str = "Originalbilder — alle Kollektionen") -> str:
    """EINE permanente Landing-Page über ALLE Lieferanten/Kollektionen.
    Auto-entdeckt jeden originals/<prefix>/-Ordner; verlinkt auf dessen Galerie.
    Upload nach originals/index.html. Gibt die permanente Public-URL zurück."""
    prefixes = _discover_prefixes(client)

    # Anzeigenamen aus lieferanten_mapping (r2_prefix -> anzeigename)
    namen = {}
    for s in config.load_mapping().get("lieferanten", {}).values():
        if s.get("r2_prefix"):
            # Marke/Hersteller statt Lieferanten-Langname (sauberer für die Galerie).
            namen[s["r2_prefix"]] = (s.get("hersteller") or s.get("marke_kurz")
                                     or s.get("anzeigename") or s["r2_prefix"])

    entries = []
    for p in prefixes:
        imgs = _list_originals(client, p)
        dts = [_latest(v) for v in imgs.values() if _latest(v)]
        latest = max(dts) if dts else None
        first = next(iter(imgs.values()), None)
        preview = _urls(first)[0] if first else None
        span = _artikel_span(client, p)
        entries.append((p, len(imgs), sum(len(v) for v in imgs.values()), latest, preview, span))
    # Chronologischer Rang: älteste Kollektion = #1 (stabil); Anzeige neueste zuerst.
    entries.sort(key=lambda e: e[3].timestamp() if e[3] else 0)
    cards = []
    for i in range(len(entries) - 1, -1, -1):
        p, n_art, n_img, latest, preview, span = entries[i]
        num = i + 1
        marker = latest.strftime("%Y-%m") if latest else ""
        # Einzelartikel -> nur eine Nummer, sonst von–bis.
        spantxt = ""
        if span:
            s = span[0] if span[0] == span[1] else f"{span[0]} – {span[1]}"
            spantxt = f'<span class="artnr">{s}</span>'
        name = namen.get(p, p.title())
        prev_html = f'<img loading="lazy" src="{preview}" alt="{name}">' if preview else ""
        cards.append(
            f'<a class="card" href="{p}/index.html">{prev_html}'
            f'<div class="meta"><span class="badge">{marker} · #{num}</span>'
            f'<strong>{name}</strong>{spantxt}'
            f'<span>{n_art} Artikel · {n_img} Bilder</span></div></a>')

    html = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{titel}</title>
<style>body{{font-family:system-ui,sans-serif;margin:0;background:#faf7f5;color:#222}}
header{{padding:24px;background:#fff;border-bottom:1px solid #eee}}h1{{margin:0;font-size:20px}}
.sub{{color:#888;font-size:13px;margin-top:4px}}.grid{{display:flex;flex-wrap:wrap;gap:16px;padding:24px}}
.card{{width:240px;background:#fff;border-radius:12px;overflow:hidden;text-decoration:none;color:inherit;box-shadow:0 1px 6px rgba(0,0,0,.1)}}
.card img{{width:100%;height:300px;object-fit:cover;display:block}}
.meta{{padding:12px}}.meta strong{{display:block;font-size:15px}}.meta span{{color:#888;font-size:12px}}
.meta .badge{{display:block;color:#a0508c;font-size:11px;font-weight:700;letter-spacing:.04em;margin-bottom:2px}}
.meta .artnr{{display:block;color:#555;font-size:12px;font-weight:600;margin:2px 0}}</style></head><body>
<header><h1>{titel}</h1><div class="sub">Klick auf eine Kollektion = alle Originalbilder in voller Auflösung zum Download. Neueste zuerst, ältere weiter unten. Neue Kollektionen erscheinen automatisch.</div></header>
<div class="grid">{''.join(cards)}</div>
</body></html>"""
    _put(client, "originals/index.html", html.encode("utf-8"), "text/html; charset=utf-8")
    return f"{config.R2_PUBLIC_BASE}/originals/index.html"
