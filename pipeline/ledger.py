"""
Artikel-Ledger (E102): zentraler Stand ALLER angelegten Artikel, gekeyt auf die
A-Nummer (Vater-Ebene, Kinder eingebettet).

Prinzip wie ein Git-Working-Tree: die Datei hält IMMER nur den *letzten* Stand pro
Artikel. Die Historie liefert git über die Commits dieser einen Datei
(`pipeline/state/artikel_ledger.json`) — kein Append-Log, kein Durchsuchen alter
Output-Ordner mehr. Jeder kanonische Lauf (persist=True) ruft `upsert(...)` und
überschreibt die betroffenen A-Nummern mit dem neuen Stand.

Relevante Felder pro Vater: Lieferant + WaWi-Nr, sprechender Schlüssel, Anzeigename,
Modell/Typ/Farbe, Währung + fx, EK (original + EUR), GLD, Brutto-VK, Herkunftsland,
Kinder {A-Nummer: Größe}, EAN je Größe (falls vorhanden), Quelle, Stand-Datum.
"""
from __future__ import annotations

import json
from datetime import datetime

from . import spec, config

LEDGER_PATH = config.PIPELINE_DIR / "state" / "artikel_ledger.json"


def load() -> dict:
    if LEDGER_PATH.exists():
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return {}


def _record(v, supplier: dict, stand: str, quelle: str = "") -> dict:
    sk = spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)
    marke = supplier.get("marke_kurz") or supplier.get("hersteller") or supplier["anzeigename"]
    ean = {k.groesse: k.ean for k in v.kinder if k.ean}
    return {
        "lieferant": supplier["anzeigename"],
        "lieferant_nr": supplier.get("lieferantennummer_wawi"),
        "artnr_lieferant": sk,
        "name_de": spec.vater_artikelname(marke, v.garment_type, v.modell_basis,
                                          v.farbe_raw, "de", v.name_typ),
        "modell": v.modell_basis, "typ": v.garment_type,
        "name_typ": v.name_typ, "farbe": v.farbe_raw,
        "waehrung": supplier.get("waehrung", "EUR"),
        "fx_to_eur": float(supplier.get("fx_to_eur", 1.0) or 1.0),
        "ek_original": v.ek_original, "ek_eur": v.ek_netto,
        "gld": v.gld, "vk_brutto": v.vk_brutto,
        "herkunftsland": supplier.get("herkunftsland", ""),
        "kinder": {k.artikelnummer: k.groesse for k in v.kinder},
        "ean": ean or None,
        "quelle": quelle,
        "stand": stand,
    }


def upsert(vaeter, supplier: dict, stand: str | None = None, quelle: str = "") -> int:
    """Überschreibt die A-Nummern der übergebenen Väter mit ihrem aktuellen Stand.
    Gibt die Gesamtzahl der Artikel (Väter) im Ledger zurück."""
    stand = stand or datetime.now().strftime("%Y-%m-%d")
    led = load()
    for v in vaeter:
        if v.artikelnummer:
            led[v.artikelnummer] = _record(v, supplier, stand, quelle)
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(
        json.dumps(led, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")
    return len(led)
