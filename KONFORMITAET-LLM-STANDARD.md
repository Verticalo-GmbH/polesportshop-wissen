# Konformität — LLM-Architektur-Standard

Abgleich von `polesportshop-wissen` gegen `verticalo-ops/standards/llm-architektur-prinzipien.md` (§9-Konformitäts-Review). Stand: 2026-07-01. Grundsatz: nur **getriggerte** Lücken schließen, premature = Anti-Pattern.

## Status je Prinzip
| # | Prinzip | Status |
|---|---|---|
| 1 | Fundament (Git-SSOT, HITL, det. Tools, Validierungs-Grenze, DECISIONS) | 🟡 **teilweise** — alles da, aber Validierung nur runtime |
| 2 | Dünnes Frontend / schwere Cloud | ✅ erfüllt |
| 3 | Retrieval (Keyword/Kärtchen) | ⚪️ premature (key-basierte YAML/JSON, ~10 Lieferanten) |
| 4 | Evaluation | 🟡 nur Stufe 1 (Error-Analysis de facto; Golden-Set fehlt) |
| 5 | Observability | ⚪️ premature (kein Volumen, kein Auto-Versand) |
| 6 | Governance/Dedup | ⚪️ premature (Ledger überschaubar, Git-Audit reicht) |
| 7 | Anti-Patterns vermieden | ✅ erfüllt |
| 8 | Reifegrad-Reihenfolge | ✅ erfüllt |

## Fällige Lücken (priorisiert)
- **P1 — `pipeline/validate.py` (Schema-as-Code für statische Artefakte).** Validierung der LLM-geschriebenen Artefakte (`content/*.json` vollständig, Merkmal-Werte ∈ `spec`-Whitelists, `lieferanten_mapping.yaml` parst + Pflichtfelder). Exit≠0 bei ERRORS. *(KERN §1)*
- **P2 — GitHub-Actions-CI** (`.github/workflows/validate.yml`): ruft `validate.py` bei jedem Push. Fängt Direkt-/Bridge-Commits, die lokale Hooks umgehen. *(§1b)*
- **P3 — Pre-commit-Hook** auf `validate.py` (schnelles lokales Feedback). *(§1a)*
- **P4 — Golden-Set** der Content-Generierung (klein starten, vor Prompt-/Modell-Wechsel). *(§4 — Kür, Backlog)*

## Bewusst premature (NICHT bauen)
Vektor-DB/Embeddings/Hybrid-Retrieval (§3) · LLM-Judge + Eval-CI (§4 spätere Stufen) · Observability/Token-Kosten-Logging (§5) · semantische Dedup-Erkennung (§6) · Server-Alert/Server-Hygiene §1c (kein autonomer Dienst — n/a).

## Umsetzung (Stand 2026-07-01)
- ✅ **P1** — `pipeline/validate.py` (Schema-as-Code über `content/*.json` + `lieferanten_mapping.yaml`, nutzt bestehende `content.validate` + `spec`-Whitelist). Trennt ERRORS (blocken: malformte JSON/YAML, Farbe außerhalb Whitelist, Struktur) von WARNINGS (Vollständigkeit). Aktuell: **0 Fehler, 3 Warnungen**.
- ✅ **P2** — `.github/workflows/validate.yml`: CI ruft `python -m pipeline.validate` bei jedem Push/PR (§1b).
- ✅ **P3** — `.pre-commit-config.yaml`: lokaler Hook (§1a). Einmal aktivieren: `pip install pre-commit && pre-commit install`.
- ⏳ **P4** — Golden-Set: bleibt Backlog (Kür).

**Nebenbefund (WARNING, bitte fixen):** `POLE_JUNKIE` im Mapping hat weder `hersteller` noch `marke_kurz` → der Markentext-H2 würde bei einem Lauf leer bleiben. Beim nächsten Pole-Junkie-Onboarding den Markennamen nachtragen (siehe Prinzip „Markentext nie erfinden, immer erfragen").
