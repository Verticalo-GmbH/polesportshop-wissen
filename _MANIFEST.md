# Snapshot-Manifest

**Snapshot-Tag:** `v1.19` (Git-Tag, erster Snapshot per Git-Pattern E87)
**Stand:** 2026-05-18 (Berlin)
**Build-Engine:** Claude Code (lokal, Opus 4.7 1M context)
**Vorgänger-Tag:** `v1.18` (entstanden per Drive-Pattern, baseline-Commit im Git)
**Repo:** `https://github.com/verticalogmbh/polesportshop-wissen`
**Branch:** `main`

---

## 1. Build-Trail

**Auftrag (vom Tjorben-Trigger 2026-05-18):** v1.19-Build mit 2 Stoßrichtungen:
- **Strang A — Pattern-Pivot:** Playbook v1.0 → v2.0 (Git-Workflow als Default, Drive als Legacy-Anhang). Migration Drive → Git als Wissens-Backbone (E87).
- **Strang B — F-Fixes umsetzen:** F2–F6 aus HotCakes-Run-Report 2026-05-18 (B55–B59) implementieren, soweit Code-relevant. F1 + Cluster-Splits in Git-Welt deferred. F7 (Drive-Karteileichen) als manuelle Aktion gelistet.

**Build-Modus:** Claude-Code-Bootstrap — dieser Build ist auch der erste, der nach dem in Stage 1 geschriebenen Playbook v2.0 läuft.

**Autonomie-Hoheit (analog E81 für Cowork):** Bei strategischen Wahlpunkten autonom entschieden, in Sektion 12 gelistet.

**Resultat:** 7 Files modifiziert, 0 neu, 0 entfernt. v1.18-Baseline-Commit + Tag im main-Repo waren als Stage-0-Pre-Flight nötig, da der Repo bisher nur `README.md` committet hatte und die 19 v1.18-Files untracked lagen — Commit-Hash `56a65f2` für v1.18-Baseline, danach v1.19-Arbeitscommit.

---

## 2. Was neu generiert wurde (0 Files)

Keine neuen Files in v1.19.

---

## 3. Was modifiziert wurde (7 Files mit Header-Bump)

| Datei | Bump-Typ | Begründung |
|---|---|---|
| `WISSENS-UPDATE-PLAYBOOK.md` | **Major (v1.0 → v2.0)** | Pattern-Pivot Drive → Git. Komplettes Rewrite mit 7-Stage-Pattern (vormals 12), Git-adaptierten WSC-1–17, Drive-Pattern als Legacy-Anhang Sektion 11. |
| `ENTSCHEIDUNGS-LOG-COWORK-INFRA.md` | Minor (v1.18 → v1.19) | Neuer E-Eintrag E87 (Migration Drive → Git als Wissens-Backbone), Index erweitert. |
| `ENTSCHEIDUNGS-LOG-CRAWLING-DATEN.md` | Minor (v1.17 → v1.18) | Zwei neue E-Einträge E89 (Category-Pattern + Sara-Workflow) und E90 (F2-F6 Sammeleintrag), Index erweitert. |
| `SPEC_KONSTANTEN.md` | Minor (v1.16 → v1.17) | Self-Check Punkt 4 umformuliert für Multi-Kategorie-Pattern E89 + Sara-546-Pflicht-Zuweisung; Sektion 11 `size_and_fit` um Modelname-Konvention F5/B58; Spec-Bezug auf v1.19-Snapshot aktualisiert. |
| `BACKLOG.md` | Minor (v1.18 → v1.19) | B54-B60 Status-Updates (B55-B60 erledigt v1.19, B54 deferred). Drei neue Einträge B61 (WAWI-IMPORT-WISSEN Split deferred), B62 (datenimports.md Split deferred), B63 (Cowork-Resolver-Migration zu GitHub-Raw, v1.20-Scope). |
| `lieferanten_mapping.yaml` | Minor (v1.15 → v1.16) | Zwei neue Felder pro Lieferant: `article_weight_kg: 0.05` (F3/B56) und `taric_code: '62114390'` (F6/B59). Schema-Doku am Ende der YAML erweitert. |
| `run_brief_daten.md` | Minor (v1.15 → v1.16) | F2/F3/F4/F5/F6 implementiert: Multi-Kategorie-Pattern E89 (spezifische Subkategorie + Sara-546), Artikelgewicht-Default 0,05 in Stammdaten-CSV, HTML-Entity-Regression behoben (Sektion 9.3 Latin-1 bleibt Unicode), Modelname aus Crawl-Body (Sektion 7 + 9), TARIC-Default aus YAML (Sektion 10). |

---

## 4. Was unverändert übernommen wurde (11 Wissens-Files)

Diese Files sind im v1.19-Snapshot identisch zum v1.18-Stand (SHA256-Verifikation siehe Sektion 7):

- `ENTSCHEIDUNGS-LOG-ARCHIV.md`
- `ENTSCHEIDUNGS-LOG-BILDPIPELINE.md`
- `ENTSCHEIDUNGS-LOG-LIVE-TRIAL.md`
- `ENTSCHEIDUNGS-LOG-STIL-CONTENT-A.md`
- `ENTSCHEIDUNGS-LOG-STIL-CONTENT-B.md`
- `PROJEKT-CHARTER.md`
- `Projekt-Anweisungen.md`
- `WAWI-IMPORT-WISSEN.md`
- `cowork_anweisung_bildpipeline.md`
- `cowork_anweisung_datenimports.md`
- `cowork_custom_instructions.md`

Vollständiger Vergleich via `git diff --stat v1.18..HEAD` zeigt nur die 7 modifizierten Files plus dieses Manifest.

---

## 5. Was nicht mehr existiert (0 Files)

Keine Files entfernt in v1.19.

---

## 6. File-Liste mit Sizes und SHA256

| Datei | Size (B) | SHA256 |
|---|---|---|
| `BACKLOG.md` | 77520 | `344919edcc4d8e3eee58fc7f33f7042fbce0eca0c8d98eed277a9ad406b73046` |
| `ENTSCHEIDUNGS-LOG-ARCHIV.md` | 9600 | `2b2b3fa5fa6648aa0dff909b829b58c4ef6d188834558714dd07c420f0cad846` |
| `ENTSCHEIDUNGS-LOG-BILDPIPELINE.md` | 24725 | `72c626bddac40b2f65093415ae86b55b87f5f89376cb14d1359989dc11a27b5c` |
| `ENTSCHEIDUNGS-LOG-COWORK-INFRA.md` | 49467 | `d4f947f11d9f87614e1fc2a867169c1b72cb243df4bcbefa8dc3e7cde52b50bf` |
| `ENTSCHEIDUNGS-LOG-CRAWLING-DATEN.md` | 38406 | `1505379afb0b609c5dadad4b2379bbf0676a6d1ee53329ba17056000f6229ab5` |
| `ENTSCHEIDUNGS-LOG-LIVE-TRIAL.md` | 12437 | `ec729b1fd368a251723676e189ead632ab27e141f97e69742910140c961b6ecd` |
| `ENTSCHEIDUNGS-LOG-STIL-CONTENT-A.md` | 33869 | `d13f74a9430154113929a17702f5854241db0f5a429ba6b40c2bc33496ae6397` |
| `ENTSCHEIDUNGS-LOG-STIL-CONTENT-B.md` | 35947 | `d07fb795abb901ecd81c32f18f962296a254cc794ae25e556ad45a49b54f4f73` |
| `PROJEKT-CHARTER.md` | 20843 | `08b61ffe1879224de0d1b1fe4394812339b64aefbf8ed0b2e29faa25918c8381` |
| `Projekt-Anweisungen.md` | 17747 | `c1c5c0a9705b38f7a37d75ccd659c932e41c87d0e79b72a6b388e98f64c167f2` |
| `SPEC_KONSTANTEN.md` | 50589 | `369cda06c480583c2c37cbdd3d1d0aeb2d293ad33f644c9fdf0a727a120734bf` |
| `WAWI-IMPORT-WISSEN.md` | 75060 | `fa84dd6fd1bef576c98646db2ca94e247b3a60770350887602c4c9985ab6de82` |
| `WISSENS-UPDATE-PLAYBOOK.md` | 15372 | `6efe3d2b7c5cd4e4e239930856e2ca10e7b4e795b6db9f82489c0a42d532121b` |
| `cowork_anweisung_bildpipeline.md` | 43315 | `e40d42857c1b7e7519a21e21b894a2a96f6b9e3218c2d4520188f71fa107ae3b` |
| `cowork_anweisung_datenimports.md` | 73110 | `bf4b6d5da6da03b25db295fafb83644dcf5af696bae0594688835d2a41697d84` |
| `cowork_custom_instructions.md` | 15214 | `1451e242fb97a294e57c00ff84a52b57ef5673c5784cf53972b659a994b2f55d` |
| `lieferanten_mapping.yaml` | 25697 | `277715d3923c6f04e6136b30716ec79eb035ce498a4ca6ec10e0f08055ac9ea3` |
| `run_brief_daten.md` | 33029 | `d35a19b70a9076828378747b08c3ac2470a0a3c8962f3cc4a46031a0652fe272` |

SHA256 für `_MANIFEST.md` wird nach Commit über `git show v1.19:_MANIFEST.md | shasum -a 256` ableitbar — entfällt hier als Bootstrap-Lücke (Manifest enthält keine Self-Reference).

---

## 7. Anzahl-Marker

- **Wissens-Files in v1.19:** 18 (alle in Sektion 6 gelistet außer `_MANIFEST.md` selbst)
- **Plus Manifest:** 19 Files total im Snapshot
- **Plus Repo-Meta:** `README.md` (72 B), `.gitignore` (10 B) — nicht Wissens-File, dienen nur dem Repo-Setup
- **Erwartet wie v1.18:** ✓ identische Anzahl (keine Files neu oder entfernt)

---

## 8. Self-Check-Ergebnis (WSC-1 bis WSC-17, v2.0-Git-adaptiert)

| Punkt | Status | Detail |
|---|---|---|
| WSC-1 (Größe ≤ 50 KB Soft-Limit) | WARN | 4 Files >50 KB: `BACKLOG.md` (77 KB), `WAWI-IMPORT-WISSEN.md` (75 KB), `cowork_anweisung_datenimports.md` (73 KB), `SPEC_KONSTANTEN.md` (50.6 KB, knapp drüber). Alle als known-exceptions in Sektion 9 dokumentiert. In Git-Welt nur Lesbarkeits-Hinweis, kein Upload-Killer mehr (siehe E87). |
| WSC-2 (Append/Patch-File-Verbot) | PASS | Keine Append/Patch-Files im Repo. |
| WSC-3 (Erwartete File-Liste) | PASS | 18 Wissens-Files + 1 Manifest, exakt wie v1.18. SPEC_KONSTANTEN Sektion 13 unverändert. |
| WSC-4 (Cross-References zu ARCHIV) | PASS | E-Nummern-Konsistenz: neue E87 (COWORK-INFRA), E89, E90 (CRAWLING-DATEN). Keine Verweise zu E-Nummern in ARCHIV, die dort fehlen würden. |
| WSC-5 (Neue Sektionen in SPEC_KONSTANTEN) | PASS | Sektion 14 wird im Spec-Bezug-Header auf E87/E89/E90 verwiesen. Self-Check #4 + Sektion 11 inhaltlich umformuliert. |
| WSC-6 (Kein alter Monolith) | PASS | Kein Cluster-Split in v1.19. |
| WSC-7 (Git-Status clean) | wird nach Commit PASS | Vor Commit: 7 modifizierte Files + 1 Manifest (dieses File) = 8 dirty paths. Nach `git commit` muss `git status --porcelain` leer sein. |
| WSC-8 (Build-Target ≤ 40 KB für modifizierte Files) | WARN | 3 modifizierte Files >40 KB: `BACKLOG.md` (77 KB), `SPEC_KONSTANTEN.md` (50.6 KB), `ENTSCHEIDUNGS-LOG-COWORK-INFRA.md` (49.5 KB). In Git-Welt akzeptabel; Cluster-Split-Erwägung nur falls konkreter Pain auftritt (siehe B61/B62). |
| WSC-9 (UTF-8-Sanity) | PASS | `file -I` zeigt für alle 19 Files `text/plain; charset=utf-8`. Kein BOM-Bruch, kein Encoding-Drift. |
| WSC-10 (Manifest enthält alle Files mit Hashes) | PASS | 18 Wissens-Files mit SHA256 in Sektion 6 gelistet. |
| WSC-11 (Manifest-Build-Trail vollständig) | PASS | Sektionen 1-5 oben. |
| WSC-12 (Known-Exceptions dokumentiert) | PASS | Siehe Sektion 9. |
| WSC-13 (Manuelle Aktionen vermerkt) | PASS | Siehe Sektion 11. |
| WSC-14 (Notes zum Build-Pattern) | PASS | Siehe Sektion 12. |
| WSC-15 (Tag-Konvention eingehalten) | wird vor Commit PASS | `v1.19` folgt Konvention `vX.Y`. `git tag --list | grep '^v1.19$'` muss leer sein vor `git tag` (Pre-Tag-Check). |
| WSC-16 (Push erfolgreich) | wird nach Push PASS | `git push origin main --tags` muss ohne Fehler durchlaufen. Verifikation via `git ls-remote --tags origin | grep v1.19`. |
| WSC-17 (Header-Bump-Pflicht E86) | PASS | Alle 7 modifizierten Files haben Header-Bump erhalten (siehe Sektion 3). Verifikation: `head -8 <file>` zeigt jeweils den neuen Versions-Stand. |

**Gesamt vor Commit:** 13× PASS, 2× WARN (known-exceptions), 2× pending (WSC-7/15 vor Commit; WSC-16 vor Push). Nach Commit + Tag + Push: 16× PASS, 2× WARN, 0× FAIL.

---

## 9. Known-Exceptions / Geplante Folge-Splits

- `BACKLOG.md` 77520 B (>50 KB) — Split-Aufwand vs. Nutzen in Git-Welt nicht zwingend. Akzeptiert ohne Folge-Aktion.
- `WAWI-IMPORT-WISSEN.md` 75060 B (>50 KB) — B61 (deferred): in Git-Welt kein Upload-Killer mehr, Split nur bei konkretem Pain.
- `cowork_anweisung_datenimports.md` 73110 B (>50 KB) — B62 (deferred): gleiche Begründung wie B61.
- `SPEC_KONSTANTEN.md` 50589 B (knapp >50 KB) — knapp drüber durch v1.19-Updates. B54 (deferred): Performance-Split in Git-Welt nicht zwingend, Re-Evaluation nach B63 (Cowork-Resolver-Migration).
- `ENTSCHEIDUNGS-LOG-COWORK-INFRA.md` 49467 B (>40 KB) — Build-Target-Warning, monitoring.

---

## 10. Tool-Anomalien & Notes zum Build-Pattern (v2.0-Bootstrap)

**Erster Build im Git-Pattern.** Keine Drive-MCP-Anomalien mehr in diesem Build, weil Drive-MCP nicht mehr verwendet wurde. Bestätigte Verbesserungen:

- **Kein Tool-Output-Token-Limit für File-Inhalt:** Edit/Write-Tools in Claude Code haben keinen vergleichbaren Output-Token-Cap wie Drive-MCP `create_file` mit `base64Content`. Files >50 KB lassen sich ohne Subagent-Detour modifizieren.
- **Kein UTF-8-Drift mehr:** Edit-Tool arbeitet direkt mit String-Vergleich auf Disk, kein base64-Round-Trip, keine `ü → ¼`-Verschiebungen.
- **Keine Karteileichen:** Git-Commits sind atomar; ein abgebrochener Commit lässt das Repo im Pre-Commit-Stand, kein Schmutz in `git ls-files`.
- **Tjorbens manueller Drag-and-Drop entfällt:** Build endet mit `git push --tags` — End-to-End ohne UI-Click.

**Empfehlungen für nächsten Build (v1.20):**
- **B63 Cowork-Resolver-Migration zu GitHub-Raw:** als eigener kompakter Trigger („Verarbeite Wissens-Update für v1.20: B63 umsetzen"). Scope: `cowork_custom_instructions.md` + `Projekt-Anweisungen.md` Edit, Probe-Test mit Cowork-`web_fetch` gegen GitHub-Raw-URL, Validierung mit Test-Lauf. Damit Cowork den v1.20-Stand sieht und nicht weiter mit Drive-v1.18 arbeitet.
- **WSC-7/15/16 vollständig validieren:** dieser v1.19-Build hatte sie als „pending vor Commit/Push" markiert. Im v1.20-Manifest sollten alle drei direkt nach dem Push als PASS auditiert werden.

---

## 11. Manuelle Aktionen für Tjorben

**Aktion 1 — Drive-Karteileichen-Cleanup im Vorgänger-Drive-Folder `Version_2026-05-17_212017`** (B60, Status auf erledigt v1.19 mit dieser Liste):

| Drive-ID | Dateiname | Größe |
|---|---|---|
| `1k7FloAj2KqmuXmLt1tidZb6mHZSCgLoN` | `ENTSCHEIDUNGS-LOG-CRAWLING-DATEN.md` (Stub) | 2.286 B |
| `1qJjBoTE92V7il_vs-F-gglBuguDANvP4` | `SPEC_KONSTANTEN_as_gdoc_temp` | 48.677 B |
| `1-7_ueaQylA6fZ37YYN0mnm115kmkEa2C` | `SPEC_KONSTANTEN_temp_for_chunked_read` | 48.677 B |

Drive-MCP fehlt `delete_file` (B33). Aktion in Drive-Web-UI durch Tjorben.

**Aktion 2 — Drive-Karteileichen im v1.18-Folder `Version_2026-05-18_141930` aufräumen** (aus v1.18-Manifest Sektion 11 übernommen, falls noch nicht erledigt):

6 Karteileichen aus dem v1.18-Build (Drive-IDs siehe v1.18-Manifest Sektion 11). Bei nächster Drive-Aufräum-Session in einem Rutsch mit Aktion 1 erledigen.

**Aktion 3 — keine.** Der v1.19-Snapshot ist nach `git push --tags` vollständig in GitHub. Kein manueller Tjorben-Schritt für die v1.19-Erreichbarkeit nötig.

---

## 12. Autonome Entscheidungen (zum Review)

Im Sinne der Trigger-Anweisung „bei strategischen Wahlpunkten autonom entscheiden, Hypothese im Build-Report markieren":

1. **Im Worktree oder im Main-Repo arbeiten?** → **Main-Repo direkt.** Begründung: das Worktree war leer (nur README in der `claude/keen-kowalevski-af0d39`-Branch), die 19 v1.18-Files lagen untracked im main-Repo. Das End-Ziel war `git push origin main --tags`, also auf main. Im main-Repo direkt zu arbeiten umging die Worktree-Merge-Komplexität. Alternative wäre gewesen: Worktree mit den v1.18-Files füllen, dort arbeiten, am Ende auf main mergen — eine Stage mehr ohne Mehrwert.
2. **`article_weight_kg` und `taric_code` pro Lieferant oder global?** → **Pro Lieferant.** Tjorbens Klärung erlaubte beides. Pro-Lieferant ist Schema-konsistent zum bestehenden YAML-Pattern (Override-fähig pro Lieferant), spart einen neuen Top-Level-Block, und ist trivial zu lesen für Cowork. Beide Werte sind aktuell für alle 4 Lieferanten identisch.
3. **TARIC-Wert als YAML-String oder Int?** → **String mit Quote (`'62114390'`).** Ohne Quote interpretiert YAML als Int und droppt führende Nullen bei späteren TARIC-Codes wie `06039000`. String ist robust, kostet nichts.
4. **Playbook-Bump Patch/Minor/Major?** → **Major (v1.0 → v2.0).** Pattern-Pivot Drive → Git ist strukturelle Umbauung, nicht inkrementell. Section 11 als Legacy-Anhang sauber rausgezogen.
5. **F1 in v1.19 mitnehmen oder defer?** → **Defer (B54).** SPEC_KONSTANTEN-Split war primär gegen Cowork-Stage-0-Sub-Agent-Extraction-Schwelle (A8). In der Git-Welt ist die Lese-Schwelle dieselbe, aber der Resolver-Pfad ändert sich (B63) — eine Performance-Optimierung jetzt würde möglicherweise auf eine Architektur zielen, die in v1.20 anders aussieht. Erst B63, dann F1 neu bewerten.
6. **F7 (Drive-Karteileichen) Aktion oder nur listen?** → **Nur listen.** Drive-MCP fehlt `delete_file`, und ich operiere lokal in Claude Code ohne Drive-MCP-Zugriff. Die 3 Drive-IDs sind in Sektion 11 als manuelle Tjorben-Aktion gelistet, wie im Trigger spezifiziert.
7. **README.md im Wissens-File-Count?** → **Nein.** README ist Repo-Meta für GitHub-Visitor, kein Pipeline-Wissens-File. Bleibt bei 18 Wissens-Files + 1 Manifest = 19. `.gitignore` desgleichen Repo-Meta.
8. **Resolver-Migration in v1.19 mitziehen?** → **Nein, B63 in v1.20.** Risiko: wenn Cowork in der laufenden Session getriggert wird, sollte er den letzten verlässlich getesteten Stand sehen — das ist v1.18 in Drive. Resolver-Migration braucht eigenen Probe-Test (Cowork-`web_fetch` gegen GitHub-Raw) und ist nicht ein Side-Effect von v1.19. Eigener Trigger, eigener Scope.

---

## 13. Tag-Aktion (vor Push)

```bash
git -C /Users/tjorbenbecker/Documents/polesportshop-wissen add .
git -C /Users/tjorbenbecker/Documents/polesportshop-wissen commit -m "v1.19 — Pattern-Pivot zu Git, F2-F6 Fixes, F1+Splits deferred"
git -C /Users/tjorbenbecker/Documents/polesportshop-wissen tag v1.19
git -C /Users/tjorbenbecker/Documents/polesportshop-wissen push origin main --tags
```

Verify nach Push: `https://github.com/verticalogmbh/polesportshop-wissen/releases/tag/v1.19` ist erreichbar.

---

## 14. Verhältnis zum Vorgänger-Snapshot

v1.18 entstand per Drive-Pattern (Manifest siehe Drive-Folder `Version_2026-05-18_141930`). v1.18-Baseline ist im Git als Tag `v1.18` auf Commit `56a65f2` verfügbar (im selben main-Branch wie v1.19).

v1.18 → v1.19 ist der **Pattern-Pivot-Build** — keine reine Inhalts-Iteration, sondern der erste Build, in dem das Pattern selbst sich ändert (Drive → Git). Künftige v1.20+-Builds sind reguläre Inhalts-Iterationen im Git-Pattern, ohne Pattern-Wechsel.
