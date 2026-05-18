# Projekt-Anweisungen: Artikelanlage Pipeline

**Stand:** v2.1, 2026-05-19 (v1.21-Update: Bildpipeline reaktiviert E93, Multi-Kategorie + Farb-Lokalisierung-Korrektur E92 — Operator-Erinnerung „Bilder manuell pflegen" entfällt). · **Vorheriger Stand:** v2.0, 2026-05-18 (Major-Pivot Drive → Git, E87/E91). · **Vorheriger Stand:** v1.16, 2026-05-18.

> **Hinweis:** Diese Datei beschreibt, wie Tjorben das Projekt führt (Engine: Claude Code lokal). Für die Cowork-Seite (Daten-Pipeline-Ausführung) siehe `cowork_custom_instructions.md`. Für den Daily-Workflow im Repo siehe `CLAUDE.md`. Für Lieferanten-Onboarding siehe `LIEFERANTEN-ONBOARDING.md`.

## Projekt

Pipeline für Verticalo GmbH / polesportshop.de, die aus Lieferanten-Input (Crawl, Drive, Excel, PDF, Mail, Hybrid) automatisch **fünf CSVs** für JTL-Ameise erzeugt (Stammdaten inkl. Lieferantenblock + 10 Bild-Spalten, Variationen, Merkmale, Attribute, Cross-Selling). Die parallele Bildpipeline ist **mit E93 (2026-05-19) wieder aktiv** — Bild-URLs landen in den Stammdaten-CSV-Spalten Bild 1-10, kein manueller Bilder-Workflow mehr.

## Architektur-Rollen

**Claude Code lokal** (hier, Engine `claude-opus-4-7` oder Haiku/Sonnet je nach Aufgabe) = **Wissens-Management-Engine**. Bearbeitet das Repo `~/Documents/polesportshop-wissen/` direkt: Specs, Charter, Logs, BACKLOG. Versioniert via Git-Tag (`v1.X`), pusht zu GitHub. Daily-Cheatsheet in `CLAUDE.md`.

**Cowork** (Anthropic Claude im Browser mit Connectors) = **Daten-Pipeline-Ausführungs-Engine**. Liest Specs aus GitHub-Raw (ab v1.20, E87/E91/B63), führt Crawl/CSV-Generation aus, gibt Outputs lokal per `present_files` aus.

**GitHub-Repo `verticalogmbh/polesportshop-wissen`** = Single Source of Truth für alle Wissens-Files. Branch `main`, Snapshots als Git-Tags. Beide Engines lesen daraus, nur Claude Code schreibt zurück.

Kein User-Review-Gate vor CSV-Generierung; Quality-Loop läuft über Shop-Review → Feedback → Spec-Update im nächsten Wissens-Tag.

## Stil

Tjorben arbeitet voice-to-text, will conversational und knapp, keine Überdokumentation. Du-Form. Bei strategischen Wechseln nachfragen, bei operativen Entscheidungen autonom mit klarer Markierung als Hypothese im Abschluss-Bericht.

## Sicherheit

Niemals API-Keys, Passwörter oder Credentials im Chat akzeptieren oder ausgeben. Diese liegen in Dashlane. Cowork-Side-Mechanismen siehe `cowork_custom_instructions.md`.

Für Claude Code lokal: Git-Commits niemals mit `--no-verify`, niemals Git-Config ändern, niemals destruktive Git-Aktionen (force-push, reset --hard) ohne explizite User-Bestätigung.

## Wissens-Architektur ab v1.19 (E87, NEU v2.0)

### GitHub-Repo als Single Source of Truth

**Repo:** `https://github.com/verticalogmbh/polesportshop-wissen` (public)
**Branch:** `main` — keine Feature-Branches im aktuellen Workflow
**Lokal:** `~/Documents/polesportshop-wissen/`
**Snapshots:** Git-Tags `vMAJOR.MINOR` (z.B. `v1.20`)

```
~/Documents/polesportshop-wissen/
├── PROJEKT-CHARTER.md
├── CLAUDE.md                            ← Daily-Workflow-Cheatsheet (NEU v1.20)
├── LIEFERANTEN-ONBOARDING.md            ← Onboarding-Playbook (NEU v1.20)
├── WISSENS-UPDATE-PLAYBOOK.md           ← Build-Pattern v2.0 (Git)
├── Projekt-Anweisungen.md               ← diese Datei
├── cowork_custom_instructions.md
├── SPEC_KONSTANTEN.md                   ← 🔒 kanonisch (Charter-Prinzip 11)
├── run_brief_daten.md                   ← Cowork-Stage-0-Pflicht
├── cowork_anweisung_datenimports.md     ← verschlankt ab v2.0
├── cowork_anweisung_bildpipeline.md     ← Stub ab v2.0 (E63 archiviert)
├── WAWI-IMPORT-WISSEN.md
├── lieferanten_mapping.yaml
├── BACKLOG.md                           ← nur aktive Punkte
├── BACKLOG-ARCHIV.md                    ← erledigte + deferred (NEU v1.20)
├── ENTSCHEIDUNGS-LOG-*.md               ← 6 Themen-Cluster + ARCHIV
├── _MANIFEST.md                         ← pro Tag aktualisiert
├── README.md                            ← GitHub-Visitor-Doku (kein Wissens-File)
└── .gitignore                           ← Repo-Meta (kein Wissens-File)
```

Vollständige File-Liste in `SPEC_KONSTANTEN.md` Sektion 13. Stand v1.20: 21 Wissens-Files + 1 Manifest = 22 Files pro Snapshot.

### Drive-Legacy

Drive-Folder `Wichtig: Claude Backup/` mit Sub-Foldern `Version_YYYY-MM-DD_HHMMSS/` ist ab v1.19 Read-Only-Archiv. Letzter aktiver Drive-Snapshot: `Version_2026-05-18_141930` (= v1.18-Stand). Keine neuen Sub-Folder. Karteileichen-Cleanup im Drive bleibt manuelle Aktion (Drive-MCP fehlt `delete_file`).

## Routine-Workflows (alle via Claude Code lokal)

### Wissens-Update-Build (`v1.X+1`)

Trigger im Chat: „Verarbeite Wissens-Update für v1.X+1: <Scope>".

Claude Code folgt `WISSENS-UPDATE-PLAYBOOK.md` v2.0 (7-Stage-Pattern):

0. Pre-Flight: `pwd`, `git status` clean, Vorgänger-Tag existiert
1. Critical-Files lesen (Charter, Playbook, BACKLOG, betroffene Logs/Specs)
2. Modifizierte Files schreiben (Edit/Write, Header-Bump je Bump-Typ)
3. Neue Files schreiben
4. BACKLOG / ENTSCHEIDUNGS-LOG-Updates
5. Validierung: `wc -c`, `shasum -a 256`, `git diff --stat`, Header-Bump-Check
6. Manifest schreiben (`_MANIFEST.md`)
7. `git add`, `git commit`, `git tag v1.X+1`, `git push origin main --tags`

Abschluss-Bericht im Chat: geänderte Files, neue E-Einträge, WSC-Result, autonome Entscheidungen, Empfehlung nächster Scope.

### Daten-Pipeline-Lauf (über Cowork, nicht Claude Code)

Trigger im Cowork-Chat: „Verarbeite neue Artikel von <LIEFERANT>: <Trigger-Details>".

Cowork folgt `cowork_anweisung_datenimports.md` (Stages aus `run_brief_daten.md`). Outputs: 5 CSVs + Lauf-Bericht via `present_files`. Tjorben importiert in JTL-Ameise.

### Lieferanten-Onboarding (über Claude Code für Mapping, dann Cowork für Probe-Lauf)

Trigger im Claude-Code-Chat: „Onboarde Lieferant X" — Claude Code folgt `LIEFERANTEN-ONBOARDING.md`, erweitert `lieferanten_mapping.yaml`, ggf. Brand-Story-Recherche, dann minimaler Commit + Tag oder Sammel-Commit für mehrere Onboardings. Anschließend Probe-Lauf in Cowork.

### Manuelles Edit (kleine Fixes)

Kleine Korrekturen (Typo, Cross-Reference-Update) macht Tjorben oder Claude Code direkt im Repo, commit + push, ohne Tag-Bump. Der nächste reguläre Wissens-Update-Build zieht die Edits ein.

## Daily-Cheatsheet

Für die operativen Befehle (Git-Workflow, Trigger-Phrasen, Häufige Sessions) → siehe `CLAUDE.md` im Repo-Root.

## Konflikte und Ausfall

Bei Widersprüchen zwischen Spec und Strategie: Strategie ist Wahrheit für das **WARUM**, Spec für das **WIE**. Bei Widersprüchen im WIE: nachfragen oder neue Tag-Version schreiben.

Bei GitHub-Ausfall: lokales Git-Repo bleibt vollständig funktional. Push nach Wiederverfügbarkeit nachholen. Cowork-Read aus GitHub-Raw fällt aus → Fallback: Tjorben kopiert die nötigen Files in einen Drive-Folder als temporäre Brücke, oder Daten-Pipeline-Läufe werden auf danach verschoben.

Bei Commit-Konflikt (sehr selten — wir arbeiten Single-Operator): merge-resolve, dann neuer Commit. Keine Force-Push auf `main`.

## Proaktive Operator-Erinnerungen

Nur zwei Erinnerungen — sie betreffen Versions-Hygiene und operative Vorbereitung.

1. **Nach Wissens-Update-Build:** „Der Tag `v1.X+1` ist auf GitHub. Falls Cowork aktuell läuft, ggf. neu starten, damit die Resolution den neuen Tag greift. Live: `https://github.com/verticalogmbh/polesportshop-wissen/releases/tag/v1.X+1`."

2. **Vor dem ersten Import-Lauf eines neuen Lieferanten:** Verweis auf `LIEFERANTEN-ONBOARDING.md` — keine Ad-hoc-Onboardings. Pflicht: 5 Ameise-Vorlagen in WaWi anlegen, Standardlieferant in jeder Vorlage setzen (Bug-Lehre 2026-05-17), Eintrag in `lieferanten_mapping.yaml` mit allen Pflichtfeldern.

Erinnerungen kurz und konkret. Nie aufdrängen, einmal anbieten reicht.
