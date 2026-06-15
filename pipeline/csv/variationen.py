"""
CSV 2: Variationen (12 Spalten, run_brief §5).
Eine Zeile pro Größen-Variante des Vaters. Darstellungsform DROPDOWN.
Variationsname lokalisiert (Größe/Size/Taille/Taglia/Talla); Werte universal.
"""
from __future__ import annotations

from .. import spec, constants as C
from ..model import Vater


def _rank(groesse: str) -> int:
    return C.GROESSEN_RANG.index(groesse) if groesse in C.GROESSEN_RANG else -1

COLUMNS = [
    "Artikelnummer", "Variationsname", "Darstellungsform", "Variationswertname",
    "Global-Englisch: Variationsname", "Global-Englisch: Variationswertname",
    "Global-Französisch: Variationsname", "Global-Französisch: Variationswertname",
    "Global-Italienisch: Variationsname", "Global-Italienisch: Variationswertname",
    "Global-Spanisch: Variationsname", "Global-Spanisch: Variationswertname",
    # JTL-Ameise sortiert Variationswerte sonst ALPHABETISCH (L,M,S,XS). Mit
    # expliziter Sortiernummer respektiert JTL die Reihenfolge (XS=1..XL=5).
    "Sortiernummer Variation", "Sortiernummer Variationswert",
]

VARIATIONSNAME = {"de": "Größe", "en": "Size", "fr": "Taille", "it": "Taglia", "es": "Talla"}


def build_rows(vaeter: list[Vater], supplier: dict, run_date: str) -> list[dict]:
    rows: list[dict] = []
    for v in vaeter:
        vnr = spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)
        # Aufsteigend ausgeben; die Anzeige-Reihenfolge steuert die Sortiernummer.
        for k in sorted(v.kinder, key=lambda x: _rank(x.groesse)):
            sort_wert = _rank(k.groesse) + 1  # XS=1, S=2, M=3, L=4, XL=5
            rows.append({
                "Artikelnummer": vnr,
                "Variationsname": VARIATIONSNAME["de"], "Darstellungsform": "DROPDOWN",
                "Variationswertname": k.groesse,
                "Global-Englisch: Variationsname": VARIATIONSNAME["en"],
                "Global-Englisch: Variationswertname": k.groesse,
                "Global-Französisch: Variationsname": VARIATIONSNAME["fr"],
                "Global-Französisch: Variationswertname": k.groesse,
                "Global-Italienisch: Variationsname": VARIATIONSNAME["it"],
                "Global-Italienisch: Variationswertname": k.groesse,
                "Global-Spanisch: Variationsname": VARIATIONSNAME["es"],
                "Global-Spanisch: Variationswertname": k.groesse,
                "Sortiernummer Variation": "1",
                "Sortiernummer Variationswert": str(sort_wert),
            })
    return rows
