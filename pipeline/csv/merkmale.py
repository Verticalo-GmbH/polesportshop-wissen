"""
CSV 3: Merkmale (4 Spalten, nur Deutsch, SPEC §7).
Lieferant; Artikelnummer (Lieferant); Merkmalname; Merkmalwertname 1

- Farbe Kleidung: Vater + alle Kinder (Wert aus content.merkmal_farbe)
- Größe Kleidung: nur Kinder (Wert = Kind-Größe)
- Style Tops/Shorts: Vater + alle Kinder (mehrere Werte -> mehrere Zeilen)
Alle auf Vater UND Kinder explizit dupliziert (E34).
"""
from __future__ import annotations

from .. import spec
from ..model import Vater

COLUMNS = ["Lieferant", "Artikelnummer (Lieferant)", "Merkmalname", "Merkmalwertname 1"]


def _style_merkmalname(garment_type: str) -> str:
    # Bodysuit läuft über Style Tops (SPEC §7); Leggings über Style Shorts.
    return "Style Tops" if garment_type in ("Top", "Bodysuit") else "Style Shorts"


def build_rows(vaeter: list[Vater], supplier: dict, content: dict) -> list[dict]:
    lieferant = supplier["anzeigename"]
    rows: list[dict] = []

    def add(artnr: str, name: str, wert: str):
        rows.append({"Lieferant": lieferant, "Artikelnummer (Lieferant)": artnr,
                     "Merkmalname": name, "Merkmalwertname 1": wert})

    for v in vaeter:
        vnr = spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)
        c = content[vnr]
        farbe = c["merkmal_farbe"]
        style_name = _style_merkmalname(v.garment_type)
        style_werte = c["style_werte"]

        # Vater: Farbe + Style (keine Größe)
        add(vnr, "Farbe Kleidung", farbe)
        for w in style_werte:
            add(vnr, style_name, w)

        # Kinder: Farbe + Größe + Style
        for k in v.kinder:
            knr = spec.kind_artnr(vnr, k.groesse)
            add(knr, "Farbe Kleidung", farbe)
            add(knr, "Größe Kleidung", k.groesse)
            for w in style_werte:
                add(knr, style_name, w)
    return rows
