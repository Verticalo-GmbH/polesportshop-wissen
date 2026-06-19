"""CSV (optional): Lieferantenbestellung (Ameise-Import-Typ „Lieferanten > Lieferantenbestellungen").

Übersetzt eine Lieferanten-Rechnung in eine importierbare Bestellung: pro bestellter
Größe eine Zeile mit Menge + Lieferdatum.

Schema: `Artikelnummer; Menge; Lieferdatum; Zugehörige Auftragsnummer; Lieferant; Warenlager; Firma; Benutzer`
- **Artikelnummer** = A-Nummer des Kind-Artikels (identifizieren anhand „Artikelnummer", JTL-Default).
- **Lieferant / Warenlager / Firma / Benutzer als SPALTEN** (nicht als Standardwerte) → **eine**
  universelle Ameise-Vorlage für ALLE Lieferanten, keine pro-Lieferant-Vorlage nötig. Warenlager/
  Firma/Benutzer sind WaWi-instanz-konstant (Defaults unten), Lieferant variiert pro Lieferant.
- **EK** NICHT mitgeben: „Netto-EK aus Lieferantenartikel übernehmen = Ja" zieht ihn aus dem Artikel (E97).
- **Lieferdatum** = Importdatum + Lieferzeit des Lieferanten (E97).
- **Zugehörige Auftragsnummer** = Referenz fürs Lager (E99/E100). **Beschreibend + stichpunktartig,
  einzeilig, Trenner Pipe ` | `** — jede Info hilft dem Lager bei der Zuordnung. Aufbau:
  `Bestellung <Bestell-Ref> | Rechnung <Nr> | <Kollektion/Quelle>`. Die **vorab vergebene Bestell-Referenz**
  (`<PREFIX>-<JAHR>-<NN>` pro Lieferant, E100) steht **führend** und ist der Matching-Schlüssel
  fürs Lager (Wareneingang). Beispiele: `Bestellung LUN-2026-01 | Rechnung #3124 | Diamante`,
  `Rechnung APRIL26` (wenn keine Bestell-Referenz). Fehlt eine Rechnungsnummer: sinnvoller Zeitstempel.
  „Lieber zu viele Referenzen als zu wenige."

Mengen-Quelle: `EK_input/menge_<lieferant>.csv` (modell_basis;garment_type;farbe;groesse;menge).
"""
from __future__ import annotations

import csv

from ..model import Vater

COLUMNS = ["Artikelnummer", "Menge", "Lieferdatum", "Zugehörige Auftragsnummer",
           "Lieferant", "Warenlager", "Firma", "Benutzer"]

# WaWi-instanz-konstante Bestell-Header-Defaults (gleich für alle Lieferanten).
WARENLAGER_DEFAULT = "Standardlager_WMS"
FIRMA_DEFAULT = "Verticalo GmbH - Polesportshop"
BENUTZER_DEFAULT = "Tjorben Becker"


def load_menge(path) -> dict[tuple, int]:
    """(modell_basis, garment_type, farbe, groesse) -> Menge (int)."""
    m: dict[tuple, int] = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            menge = (r.get("menge") or "").strip()
            if menge:
                m[(r["modell_basis"], r["garment_type"], r["farbe"], r["groesse"])] = int(menge)
    return m


def artnr_map(vaeter: list[Vater]) -> dict[tuple, str]:
    """(modell_basis, garment_type, farbe, groesse) -> A-Nummer des Kindes.
    Setzt voraus, dass numbering.assign(...) vorher die A-Nummern vergeben hat."""
    return {(v.modell_basis, v.garment_type, v.farbe_raw, k.groesse): k.artikelnummer
            for v in vaeter for k in v.kinder}


def build_rows(menge_map: dict, artnr: dict, lieferdatum: str, referenz: str = "",
               lieferant: str = "", warenlager: str = WARENLAGER_DEFAULT,
               firma: str = FIRMA_DEFAULT, benutzer: str = BENUTZER_DEFAULT) -> list[dict]:
    """Pro bestellter (modell,typ,farbe,größe) eine Bestellzeile. Header-Felder (Lieferant/
    Warenlager/Firma/Benutzer) als Spalten → universelle Ameise-Vorlage."""
    rows: list[dict] = []
    for key, menge in menge_map.items():
        if not menge:
            continue
        a = artnr.get(key)
        if not a:
            continue
        rows.append({"Artikelnummer": a, "Menge": str(menge), "Lieferdatum": lieferdatum,
                     "Zugehörige Auftragsnummer": referenz, "Lieferant": lieferant,
                     "Warenlager": warenlager, "Firma": firma, "Benutzer": benutzer})
    rows.sort(key=lambda r: r["Artikelnummer"])
    return rows
