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


def _style_merkmalname(garment_type: str) -> str | None:
    # Bodysuit läuft über Style Tops (SPEC §7); Leggings über Style Shorts.
    # Accessoires (z.B. Garter Belt) bekommen KEIN Style-Merkmal — sie tauchen sonst
    # in den Shorts-/Tops-Style-Filtern auf, gehören aber in die Accessoires-Kategorie.
    if garment_type == "Accessoire":
        return None
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
        # merkmal_farbe: str ODER Liste (mehrere Farben, wenn keine eindeutige
        # Dominante -> Artikel wird unter mehreren Farbfiltern gefunden).
        farben = c["merkmal_farbe"]
        if isinstance(farben, str):
            farben = [farben]
        style_name = _style_merkmalname(v.garment_type)
        style_werte = c["style_werte"]

        # Vater: Farbe(n) + Style (keine Größe). Accessoires: kein Style (style_name None).
        for f in farben:
            add(vnr, "Farbe Kleidung", f)
        if style_name:
            for w in style_werte:
                add(vnr, style_name, w)

        # Kinder: Farbe(n) + Größe + Style
        for k in v.kinder:
            knr = spec.kind_artnr(vnr, k.groesse)
            for f in farben:
                add(knr, "Farbe Kleidung", f)
            # Größe Kleidung nur für Standardgrößen — JTLs Größen-Merkmal ist eine
            # statische Liste (XS..2XL). Kombi-/Sondergrößen (z.B. Garter Belt „XS/S“,
            # „XL/XXL“) sind reine Variationswerte und bekommen kein Filter-Merkmal.
            if k.groesse in spec.MERKMAL_GROESSE_ERLAUBT:
                add(knr, "Größe Kleidung", k.groesse)
            if style_name:
                for w in style_werte:
                    add(knr, style_name, w)
    return rows
