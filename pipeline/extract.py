"""
Extraktion: rohe Shopify-Produkte -> interne Vater/Kind-Modelle (P2).

Scope: STRIKT Pole-Kleidung (Tjorben 2026-06-15). Drei Buckets:
  - keep:    sauber geparst, geht in die Pipeline
  - review:  mehrdeutig (Color-Achse, Sports/Athletic, kein Garment-Typ) -> User-Sign-off
  - exclude: Swimwear/Outerwear/Streetwear/Accessoires

Trennung Modell/Farbe/Typ: deterministisch + kuratierte Vokabular-/Override-Tabelle
(constants.py). Farbe nur aus Dash-Suffix ODER Color-in-Name-Familie (Savanna);
Colorway-Namen wie "Black Coffee" bleiben Modellname (farbe="").
"""
from __future__ import annotations

import re
from typing import Optional

from . import constants as C
from .model import Vater, Kind


def normalize_size(raw: Optional[str]) -> Optional[str]:
    """E27 kombi_reduziert_auf_kleinste. None = keine echte Größen-Achse."""
    if raw is None:
        return None
    r = raw.strip()
    if r.lower() in C.GROESSE_EINHEIT:
        return None
    tokens = [t.strip().upper() for t in r.split("/") if t.strip()]
    ranked = [t for t in tokens if t in C.GROESSEN_RANG]
    if ranked:
        return min(ranked, key=C.GROESSEN_RANG.index)
    return tokens[0] if tokens else None


def classify(title: str) -> tuple[str, Optional[str], str, Optional[str]]:
    """
    -> (bucket, garment_type, reason, matched_token)
    bucket in {keep, review, exclude}.
    """
    t = title.lower().strip()
    if t in C.EXCLUDE_TITLES_EXPLICIT:
        return ("exclude", None, "explizit ausgeschlossen (kein Pole-Kleidungs-Typ)", None)
    if t in C.FORCE_REVIEW_TITLES:
        return ("review", None, "Material-als-Modell / Streetwear — manuell", None)
    for tok in C.EXCLUDE_TOKENS:
        if re.search(r"\b" + re.escape(tok) + r"\b", t):
            return ("exclude", None, f"Ausschluss-Token '{tok}' (Swim/Outerwear/Accessoire)", None)
    for tok, canonical in C.GARMENT_TYPES_KEEP:
        if re.search(r"\b" + re.escape(tok) + r"\b", t):
            # Sports/Athletic -> Review (Gym vs. Pole, Tjorben entscheidet)
            if re.search(r"\b(sports?|athletic)\b", t):
                return ("review", canonical, "Sports/Athletic — Pole oder Gym?", tok)
            return ("keep", canonical, "ok", tok)
    return ("review", None, "kein Garment-Typ erkennbar", None)


def _has_color_axis(product: dict) -> bool:
    return any((o.get("name") or "").strip().lower() == "color" for o in product.get("options", []))


def _split_model_color(title: str, garment_type: str, matched_token: str) -> tuple[str, str]:
    """-> (modell_basis ohne Typ/Farbe, farbe_raw)."""
    raw = title.strip()
    low = raw.lower()

    # (a) Color-in-Name-Familie (Savanna): "Savanna <Farbe/Print> <Typ>"
    for fam in C.COLOR_IN_NAME_FAMILIES:
        if low.startswith(fam):
            rest = raw[len(fam):].strip()
            # Garment-Typ-Wort hinten entfernen
            rest = re.sub(r"\b" + re.escape(matched_token) + r"\b", " ", rest, flags=re.I).strip()
            rest = re.sub(r"\s+", " ", rest)
            farbe = rest.strip().lower()  # casefold: "Original"/"original" -> eine Familie
            return (fam.capitalize(), farbe)

    # (b) Dash-Suffix-Farbe: alles nach dem (ersten) Bindestrich, wenn bekannte Farbe
    if "-" in raw:
        head, tail = raw.split("-", 1)
        cand = tail.strip().lower()
        if cand in C.COLOR_VOCAB:
            model = re.sub(r"\b" + re.escape(matched_token) + r"\b", " ", head, flags=re.I)
            model = re.sub(r"\s+", " ", model).strip()
            return (model, tail.strip().lower())

    # (c) keine Farb-Variante im Titel -> Colorway-/Modellname bleibt Modell
    model = re.sub(r"\b" + re.escape(matched_token) + r"\b", " ", raw, flags=re.I)
    model = re.sub(r"\s+", " ", model).strip()
    return (model, "")


def _build_kinder(product: dict) -> list[Kind]:
    # Größen-Achse finden (Option-Name size/Size); sonst option1
    size_idx = 0
    for i, o in enumerate(product.get("options", [])):
        if (o.get("name") or "").strip().lower() == "size":
            size_idx = i
            break
    key = f"option{size_idx + 1}"
    kinder: list[Kind] = []
    for v in product.get("variants", []):
        raw = v.get(key) or v.get("option1")
        norm = normalize_size(raw)
        kinder.append(Kind(
            groesse=norm or (raw or "").strip(),
            groesse_raw=(raw or "").strip(),
            position=v.get("position", 0),
            sku=v.get("sku") or None,
            grams=v.get("grams"),
            price_retail=float(v["price"]) if v.get("price") else None,
            available=bool(v.get("available", True)),
        ))
    return kinder


def parse_product(product: dict, garment_type: str, matched_token: str) -> Vater:
    modell_basis, farbe_raw = _split_model_color(product["title"], garment_type, matched_token)
    return Vater(
        handle=product.get("handle", ""),
        product_id=product.get("id", 0),
        title_raw=product["title"],
        vendor=product.get("vendor", ""),
        product_type=product.get("product_type") or None,
        tags=product.get("tags", []) if isinstance(product.get("tags"), list) else [],
        modell_basis=modell_basis,
        garment_type=garment_type,
        farbe_raw=farbe_raw,
        body_html=product.get("body_html") or "",
        image_urls=[img["src"] for img in product.get("images", []) if img.get("src")],
        kinder=_build_kinder(product),
    )


def build_dataset(products: list[dict]) -> dict:
    """-> {'keep': [Vater], 'review': [(title, reason)], 'exclude': [(title, reason)]}."""
    keep: list[Vater] = []
    review: list[tuple[str, str]] = []
    exclude: list[tuple[str, str]] = []
    for p in products:
        ov = C.TITLE_OVERRIDES.get(p["title"].lower().strip())
        if ov:
            model, gtype, farbe = ov
            v = parse_product(p, gtype, gtype)  # gtype als Dummy-Token (kein Titel-Match nötig)
            v.modell_basis, v.garment_type, v.farbe_raw = model, gtype, farbe
            keep.append(v)
            continue
        bucket, gtype, reason, tok = classify(p["title"])
        if bucket == "exclude":
            exclude.append((p["title"], reason))
        elif bucket == "review":
            review.append((p["title"], reason))
        else:  # keep
            if _has_color_axis(p):
                review.append((p["title"], "Color-Option-Achse (mehrere Farben in 1 Produkt) — manuell"))
                continue
            keep.append(parse_product(p, gtype, tok))
    return {"keep": keep, "review": review, "exclude": exclude}
