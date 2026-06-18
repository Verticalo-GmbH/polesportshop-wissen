# Snapshot-Manifest

**Snapshot-Tag:** `v1.24` (Konsolidierungs-Build — Wissensbasis verschlankt, Code-Pipeline-Stand)
**Stand:** 2026-06-18 (Berlin) · **Vorgänger:** `v1.23` (Code-only-Refactor: Charter-Pivot + Cowork deprecated) · `v1.22` (Daten-Pipeline-Code-Pivot) · E94–E98 als Daily-Commits dazwischen
**Engine:** Claude Code lokal (Opus 4.8) · **Repo:** `https://github.com/verticalogmbh/polesportshop-wissen` · **Branch:** `main`

> **Lean-Hinweis (v1.23):** Dieses Manifest ist bewusst schlank. Datei-Integrität/Historie liefert **git** (kein SHA256-Block mehr), die E-Nummern der `SPEC_KONSTANTEN.md`-Index, offene Punkte der `BACKLOG.md`. Pro Snapshot nur noch: Build-Trail + Architektur-Stand + Slot-Pattern.

---

## 1. Was dieser Build gemacht hat (Konsolidierung)

Ziel: schlank + agil bleiben für die kommenden ~50 Lieferanten. Sicherheit vor Risiko — **archiviert/gekennzeichnet statt gelöscht.**
- **Cowork-Docs als Cold-Storage gekennzeichnet** (`cowork_anweisung_datenimports.md`, `cowork_anweisung_bildpipeline.md`, `cowork_custom_instructions.md`, `run_brief_daten.md`): deprecated seit v1.22-Code-Pivot, Deprecation-Kopf ergänzt. **Nicht verschoben** (in ~15 Files querverlinkt → Verschieben bräche Referenzen). Voller Inhalt bleibt + via git-Tag `v1.21`.
- **Backlog konsolidiert:** gelöste B-Einträge → `BACKLOG-ARCHIV.md`, aktiver Backlog zeigt nur Offenes.
- **Frontdoor-Sync:** `CLAUDE.md` + dieses Manifest auf Code-Stand (Module, E94–E98, Lieferanten-Slot-Pattern).
- **`LIEFERANTEN-ONBOARDING.md`** auf Code-Pipeline + Datei-Slot-Pattern aktualisiert (Onboarding #6–#50 mechanisch).
- **Decision-Logs unangetastet** (append-only Historie).

## 2. Architektur-Stand (v1.23)

**Ausführung = lokaler Python-Code (`pipeline/`), Engine Claude Code.** Cowork = Fallback (deprecated). Pipeline pro Lieferanten-Lauf: Crawl/Builder → Pricing → A-Nummern (Weg B) → EAN → Content → Bilder/R2 → 5 CSVs + optional Bestellung → Self-Check 16/16.

Code-Module (`pipeline/`): `orchestrator`, `config`, `constants`, `spec`, `numbering` (A-Nummern E94), `barcodes` (EAN E95), `pricing` (fx + Margen-Aufschlag E97/E98), `extract`, `model`, `selfcheck`, `crawl/`, `images/`, `csv/` (stammdaten, variationen, merkmale, attribute, crossselling, bestellung). State: `state/nummernkreis.json`. Referenzen: `content/<x>_content.json`, `content/ean_<x>.csv`.

Produktiv (4 Lieferanten): HotCakes (Shopify/EUR), Rolling (VNDA-Browser/USD), Lunalae Diamante + Odessa (Shopify/AUD). A-Nummern-Bereich `A1009262`–`A1009302`, nächste frei laut `state/nummernkreis.json`.

## 3. Pro-Lieferant-Slot-Pattern (Skalierungs-Rückgrat)

Ein neuer Lieferant = Dateien in festen Fächern, kein Kern-Bloat:

| Slot | Datei | Pflicht? |
|---|---|---|
| Mapping/Config + Brand-Story | `lieferanten_mapping.yaml` (1 Eintrag) | ja |
| Content (Merkmale/Attribute, 5 Sprachen) | `pipeline/content/<kuerzel>_content.json` | ja |
| Barcodes (UTC/EAN pro Größe) | `pipeline/content/ean_<kuerzel>.csv` | nur wenn vorhanden (E95) |
| Crawl-Builder (Nicht-Shopify) | `pipeline/suppliers/<kuerzel>.py` | nur Nicht-Shopify |
| EK + Bestell-Mengen (Rechnung) | `EK_input/ek_<x>.csv`, `menge_<x>.csv` (gitignored) | pro Lauf |
| Registry-Eintrag | `orchestrator.SUPPLIERS` | ja |

Detail-Checkliste: `LIEFERANTEN-ONBOARDING.md`.

## 4. Self-Check (Build)

- Pipeline-Self-Check je Lieferant 16/16 (Lunalae/Rolling/HotCakes nach E94–E98 verifiziert).
- Wissensbasis: Frontdoor (CLAUDE.md/_MANIFEST) deckt sich mit `pipeline/`-Stand; E-Index SPEC enthält E94–E98; Cowork-Docs als deprecated gekennzeichnet; Decision-Logs unverändert.
- Git: clean nach Commit; Tag `v1.23`; Push verifiziert.

## 5. Offen / nächste Schritte

- WaWi-Import-Verifikation der Lunalae/Rolling-Neu-Sets (EK-AUD am Lieferanten, GLD +2,30, Bestellung mit Lieferdatum) steht aus.
- B68: GLD/VK-Kosten pro Lieferant aus historischen Mittelwerten (löst die Interim-Aufschläge E98 ab).
- Größen-Wächter Docs (`WAWI-IMPORT-WISSEN.md` 76 KB, `BACKLOG.md`, `SPEC_KONSTANTEN.md`): in Git-Welt kein Blocker, bei Bedarf später Cluster-Split.
