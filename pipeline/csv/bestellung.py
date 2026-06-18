"""CSV (optional): Lieferantenbestellung (Ameise-Import-Typ „Lieferanten > Lieferantenbestellungen").

Übersetzt eine Lieferanten-Rechnung in eine importierbare Bestellung: pro bestellter
Größe eine Zeile mit Menge + Lieferdatum.

Schema (verifiziert am echten Import 2026-06-17): `Artikelnummer; Menge; Lieferdatum`
- **Artikelnummer** = die A-Nummer des Kind-Artikels (identifizieren anhand „Artikelnummer",
  JTL-Default). Funktioniert direkt mit der bestehenden Ameise-Standardeinstellung.
- **Lieferant** wird als Ameise-Standardwert gesetzt (z.B. „Lunalae"), NICHT als Spalte.
- **Warenlager / Firma / Benutzer** ebenfalls als Standardwerte.
- **EK** NICHT mitgeben: Einstellung „Netto-EK aus Lieferantenartikel übernehmen = Ja"
  zieht ihn aus dem Artikel (dort als Lieferanten-Original-Währung, E97).
- **Lieferdatum** = Importdatum + Lieferzeit des Lieferanten (z.B. Lunalae 30 Tage, E97).

Mengen-Quelle: `EK_input/menge_<lieferant>.csv` (modell_basis;garment_type;farbe;groesse;menge).
"""
from __future__ import annotations

import csv

from ..model import Vater

COLUMNS = ["Artikelnummer", "Menge", "Lieferdatum"]


def load_menge(path) -> dict[tuple, int]:
    """(modell_basis, garment_type, farbe, groesse) -> Menge (int)."""
    m: dict[tuple, int] = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            menge = (r.get("menge") or "").strip()
            if menge:
                m[(r["modell_basis"], r["garment_type"], r["farbe"], r["groesse"])] = int(menge)
    return m


def artnr_map(vaeter: list[Vater]) -> dict[tuple, str]:
    """(modell_basis, garment_type, farbe, groesse) -> A-Nummer des Kindes.
    Setzt voraus, dass numbering.assign(...) vorher die A-Nummern vergeben hat."""
    return {(v.modell_basis, v.garment_type, v.farbe_raw, k.groesse): k.artikelnummer
            for v in vaeter for k in v.kinder}


def build_rows(menge_map: dict, artnr: dict, lieferdatum: str) -> list[dict]:
    """Pro bestellter (modell,typ,farbe,größe): A-Nummer + Menge + Lieferdatum."""
    rows: list[dict] = []
    for key, menge in menge_map.items():
        if not menge:
            continue
        a = artnr.get(key)
        if not a:
            continue
        rows.append({"Artikelnummer": a, "Menge": str(menge), "Lieferdatum": lieferdatum})
    rows.sort(key=lambda r: r["Artikelnummer"])
    return rows
