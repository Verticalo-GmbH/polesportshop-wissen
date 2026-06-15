"""
Content-Schicht (Hybrid, P5): hält die in-Session generierten Werte, die nicht
deterministisch aus dem Crawl ableitbar sind — Merkmal-Farbe (für Modelle ohne
Farbnamen), Style-Werte, und die 3 per-Modell-Attributtexte
(artikeldetails / material_and_care / size_and_fit) in 5 Sprachen.

`markentext` wird NICHT hier gehalten — er ist die evergreen Brand-Story aus dem
Lieferanten-Mapping (E72/E79), für alle Modelle identisch.

Schema (JSON, gekeyt auf Vater-Artikelnummer):
{
  "HC-Hekate-Bodysuit": {
    "merkmal_farbe": "Schwarz",
    "style_werte": ["Bodysuit", "Rundausschnitt", "Open Back"],
    "attribute": {
      "artikeldetails":     {"de": "...","en": "...","fr": "...","it": "...","es": "..."},
      "material_and_care":  {"de": "...", ...},
      "size_and_fit":       {"de": "...", ...}
    }
  }
}
"""
from __future__ import annotations

import json
from pathlib import Path

from . import constants as C

PER_MODEL_ATTRS = ["artikeldetails", "material_and_care", "size_and_fit"]
ALL_ATTRS = ["markentext"] + PER_MODEL_ATTRS


def load_content(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def markentext_from_mapping(supplier: dict) -> dict[str, str]:
    """Evergreen Brand-Story (Mapping) -> markentext HTML pro Sprache."""
    marke = supplier["hersteller"]
    out = {}
    for lang in C.LANGUAGES:
        story = (supplier.get(f"brand_story_{lang}") or "").strip()
        story = " ".join(story.split())  # Mehrzeiler -> ein Absatz
        out[lang] = f"<h2>{marke}</h2><p>{story}</p>"
    return out


def validate(content: dict, vater_nummern: list[str]) -> list[str]:
    """Fehlende Content-Einträge melden (STOPP-Liste). Leer = vollständig."""
    missing = []
    for vnr in vater_nummern:
        c = content.get(vnr)
        if not c:
            missing.append(f"{vnr}: kein Content-Eintrag")
            continue
        if not c.get("merkmal_farbe"):
            missing.append(f"{vnr}: merkmal_farbe fehlt")
        if not c.get("style_werte"):
            missing.append(f"{vnr}: style_werte fehlen")
        for a in PER_MODEL_ATTRS:
            entry = c.get("attribute", {}).get(a, {})
            for lang in C.LANGUAGES:
                if not entry.get(lang):
                    missing.append(f"{vnr}: attribute.{a}.{lang} fehlt")
    return missing
