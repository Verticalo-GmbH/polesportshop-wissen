"""Schema-as-Code für die statischen, LLM-/hand-geschriebenen Artefakte
(Content-JSONs + Lieferanten-Mapping) — durchgesetzt an pre-commit + CI (§1 KERN
des LLM-Architektur-Standards, verticalo-ops).

Trennung ERRORS vs. WARNINGS:
- ERRORS (Exit 1, blockt Commit/CI): kaputte/ungültige Daten — malformte JSON/YAML,
  Merkmal-Farbe außerhalb der Whitelist, falsche Struktur.
- WARNINGS (Exit 0, nur Meldung): Vollständigkeits-Lücken (fehlende Übersetzungen etc.),
  die im laufenden Onboarding legitim sein können — der Orchestrator-Self-Check
  (STOPP-Liste) fängt sie vor dem echten Import ohnehin ab.

Aufruf:  python -m pipeline.validate
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from . import content as content_mod
from .spec import MERKMAL_FARBE_ERLAUBT

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = Path(__file__).resolve().parent / "content"
MAPPING = ROOT / "lieferanten_mapping.yaml"


def check_content(errors: list[str], warnings: list[str]) -> None:
    for f in sorted(CONTENT_DIR.glob("*_content.json")):
        rel = f.relative_to(ROOT)
        try:
            data = content_mod.load_content(f)
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: ungültiges JSON ({e})")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: Top-Level ist kein Objekt")
            continue
        # ERROR: Merkmal-Farbe außerhalb der Whitelist
        for vnr, c in data.items():
            if not isinstance(c, dict):
                errors.append(f"{rel}:{vnr}: Eintrag ist kein Objekt")
                continue
            farbe = c.get("merkmal_farbe")
            farben = farbe if isinstance(farbe, list) else ([farbe] if farbe else [])
            for fb in farben:
                if fb not in MERKMAL_FARBE_ERLAUBT:
                    errors.append(
                        f"{rel}:{vnr}: merkmal_farbe '{fb}' nicht in Whitelist "
                        f"(spec.MERKMAL_FARBE_ERLAUBT)")
        # WARNING: Vollständigkeit über die bestehende Logik
        for m in content_mod.validate(data, list(data.keys())):
            warnings.append(f"{rel}: {m}")


def check_mapping(errors: list[str], warnings: list[str]) -> None:
    if not MAPPING.exists():
        errors.append(f"{MAPPING.name}: fehlt")
        return
    try:
        import yaml
    except ImportError:
        errors.append("PyYAML nicht installiert (für Mapping-Validierung nötig)")
        return
    try:
        data = yaml.safe_load(MAPPING.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        errors.append(f"{MAPPING.name}: ungültiges YAML ({e})")
        return
    if not isinstance(data, dict) or not data:
        errors.append(f"{MAPPING.name}: kein (nicht-leeres) Objekt")
        return
    suppliers = data.get("lieferanten") if isinstance(data.get("lieferanten"), dict) else data
    if not suppliers:
        errors.append(f"{MAPPING.name}: keine Lieferanten-Einträge")
        return
    for key, sup in suppliers.items():
        if not isinstance(sup, dict):
            errors.append(f"{MAPPING.name}:{key}: Eintrag ist kein Objekt")
            continue
        if not (sup.get("hersteller") or sup.get("marke_kurz")):
            warnings.append(f"{MAPPING.name}:{key}: weder 'hersteller' noch 'marke_kurz' gesetzt "
                            f"(Markentext-H2 würde leer bleiben)")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    check_content(errors, warnings)
    check_mapping(errors, warnings)

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    print(f"\nvalidate: {len(errors)} Fehler, {len(warnings)} Warnungen.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
