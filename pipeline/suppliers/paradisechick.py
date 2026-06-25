"""
Paradise Chick — Erstanlage (Rechnung ΤΙΜ-EU-0000000512, 24.06.2026). WooCommerce-Fetch.

NUR die 9 Artikel aus Sofias Link-Liste — die übrige Rechnung (280 Stk) sind andere
Modelle und gehören NICHT hierher. Shop ist WooCommerce (Store API), nicht Shopify.
Größen = voller Shop-Stand XS–XL (pures XXL raus). Garter Belt hat Kombigrößen
(XS/S, M/L, XL/XXL) und wird als Shorts geführt (statische Merkmalsverwaltung),
Anzeigename behält „Garter Belt“ (name_typ). EK in EUR (Rechnung, Netto = Stückpreis
× 0,55 wegen 45 % Wholesale-Rabatt). Keine Barcodes auf der Rechnung/im Shop.
"""
from __future__ import annotations

import json
import urllib.request

from ..model import Vater, Kind

_UA = {"User-Agent": "Mozilla/5.0"}
_STORE_API = "https://paradisechick.com/wp-json/wc/store/v1/products?slug="

# Shop-Größenname -> normalisiert. Pures XXLarge fliegt raus (nie XXL); kombinierte
# Garter-Belt-Größen bleiben als Anzeige-Variationswert erhalten.
SIZE_MAP = {
    "XSmall": "XS", "Small": "S", "Medium": "M", "Large": "L", "XLarge": "XL",
    "XXLarge": None,  # pures XXL nie anlegen
    "XSmall/Small": "XS/S", "Medium/Large": "M/L", "XLarge/XXLarge": "XL/XXL",
}
SIZE_ORDER = ["XS", "S", "M", "L", "XL", "XS/S", "M/L", "XL/XXL"]

# (handle, modell_basis, garment_type, name_typ, farbe_raw)
PRODUCTS = [
    ("florida-bodysuit-lilly",            "Florida",         "Bodysuit", None,          "lilly"),
    ("florida-garter-belt-lilly",         "Florida",         "Accessoire","Garter Belt", "lilly"),
    ("florida-strappy-top-plum",          "Florida Strappy", "Top",      None,          "plum"),
    ("florida-strappy-top-banana",        "Florida Strappy", "Top",      None,          "banana"),
    ("florida-v-short-stripes-plum",      "Florida Stripes", "Shorts",   None,          "plum"),
    ("florida-v-short-stripes-banana",    "Florida Stripes", "Shorts",   None,          "banana"),
    ("gigi-active-bodysuit-shimmery-haze","Gigi Active",     "Bodysuit", None,          "shimmery-haze"),
    ("gigi-v-short-thunderstorm",         "Gigi",            "Shorts",   None,          "thunderstorm"),
    ("iconic-v-short-stripes",            "Iconic",          "Shorts",   None,          "stripes"),
]


# Explizite Outfit-Cross-Sells (sprechende Vater-ArtNr, Präfix PC) — die Marke
# designt diese als Sets, die generische Heuristik erfasst sie aber nicht
# (unterschiedliche Modellnamen). Beidseitig „Vervollständige Dein Outfit".
OUTFIT_PAIRS = [
    ("PC-Florida-Bodysuit-Lilly",   "PC-Florida-Accessoire-Lilly"),     # Bodysuit + Garter Belt Lilly
    ("PC-FloridaStrappy-Top-Plum",  "PC-FloridaStripes-Shorts-Plum"),   # Top + V-Short Plum
    ("PC-FloridaStrappy-Top-Banana","PC-FloridaStripes-Shorts-Banana"), # Top + V-Short Banana
]


def _fetch(slug: str) -> dict:
    req = urllib.request.Request(_STORE_API + slug, headers=_UA)
    data = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if not data:
        raise RuntimeError(f"Paradise Chick: kein Produkt für slug {slug!r}")
    return data[0]


def _sizes(product: dict) -> list[str]:
    raw = []
    for a in product.get("attributes", []):
        name = (a.get("name", "") + a.get("taxonomy", "")).lower()
        if "size" in name:
            raw = [t.get("name", "") for t in a.get("terms", [])]
    mapped = [SIZE_MAP.get(s, s) for s in raw]
    mapped = [m for m in mapped if m]  # XXLarge (None) raus
    return sorted(set(mapped), key=lambda s: SIZE_ORDER.index(s) if s in SIZE_ORDER else 99)


def build_vaeter() -> list[Vater]:
    vaeter = []
    for handle, modell, typ, name_typ, farbe in PRODUCTS:
        p = _fetch(handle)
        images = [i["src"] for i in p.get("images", []) if i.get("src")]
        groessen = _sizes(p)
        kinder = [Kind(groesse=g, groesse_raw=g, position=i) for i, g in enumerate(groessen)]
        vaeter.append(Vater(
            handle=handle, product_id=p.get("id", 0), title_raw=p.get("name", ""),
            vendor="Paradise Chick", modell_basis=modell, garment_type=typ,
            name_typ=name_typ, farbe_raw=farbe,
            body_html=p.get("description", ""), image_urls=images, kinder=kinder,
        ))
    return vaeter
