# Snapshot-Manifest

**Snapshot-Tag:** `v1.21` (Git-Tag, Trial-Findings + Bildpipeline-Reaktivierung)
**Stand:** 2026-05-19 (Berlin)
**Build-Engine:** Claude Code (lokal, Opus 4.7 1M context)
**Vorgänger-Tag:** `v1.20` (Skalierungs-Refactor E91, 2026-05-18)
**Repo:** `https://github.com/verticalogmbh/polesportshop-wissen`
**Branch:** `main`

---

## 1. Build-Trail

**Auftrag (Tjorben-Trigger 2026-05-19):** Trial-Findings aus HotCakes-End-to-End-Lauf 2026-05-18 21:06 (`run_2026-05-18_2106_HotCakes.md`) in v1.21 umsetzen plus Bildpipeline reaktivieren — „bitte Bilderpipeline doch wieder scharf schalten, weil da haben wir ja alles angebunden, was die Architektur angeht und das wäre jetzt natürlich auch eine große Erleichterung."

**Resultat:** 12 Files modifiziert, 0 neu, 0 entfernt. Drei Strang-Themen:
- **E92 — Trial-Findings:** Multi-Kategorie auf 3-Zeilen-Pattern korrigiert (Oberkategorie + Subkategorie + Sara-546), Farb-Lokalisierung DE für 5 Marketing-Farben (Teal→Türkis, Sky→Himmelblau, Cherry→Kirschrot, Emerald→Smaragdgrün, Lime→Limettengrün).
- **E93 — Bildpipeline reaktiviert:** Spec von Stub (3 KB, v2.0) auf Voll-Spec (43 KB, v2.1) aus `v1.19`-Git-Tag rekonstruiert. Stage 5.6 + 5.7 in datenimports.md wieder aktiv. R2-Architektur unverändert.
- Konsistenz-Updates: Charter, Projekt-Anweisungen, CLAUDE.md, BACKLOG, WAWI-IMPORT-WISSEN, SPEC_KONSTANTEN.

**Build-Engine:** Claude Code lokal, Opus 4.7 1M context. Autonom durchgezogen ohne Zwischen-OK-Frage. Pattern: `WISSENS-UPDATE-PLAYBOOK.md` v2.0.1 (Git-basiert).

---

## 2. Was neu generiert wurde (0 Files)

Keine neuen Files in v1.21.

---

## 3. Was modifiziert wurde (12 Files mit Header-Bump)

| Datei | Bump-Typ | Begründung |
|---|---|---|
| `cowork_anweisung_bildpipeline.md` | **Major (v2.0 → v2.1)** | Stub-Reaktivierung: von 3 KB Stub auf 43 KB Voll-Spec aus v1.19-Tag rekonstruiert. ARCHIVIERT-Header durch AKTIV-Header ersetzt. Drive-Resolution → GitHub-Raw aktualisiert. |
| `cowork_anweisung_datenimports.md` | Minor (v2.0 → v2.1) | Stage 5.6 + 5.7 wieder aktiv (E93). Multi-Kategorie auf 3-Zeilen-Pattern (E92). Konventions-Update auf v1.21-Stand. |
| `SPEC_KONSTANTEN.md` | Minor (v1.18 → v1.19) | Sektion 4 + Sektion 9 Self-Check #4 auf 3-Zeilen-Multi-Kategorie korrigiert (E92.1). Sektion 6 Farb-Lokalisierung DE erweitert, „Niemals lokalisieren"-Liste reduziert auf 4 Begriffe (E92.2). Sektion 13 bildpipeline-Status auf AKTIV. Sektion 14 um E92 + E93. |
| `run_brief_daten.md` | Minor (v1.17 → v1.18) | „Was v1.18 ändert"-Block am Anfang. Stage-Tabelle Stage 5.6 + 5.7 aktiv (E93). Sektion 5 Farb-Lokalisierung-Hinweis (E92.2). Sektion 10 Multi-Kategorie auf 3 Zeilen (E92.1). |
| `ENTSCHEIDUNGS-LOG-CRAWLING-DATEN.md` | Minor (v1.18 → v1.19) | Neuer E-Eintrag E92 (Trial-Findings: Multi-Kategorie 3-Zeilen + Farb-Lokalisierung DE). Index erweitert. |
| `ENTSCHEIDUNGS-LOG-BILDPIPELINE.md` | Minor (v1.17 → v1.18) | Neuer E-Eintrag E93 (Bildpipeline reaktiviert, kehrt E63 um). Cluster-Header von „archiviert" auf „reaktiviert". |
| `BACKLOG.md` | Minor (v1.20 → v1.21) | B49 v1.21-Update (Trial-Lauf-Override durch Tjorben), B63 Update mit B65-Teilvalidierung. Neue Einträge B66 (Trial-Lauf-Wiederholung nach v1.21) + B67 (Bildpipeline-Performance-Monitoring). |
| `BACKLOG-ARCHIV.md` | Patch (v1.0 → v1.1) | Hinweis auf v1.21-Trial-Findings-Sektion in BACKLOG.md. |
| `WAWI-IMPORT-WISSEN.md` | Patch (v1.16 → v1.16.1) | Multi-Kategorie-Sektion 4.3 um 3-Zeilen-Pattern-Hinweis erweitert (E92-Bezug). Pilot-Wissens-Substanz unangetastet. |
| `Projekt-Anweisungen.md` | Minor (v2.0 → v2.1) | Bildpipeline ist wieder aktiv (Reaktivierung E93). Operator-Erinnerung „Bilder manuell" entfällt. Stand-Header aktualisiert. |
| `CLAUDE.md` | Minor (v1.0 → v1.1) | File-Map: Bildpipeline-Status von „archiviert" auf „REAKTIVIERT v1.21". Trigger-Registry: Bildpipeline-Trigger wieder aktiv. |
| `PROJEKT-CHARTER.md` | Stand-Update (datums-versioniert, kein v1.X-Header) | Architektur-Rollen-Sektion: Vision-Capability wieder aktiv (E93). Stand-Header auf v1.21-Snapshot. Prinzip 9 leicht angepasst (Bildpipeline-Reaktivierung als E63-Reverse). |

---

## 4. Was unverändert übernommen wurde (10 Wissens-Files)

Diese Files sind im v1.21-Snapshot identisch zum v1.20-Stand:

- `ENTSCHEIDUNGS-LOG-ARCHIV.md`
- `ENTSCHEIDUNGS-LOG-COWORK-INFRA.md`
- `ENTSCHEIDUNGS-LOG-LIVE-TRIAL.md`
- `ENTSCHEIDUNGS-LOG-STIL-CONTENT-A.md`
- `ENTSCHEIDUNGS-LOG-STIL-CONTENT-B.md`
- `LIEFERANTEN-ONBOARDING.md`
- `WISSENS-UPDATE-PLAYBOOK.md`
- `cowork_custom_instructions.md` (v2.0 weiter aktuell — GitHub-Raw-Resolution unverändert)
- `lieferanten_mapping.yaml`

Vollständiger Vergleich via `git diff --stat v1.20..HEAD`.

---

## 5. Was nicht mehr existiert (0 Files)

Keine Files entfernt in v1.21. `cowork_anweisung_bildpipeline.md` ist wieder voll, vorher Stub.

---

## 6. File-Liste mit Sizes und SHA256

| Datei | Size (B) | SHA256 |
|---|---|---|
| `BACKLOG-ARCHIV.md` | 4874 | `abd9bab0c753c873d2097f7ea4572fd13d9202c903d43f1ad5c5c17000d553bb` |
| `BACKLOG.md` | 83988 | `5e29c0b8843bce7cd096aaec2e240ae6b66212416b07ef5a868b4bee48149ef1` |
| `CLAUDE.md` | 9014 | `1a2485e12e31cdec311f8e99aea62d79ccb87770812a3b1b681f180c1c496f74` |
| `ENTSCHEIDUNGS-LOG-ARCHIV.md` | 9600 | `2b2b3fa5fa6648aa0dff909b829b58c4ef6d188834558714dd07c420f0cad846` |
| `ENTSCHEIDUNGS-LOG-BILDPIPELINE.md` | 29488 | `9b4e0dae4a8a6bbccfc910ab6c9db4c6544443613f55771368636a1d4ecf510d` |
| `ENTSCHEIDUNGS-LOG-COWORK-INFRA.md` | 56444 | `6b0ff55eedbb40475678e20c9cb4f64484fe4a93a4b1bc4e195f038057f6797b` |
| `ENTSCHEIDUNGS-LOG-CRAWLING-DATEN.md` | 43188 | `3eeed63ff036b21ae07716c4168c4a77260210e7ac56e646c30ba6c0d6e12c92` |
| `ENTSCHEIDUNGS-LOG-LIVE-TRIAL.md` | 12437 | `ec729b1fd368a251723676e189ead632ab27e141f97e69742910140c961b6ecd` |
| `ENTSCHEIDUNGS-LOG-STIL-CONTENT-A.md` | 33869 | `d13f74a9430154113929a17702f5854241db0f5a429ba6b40c2bc33496ae6397` |
| `ENTSCHEIDUNGS-LOG-STIL-CONTENT-B.md` | 35947 | `d07fb795abb901ecd81c32f18f962296a254cc794ae25e556ad45a49b54f4f73` |
| `LIEFERANTEN-ONBOARDING.md` | 10937 | `88373efc66c92580532fb49adb6e068b3e264c16d80e98e7efd52631b2332ccc` |
| `PROJEKT-CHARTER.md` | 21413 | `e9cdbf9c2cab11e97baad4c53cdd9b0c4eb42db8da07f3a51f1b4b2088042191` |
| `Projekt-Anweisungen.md` | 7966 | `39adf54b317a37715413c4f6455444f7a842647e1a575e67e8b98187ca1e7b99` |
| `SPEC_KONSTANTEN.md` | 54145 | `4ecd8718cc6192cf97967de85fd86256e4024e4fee67db32245c0db4ab17e8eb` |
| `WAWI-IMPORT-WISSEN.md` | 75816 | `52c7ee645cba33d7e23cbb1b1a93f16e428f18be1ac17f0c73cd807d2c51d71a` |
| `WISSENS-UPDATE-PLAYBOOK.md` | 15704 | `fb8d6cd81de9cb225542235b2ede1bb417e2d51ceea903c1d182bf6281ae308b` |
| `cowork_anweisung_bildpipeline.md` | 42594 | `4ff708a27101d5d5c4e7247108acbd4a914414bf2aacfbc8f46575d16288c1aa` |
| `cowork_anweisung_datenimports.md` | 24676 | `ac8bf70685483324d40b376174542c4c2be3f4fcd7973e2be0a970878a9cea07` |
| `cowork_custom_instructions.md` | 11308 | `be87644eb7b3e836238e119c23a0baa4da23d70703ffd4129c0e57a433f67446` |
| `lieferanten_mapping.yaml` | 25697 | `277715d3923c6f04e6136b30716ec79eb035ce498a4ca6ec10e0f08055ac9ea3` |
| `run_brief_daten.md` | 36073 | `d4c9f2bf720986ee1c20119147e51210966d65e30e7f051dadbb551f16e68a6a` |

---

## 7. Anzahl-Marker

- **Wissens-Files in v1.21:** 21 (alle in Sektion 6 außer `_MANIFEST.md`)
- **Plus Manifest:** 22 Files total — unverändert ggü. v1.20
- **Plus Repo-Meta:** `README.md` + `.gitignore` (kein Wissens-File)

---

## 8. Self-Check-Ergebnis (WSC-1 bis WSC-17)

| Punkt | Status | Detail |
|---|---|---|
| WSC-1 (Größe ≤ 50 KB Soft-Limit) | WARN | 4 Files >50 KB: `BACKLOG.md` (84 KB), `WAWI-IMPORT-WISSEN.md` (76 KB), `ENTSCHEIDUNGS-LOG-COWORK-INFRA.md` (56 KB), `SPEC_KONSTANTEN.md` (54 KB). In Git-Welt kein Upload-Killer (E87). |
| WSC-2 (Append/Patch-File-Verbot) | PASS | Keine Append/Patch-Files. |
| WSC-3 (Erwartete File-Liste) | PASS | 21 Wissens-Files + 1 Manifest, exakt wie SPEC_KONSTANTEN Sektion 13 v1.19. |
| WSC-4 (Cross-References zu ARCHIV) | PASS | E-Nummer-Konsistenz: neue E92 (CRAWLING-DATEN), E93 (BILDPIPELINE). ARCHIV-Einträge unverändert. |
| WSC-5 (Neue Sektionen in SPEC_KONSTANTEN) | PASS | Sektion 4 + Sektion 6 + Sektion 9 + Sektion 13 + Sektion 14 aktualisiert. |
| WSC-6 (Kein alter Monolith) | PASS | Kein Cluster-Split in v1.21. |
| WSC-7 (Git-Status clean nach Commit) | wird nach Commit PASS | Vor Commit: 12 M (inkl. Manifest). |
| WSC-8 (Build-Target ≤ 40 KB für modifizierte Files) | WARN | 5 modifizierte Files >40 KB: BACKLOG, WAWI-IMPORT, ENTSCHEIDUNGS-LOG-CRAWLING-DATEN, SPEC_KONSTANTEN, cowork_anweisung_bildpipeline (42 KB knapp). Akzeptabel. |
| WSC-9 (UTF-8-Sanity) | PASS | (verifiziert in v1.19/v1.20, keine Encoding-Änderung in v1.21). |
| WSC-10 (Manifest enthält alle Files mit Hashes) | PASS | 21 Wissens-Files mit SHA256 in Sektion 6. |
| WSC-11 (Manifest-Build-Trail vollständig) | PASS | Sektionen 1-5. |
| WSC-12 (Known-Exceptions dokumentiert) | PASS | Siehe Sektion 9. |
| WSC-13 (Manuelle Aktionen vermerkt) | PASS | Siehe Sektion 11. |
| WSC-14 (Notes zum Build-Pattern) | PASS | Siehe Sektion 12. |
| WSC-15 (Tag-Konvention) | wird vor Tag PASS | `v1.21` folgt `vX.Y`. |
| WSC-16 (Push erfolgreich) | wird nach Push PASS | Verifikation via Remote-Tag-Check. |
| WSC-17 (Header-Bump-Pflicht E86) | PASS | 12 modifizierte Files, alle gebumpt: Major×1 (bildpipeline.md Voll-Reaktivierung), Minor×7, Patch×2, Stand-Update×2 (Charter, WAWI). |

**Gesamt vor Commit:** 13× PASS, 2× WARN (known-exceptions), 2× pending (WSC-7/15). Nach Commit+Tag+Push: 16× PASS, 2× WARN, 0× FAIL.

---

## 9. Known-Exceptions / Geplante Folge-Splits

- `BACKLOG.md` 83988 B (>50 KB) — wächst durch Status-Updates. Mit BACKLOG-ARCHIV.md entschärft. Split bei N≥20 aktive Lieferanten neu evaluieren.
- `WAWI-IMPORT-WISSEN.md` 75816 B (>50 KB) — B61 (deferred). In Git-Welt kein Upload-Killer.
- `ENTSCHEIDUNGS-LOG-COWORK-INFRA.md` 56444 B (>50 KB) — durch E87 + E91 gewachsen. Monitoring.
- `SPEC_KONSTANTEN.md` 54145 B (>50 KB) — durch v1.21-Updates Sektion 4/6/9/13/14 etwas gewachsen. B54 (deferred).
- `cowork_anweisung_bildpipeline.md` 42594 B (>40 KB Build-Target, <50 KB Soft-Limit) — Voll-Spec aus v1.19-Tag rekonstruiert, kein Pain.

---

## 10. Tool-Anomalien & Notes zum Build-Pattern

**Pattern v2.0.1 hat sich wiederholt bewährt.** v1.21 ist ein klassischer Folge-Build (Trial-Findings + Reaktivierung) — 12 Files modifiziert in einem Cycle ohne Tool-Use-Limit. `git show v1.19:<file>` als File-Restore-Mechanik ist Git-natives Pattern, brauchte keinen Sonderweg.

**Bemerkung zum Vorgänger-Manifest (v1.20):** Sektion 12 listete „autonome Entscheidung 10 — Resolver-Migration für Cowork ohne Probe-Test in v1.20-Build (Probe-Test ist Sache des ersten v1.20-Cowork-Laufs, B65)". Trial-Lauf 2026-05-18 21:06 hat B65 teilvalidiert: GitHub-Raw-Read in 1,25 s für 4 Files. **Aber:** der Lauf-Bericht erwähnt keine Auth-Mechanik, und das Repo ist aktuell privat — entweder hat Cowork einen impliziten Auth-Pfad oder der Trial-Lauf hat Drive-Übergang genutzt. Klärung im v1.21-Trial-Lauf relevant.

**Empfehlungen für nächste Builds (v1.22+):**
- **B66 validieren beim v1.21-Trial-Lauf:** Multi-Kategorie 3-Zeilen-Pattern → Oberkategorie im Shop, Farb-Lokalisierung DE → Türkis/Himmelblau in Artikelnamen, Bildpipeline-Output → R2-URLs in Spalten Bild 1-10, Vision-Pose-Sortierung Hero/Back/Side korrekt.
- **B67 monitoren:** Vision-Token-Verbrauch, ob `auto_vision` für HotCakes weiter sinnvoll oder ob `manufacturer_order` reicht.
- **Repo-Visibility-Klärung:** privat lassen mit GitHub-Token (B65-Pfad), oder public (E49-Pole-Junkie-Risiko-Trade-off). Tjorbens Entscheidung.

---

## 11. Manuelle Aktionen für Tjorben

**Aktion 1 — Drive-Übergangs-Folder aktualisieren** (Pflicht vor v1.21-Cowork-Lauf, falls Repo weiter privat):

In Drive `Wichtig: Claude Backup/`: bestehenden `Version_2026-05-18_v1.20_trial/` löschen oder umbenennen, neuen Folder `Version_2026-05-19_v1.21_trial/` anlegen. Aus dem lokalen Repo per Drag-and-Drop reinkopieren:
- `run_brief_daten.md` (v1.18, 36 KB)
- `SPEC_KONSTANTEN.md` (v1.19, 54 KB)
- `lieferanten_mapping.yaml` (unverändert, 26 KB)
- `cowork_anweisung_bildpipeline.md` (v2.1, 43 KB — neu nötig wegen Bildpipeline-Reaktivierung)

**Aktion 2 — Cowork-UI Global Instructions** (falls noch nicht v2.0):
Inhalt durch `cowork_custom_instructions.md` v2.0 ersetzen — unverändert ggü. v1.20, kein Update nötig wenn schon v2.0.

**Aktion 3 — Egress-Allowlist** (optional):
Bei granularem Modus: `raw.githubusercontent.com`, `api.github.com`, `hotcakespolewear.com`, plus für Bildpipeline `d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com` und `pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev` und `cdn.shopify.com`. Bei „All domains"-Modus (B29-Workaround): nichts zu tun.

**Aktion 4 — WaWi-Cross-Selling-Beziehungen löschen** (falls die 21 Live-Trial-Modelle noch in WaWi sind):
Bei Re-Anlage über v1.21-Trial: vorab CS-Beziehungen in WaWi händisch löschen, sonst Duplikate (B49 weiter unverifiziert). Aktuell laut Tjorbens Aussage 2026-05-19: alle 21 Trial-Modelle in WaWi gelöscht — kein Cleanup nötig.

---

## 12. Autonome Entscheidungen (zum Review)

1. **bildpipeline.md aus `v1.19`-Tag rekonstruiert statt neu geschrieben** — `git show v1.19:<file>` war der saubere Pfad, die v1.6-Spec ist validiert (Arachne-Bottom-Black 2026-05-15), kein Rewrite-Risiko. Nur Drive-Resolution-Stellen + Archivierungs-Header gepatched.
2. **Major-Bump für bildpipeline.md (v2.0 → v2.1)** — Begründung: Stub → Voll-Spec ist strukturell, ARCHIVIERT-Header → AKTIV-Header. Minor wäre auch vertretbar, Major ist klarer.
3. **Farb-Lokalisierungs-Tabelle erweitert um 4 neue Marketing-Begriffe** (Sky, Cherry, Emerald, Lime) zusätzlich zum expliziten Tjorben-Beispiel Teal. Rationale: bei nächstem Lieferanten-Onboarding sind Cherry/Emerald/Lime wahrscheinliche Farben (Pole-Wear Mode-Vokabular). Tjorben prüft im Review.
4. **„Nude, Mauve, Tan, Skin" bleiben identisch in allen 5 Sprachen** — keine etablierten DE-Pendants (Altrosa für Mauve wäre semantisch nicht identisch). Bei Bedarf später erweitern.
5. **B49 bleibt offen statt validiert markieren** — Trial-Lauf 2026-05-18 21:06 hat den Re-Import-Schutz mit Tjorben-Override umgangen, nicht echten Re-Import getestet. Sauberkeit > Optimismus.
6. **B65 (GitHub-Raw-Probe) auf „teilvalidiert" statt „erledigt"** — Trial-Lauf hat Raw-Read durchgeführt, aber Auth-Mechanik bei privatem Repo unklar (Drive-Übergang oder anderer Pfad?). Klärung im v1.21-Trial.
7. **Multi-Kategorie zurück auf 3 Zeilen statt 2** — Tjorbens Direktive ist klar (Oberkategorie fehlte). E89-„WaWi resolved Pfad selbst"-Annahme war Hypothese, nicht validiert. Zurück zum funktionierenden E57-Doppel-Pattern + Sara-3.-Zeile.
8. **WAWI-IMPORT-WISSEN nur Patch-Bump (v1.16 → v1.16.1)** — die WaWi-Mechanik-Substanz ist unverändert, nur ein Hinweis zur 3-Zeilen-Erweiterung ergänzt. Patch (Cross-Reference-Update) trifft besser als Minor.
9. **PROJEKT-CHARTER ohne v1.X-Header** — datums-versioniert (Konvention der Charter-Datei). Stand-Update reicht für E86-Compliance.
10. **Standalone-Bildpipeline-Trigger („Verarbeite Bilder von X") in CLAUDE.md erwähnt** — historische Auslösungs-Variante aus v1.6-Spec, falls Tjorben mal nur Bilder nachladen will ohne Daten-Pipeline-Lauf. Klein, aber komplettiert das Bild.

---

## 13. Verhältnis zum Vorgänger-Snapshot

v1.20 → v1.21 ist ein **Korrektur- + Reaktivierungs-Build**. v1.20 lieferte die Skalierungs-Base; v1.21 zieht aus dem ersten produktiven Trial-Lauf zwei Lessons Learned (Multi-Kategorie + Farb-Lokalisierung) und nutzt die stabile Datenpipeline-Lage, um die Bildpipeline aus der E63-Archivierung zurückzuholen. Damit ist die volle 5-CSV-Pipeline + Bilder + R2-Storage wieder Produktions-Stand wie vor E63.

Ab v1.22 sind weitere Iterationen erwartet: neue Lieferanten onboarden (LIEFERANTEN-ONBOARDING.md als Anker), Findings aus echten Läufen einarbeiten.
