"""EAN/GTIN-Anreicherung (E95): UTC-Barcodes pro Größe aus Lieferanten-Referenz.

Quelle = committete Referenz-CSV `content/ean_<datei>.csv` mit Spalten
`modell_basis;garment_type;farbe;groesse;ean`. Schlüssel deckt sich mit der
Väter-Identität (modell_basis, garment_type, farbe_raw) + Kind-Größe.

Hintergrund: Bei Lunalae kommen die Barcodes (UTC) aus dem Wholesale-Sheet ins
EAN-Feld der WaWi. Jede Größe hat einen eigenen Barcode -> auf Kind-Ebene gesetzt.
"""
from __future__ import annotations

import csv

from .model import Vater


def load_map(path) -> dict[tuple, str]:
    """(modell_basis, garment_type, farbe, groesse) -> ean."""
    m: dict[tuple, str] = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            m[(r["modell_basis"], r["garment_type"], r["farbe"], r["groesse"])] = r["ean"].strip()
    return m


def attach(vaeter: list[Vater], path) -> tuple[int, list[str]]:
    """Setzt k.ean je Kind aus der Referenz. Gibt (gesetzt, fehlende) zurück."""
    m = load_map(path)
    gesetzt, fehlend = 0, []
    for v in vaeter:
        for k in v.kinder:
            ean = m.get((v.modell_basis, v.garment_type, v.farbe_raw, k.groesse))
            if ean:
                k.ean = ean
                gesetzt += 1
            else:
                fehlend.append(f"{v.modell_basis}|{v.garment_type}|{v.farbe_raw}|{k.groesse}")
    return gesetzt, fehlend
