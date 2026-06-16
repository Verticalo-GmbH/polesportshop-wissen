"""
Lunalae (Shopify, offen) — Väter-Builder für die Diamante May Release (2026-06-15).

Scope = NUR die im Lookbook enthaltenen Diamante-Artikel (Rechnung #3124 bestätigt;
Rest der Rechnung = Restock, out of scope). 10 Väter (5 Stile × Farben).
AU-Größen 6/8/10/12/14 -> XS/S/M/L/XL (AU16 nicht übernommen). Shopify-Fetch live.
"""
from __future__ import annotations

import json
import re
import urllib.request

from ..model import Vater, Kind

_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
_BASE = "https://www.lunalae.com/products/"
AU_MAP = {"6": "XS", "8": "S", "10": "M", "12": "L", "14": "XL"}  # AU16 raus

# handle, modell_basis, garment_type, farbe_raw
PRODUCTS = [
    ("imogen-diamante-bodysuit-black", "Imogen Diamante", "Bodysuit", "black"),
    ("imogen-diamante-bodysuit-taupe", "Imogen Diamante", "Bodysuit", "taupe"),
    ("demi-mesh-diamante-halter-black", "Demi Diamante", "Top", "black"),
    ("demi-mesh-diamante-halter-lilac", "Demi Diamante", "Top", "lilac"),
    ("sarah-mesh-diamante-high-waist-shorts-black", "Sarah Diamante", "Bottom", "black"),
    ("sarah-mesh-diamante-high-waist-shorts-lilac", "Sarah Diamante", "Bottom", "lilac"),
    ("roxie-diamante-top-black", "Roxie Diamante", "Top", "black"),
    ("roxie-diamante-top-taupe", "Roxie Diamante", "Top", "taupe"),
    ("roxie-mesh-diamante-high-waist-bottoms-black", "Roxie Diamante", "Bottom", "black"),
    ("roxie-mesh-diamante-high-waist-bottoms-taupe", "Roxie Diamante", "Bottom", "taupe"),
]


def _fetch(handle: str) -> dict:
    req = urllib.request.Request(_BASE + handle + ".json", headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["product"]


def build_vaeter() -> list[Vater]:
    vaeter = []
    for handle, modell, typ, farbe in PRODUCTS:
        p = _fetch(handle)
        # Größen: AU-Nummer aus Size-Option (option2), AU->Buchstabe, AU16 raus
        seen, kinder = set(), []
        for v in p["variants"]:
            sval = v.get("option2") or v.get("option1") or ""
            m = re.search(r"AU\s*(\d+)", sval)
            if not m:
                continue
            letter = AU_MAP.get(m.group(1))
            if letter and letter not in seen:
                seen.add(letter)
                kinder.append(Kind(groesse=letter, groesse_raw=sval, position=len(kinder)))
        images = [img["src"] for img in p.get("images", []) if img.get("src")]
        vaeter.append(Vater(
            handle=handle, product_id=p.get("id", 0), title_raw=p["title"],
            vendor="Lunalae", modell_basis=modell, garment_type=typ, farbe_raw=farbe,
            body_html=p.get("body_html", ""), image_urls=images, kinder=kinder,
        ))
    return vaeter
