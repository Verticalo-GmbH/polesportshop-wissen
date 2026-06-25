"""
RAD Polewear — Erstanlage (Bestellung #UM8DLUT8M, 2026-06-25). Shopify-Fetch.

9 Väter, alle Schwarz. Größen = exakt die bestellten Größen je Modell (Tjorben:
Shop-Logik, nie XXL). „Lara skirt" wird als Shorts geführt (kein eigener Produkttyp —
WaWi-Merkmalsverwaltung ist statisch, Tjorben-Entscheidung 2026-06-25).
Modellnamen ohne redundantes Typ-Wort (z.B. „Twinkle Tulle" statt „Twinkle tulle shorts").
"""
from __future__ import annotations

import json
import urllib.request

from .. import constants as C
from ..model import Vater, Kind

_UA = {"User-Agent": "Mozilla/5.0"}

# (handle, modell_basis, garment_type, farbe_raw, [bestellte_groessen])
PRODUCTS = [
    ("mercy-top-black",             "Mercy",          "Top",    "black", ["S", "M"]),
    ("mercy-bottom-black",          "Mercy",          "Bottom", "black", ["S", "M", "L"]),
    ("hecate-twinkle-top-black",    "Hecate Twinkle", "Top",    "black", ["XS", "S", "M", "L"]),
    ("hecate-twinkle-bottom-black", "Hecate Twinkle", "Bottom", "black", ["S", "M", "L"]),
    ("chandra-twinkle-top-black",   "Chandra Twinkle", "Top",   "black", ["XS", "S", "M", "L"]),
    ("chandra-twinkle-bottom-black", "Chandra Twinkle", "Bottom", "black", ["XS", "S", "M", "L", "XL"]),
    ("twinkle-tulle-shots-black",   "Twinkle Tulle",  "Bottom", "black", ["XS", "S", "M", "L", "XL"]),
    ("lara-shirt-black",            "Lara",           "Bottom", "black", ["S", "M"]),
    ("rad-strings-short-black",     "Rad Strings",    "Bottom", "black", ["XS", "S", "M", "L", "XL"]),
]


def _fetch(handle: str) -> dict:
    req = urllib.request.Request(f"https://radpolewear.com/products/{handle}.json", headers=_UA)
    return json.loads(urllib.request.urlopen(req, timeout=30).read())["product"]


def _rank(g: str) -> int:
    return C.GROESSEN_RANG.index(g) if g in C.GROESSEN_RANG else 99


def build_vaeter() -> list[Vater]:
    vaeter = []
    for handle, modell, typ, farbe, groessen in PRODUCTS:
        p = _fetch(handle)
        images = [i["src"] for i in p.get("images", []) if i.get("src")]
        kinder = [Kind(groesse=g, groesse_raw=g, position=i)
                  for i, g in enumerate(sorted(groessen, key=_rank))]
        vaeter.append(Vater(
            handle=handle, product_id=p.get("id", 0), title_raw=p.get("title", ""),
            vendor="RAD Polewear", modell_basis=modell, garment_type=typ, farbe_raw=farbe,
            body_html=p.get("body_html", ""), image_urls=images, kinder=kinder,
        ))
    return vaeter
