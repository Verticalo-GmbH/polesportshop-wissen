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
