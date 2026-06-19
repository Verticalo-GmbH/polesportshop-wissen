# CLAUDE.md — Daily-Workflow für Wissens-Management

**Stand:** v1.24, 2026-06-18 (Konsolidierungs-Build: Wissensbasis verschlankt, Cowork-Docs deprecated gekennzeichnet, Backlog archiviert, Frontdoor auf Code-Stand). · **v1.22/v1.23:** Daten-Pipeline-Code-Pivot + Code-only-Refactor (`pipeline/`, `pipeline/README.md`). · **Seither E94–E98** (siehe unten).
**Zweck:** Cheatsheet für Tjorben + jede Claude-Code-Session, die das Repo `polesportshop-wissen` aufmacht. Beantwortet: Wie starte ich was, wie reviewe ich, wo finde ich was, wie commite ich kleine Edits.
**Auch von Claude Code automatisch gelesen:** Diese Datei liegt im Repo-Root und wird von Claude Code beim Session-Start als Projekt-Kontext aufgenommen. Daher kurz und bündig halten.

---

## Repo-Identität

- **Pfad:** `~/Documents/polesportshop-wissen/`
- **Remote:** `https://github.com/verticalogmbh/polesportshop-wissen` (public)
- **Branch:** `main` (kein Feature-Branch-Workflow)
- **Snapshots:** Git-Tags `vMAJOR.MINOR` (z.B. `v1.20`). Aktueller Stand siehe `git describe --tags --abbrev=0`.
- **Engine:** Claude Code lokal (Opus 4.7 / Sonnet je nach Aufgabe). Cowork (Browser-Engine) liest GitHub-Raw für Daten-Pipeline-Läufe — siehe `cowork_custom_instructions.md`.

## Daten-Pipeline als Code (NEU v1.22 — lokal in Claude Code)

**Großer Pivot 2026-06-15:** Die Artikelanlage-Pipeline läuft jetzt als **lokaler Python-Code im `pipeline/`-Package**, ausgeführt von Claude Code auf Tjorbens Mac — nicht mehr in Cowork. Cowork (Browser-Engine, liest die Markdown-Specs via GitHub-Raw) bleibt als **Fallback** bestehen, ist aber nicht mehr der Primärpfad. Das kippt Charter-Prinzip 2 (bewusst).

- **Bedienung / Setup / Run:** siehe **`pipeline/README.md`** (Runbook — clone, venv, EK + R2-Keys, `python -m pipeline.orchestrator [--images]`). Selbst-bootstrappend: neue Session/neuer Laptop braucht nur `git clone` + Runbook.
- **Erst-Lauf 2026-06-15:** HotCakes 21 Modelle (Rechnung #00034), 5 CSVs + Bilder auf R2, Self-Check 16/16, in WaWi importiert.
- **Code ist führend; Markdown-Specs = Referenz + Cowork-Fallback.** Bei Logik-Änderung: Code in `pipeline/` ändern + betroffene Spec synchron halten + commit/push.
- **Lernpunkte (in WaWi 1.11 verifiziert):** (1) Variationen-CSV braucht Spalten `Sortiernummer Variation`+`Sortiernummer Variationswert`, sonst sortiert JTL alphabetisch (L,M,S,XS) — und sie müssen in der Ameise-Vorlage gemappt sein. (2) `Bild 1`–`Bild 10` müssen in der Stammdaten-Vorlage gemappt sein. (3) Farbmerkmal qualitativ aus Kundensicht (dominante Such-Farbe, im Zweifel mehrere) statt `Bunt`-Listen.

### Was seit dem Pivot dazukam (E94–E101, 2026-06-17/18)
- **E94 — A-Nummern (Weg B):** Artikelnummer = `A`+laufende Nummer aus WaWi-Nummernkreis, Kinder `-001`… (Lager-Scan hängt an der ArtNr). Pipeline vergibt vorab via `numbering.py`, Zähler in `state/nummernkreis.json`. Sprechender Schlüssel lebt in `Artikelnummer (Lieferant)`.
- **E95 — EAN/GTIN-Spalte** (Schema 48→49, ans Ende): Barcodes pro Größe aus `content/ean_<x>.csv`, nur Kind-Ebene. Ameise: Spalte `EAN` → GTIN mappen.
- **E97 — Lieferanten-EK in Original-Währung** (AUD), GLD/VK in EUR; `lieferzeit_tage` im Mapping nur fürs **Lieferdatum der Bestellung** (`csv/bestellung.py`, Ameise-Typ „Lieferanten > Lieferantenbestellungen"); Lieferanten-EK über Stammdaten-Feld „Netto-EK" (Lieferanteneinstellungen) + Standardwert Lieferant + Währung.
- **E98 — Interim-Margen-Schutz** (bis GLD vollständig, B68): Nicht-EU **+5€ VK**, EU **+1€ EK**; **GLD +2,30€/Stück**; Lieferzeit aus Stammdaten raus. Erkennung EU/Nicht-EU über `waehrung`.
- **E99 — Lieferantenbestellung als fester 6. Output:** Orchestrator gibt `6_Lieferantenbestellung_…csv` mit aus, sobald `EK_input/menge_<x>.csv` da ist. Universelle Ameise-Vorlage (Header-Felder Lieferant/Warenlager/Firma/Benutzer als Spalten). Referenz pipe-getrennt + beschreibend im Feld „Zugehörige Auftragsnummer". Lieferdatum = Importdatum + `lieferzeit_tage`.
- **E100 — Bestell-Referenz (`<PREFIX>-<JAHR>-<NN>`, z.B. `LUN-2026-01`):** vorab vergeben, an Lieferant + auf Etikett, **führend** in jeder BE-Referenz (`Bestellung LUN-2026-01 | Rechnung #3124 | Diamante`). Matching beim Wareneingang; Indent-Orders (Artikel/BE erst bei Ware+EK). Records in `pipeline/orders/`. *(Nicht zu verwechseln mit der JTL-`BE…`-Nummer.)*
- **E101 — Shop-Qualität:** Variation `Darstellungsform = TEXTSWATCHES` (statt Dropdown); **Charm-VK** (keine runden Zehner, 40,90→39,90, `pricing.charm_vk`); `artikeldetails` beim Crawl mit verkaufsfördernden Infos anreichern (nach Ermessen, Stil E74/E78/E82).

### Pro-Lieferant-Slot-Pattern (Skalierung auf ~50 Lieferanten)
Neuer Lieferant = Dateien in festen Fächern, kein Kern-Bloat: `lieferanten_mapping.yaml` (1 Eintrag) · `pipeline/content/<x>_content.json` · `pipeline/content/ean_<x>.csv` (wenn Barcodes) · `pipeline/suppliers/<x>.py` (nur Nicht-Shopify) · `EK_input/ek_<x>.csv` + `menge_<x>.csv` (gitignored) · `orchestrator.SUPPLIERS`-Eintrag. Checkliste: `LIEFERANTEN-ONBOARDING.md`. Die großen Wissens-Docs wachsen mit neuen **Mechaniken**, nicht mit der Lieferanten-Zahl.

## File-Map (Orientierung)

| Frage / Bedarf | Datei |
|---|---|
| Verfassung, Prinzipien, Trade-offs | `PROJEKT-CHARTER.md` |
| Wie führe ich einen Wissens-Update-Build durch | `WISSENS-UPDATE-PLAYBOOK.md` |
| Wie führe ich Tjorben das Projekt | `Projekt-Anweisungen.md` |
| **Pipeline-Bedienung (Code, primär)** | **`pipeline/README.md`** |
| Cowork-Side — 🗄️ DEPRECATED v1.22, Fallback | `cowork_custom_instructions.md` |
| Cowork-Daten-Pipeline operative Spec — 🗄️ DEPRECATED v1.22 | `cowork_anweisung_datenimports.md` |
| Cowork-Run-Brief — 🗄️ DEPRECATED v1.22 | `run_brief_daten.md` |
| Cowork-Bildpipeline — 🗄️ DEPRECATED v1.22 | `cowork_anweisung_bildpipeline.md` |
| Onboarding neuer Lieferant | `LIEFERANTEN-ONBOARDING.md` |
| Lieferanten-Metadaten | `lieferanten_mapping.yaml` |
| WaWi-Pilot-Wissen (CSV-Stolperfallen, Vorlagen-Setup) | `WAWI-IMPORT-WISSEN.md` |
| Alle Konstanten (Schema, SEO, Sprach-Lookup, Self-Check, AP1-AP12, File-Index, E-Nummer-Index) | `SPEC_KONSTANTEN.md` |
| Architektur-Entscheidungen | `ENTSCHEIDUNGS-LOG-*.md` (6 Cluster + ARCHIV; Index in SPEC_KONSTANTEN Sektion 14) |
| Offene Punkte, Risiken, neue Findings | `BACKLOG.md` |
| Erledigte / deferred B-Einträge | `BACKLOG-ARCHIV.md` |
| Manifest des aktuellen Snapshots | `_MANIFEST.md` |

## Trigger-Registry

**Wissens-Update-Build** (im Claude-Code-Chat):
- „Verarbeite Wissens-Update für v1.X+1: <Scope>"
- „Baue Snapshot v1.X+1"
- „Wissens-Build v1.X+1"

→ Claude Code folgt `WISSENS-UPDATE-PLAYBOOK.md` v2.0 (7-Stage-Pattern, Git-basiert). Ende: `git push origin main --tags`.

**Daten-Pipeline-Lauf** (ab v1.22 **primär in Claude Code lokal**, Code in `pipeline/`):
- „Verarbeite neue Artikel von <LIEFERANT>: <Details>" + EK-Liste/Rechnung

→ Claude Code: EK-Liste in `pipeline/EK_input/` legen, `python -m pipeline.orchestrator [--images]` laufen, 5 CSVs + Lauf-Bericht in `pipeline/outputs/`, reviewen, in WaWi-Ameise importieren. Details: **`pipeline/README.md`**.
→ **Fallback Cowork:** lädt `run_brief_daten.md` + `SPEC_KONSTANTEN.md` + `lieferanten_mapping.yaml` aus dem jüngsten Git-Tag via GitHub-Raw und gibt 5 CSVs per `present_files` aus (nicht mehr Primärpfad).

**Lieferanten-Onboarding** (im Claude-Code-Chat für Mapping/Brand-Story, dann Cowork für Probe-Lauf):
- „Onboarde Lieferant <NAME>"

→ Claude Code folgt `LIEFERANTEN-ONBOARDING.md`. Ergebnis: erweitertes `lieferanten_mapping.yaml`, ggf. neue Brand-Stories, dann minimaler Commit oder Sammel-Commit. Anschließend Probe-Lauf in Cowork.

**Bildpipeline** (REAKTIVIERT v1.21, E93):
- Läuft als Sub-Process aus dem Daten-Pipeline-Lauf (Stage 5.6 + 5.7 in `cowork_anweisung_datenimports.md` v2.1). R2-URLs landen direkt in den Stammdaten-CSV-Spalten Bild 1-10.
- Standalone-Trigger: „Verarbeite Bilder von <LIEFERANT>" — Cowork lädt `cowork_anweisung_bildpipeline.md` v2.1, Output Map `{artikelnummer: [bild_urls]}`.

## Daily-Ops für Tjorben (Quick-Reference)

### Stand schnell sehen
```bash
git -C ~/Documents/polesportshop-wissen describe --tags --abbrev=0   # aktueller Tag
git -C ~/Documents/polesportshop-wissen log --oneline -5             # letzte Commits
git -C ~/Documents/polesportshop-wissen status                       # untracked / modified
```

### Kleinen manuellen Edit machen (z.B. Typo, Cross-Reference-Update)
1. Datei direkt editieren (Editor deiner Wahl oder Claude Code).
2. `git -C ~/Documents/polesportshop-wissen status` — was wurde geändert.
3. `git -C ~/Documents/polesportshop-wissen add <datei>` — gezielt staging.
4. `git -C ~/Documents/polesportshop-wissen commit -m "<Kurz-Begründung>"` — kein Tag-Bump für Mini-Edit.
5. `git -C ~/Documents/polesportshop-wissen push` — nicht `--tags`, weil kein neuer Tag.

Der nächste reguläre Wissens-Update-Build zieht die Edits ein.

### Wissens-Update-Build starten

Im Claude-Code-Chat im Repo:
```
Verarbeite Wissens-Update für v1.X+1: <kompakter Scope-Vorschlag, was rein soll>
```

Claude Code antwortet mit kompaktem Plan, fährt dann autonom durch alle 7 Stages, am Ende: Commit, Tag, Push, Abschluss-Bericht. Bei strategischen Wahlpunkten autonom entschieden, im Bericht gelistet (siehe `WISSENS-UPDATE-PLAYBOOK.md` Sektion 10).

### Daten-Pipeline-Lauf reviewen

Cowork gibt nach Lauf via `present_files` 5 CSVs + Lauf-Bericht aus:
1. Lauf-Bericht öffnen — Stage 0.5 Scope, Self-Check 16 Punkte, autonome Entscheidungen, ggf. Eigeninterpretations-Marker (E70).
2. Falls Self-Check 16/16 grün: CSVs im WaWi-Ameise importieren in Reihenfolge `_1_Stammdaten`, `_2_Variationen`, `_3_Merkmale`, `_4_Attribute`, `_5_CrossSelling`.
3. Im Shop-Review: Artikel anschauen, Sara reviewt + entfernt 546-Zuweisung (E89-Workflow).
4. Bei Findings: in den nächsten Wissens-Update-Build mitnehmen oder via Daily-Edit reparieren.

### Memory aktualisieren (Claude-Code-spezifisch)

Memory-Dir: `/Users/tjorbenbecker/.claude/projects/-Users-tjorbenbecker-Documents-polesportshop-wissen/memory/`

Nach größeren Builds: `project_status_v1_X.md` updaten, `MEMORY.md`-Index pflegen. Macht Claude Code in der Regel selbst, wenn der Build durch ist.

## Naming-Konventionen (Wichtig)

- **Tag:** `vMAJOR.MINOR`, z.B. `v1.20`. Patch-Tag `v1.20.1` nur für Hotfix zwischen regulären Snapshots.
- **Commit-Message bei Wissens-Update-Build:** `vX.Y — <Kurz-Beschreibung>` plus Body mit Strang-Übersicht. HEREDOC für Mehrzeiler. Co-Authored-By-Footer.
- **File-Header-Bumps (E86):** Patch v1.15 → v1.15.1 (Cross-Reference-Update), Minor v1.15 → v1.16 (Inhalts-Update), Major v1.X → v2.0 (struktureller Umbau). Edge-Case: nur mitgenommen ohne Edit = kein Bump.
- **CSV-Files (Cowork-Output):** `<NR>_<Typ>_<LIEFERANT>_<YYYY-MM-DD_HHMM>.csv` (AP11).

## Charter-Prinzipien (12 Stück, kurz)

Volle Liste in `PROJEKT-CHARTER.md`. Kurzform für Daily-Reference:
1. Mensch initiiert, Maschine arbeitet
2. Claude.ai plant, Cowork produziert *(seit v1.19: Claude Code statt Claude.ai)*
3. Cowork schreibt nichts in WaWi
4. Lineare Pipeline ohne User-Gate
5. Multi-Input statt erzwungener Standard
6. Deutsch ist Master
7. Pipeline-Output ist normalisiert
8. Pipeline-Kalkulation ist tabellengestützt
9. Klein nach groß, modular wachsen
10. Mapping-Bibel mit Konsultations-Pflicht
11. Konstanten-Datei-Architektur (SPEC_KONSTANTEN)
12. File-Header-Versionierungs-Disziplin (E86)

## Was Claude Code in diesem Repo NIE tut

- `git push --force` auf `main`
- `git rebase -i` (interaktiv, nicht supported)
- `--no-verify`, `--no-gpg-sign`
- Git-Config ändern
- `lieferanten_mapping.yaml` ohne explizite Tjorben-Bestätigung schreiben
- Drive-Schreibzugriffe (Drive ist Read-Only-Archiv seit v1.19, E87)
- API-Keys/Credentials annehmen oder ausgeben

## Häufige Sessions

| Session | Trigger | Dauer (grob) |
|---|---|---|
| Klärungs-Chat (Architektur-Frage) | „Warum machen wir X so?" | 5-10 Min |
| Daily-Edit | „Fix Typo in <Datei>" | 2-5 Min |
| Kleiner Wissens-Update-Build (1-2 Files) | „Wissens-Update v1.X+1: nur F-Fix Y" | 10-20 Min |
| Großer Wissens-Update-Build (Refactor) | „Wissens-Update v1.X+1: Refactor <Scope>" | 30-90 Min (mehrere Cycles möglich) |
| Lieferanten-Onboarding | „Onboarde <Lieferant>" | 15-30 Min für Mapping + Brand-Story |

## Bei Problemen

- **Git in komischem Zustand:** `git status` zeigt alles. Bei Conflict: niemals destruktiv handeln, erst nachfragen.
- **GitHub-Push abgelehnt:** Pull mit Rebase oder Merge, dann Push. Bei Force-Push-Wunsch: zuerst nachfragen.
- **Cowork sieht den neuen Tag nicht:** Cowork-Session neu starten (Stage 0 Resolution holt dann den neuen Tag).
- **Claude Code findet `SPEC_KONSTANTEN.md` nicht:** falsches Verzeichnis. `pwd` checken.

## Memory-System

Claude Code hat ein persistentes Memory-System unter `/Users/tjorbenbecker/.claude/projects/-Users-tjorbenbecker-Documents-polesportshop-wissen/memory/`. Dort liegen:
- `repo_setup.md` — Repo-Pfad, Remote, Tag-Konvention
- `user_role.md` — Tjorbens Rolle, Präferenzen
- `feedback_build_style.md` — autonomer Build-Stil
- `project_engines.md` — Claude Code vs. Cowork
- `project_status_v1_X.md` — aktueller Projekt-Stand

Werden automatisch in jeden Claude-Code-Chat geladen. Bei Bedarf aktualisieren.
