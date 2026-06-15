"""
CSV 4: Attribute (8 Spalten, QUOTE_ALL, SPEC §11 / run_brief §7).
Eine Zeile pro Artikel × Attribut, auf Vater UND alle Kinder dupliziert (E34).
Mindest-Set: markentext, artikeldetails, material_and_care, size_and_fit.

markentext = evergreen Brand-Story aus Mapping; die 3 anderen aus content.
Alle 5 Sprachen voll ausformuliert (E73).
"""
from __future__ import annotations

from .. import spec, content as content_mod
from ..model import Vater

COLUMNS = [
    "Lieferant", "Artikelnummer (Lieferant)", "Attributname", "Attributwert",
    "Englisch: Attributwert", "Französisch: Attributwert",
    "Italienisch: Attributwert", "Spanisch: Attributwert",
]
ATTR_ORDER = ["markentext", "artikeldetails", "material_and_care", "size_and_fit"]


def build_rows(vaeter: list[Vater], supplier: dict, content: dict) -> list[dict]:
    lieferant = supplier["anzeigename"]
    markentext = content_mod.markentext_from_mapping(supplier)
    rows: list[dict] = []

    for v in vaeter:
        vnr = spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)
        c = content[vnr]
        attrs = {"markentext": markentext, **c["attribute"]}
        article_ids = [vnr] + [spec.kind_artnr(vnr, k.groesse) for k in v.kinder]
        for aid in article_ids:
            for name in ATTR_ORDER:
                a = attrs[name]
                rows.append({
                    "Lieferant": lieferant,
                    "Artikelnummer (Lieferant)": aid,
                    "Attributname": name,
                    "Attributwert": a["de"],
                    "Englisch: Attributwert": a["en"],
                    "Französisch: Attributwert": a["fr"],
                    "Italienisch: Attributwert": a["it"],
                    "Spanisch: Attributwert": a["es"],
                })
    return rows
