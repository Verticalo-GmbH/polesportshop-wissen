# Wissens-Update-Playbook

**Stand:** v2.0, 2026-05-18 (Berlin)
**Zweck:** Operative Spec für Claude-Code-getriebene Wissens-Update-Builds im Git-Repo `polesportshop-wissen`. Wird bei Trigger „Verarbeite Wissens-Update für v<NEW>..." gelesen und als Wie-Vorgabe befolgt.
**Bezug:** Charter-Prinzip 12 (File-Header-Versionierungs-Disziplin), E85 (Build-Pattern als Standard), E86 (SemVer-Konvention), **E87 (Migration Drive → Git als Wissens-Backbone, NEU v1.19)**.
**Pattern-Pivot:** v2.0 ersetzt das Drive-Snapshot-Pattern (v1.0–v1.18) durch Git-Tags. Single Source of Truth ist das lokale Git-Repo, jeder Build endet mit `git commit`, `git tag v<NEW>`, `git push origin main --tags`. Drive-Build-Pattern bleibt als Legacy-Anhang dokumentiert (Sektion 11).

---

## 1. Trigger-Erkennung

Trigger-Phrasen die diesen Playbook aktivieren:
- „Verarbeite Wissens-Update für v<NEW>..."
- „Baue Snapshot v<NEW>..."
- „Wissens-Build v<NEW>..."

Bei diesen Triggern: lese diesen Playbook + den Auftrag aus dem Chat. Der Auftrag definiert den **Scope** (welche Files modifiziert, welche neu, welche unverändert). Der Playbook definiert das **Wie**.

Bei Daten-Pipeline-Triggern („Verarbeite neue Artikel von X...") lädt Cowork stattdessen `run_brief_daten.md` (E68).

---

## 2. Architektur (v2.0)

### 2.1 Single Source of Truth

- **Lokales Git-Repo:** `~/Documents/polesportshop-wissen/` (Branch `main`)
- **Remote:** `https://github.com/verticalogmbh/polesportshop-wissen`
- **Snapshots:** Git-Tags `v1.19`, `v1.20`, ... (kein `v` im Vorgänger? siehe `git tag --list` für aktuelle Konvention; Standard ist `vX.Y`)
- **Snapshot-Inhalt:** alle Wissens-Files (Markdown + YAML) im Repo-Root plus `_MANIFEST.md`. Kein Sub-Folder-Pattern mehr.

### 2.2 Build-Engine

- **Claude Code** (lokale CLI, Opus 4.7 oder Sonnet) öffnet das Repo, liest, modifiziert, committet, taggt, pusht.
- **Tjorben** triggert im Chat, reviewt am Ende, kann zwischendurch eingreifen.
- **Cowork** liest den Snapshot beim nächsten Pipeline-Lauf — entweder über lokales Clone (zukünftig) oder über GitHub-Raw-URL-Resolution (v1.20-Scope, B63).

### 2.3 Resolution für Cowork (v1.20-Scope)

Geplant: `https://raw.githubusercontent.com/verticalogmbh/polesportshop-wissen/<tag>/<file>`
- Tag-pinning ersetzt das Drive-Folder-Resolution-Pattern.
- Cowork-`cowork_custom_instructions.md` und `Projekt-Anweisungen.md` werden in v1.20 entsprechend angepasst.
- Bis dahin (v1.19): Cowork läuft weiter mit dem letzten gültigen Drive-Snapshot `Version_2026-05-18_141930`. Git-Snapshot v1.19 ist parallel verfügbar für lokale Klärungs-Chats und Claude-Code-Sessions.

---

## 3. 7-Stage-Build-Pattern (v2.0)

Stage-Reihenfolge linear. Jede Stage hat einen klaren Output, der von der nächsten Stage konsumiert wird. Konsolidiert von vormals 12 Stages — Snapshot-Resolution + Workspace-Vorbereitung entfallen, weil das Git-Repo bereits die kanonische Arbeitsfläche ist.

| Stage | Was | Output |
|---|---|---|
| 0 | Pre-Flight: `pwd`, `git status` clean, Repo-Files vorhanden, Vorgänger-Tag existiert | OK-Bestätigung |
| 1 | Critical-Files lesen (Charter, Playbook, BACKLOG, betroffene Logs, betroffene Specs) | mentaler Stand |
| 2 | Modifizierte Files schreiben (Edit/Write, mit Header-Bump je nach Bump-Typ) | modifizierte Files im Working Tree |
| 3 | Neue Files schreiben (Write) | neue Files im Working Tree |
| 4 | BACKLOG / ENTSCHEIDUNGS-LOG-Updates schreiben (E-Einträge, B-Status) | aktualisierte Cluster-Files |
| 5 | Validierung: `wc -c`, `shasum -a 256`, `git diff --stat`, Header-Bump-Check | `selfcheck`-Resultate |
| 6 | Manifest schreiben (SHA256-Liste, WSC-Self-Check, Change-Summary) | aktualisierte `_MANIFEST.md` |
| 7 | `git add`, `git commit`, `git tag v<NEW>`, `git push origin main --tags`, Verify | Tag auf GitHub erreichbar |

---

## 4. Tool-Patterns (Claude Code)

### 4.1 Edit für kleine Patches, Write für Rewrites

- **<30 % geändert:** `Edit` mit präzisem `old_string`/`new_string`. Reduziert Diff-Lärm.
- **>50 % oder strukturell:** `Write` mit Komplett-Inhalt. Header explizit setzen (Bump-Typ Major/Minor).
- **0 % geändert:** nicht anfassen, kein Header-Bump.

### 4.2 Parallele Reads, sequenzielle Writes

- Critical-Files-Reads in Stage 1 parallel (mehrere `Read`-Calls in einem Message-Block).
- Writes sequenziell, weil Reihenfolge meist semantisch wichtig ist (z.B. Cluster-File vor Cross-Reference).

### 4.3 Validierung via Bash

- `wc -c *.md *.yaml | sort -n` — Größen-Übersicht für WSC-1/8
- `shasum -a 256 *.md *.yaml` — SHA256 für Manifest
- `grep -c "^# " *.md` — Header-Anzahl-Check für sanity
- `git diff --stat` — Welche Files modifiziert
- `git diff <last-tag>..HEAD -- <file>` — Was hat sich seit Vorgänger geändert (für Header-Bump-Entscheidung)

### 4.4 Tag-Konvention

- Format: `v<MAJOR>.<MINOR>` für reguläre Snapshots (`v1.19`, `v1.20`, `v2.0` bei strukturellem Pivot).
- Patch-Releases (`v1.19.1`) nur bei Hotfix zwischen regulären Snapshots, sonst sammeln im nächsten Minor.
- Tag annotiert nicht (lightweight tag reicht für Snapshot-Marker). Bei Bedarf annotiert mit `-a -m "Snapshot v1.19"` für Release-Notes.

---

## 5. Anti-Patterns (lessons learned, vermeiden)

- **Push ohne Tag:** `git push origin main` ohne `--tags` macht den Snapshot nicht referenzierbar. Immer `--tags` mit-pushen.
- **Tag vor Commit:** `git tag` auf nicht committetem Stand zeigt auf falschen Hash. Reihenfolge ist immer `commit` → `tag` → `push --tags`.
- **Header-Bump-Vergessen:** Modifiziertes File mit unverändertem `**Stand:** v1.X`-Header. Verifikation via WSC-17 (Stage 5).
- **`git add .` ohne Check:** Kann unbeabsichtigt Dateien einbeziehen (z.B. `.claude/`-Worktree-State, `_PIPELINE/`-Logs). `.gitignore` pflegen + `git status` vor `add` prüfen.
- **Force-Push auf main:** verboten. Bei Fehler: neuen Commit mit Korrektur + neuen Tag (`v1.19.1`).
- **Pushing während laufender Cowork-Session:** Cowork resolved beim Lauf-Start einmal — ein Mid-Run-Snapshot-Wechsel würde Drift erzeugen. Pushes wenn keine Cowork-Pipeline läuft, oder Cowork-Lauf bewusst danach starten.

---

## 6. Versionierungs-Policy (E86, unverändert übernommen aus v1.0)

### 6.1 Snapshot-Version vs. File-Header sind entkoppelt

- **Snapshot-Version** = Git-Tag (z.B. `v1.19`) = Stand des gesamten Sets
- **File-Header** `**Stand:** v1.X` = Inhalts-Stand der einzelnen Datei

Folge: ein File im Snapshot `v1.19` kann File-Header `v1.15.1` haben (kein Touch in v1.19), während ein anderes File auf `v2.0` ist (Major-Bump in v1.19).

### 6.2 Bump-Konvention (SemVer-style)

| Bump-Typ | Wann | Beispiel |
|---|---|---|
| **Patch** (v1.15 → v1.15.1) | reine Referenz-/Cross-Verweis-Updates ohne Inhalts-Änderung | „Verweis auf neue E-Nummer" |
| **Minor** (v1.15 → v1.16) | Inhalts-Updates, neue Sektionen, neue Regeln | „neuer Eintrag F5, neue Self-Check-Punkte" |
| **Major** (v1.15 → v2.0) | strukturelle Umbauten, Architektur-Pivots | „Drive → Git, Build-Pattern komplett neu" |

### 6.3 Edge-Case: nur-mitgenommen ≠ Bump

Wenn ein File ohne Modifikation aus dem Vorgänger-Snapshot übernommen wird: **kein Bump**. Der Header bleibt unverändert. Im Manifest als „unverändert" gelistet.

Wenn auch nur eine Referenz/ein Cross-Verweis aktualisiert wird: **Patch-Bump**.

### 6.4 Verifikation

Vor Manifest-Schreibung prüft Self-Check WSC-17: Alle im Manifest als „modifiziert" gelisteten Files haben gegenüber dem Vorgänger-Snapshot einen Header-Bump erhalten. Diff-Check via `git diff v<PREV>..HEAD -- <file>` plus Header-Grep.

---

## 7. Self-Check-Liste WSC-1 bis WSC-17 (v2.0 — Git-adaptiert)

Pflicht vor Tag-Setzen. Output: `selfcheck`-Section im `_MANIFEST.md` mit PASS / WARN / FAIL pro Punkt.

1. **WSC-1 — Größen-Limit ≤ 50 KB Soft-Limit:** Alle Files unter Limit, außer dokumentierte Known-Exceptions. Git hat kein hartes File-Size-Problem, aber 50 KB bleibt Richtwert für Lesbarkeit + Cowork-Token-Effizienz.
2. **WSC-2 — Append-/Patch-File-Verbot:** Keine `*_Append*` oder `*_Patch*`-Files im Repo-Root.
3. **WSC-3 — Erwartete File-Liste vorhanden:** Repo-Inhalt matched die in SPEC_KONSTANTEN Sektion 13 gelistete File-Liste exakt.
4. **WSC-4 — Cross-References zu ARCHIV:** Alle E-Nummer-Verweise in den Cluster-Files sind in `ENTSCHEIDUNGS-LOG-ARCHIV.md` vorhanden.
5. **WSC-5 — Neue Sektionen in SPEC_KONSTANTEN vorhanden:** Falls Sektion 13/14 erweitert wurde, sind die neuen Einträge da.
6. **WSC-6 — Kein alter Monolith:** Falls Cluster-Split passierte, das alte Monolith-File ist nicht im Repo (`git rm`).
7. **WSC-7 — Git-Status clean:** `git status --porcelain` ist leer nach Commit. Kein untracked oder uncommitted Drift.
8. **WSC-8 — Build-Target ≤ 40 KB für neue/modifizierte Files:** Sonst Cluster-Split planen (in BACKLOG eintragen).
9. **WSC-9 — UTF-8-Sanity:** Kein BOM-Bruch (außer für CSVs), kein Encoding-Drift. `file -I *.md` zeigt `utf-8`.
10. **WSC-10 — Manifest enthält alle Files mit Hashes:** SHA256 für jedes Wissens-File im Snapshot.
11. **WSC-11 — Manifest-Build-Trail vollständig:** Sektionen „neu / modifiziert / unverändert / nicht mehr existiert" gefüllt.
12. **WSC-12 — Known-Exceptions dokumentiert:** Files > 50 KB mit Begründung + geplanter Split-Snapshot.
13. **WSC-13 — Manuelle Aktionen für Tjorben vermerkt:** Drive-Karteileichen-IDs, externe Aufräum-Aktionen.
14. **WSC-14 — Notes zum Build-Pattern:** Tool-Anomalien, Drift-Pfade, Empfehlungen für nächste Iteration.
15. **WSC-15 — Tag-Konvention eingehalten:** `v<MAJOR>.<MINOR>`, kein Konflikt mit existierendem Tag (`git tag --list | grep <NEW>` ist leer vor `git tag`).
16. **WSC-16 — Push erfolgreich:** `git push origin main --tags` hat ohne Fehler durchgelaufen, Remote zeigt neuen Tag (`git ls-remote --tags origin` enthält `v<NEW>`).
17. **WSC-17 — File-Header-Bump-Pflicht (E86):** Alle im Manifest als „modifiziert" gelisteten Files haben gegenüber Vorgänger einen Header-Bump (Patch/Minor/Major gemäß 6.2). Verifikation: für jedes modifizierte File `git diff v<PREV>..HEAD -- <file>` zeigt eine Header-Zeilen-Änderung.

**Fails sind blockierend** — bei FAIL: korrigieren und neu validieren, **nicht taggen/pushen**. Warnings dokumentieren im Manifest unter „informational Warnings".

---

## 8. Manifest-Spec (v2.0)

Pflichtsektionen in jedem `_MANIFEST.md`:

1. **Header** — Snapshot-Tag, Stand, Vorgänger-Tag, Commit-Hash (nach Commit ergänzen oder mit `git rev-parse HEAD`)
2. **Build-Trail** — Auftrag (was Tjorben getriggert hat), Resultat (was passiert ist), Build-Engine (Claude Code Opus 4.7), autonome Entscheidungen
3. **Was neu generiert wurde** — Liste mit File-Name + Zweck
4. **Was modifiziert wurde** — Liste mit File-Name + Bump-Typ (Patch/Minor/Major) + Begründung
5. **Was unverändert kopiert wurde** — Liste (in Git: alle übrigen committeten Files — kann auch als „siehe `git diff --stat v<PREV>..HEAD` für vollständigen Vergleich" abgekürzt werden, wenn Liste groß)
6. **Was nicht mehr existiert** — Liste (bei `git rm` oder Cluster-Splits)
7. **File-Liste mit Sizes und SHA256-Hashes** — Tabelle
8. **Anzahl-Marker** — Wissens-Files + Manifest = Total
9. **Self-Check-Ergebnis** — Status (PASS/WARN/FAIL), pro WSC-Punkt
10. **Known-Exceptions / Geplante Folge-Splits**
11. **Manuelle Aktionen für Tjorben** (Drive-Karteileichen, externe Cleanup)
12. **Notes zum Build-Pattern** — Spec-Feedback, Anomalien, Empfehlungen

---

## 9. Output-Format

Am Ende des Builds:
- Repo-Working-Tree: alle Files final
- Commit mit aussagekräftiger Nachricht: `v<NEW> — <Kurz-Beschreibung>`
- Tag: `git tag v<NEW>` auf dem Commit
- Push: `git push origin main --tags`
- Verify: `https://github.com/verticalogmbh/polesportshop-wissen/releases/tag/v<NEW>` ist erreichbar (Browser-Check optional, GitHub-Release-Page wird auto-generiert für lightweight tags)
- Lauf-Bericht im Chat: kompakter Abschluss-Report (siehe Sektion 10)

---

## 10. Abschluss-Report-Template

Nach erfolgreichem Push pro Build an Tjorben:

```
v<NEW> Build done.

Geänderte Files (mit 1-Zeiler):
- <File>: <Was> [Bump-Typ]
- ...

Neue E-Einträge: E<X>, E<Y>, ...
BACKLOG-Updates: B<X> erledigt, B<Y> deferred, B<Z> neu.

WSC-Result: <P> PASS / <W> WARN / <F> FAIL
- WARNs: <Kurzbegründung>

Autonome Entscheidungen (zum Review):
- <Entscheidung 1>: <Begründung>
- ...

Empfehlung nächster Scope: <v1.20-Scope-Vorschlag>

Live: https://github.com/verticalogmbh/polesportshop-wissen/releases/tag/v<NEW>
```

---

## 11. Anhang: Legacy — Drive-Build-Pattern (v1.0–v1.18)

Dieser Anhang dokumentiert das abgelöste Pattern für Forensik und mögliche Reaktivierung im Notfall.

### 11.1 Charakteristik

- **Storage:** Google Drive Ordner `Wichtig: Claude Backup/`, parent-ID `12wDy0Z0cmB0p-OAs10Y7XqBWhmtQEip5`.
- **Snapshots:** Sub-Folder `Version_YYYY-MM-DD_HHMMSS/`, sekundengenauer Timestamp, jüngster vollständiger Folder = aktueller Stand.
- **Build-Engine:** Cowork (Anthropic Claude-im-Browser mit Drive-MCP-Connector + Code-Execution-Sandbox).
- **Build-Pattern:** 12 Stages, Snapshot-Resolution + lokales Caching unter `/home/claude/wissens_in/`, Modifikation, Upload via Drive-MCP, Manifest als Komplettheits-Marker.

### 11.2 Bekannte Probleme die zur Migration führten (siehe E87)

- **Tool-Limits (A9/A10/A11):** Drive-MCP `create_file` mit `base64Content` für Files >50 KB markdown ≈ >67 KB base64 ≈ >17k Output-Tokens scheitert reproduzierbar am Main-Agent-Output-Cap. Subagent (Sonnet) leidet zusätzlich an UTF-8-Drift bei base64-Strings (Drift-Rate ~1 char/10KB).
- **Drive-MCP fehlt `delete_file` (B33):** Fehlgeschlagene Uploads bleiben als Karteileichen liegen, müssen manuell in Drive-Web-UI bereinigt werden.
- **Drive-MCP `textContent` strippt trailing `\n`:** 1-Byte-Diff zur Quelle, WSC-7 (Byte-Identität) bricht.
- **Manuelles Tjorben-Upload bei Subagent-Limits:** Bei Files die das Subagent-Limit übersteigen muss Tjorben den `present_files`-Output manuell per Drag-and-Drop in den Drive-Sub-Folder ziehen — bricht die End-to-End-Automation.
- **Karteileichen-Akkumulation:** Drive-MCP fehlt `delete_file`, Fail-Uploads stapeln sich (v1.18 hatte 6 neue Karteileichen + 3 Altlasten aus v1.17).

### 11.3 Reaktivierung im Notfall

Falls Git/GitHub als Backbone ausfällt: das Drive-Pattern ist im Vorgänger-Snapshot `Version_2026-05-18_141930` voll dokumentiert (Manifest + Playbook v1.0). Reaktivierung braucht keinen Code-Change im Pattern selbst, nur Wechsel der Resolution-Quelle in `cowork_custom_instructions.md` und `Projekt-Anweisungen.md` zurück auf Drive-Folder-Resolution.

### 11.4 Migrations-Status

- v1.18 ist als Git-Tag verfügbar (`v1.18` auf `main`), ist aber per Drive-Pattern entstanden.
- v1.19 ist der erste Build per Git-Pattern (dieser Playbook v2.0).
- v1.20 wird die Cowork-Resolution auf GitHub-Raw umstellen (B63).
- Drive-Folder bleibt als Read-Only-Archiv erhalten, keine neuen Sub-Folder ab v1.19.

---

## 12. Bootstrap-Hinweis

Dieser Playbook v2.0 ist **selbst entstanden durch v1.19** — der erste Build, der das Pattern beschreibt, ist auch der erste Build, der nach dem Pattern läuft. Ab v1.20 ist der Trigger im Chat noch kürzer (kein Pattern-Pivot mehr zu beschreiben, nur Scope).
