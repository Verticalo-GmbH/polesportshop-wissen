"""
Pricing (P3, run_brief Stage 4).

Netto-VK = EK_netto * AUFSCHLAGSFAKTOR (2.0) — Keystone auf NETTO. Brutto-VK =
Netto-VK * MWST_FAKTOR (1,19), dann kaufm. Rundung auf das nächste X,90.
(Fix 2026-06-25: vorher ×2 fälschlich auf Brutto -> MwSt fraß die Marge.)

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


def charm_vk(vk: float) -> float:
    """Verkaufspsychologische Korrektur (E101): runde Zehner-Beträge vermeiden.
    Endet der Euro-Betrag auf 0 (z.B. 40,90 / 50,90), 1 € runter -> X9,90 (39,90 / 49,90).
    Alle anderen Endungen (46,90, 62,90) bleiben."""
    euro = int(round(vk, 2))
    return round(vk - 1.0, 2) if euro % 10 == 0 else round(vk, 2)


def load_ek_csv(path: Path) -> dict[tuple[str, str, str], float]:
    ek: dict[tuple[str, str, str], float] = {}
    with path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            ek[_key(row["modell"], row["typ"], row.get("farbe", ""))] = float(
                str(row["ek_netto"]).replace(",", ".")
            )
    return ek


def apply_pricing(vaeter: list[Vater], ek_map: dict[tuple[str, str, str], float],
                  fx_to_eur: float = 1.0, ek_aufschlag: float = 0.0, vk_aufschlag: float = 0.0,
                  gld_aufschlag: float = C.GLD_AUFSCHLAG_NICHTEU_EUR):
    """
    Setzt ek_netto (in EUR) + vk_brutto auf jedem Vater, für den ein EK existiert.
    fx_to_eur: Umrechnungsfaktor falls Rechnung nicht in EUR (z.B. USD 0.8612).
    Netto-VK = (EK_eur + ek_aufschlag) * 2.0; Brutto-VK = *MwSt -> ,90 + vk_aufschlag.
    GLD = EK_eur + gld_aufschlag (EU +0,50 / Nicht-EU +2,30, E98/E103).
    ek_aufschlag/vk_aufschlag fließen NUR in den VK; gld_aufschlag NUR in den GLD.
    Alle drei nach EU/Nicht-EU differenziert (Tag, vom Orchestrator gesetzt). -> (priced, missing).
    """
    priced, missing = [], []
    for v in vaeter:
        ek = ek_map.get(_key(v.modell_basis, v.garment_type, v.farbe_raw))
        if ek is None:
            missing.append(v)
            continue
        ek_eur = round(ek * fx_to_eur, 2)
        v.ek_original = round(ek, 2)   # Lieferanten-Währung (z.B. AUD) -> Lieferanten-Netto-EK
        v.ek_netto = ek_eur            # EUR -> Basis der VK-Kalkulation
        v.gld = round(ek_eur + gld_aufschlag, 2)   # Ø-EK/GLD inkl. EU/Nicht-EU-Kosten-Aufschlag (E98/E103)
        # Keystone auf NETTO: Netto-VK = (EK + EK-Aufschlag)*2, dann MwSt OBENDRAUF (*1,19)
        # -> Brutto-VK, kaufm. auf ,90; plus VK-Aufschlag (E98, Nicht-EU); dann Charm (E101).
        vk = round_vk_90((ek_eur + ek_aufschlag) * C.AUFSCHLAGSFAKTOR * C.MWST_FAKTOR) + vk_aufschlag
        v.vk_brutto = charm_vk(round(vk, 2))
        priced.append(v)
    return priced, missing
