"""Weg B (E94): Artikelnummern aus dem WaWi-Nummernkreis VORAB vergeben.

Hintergrund: JTL-Ameise kann das Kind-Muster 'Vaternummer-001' NICHT selbst
erzeugen (Forum-Befund). Damit das Lager-scannbare Schema lückenlos an den
fortlaufenden WaWi-Nummernkreis anschließt, vergibt die Pipeline die Nummern selbst:

- Vater = <PRAEFIX><laufende Nummer>            z.B. A1009261   (+1 pro Vater)
- Kind  = <Vaternummer>-001, -002 ...           aufsteigend nach Größe (XS=-001)
- Kinder verbrauchen KEINE eigene Hauptnummer (wie in der WaWi-UI).

Der Zähler wird im Repo mitgeführt (state/nummernkreis.json), Startwert einmalig
aus dem WaWi-Nummernkreis geseedet. Pro bestätigtem Lauf um Anzahl Väter erhöht.
Tjorben hält den WaWi-Zähler auf gleichem Stand; bei Drift hier resyncen.
"""
from __future__ import annotations

import json

from . import config, constants as C
from .model import Vater

STATE = config.PIPELINE_DIR / "state" / "nummernkreis.json"


def _rank(groesse: str) -> int:
    return C.GROESSEN_RANG.index(groesse) if groesse in C.GROESSEN_RANG else 99


def load_state() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8"))


def assign(vaeter: list[Vater], start: int | None = None,
           praefix: str | None = None, persist: bool = False) -> int:
    """Setzt v.artikelnummer + k.artikelnummer auf das A-Nummern-Schema.
    Gibt die nächste freie Nummer zurück. persist=True schreibt den Zähler fort."""
    st = load_state()
    n = st["artikel_next"] if start is None else start
    praefix = st.get("praefix", "A") if praefix is None else praefix
    for v in vaeter:
        v.artikelnummer = f"{praefix}{n}"
        for j, k in enumerate(sorted(v.kinder, key=lambda x: _rank(x.groesse)), start=1):
            k.artikelnummer = f"{v.artikelnummer}-{j:03d}"
        n += 1
    if persist:
        st["artikel_next"] = n
        STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    return n
