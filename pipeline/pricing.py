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


def apply_pricing(vaeter: list[Vater], ek_map: dict[tuple[str, str, str], float],
                  fx_to_eur: float = 1.0):
    """
    Setzt ek_netto (in EUR) + vk_brutto auf jedem Vater, für den ein EK existiert.
    fx_to_eur: Umrechnungsfaktor falls Rechnung nicht in EUR (z.B. USD 0.8612).
    EK_eur = EK_roh * fx; VK = EK_eur * 2.0 -> kaufm. ,90.
    -> (priced, missing).
    """
    priced, missing = [], []
    for v in vaeter:
        ek = ek_map.get(_key(v.modell_basis, v.garment_type, v.farbe_raw))
        if ek is None:
            missing.append(v)
            continue
        ek_eur = round(ek * fx_to_eur, 2)
        v.ek_original = round(ek, 2)   # Lieferanten-Währung (z.B. AUD) -> Lieferanten-Netto-EK
        v.ek_netto = ek_eur            # EUR -> GLD / VK
        v.vk_brutto = round_vk_90(ek_eur * C.AUFSCHLAGSFAKTOR)
        priced.append(v)
    return priced, missing
