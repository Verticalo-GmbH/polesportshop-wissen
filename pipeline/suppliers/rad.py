"""
RAD Polewear — Erstanlage (Bestellung #UM8DLUT8M, 2026-06-25). Shopify-Fetch.

9 Väter, alle Schwarz. Varianten = ALLE im Shop verfügbaren Standardgrößen je Modell
(Tjorben 2026-06-25: immer den vollen Shop-Stand anlegen, damit fehlende Größen später
nachbestellbar sind), aber NIE XXL (Shop-Logik). Die Bestellmengen (BE) betreffen nur
die tatsächlich bestellten Größen (menge_rad.csv) — unabhängig von den angelegten Varianten.
„Lara skirt" wird als Shorts geführt (kein eigener Produkttyp — WaWi-Merkmalsverwaltung
ist statisch, Tjorben-Entscheidung). Modellnamen ohne redundantes Typ-Wort.
"""
from __future__ import annotations

import json
import urllib.request

from .. import constants as C
from ..model import Vater, Kind

_UA = {"User-Agent": "Mozilla/5.0"}
# Anzulegende Standardgrößen in Reihenfolge; nur die, die der Shop führt, werden übernommen.
# XXL bewusst NICHT dabei (Shop-Logik: wir führen nie XXL).
ALLOWED_GROESSEN = ["XS", "S", "M", "L", "XL"]

# (handle, modell_basis, garment_type, farbe_raw) — Größen kommen aus dem Shop (s.u.)
PRODUCTS = [
    ("mercy-top-black",             "Mercy",          "Top",    "black"),
    ("mercy-bottom-black",          "Mercy",          "Bottom", "black"),
    ("hecate-twinkle-top-black",    "Hecate Twinkle", "Top",    "black"),
    ("hecate-twinkle-bottom-black", "Hecate Twinkle", "Bottom", "black"),
    ("chandra-twinkle-top-black",   "Chandra Twinkle", "Top",   "black"),
    ("chandra-twinkle-bottom-black", "Chandra Twinkle", "Bottom", "black"),
    ("twinkle-tulle-shots-black",   "Twinkle Tulle",  "Bottom", "black"),
    ("lara-shirt-black",            "Lara",           "Bottom", "black"),
    ("rad-strings-short-black",     "Rad Strings",    "Bottom", "black"),
]


def _fetch(handle: str) -> dict:
    req = urllib.request.Request(f"https://radpolewear.com/products/{handle}.json", headers=_UA)
    return json.loads(urllib.request.urlopen(req, timeout=30).read())["product"]


def build_vaeter() -> list[Vater]:
    vaeter = []
    for handle, modell, typ, farbe in PRODUCTS:
        p = _fetch(handle)
        images = [i["src"] for i in p.get("images", []) if i.get("src")]
        shop_sizes = {v.get("title") for v in p.get("variants", [])}
        # Voller Shop-Stand in Standard-Reihenfolge, XXL raus.
        groessen = [g for g in ALLOWED_GROESSEN if g in shop_sizes]
        kinder = [Kind(groesse=g, groesse_raw=g, position=i)
                  for i, g in enumerate(groessen)]
        # „Lara" ist ein Rock: als Bottom/Shorts gefiltert (Merkmal/Kategorie statisch),
        # aber im Anzeigenamen „Rock" (reiner Content, Tjorben 2026-06-25).
        name_typ = "Rock" if modell == "Lara" else None
        vaeter.append(Vater(
            handle=handle, product_id=p.get("id", 0), title_raw=p.get("title", ""),
            vendor="RAD Polewear", modell_basis=modell, garment_type=typ, farbe_raw=farbe,
            name_typ=name_typ, body_html=p.get("body_html", ""), image_urls=images, kinder=kinder,
        ))
    return vaeter
