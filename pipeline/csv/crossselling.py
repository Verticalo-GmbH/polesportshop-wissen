"""
CSV 5: Cross-Selling (3 Spalten, SPEC §12 / E80).
Artikelnummer; Artikelnummer Cross-Seller; Cross-Selling-Gruppe

Beziehungen werden NUR innerhalb des Lauf-Scopes (= erstellte Väter) berechnet —
die rechte Spalte muss auf existierende Vater-Artikel verweisen. Schwester-Artikel
außerhalb des Scopes kommen später via Family-Refresh (§12.1 Punkt 7).

- Vervollständige Dein Outfit: gleiche (modell_basis, farbe), Top<->Bottom
- Ähnliche Artikel: gleiche (modell_basis, garment_type), andere Farbe
Kinder-Replikation: linke Spalte = Vater UND alle Kinder; rechte Spalte strikt Vater.
"""
from __future__ import annotations

from collections import defaultdict
from .. import spec
from ..model import Vater

COLUMNS = ["Artikelnummer", "Artikelnummer Cross-Seller", "Cross-Selling-Gruppe"]
GRUPPE_OUTFIT = "Vervollständige Dein Outfit"
GRUPPE_AEHNLICH = "Ähnliche Artikel"

_PARTNER = {"Top": "Bottom", "Bottom": "Top"}  # Bodysuit hat keinen Outfit-Partner


def _ids_links(v: Vater) -> list[str]:
    """Linke Spalte: Vater + alle Kinder (Kinder-Replikation). Weg B (E94):
    Verknüpfung über die vorab vergebene A-Nummer."""
    return [v.artikelnummer] + [k.artikelnummer for k in v.kinder]


def build_rows(vaeter: list[Vater], extra_outfit_pairs: list[tuple[str, str]] | None = None) -> list[dict]:
    by_modell_farbe: dict[tuple, dict[str, Vater]] = defaultdict(dict)   # (modell,farbe) -> {typ: V}
    by_modell_typ: dict[tuple, list[Vater]] = defaultdict(list)          # (modell,typ) -> [V...]
    by_vnr: dict[str, Vater] = {}                                         # Vater-ArtNr (sprechend) -> V
    for v in vaeter:
        by_modell_farbe[(v.modell_basis, v.farbe_raw)][v.garment_type] = v
        by_modell_typ[(v.modell_basis, v.garment_type)].append(v)
        by_vnr[spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)] = v

    rows: list[dict] = []
    seen: set[tuple[str, str, str]] = set()

    def add_relation(a: Vater, b: Vater, gruppe: str):
        for left in _ids_links(a):
            key = (left, b.artikelnummer, gruppe)
            if key in seen:
                continue
            seen.add(key)
            rows.append({"Artikelnummer": left, "Artikelnummer Cross-Seller": b.artikelnummer,
                         "Cross-Selling-Gruppe": gruppe})

    for v in vaeter:
        # Outfit-Partner (gleiche Farbe, gegensätzlicher Typ)
        partner_typ = _PARTNER.get(v.garment_type)
        if partner_typ:
            partner = by_modell_farbe[(v.modell_basis, v.farbe_raw)].get(partner_typ)
            if partner:
                add_relation(v, partner, GRUPPE_OUTFIT)
        # Ähnliche (gleicher Typ, andere Farbe)
        for sib in by_modell_typ[(v.modell_basis, v.garment_type)]:
            if sib is not v:
                add_relation(v, sib, GRUPPE_AEHNLICH)

    # Explizite Outfit-Paare des Lieferanten (sprechende Vater-ArtNr), wenn die
    # generische Heuristik sie nicht erfasst (z.B. Outfit-Sets mit unterschiedlichem
    # Modellnamen wie Bodysuit+Garter Belt oder Top+Short verschiedener Modell-Stämme).
    # Beidseitig, Gruppe „Vervollständige Dein Outfit".
    for a_vnr, b_vnr in (extra_outfit_pairs or []):
        a, b = by_vnr.get(a_vnr), by_vnr.get(b_vnr)
        if a and b:
            add_relation(a, b, GRUPPE_OUTFIT)
            add_relation(b, a, GRUPPE_OUTFIT)
    return rows
