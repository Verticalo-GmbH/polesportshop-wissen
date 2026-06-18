# BACKLOG-ARCHIV — erledigte und deferred B-Einträge

**Stand:** v1.1, 2026-05-18 (v1.21-Update: B63 final mit B65-Teilvalidierung, neue Sektion „v1.21 Trial-Findings" mit B49-Stand)
**Zweck:** Kompakter Index der nicht-mehr-aktiven B-Einträge aus `BACKLOG.md`. Erleichtert Übersicht über das wirklich Offene. Vollständige Eintrags-Details bleiben in `BACKLOG.md` — diese Datei verlinkt nicht, weil Markdown-Anchor unsicher; stattdessen Search-Hint (Stichwort grep-bar).

---

## Index-Konvention

Pro Eintrag: `**B<N>** — <Kurz-Titel> — <STATUS>` plus 1-Zeiler-Kontext. STATUS-Werte: `GELÖST`, `GEKLÄRT`, `TEILGELÖST`, `WEITGEHEND ERLEDIGT`, `ERLEDIGT`, `DEFERRED`. Mit Bezug auf den jeweiligen E-Eintrag oder Pilot-Lauf.

Für volle Details: `grep -A 5 "^**B<N>" BACKLOG.md` im Repo.

---

## Erledigt / gelöst (klare Auflösung)

- **B1** — Wie wird Cowork eingerichtet? — **GELÖST 2026-05-14**, präzisiert 2026-05-15. Global Instructions in Settings → Cowork, siehe `cowork_custom_instructions.md`. Ab v2.0 (v1.20): Wissens-Quelle ist GitHub-Raw, nicht mehr Drive.
- **B2** — Wo lebt das Lieferanten-Mapping? — **GELÖST 2026-05-14**. `lieferanten_mapping.yaml` als Single Source of Truth (E24).
- **B3** — Pole-Junkie-Crawling — **GEKLÄRT 2026-05-15** durch E49 (Owner-Direktive Tjorben).
- **B5** — Plattform-Aktivierung — **GELÖST 2026-05-15** durch E46 (Bilder integriert in Stammdaten-Import).
- **B15** — Versionierung der Cowork-Anweisungen — **GELÖST durch E47** (Snapshot-Architektur), ab v1.19 durch Git-Tags ersetzt (E87).
- **B22** — R2-Migration und R2-Upload-Mechanik — **TEILGELÖST 2026-05-15**, mit E63 (Bildpipeline archiviert) entschärft.
- **B23** — MCP-Connector-Inventur — **WEITGEHEND ERLEDIGT 2026-05-15** (siehe `_PIPELINE/_Logs/2026-05-15_crawl-tool-evaluation/`).
- **B24** — cowork_anweisung_bildpipeline.md Anti-Bot-Pattern — **GELÖST 2026-05-14**, mit Stub-Reduktion v1.20 (E91) auf Verweis reduziert.
- **B28** — Vision-Klassifikations-Verifikation — **GELÖST 2026-05-15 mit Negativ-Ergebnis** (manufacturer_first_vision_audit für HotCakes verworfen, Thumbnail-Vision bleibt Default).
- **B55** — Kategorie-Pattern in WaWi-CSV — **ERLEDIGT v1.19 → E89**.
- **B56** — Artikelgewicht-Default — **ERLEDIGT v1.19** (`article_weight_kg: 0.05` in `lieferanten_mapping.yaml`).
- **B57** — HTML-Entity-Encoding-Regel — **ERLEDIGT v1.19** (Latin-1 bleibt Unicode, F4-Korrektur in `run_brief_daten.md` Sektion 9.3).
- **B58** — „Unser Model"-Phrase raus — **ERLEDIGT v1.19** (Modelname aus Crawl-Body, F5).
- **B59** — TARIC-Code-Default — **ERLEDIGT v1.19** (`taric_code: '62114390'` in `lieferanten_mapping.yaml`).
- **B60** — Drive-Karteileichen-Cleanup — **ERLEDIGT v1.19** (3 Drive-IDs in v1.19-Manifest gelistet als manuelle Tjorben-Aktion).
- **B63** — Cowork-Resolver-Migration zu GitHub-Raw — **ERLEDIGT v1.20 → E91** (Sektion „Wissens-Quelle: GitHub-Raw-Resolution" in `cowork_custom_instructions.md`).
- **A6** — Drive-Upload-Tool-Output-Limit — **FINAL GELÖST mit E69 (2026-05-16)**, mit E87 (Drive → Git) komplett obsolet.

## Deferred (offen, aber bewusst aufgeschoben mit Re-Eval-Trigger)

- **B4** — A-Nummer-Strategie: wann kippen? — **DEFERRED**. Trigger: Lieferanten-Wechsel bei gleichem Artikel, oder Wachstum >X Artikel. Verdachtsfall für tote Einträge (seit v1.10 ohne konkrete Bewegung) — bei nächster v1.X-Iteration evaluieren ob streichen oder lebendig.
- **B12** — Wochen-/Monats-Reporting — **DEFERRED**. Nice-to-Have ohne Trigger. Verdachtsfall.
- **B21** — Verkaufskanal-Aktivierung beim Import steuerbar — **DEFERRED**. Mit E46 ist Plattform-Aktivierung der Bilder gelöst (B5). B21 betrifft Artikel-Aktivierung, nicht Bilder. Verdachtsfall: ggf. mit E46 implizit gelöst, nicht explizit dokumentiert.
- **B54** — SPEC_KONSTANTEN Performance-Split — **DEFERRED v1.19**. In Git-Welt nicht zwingend (E87), Re-Eval falls konkreter Pain auftritt.
- **B61** — WAWI-IMPORT-WISSEN.md Cluster-Split — **DEFERRED v1.19**. Selbe Begründung wie B54.
- **B62** — cowork_anweisung_datenimports.md Cluster-Split — **DEFERRED v1.19** → mit E91-Verschlankung v1.20 entschärft (jetzt ~25 KB statt 73 KB).

## Verdachtsfälle (zu streichen oder aktivieren in v1.21+)

- B4 (siehe oben)
- B12 (siehe oben)
- B21 (siehe oben)

Bei nächstem v1.X-Build kurz prüfen: noch relevant? Wenn nein: hier als `STRICHEN v1.X` markieren, in BACKLOG.md entsprechend.

---

## Operative Notiz

Diese Datei ist **kein** zwingender Bestandteil des Wissens-Stage-0-Lade-Sets in Cowork. Sie wird nur bei Klärungs-Chats (Architektur, „warum hatten wir das"-Fragen) lazy-geladen — Standard-Search in `BACKLOG.md` reicht meist.

`BACKLOG.md` selbst behält alle Details. Diese Datei ist ein Index, kein Ersatz.


## Aus BACKLOG.md archiviert (v1.23-Konsolidierung, 2026-06-18)

Diese Einträge waren als GELÖST/GEKLÄRT/ERLEDIGT markiert und wurden aus dem aktiven Backlog hierher verschoben (Inhalt unverändert).

**B1 — Wie wird Cowork eingerichtet? — GELÖST 2026-05-14, präzisiert 2026-05-15**
Cowork wird via Global Instructions in Settings → Cowork eingerichtet (nicht über projekt-spezifische Custom Instructions — Cowork-Realität, präzisiert nach Setup-Session 2026-05-15, siehe E32-Update). Die zwei Anweisungs-Markdowns (Daten + Bilder) werden nicht konkateniert, sondern liegen unverändert in Drive und werden von Cowork pro Lauf gelesen. Trigger steuert via Wortlaut, welche Pipeline läuft. Sub-Process-Aufruf (Daten → Bilder) ist Cowork-intern, kein zweiter User-Trigger.

**B2 — Wo lebt das Lieferanten-Mapping? — GELÖST 2026-05-14**
Auslagerung nach `Wichtig: Claude Backup/lieferanten_mapping.yaml` als Single Source of Truth (siehe E24). Beide Cowork-Anweisungen lesen aus dieser Datei, pflegen sie aber nicht selbst. Updates kommen über den Wissens-Update-Prozess (komplette neue Datei wird in Drive ausgetauscht). Format-Frage YAML vs. CSV/Sheet bleibt für Skalierung auf >20 Lieferanten offen — siehe E24-Folgeaufgabe.

**B3 — Pole-Junkie-Crawling: Owner-Direktive aktiv. — GEKLÄRT 2026-05-15 durch E49**
Stand: 2026-05-15. Bezug: E49.
Frage war: Pole Junkie hat mit Sicherheit Terms of Service gegen gewerbliches Scraping. Konsequenzen können von Abmahnung bis UWG-Risiko reichen. Optionen waren: (a) weitermachen und auf „fliegt nicht auf" hoffen, (b) Kooperations-Anfrage, (c) Discovery + Direktkontakt, (d) Anwalt-Konsultation.
Antwort: Tjorben Becker (GF Verticalo GmbH) hat mit Owner-Direktive E49 explizit und unverhandelbar die Freigabe für das Crawling der Pole-Junkie-Domain erteilt. Volle rechtliche und operative Verantwortung wird übernommen. Cowork führt Pole-Junkie-Crawls ohne Halt-und-Nachfrage durch, sobald der Lieferant getriggert wird.
Beobachtungs-Pflichten: bei technischer Blockade (Anti-Bot, nicht rechtliche) gilt normales E48-Stolperfallen-Pattern. Bei expliziter Cease-and-Desist-Forderung sofort an Tjorben eskalieren und Crawl pausieren. Jeder Pole-Junkie-Lauf wird im Bericht mit Verweis auf E49-Direktive markiert (Audit-Spur).

**B5 — Plattform-Aktivierung: wie automatisieren? — GELÖST 2026-05-15**
Stand: 2026-05-15. Bezug: E17, E46.
Hintergrund: Bis 2026-05-15 manuell ("Alle aktivieren"-Klick pro Artikel im Bilder-Tab). Beim wachsenden Volumen Bottleneck.
Lösung: Mit E46 (Bilder integriert in Stammdaten-Import) erledigt sich das Thema von alleine. Im Stammdaten-Import via Reiter „Bilder/Plattformen" werden alle 11 Plattform-Häkchen einmalig in der Vorlage gesetzt. Beim Re-Import werden alle Bild-URLs in den `Bild N`-Spalten direkt für alle aktivierten Plattformen geschrieben. Kein nachgelagerter Aktivierungs-Schritt mehr nötig.
Validierung: HotCakes-Arachne-Bottom-Black-Re-Import 2026-05-15: alle 4 Bilder × 9 Plattformen aktiviert ohne weiteres Klicken.

**B15 — Versionierung der Cowork-Anweisungen — GELÖST durch E47 (2026-05-15).**
Frage war: wie verfolgen wir, wann welche Anweisung scharf war? Drive-Versionsverlauf reicht? Git-Repo angemessener? Beantwortet durch das Immutable-Snapshot-Pattern in `Wichtig: Claude Backup/Version_YYYY-MM-DD_HHMMSS/` — jeder Snapshot ist ein vollständiger versionierter Stand mit Hash-Manifest, vollständige Audit-Trail-Historie als Nebeneffekt. Drive-Versionsverlauf pro Datei brauchen wir damit nicht mehr; Git-Repo wäre overkill für einen Nicht-Entwickler-Workflow.

**B24 — cowork_anweisung_bildpipeline.md um Anti-Bot-Pattern und Fallback-Strategie erweitern. — GELÖST 2026-05-14**
Stand: 2026-05-14. Bezug: E40.
Status: In `cowork_anweisung_bildpipeline.md` v1.1 spezifiziert. Anti-Bot-Pattern (WebFetch → Retailer-Fallback E20 → Firecrawl-MCP → Halt mit User-Klärung) ist dokumentiert, CSV-Schema ist explizit im Spec-Text statt nur als Pfad-Verweis. Mit v1.2 wurde der Firecrawl-Pfad an die neue Realität angepasst (Firecrawl nicht als nativer Connector verfügbar, Crawl im Pilot geparkt, siehe E41/B25). Mit v1.3 ist die CSV-Output-Generierung abgelöst (Bilder in Stammdaten, E46).

**B28 — Vision-Klassifikations-Verifikation in der Praxis. — GELÖST 2026-05-15 mit Negativ-Ergebnis**
Stand: 2026-05-15 Abend. Bezug: E45, E48.
Hintergrund: Mit E45 ist Pose-Sortierung via Cowork-Vision-Klassifikation spezifiziert. Spec-Niveau stand, Praxis-Validierung war nötig — insbesondere die Frage, ob die `manufacturer_first_vision_audit`-Optimierung (Vision skippen wenn Hersteller-Reihenfolge stabil = pose-sortiert) sich für HotCakes anbietet.

Konsolidierte Datenpunkte aus den 4 HotCakes-Modellen (2026-05-15):

| Modell | manuf-Order = Pose-sortiert? |
|---|---|
| Arachne Top Black (Lauf 16:50) | ❌ Nein |
| Hekate Bodysuit (Batch 20:30) | ✅ Ja |
| Arachne Bottom Teal (Batch 20:30) | ❌ Nein |
| Savanna Original Top (Batch 20:30) | ❌ Nein |

→ **1/4 konsistent (25 %).** Die Hersteller-Reihenfolge bei HotCakes ist NICHT stabil pose-sortiert. `manufacturer_first_vision_audit` würde unzuverlässige Resultate liefern. **Strategie verworfen für HotCakes.**

Positive Erkenntnisse:
- Vision-Klassifikation auf 384×576-Thumbnails ist robust: 13/13 Bilder klassifiziert, 0 unknowns, Confidence 0.80-0.95
- Thumbnail-Vision spart ~10× Tokens ohne Genauigkeits-Einbuße — Spec-Pfad ist richtig
- Within-Pose-Konvention (full-body vor crop) hat sich heuristisch bewährt → in v1.8 formell verankert (cowork_anweisung_bildpipeline.md v1.6 Stage 5.5)

Konsequenz für Spec:
- `cowork_anweisung_bildpipeline.md` v1.6: Thumbnail-Vision-Pfad bleibt der Standard, kein `manufacturer_first_vision_audit` für HotCakes
- Für andere Lieferanten kann die Konsistenz-Prüfung im ersten Lauf wiederholt werden
- Confidence-Schwelle 0.7 bleibt, keine Anpassung nötig nach 13 Datenpunkten

B28 ist abgeschlossen — kein offener Punkt mehr.

**B55 — Kategorie-Pattern in WaWi-CSV: Hierarchie statt parallele Tags + Sara-Kategorie als zusätzliche Zuweisung. — ERLEDIGT v1.19 → E89**
*Update v1.19 (2026-05-18):* Als Architektur-Entscheidung E89 in ENTSCHEIDUNGS-LOG-CRAWLING-DATEN formalisiert. Spec-Updates: `run_brief_daten.md` Sektion 10 (Stammdaten-Spezifika), SPEC_KONSTANTEN.md Self-Check Punkt 4. Sara-Workflow: Pflicht-Zuweisung `Intern > Neue Artikel für Sara` (WaWi-Key 546) als zweite CSV-Zeile pro neuem Artikel.
*Bezug:* HotCakes-Run-Report 2026-05-18 (Note N2, Screenshot 1 aus Tjorbens Feedback), Self-Check #2/#3/#4 in SPEC_KONSTANTEN, E89 (NEU v1.19). *Stand v1.18:* offen. *Stand v1.19:* erledigt.
*Problem:* Aktuelles Doppelzeilen-Pattern erzwingt 2 Zeilen pro Artikel (eine mit Oberkategorie, eine mit Unterkategorie). WaWi interpretiert das als zwei parallele Tag-Zuweisungen statt als Hierarchie. Ergebnis im HotCakes-Test: Artikel hat `Pole Dance Tops` und `Pole Dance Kleidung` als zwei flache Tags angezeigt, nicht als Baum.
*Klärung mit Tjorben (2026-05-18):* Pro Artikel-Zuweisung in der CSV nur die spezifischste Unterkategorie angeben — WaWi resolved den Pfad automatisch über die in WaWi gepflegte Kategorie-Hierarchie. Plus neuer Use-Case: Artikel zusätzlich in `Intern > Neue Artikel für Sara` (interner WaWi-Schlüssel 546) für Freigabe-Workflow durch Social-Media-Managerin.
*Folge-Pattern:* N Kategorien-Zuweisungen pro Artikel = N Zeilen in der CSV. Jede Zeile spezifiziert nur die unterste Kategorie. Self-Check #4 wird umformuliert von „alle 2×" auf „mindestens 2× (Shop-Kategorie + Intern/Sara), kann durch Marketing-Tags 3+ werden".
*Action für v1.19:* `run_brief_daten.md` Sektion 5 (Stammdaten) bekommt explizites Goldstandard-Beispiel mit den 2 Zeilen. SPEC_KONSTANTEN Self-Check-Sektion entsprechend umformuliert.

**B56 — Artikelgewicht-Default einbauen. — ERLEDIGT v1.19**
*Update v1.19 (2026-05-18):* `lieferanten_mapping.yaml` um `article_weight_kg: 0.05` pro Lieferant erweitert (POLE_ADDICT, HOTCAKES, LUNALAE, POLE_JUNKIE). `run_brief_daten.md` Sektion 10 dokumentiert den Default in Stammdaten-CSV-Spalten `Artikelgewicht` und `Versandgewicht` (DE-Locale `0,05`). Maße bleiben leer wie geplant.
*Bezug:* HotCakes-Run-Report 2026-05-18 (Screenshot 2 Maße/Gewicht leer), E90 (Sammeleintrag v1.19). *Stand v1.18:* offen. *Stand v1.19:* erledigt.
*Problem:* Pipeline füllt die Felder `Artikelgewicht` und `Versandgewicht` in der Stammdaten-CSV nicht. WaWi zeigt im Maße/Gewicht-Reiter alle Felder leer. Versand-Konfiguration in WaWi profitiert aber von einem realistischen Default.
*Klärung mit Tjorben:* Standard 0,05 kg (50 g) pro Kleidungsstück. Konservativer Default, dient als Platzhalter für Versand-Schätzung.
*Action für v1.19:* `cowork_anweisung_datenimports.md` Sektion Stammdaten bekommt Default-Eintrag `Artikelgewicht=0.05, Versandgewicht=0.05` (Komma-Dezimal). Maße bleiben leer (variabel pro Kleidungsstück, nicht pauschal sinnvoll).

**B57 — HTML-Entity-Encoding-Regel präzisieren (Latin-1-Umlaute bleiben Unicode). — ERLEDIGT v1.19**
*Update v1.19 (2026-05-18):* Regression-Quelle gefunden in `run_brief_daten.md` Zeile 319 (alte Regel „deutsche Umlaute als `&uuml;`, `&auml;`, `&szlig;` etc." war falsch). Korrigiert in v1.19: HTML-Entities NUR für Zeichen außerhalb Latin-1 (z.B. ✓ = `&#10004;`, ➔ = `&#10148;`). Latin-1-Zeichen (ß, ä, ö, ü, é, à etc.) bleiben Unicode im UTF-8-Output. SPEC_KONSTANTEN Sektion 5 + AP7 sind unverändert kanonisch korrekt.
*Bezug:* HotCakes-Run-Report 2026-05-18 (Tjorbens Feedback: HotCakes-Meta-Description hat `gro&szlig;e` während FANNA `große` hatte), E90 (Sammeleintrag v1.19). *Stand v1.18:* offen. *Stand v1.19:* erledigt.
*Problem:* Regression in v1.17 — Encoding-Filter wurde zu aggressiv. HTML-Entities werden auch für Latin-1-Umlaute (ß/ä/ö/ü) erzeugt, nicht nur für Symbole außerhalb der Range. Inkonsistenz zu vorherigem Run (FANNA) mit korrektem Unicode.
*Regel-Definition für v1.19:* HTML-Entities nur für Zeichen außerhalb Latin-1-Range (z.B. ✓ = `&#10004;`, ➔ = `&#10148;`). Latin-1-Zeichen (ß, ä, ö, ü, é, à, etc.) bleiben Unicode im UTF-8-Output. Action: `cowork_anweisung_datenimports.md` SEO-Sektion (Meta-Description-Template) bekommt explizite Encoding-Regel.

**B58 — "Unser Model"-Phrase im size_and_fit raus, persönlicher Tonfall mit Modelnamen aus Crawl. — ERLEDIGT v1.19**
*Update v1.19 (2026-05-18):* `run_brief_daten.md` Sektion 7 (Attribute) + Sektion 9 (Stil-Briefing) + SPEC_KONSTANTEN.md Sektion 11 (`size_and_fit`) tragen jetzt die Modelname-Konvention: Modelname aus Crawl-Body ziehen (z.B. Yifan, Vika, Elena bei HotCakes), bei mehreren Models pro Artikel erstes Model im Crawl-Body, bei null Modelname neutrale Formulierung („Das Model trägt...") oder Phrase weglassen.
*Bezug:* HotCakes-Run-Report 2026-05-18 (Note N4, Tjorbens Feedback), E74-aspirational vs. E78-funktional, E90 (Sammeleintrag v1.19). *Stand v1.18:* offen. *Stand v1.19:* erledigt.
*Problem:* HotCakes-Output enthielt im size_and_fit-Block die Phrase `Unser Model trägt Größe S bei 1,72 m. Passt regulär.` — das ist sachlich falsch (es sind Hersteller-Bilder, nicht „unser" Model) und stilistisch zu funktional. FANNA-Vorgänger-Run war persönlicher mit echten Modelnamen aus dem Crawl-Body.
*Klärung mit Tjorben:* An Herstellertexten orientieren. Wenn der Crawl-Body Modelnamen enthält (`Yifan`, `Vika`, `Elena` — im HotCakes-Run-Report N4 dokumentiert): mit Namen schreiben. Beispiel: `Yifan trägt Größe S bei 1,72 m. Der Schnitt fällt regulär aus, bei breiteren Schultern lieber zu M greifen.` Wenn kein Modelname im Crawl: neutralere Formulierung ohne „unser" (z.B. „Das Model trägt..." oder ganz weglassen).
*Action für v1.19:* `cowork_anweisung_datenimports.md` size_and_fit-Template + SPEC_KONSTANTEN Sektion 11 (Attribute-Stil-Differenzierung) bekommt explizite Modelnamen-Konvention.

**B59 — TARIC-Code als Default für Pole-Bekleidung in lieferanten_mapping.yaml. — ERLEDIGT v1.19**
*Update v1.19 (2026-05-18):* `lieferanten_mapping.yaml` um `taric_code: '62114390'` pro Lieferant erweitert (POLE_ADDICT, HOTCAKES, LUNALAE, POLE_JUNKIE). `run_brief_daten.md` Sektion 10 dokumentiert den TARIC-Eintrag in Stammdaten-CSV-Spalte `TARIC` (Sonstiges-Reiter in WaWi). YAML-Wert als String gequotet (sonst interpretiert YAML als Int).
*Bezug:* HotCakes-Run-Report 2026-05-18 (Screenshot 4 Sonstiges TARIC leer), E90 (Sammeleintrag v1.19). *Stand v1.18:* offen. *Stand v1.19:* erledigt.
*Problem:* TARIC-Code-Feld in WaWi-Sonstiges-Reiter wird nicht befüllt. Standard für deutsche Zoll-Anmeldung bei Pole-Bekleidung fehlt.
*Klärung mit Tjorben:* TARIC `62114390` für Pole-Bekleidung. Eintrag in `lieferanten_mapping.yaml` als globaler Default oder pro Lieferant. Action für v1.19: YAML-Update + `cowork_anweisung_datenimports.md` Stammdaten-Sektion „Sonstiges" zieht den Code aus YAML.

**B60 — Drive-Karteileichen-Cleanup für v1.17-Snapshot. — ERLEDIGT v1.19 (als manuelle Aktion an Tjorben gelistet im v1.19-Manifest)**
*Update v1.19 (2026-05-18):* 3 Drive-IDs sind im v1.19-Manifest Sektion 11 (Manuelle Aktionen für Tjorben) gelistet — Aktion bleibt manuell, da Drive-MCP `delete_file` fehlt (B33). Mit dem Migrations-Pivot E87 (Drive → Git) wird B33 für künftige Snapshots bedeutungslos; bestehende Drive-Karteileichen bleiben aber als historische Aufräum-Aktion.
*Bezug:* HotCakes-Run-Report 2026-05-18 (Note N5) + v1.17-Manifest (Warning #4) + v1.19-Manifest (siehe Sektion 11 dort). *Stand v1.18:* offen, Priorität NIEDRIG. *Stand v1.19:* erledigt (auf Manifest-Aktion verlagert).
*Karteileichen im `Version_2026-05-17_212017`-Folder:*
1. ID `1k7FloAj2KqmuXmLt1tidZb6mHZSCgLoN` (`ENTSCHEIDUNGS-LOG-CRAWLING-DATEN.md` Stub, 2.286 B) — fehlgeschlagener erster Upload-Versuch im v1.17-Build.
2. ID `1qJjBoTE92V7il_vs-F-gglBuguDANvP4` (`SPEC_KONSTANTEN_as_gdoc_temp`) — Subagent-Detour im HotCakes-Run.
3. ID `1-7_ueaQylA6fZ37YYN0mnm115kmkEa2C` (`SPEC_KONSTANTEN_temp_for_chunked_read`) — Subagent-Detour im HotCakes-Run.
Drive-MCP hat keine Delete-Operation. Tjorben muss die 3 Files in Drive-Web-UI rauswerfen. Beeinflussen aktuell nicht den Resolver (der prüft Sektion-13-Match, nicht „nur diese Files"), aber stören die Komplettheits-Wahrnehmung im Folder.

**B63 — Cowork-Resolver-Migration zu GitHub-Raw-URL. — ERLEDIGT v1.20 → E91**
*Update v1.20 (2026-05-18):* GitHub-Raw-Resolution in `cowork_custom_instructions.md` v2.0 verankert (Sektion „Wissens-Quelle: GitHub-Raw-Resolution"), `Projekt-Anweisungen.md` v2.0, `cowork_anweisung_datenimports.md` v2.0 Stage 0, `run_brief_daten.md` Sektion „DARF". Drive-Folder bleibt Read-Only-Archiv für Pre-v1.19-Stände. Probe-Test mit Cowork `web_fetch` gegen Tag-URL ausstehend bei nächstem Cowork-Lauf — falls Auth-Issue (Public-Repo sollte aber ohne Auth funktionieren): in `BACKLOG.md` erfassen.
*Bezug:* E87 (Drive → Git Pivot v1.19), `cowork_custom_instructions.md`, `Projekt-Anweisungen.md`, WISSENS-UPDATE-PLAYBOOK v2.0 Sektion 2.3.
*Stand:* offen, Priorität HOCH (v1.20-Scope, eigener Trigger).
*Problem:* Cowork resolved aktuell den letzten gültigen Drive-Sub-Folder (`Version_2026-05-18_141930` = v1.18-Stand). Mit dem v1.19-Pattern-Pivot E87 liegt der aktuelle Stand als Git-Tag `v1.19` im GitHub-Repo `verticalogmbh/polesportshop-wissen`, nicht in Drive. Cowork sieht den v1.19-Stand also bis zur Resolver-Migration nicht.
*Lösungs-Pfad:*
1. `cowork_custom_instructions.md` Sektion „Snapshot-Resolution": Drive-Folder-Resolution → GitHub-Raw-URL-Resolution. Pattern: `https://raw.githubusercontent.com/verticalogmbh/polesportshop-wissen/<tag>/<file>` mit `<tag>` = letzter `v<X.Y>`-Tag aus GitHub-API (`gh api repos/verticalogmbh/polesportshop-wissen/tags`).
2. `Projekt-Anweisungen.md` Routine-Output-Schritt 2 entsprechend anpassen.
3. Cowork-Tool-Probe: kann Cowork-`web_fetch` GitHub-Raw-URLs lesen? Falls private Repo: Auth-Token-Mechanik klären (analog zu R2-Credentials, E33).
4. Validierung: Cowork-Test-Lauf gegen den dann aktuellen Git-Tag, prüfen ob Stage 0 sauber durchläuft.
*Stolperfallen:*
- Repo-Visibility: Bei privatem Repo braucht Cowork ein GitHub-Token. Bei public Repo: trivial.
- Tag-Aktualität: Wenn ein Build noch nicht gepusht ist, sieht Cowork den alten Stand. Push-Disziplin (siehe WISSENS-UPDATE-PLAYBOOK v2.0 Sektion 5) ist Pflicht.
- Drive-Snapshot bleibt parallel als Read-Only-Archiv erhalten, aber wird ab v1.19 nicht mehr aktualisiert. Klar in der Spec markieren, damit niemand versehentlich Drive-Stand als aktuellen Stand interpretiert.
*Trigger:* eigener Wissens-Update-Trigger für v1.20, sobald Tjorben für die Resolver-Migration bereit ist.

