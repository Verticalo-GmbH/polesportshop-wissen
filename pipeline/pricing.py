"""
Pricing (P3, run_brief Stage 4).

VK_brutto = EK_netto * AUFSCHLAGSFAKTOR (2.0), dann kaufmännische Rundung auf
das nächste X,90 (run_brief_daten.md:255-257; Bsp 27*2=54 -> 53,90).

EK kommt aus einer EK-Liste/Rechnung (CSV in pipeline/EK_input/), gekeyt auf
(modell_basis, garment_type, farbe). Fehlt für einen Vater der EK -> STOPP
(Charter-Prinzip 10): nicht raten, sondern als 'missing' melden.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

from . import constants as C
from .model import Vater


def _key(modell: str, typ: str, farbe: str) -> tuple[str, str, str]:
    return (modell.strip().lower(), typ.strip().lower(), (farbe or "").strip().lower())


def round_vk_90(value: float) -> float:
    """Nächstes X,90 (kaufmännisch, Ties auf-runden)."""
    n = math.floor(value - 0.9 + 0.5 + 1e-9)  # round-half-up von (value-0.9)
    return round(n + 0.9, 2)


def load_ek_csv(path: Path) -> dict[tuple[str, str, str], float]:
    ek: dict[tuple[str, str, str], float] = {}
    with path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            ek[_key(row["modell"], row["typ"], row.get("farbe", ""))] = float(
                str(row["ek_netto"]).replace(",", ".")
            )
    return ek


def apply_pricing(vaeter: list[Vater], ek_map: dict[tuple[str, str, str], float]):
    """
    Setzt ek_netto + vk_brutto auf jedem Vater, für den ein EK existiert.
    -> (priced: list[Vater], missing: list[Vater]).
    """
    priced, missing = [], []
    for v in vaeter:
        ek = ek_map.get(_key(v.modell_basis, v.garment_type, v.farbe_raw))
        if ek is None:
            missing.append(v)
            continue
        v.ek_netto = ek
        v.vk_brutto = round_vk_90(ek * C.AUFSCHLAGSFAKTOR)
        priced.append(v)
    return priced, missing
