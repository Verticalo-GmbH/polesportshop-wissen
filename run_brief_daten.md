# RUN-BRIEF: Daten-Pipeline (E68, offiziell in v1.12 verankert, Stand 2026-05-18, v1.18)

Dieser Brief ist die kompakte operative Spec für einen reinen Daten-Lauf. Er
ersetzt das Laden von `WAWI-IMPORT-WISSEN.md` und
`cowork_anweisung_datenimports.md` in Stage 0. Die zwei Files würden Coworks
interne Sub-Agent-Extraction-Schwelle triggern (A8, ~50 KB), was den Lauf
massiv verlangsamt. Mit diesem Brief im Snapshot lädst du in Stage 0
nur drei Files: dieser Brief, **SPEC_KONSTANTEN.md** und
**lieferanten_mapping.yaml** — alle unter der Schwelle.

Bei Konflikten zwischen diesem Brief und SPEC_KONSTANTEN.md gewinnt
SPEC_KONSTANTEN.md (kanonisch nach Charter-Prinzip 11). Bei Unsicherheit:
STOPP + User-Frage, niemals raten (Charter-Prinzip 10, E59).

**Was v1.18 ändert (NEU 2026-05-18, Trial-Findings v1.21 E92 + E93):**
- **Multi-Kategorie korrigiert (E92 verfeinert E89):** pro Artikel **3 Zeilen** statt 2 — (a) Oberkategorie `Pole Dance Kleidung` (Ebene 2 leer), (b) spezifische Subkategorie (Pole Dance Tops/Shorts/Bodysuits/etc.), (c) Sara-Pflicht-Zeile `Intern > Neue Artikel für Sara` (Key 546). Trial-Lauf 2026-05-18 21:06 zeigte: Oberkategorie fehlte im Shop — WaWi resolved den Pfad NICHT automatisch über die Subkategorie. E57-Doppel-Pattern bleibt gültig, Sara kommt als 3. Zeile dazu. Self-Check #4 entsprechend.
- **Farb-Lokalisierung DE (E92):** Marketing-Farben mit DE-Pendant werden im deutschen Artikelnamen lokalisiert. Teal→Türkis, Sky→Himmelblau, Cherry→Kirschrot, Emerald→Smaragdgrün, Lime→Limettengrün. Marketing-Farben ohne sinnvolles DE-Pendant bleiben identisch: Nude, Mauve, Tan, Skin. Print-Familien (Original, Heat) bleiben überall identisch. Volle Tabelle in SPEC_KONSTANTEN Sektion 6.
- **Bildpipeline reaktiviert (E93, kehrt E63 um):** Stage 5.6 + 5.7 wieder aktiv. Cowork ruft Bildpipeline als Sub-Process auf, R2-URLs werden in die Stammdaten-CSV-Spalten Bild 1-10 eingebettet (E46-Mechanik unverändert). Crop-Profile (E45), Vision-Pose-Sortierung (E45), Magic-Byte-Detection — alles wie in v1.6 spezifiziert. Cowork-Anweisung-Bildpipeline ist auf v2.1 aktiv. Tjorben pflegt Bilder NICHT mehr manuell in WaWi.

**Was v1.17 änderte (2026-05-18, im Rahmen v1.20-Skalierungs-Refactor E91):**
- Wissens-Resolution: GitHub-Raw-URL statt Drive-Folder-Path (E87/E91/B63 erledigt v1.20). Tag-Pattern `vX.Y` auf `main`. Beispiel: `https://raw.githubusercontent.com/verticalogmbh/polesportshop-wissen/v1.20/run_brief_daten.md`.
- Stage-0-File-Count unverändert (3 Files: dieser Brief, SPEC_KONSTANTEN, lieferanten_mapping). Lade-Mechanik via `web_fetch` oder `curl/requests` auf Raw-URL.

**Was v1.16 änderte (2026-05-18, F2-F6-Fixes aus HotCakes-Run-Report 2026-05-18):**
- F2 (E89): Kategorie-Pattern korrigiert — pro CSV-Zeile nur die spezifischste Subkategorie (WaWi resolved den Pfad über die Hierarchie). Plus: jeder neue Artikel bekommt zusätzlich `Intern > Neue Artikel für Sara` (WaWi-Key 546) für den Sara-Review-Workflow. Self-Check Punkt 4 entsprechend umformuliert.
- F3: Artikelgewicht-Default 0.05 kg + Versandgewicht-Default 0.05 kg pro Kleidungsstück in der Stammdaten-CSV (Sektion 10 unten).
- F4 (B57): HTML-Entity-Regression behoben — Latin-1-Umlaute (ß, ä, ö, ü, é, à etc.) bleiben Unicode. HTML-Entities NUR für Zeichen außerhalb Latin-1 (z.B. ✓ = `&#10004;`, ➔ = `&#10148;`). Korrigiert die v1.15-Regression `gro&szlig;e` statt `große`.
- F5 (B58): „Unser Model"-Phrase raus aus `size_and_fit`. Modelnamen aus Crawl-Body ziehen (z.B. Yifan, Vika, Elena bei HotCakes). Bei mehreren Models pro Artikel: erstes Model im Crawl-Body verwenden. Bei null Modelname: neutralere Formulierung („Das Model trägt...") oder Phrase weglassen.
- F6: TARIC-Code-Default `62114390` für Pole-Bekleidung in `lieferanten_mapping.yaml` als Default pro Lieferant. Wird in Stammdaten-CSV-Spalte „TARIC" eingetragen.

**Was v1.15 änderte (2026-05-17, nach Live-Trial-Runs Batch 1+2 HotCakes, 21 Modelle in WaWi):**
- Stage 0.5 Pre-Run Scope-Analyse (E83) — Cowork schätzt Token/Wallclock-Verbrauch eigenständig und entscheidet autonom über Batch-Aufteilung (E81-Autonomie-Hoheit), Batch-Plan im Lauf-Bericht
- Stage 5.8 Cross-Selling jetzt mit Kinder-Replikation (E80-Erweiterung): linke Spalte (ArtNr) erhält Vater UND alle Kinder, rechte Spalte (Cross-Seller) bleibt strikt Vater
- Modell-Stamm-Schlüssel bei Farbvarianten inkludiert Farbe: `(modell_basis, farbe_im_namen)` statt nur `modell_basis` (Bug-Fix Batch 2 Iter. 1)
- Stilprinzip E82 (verschärft E74): Em-Dash bleibt verboten, Doppelpunkt im Fließtext NEU verboten, keine Meta-Einleitungs-Sätze
- Familien-erhaltende Split-Regel (E84): Outfit-Pair-Familien bleiben pro Batch zusammen, Cross-Selling-Stage 5.8 läuft im letzten Batch über alle Modelle vereint
- AP9-AP12 Anti-Patterns: Workflow-Frage statt autonomer Entscheidung, CSV/Bericht nach Drive uploaden, Datei-Naming ohne Nummer-Präfix, leere CSV mit nur Header
- Datei-Naming-Konvention für CSVs: `<NR>_<Typ>_<LIEFERANT>_<YYYY-MM-DD_HHMM>.csv`

---

## 1. Stage-0-Lade-Regel

In Stage 0 lädst du genau **2 Files** aus dem aktuellen Snapshot:

- `SPEC_KONSTANTEN.md` — Schema, SEO-Templates, Sprach-Lookups, Merkmalwerte, Self-Check, AP1-AP12
- `lieferanten_mapping.yaml` — Lieferanten-Kontext

NICHT laden in Stage 0: `WAWI-IMPORT-WISSEN.md`, `cowork_anweisung_datenimports.md`,
`PROJEKT-CHARTER.md`, `ENTSCHEIDUNGS-LOG.md`, `BACKLOG.md`,
`cowork_anweisung_bildpipeline.md`, `Projekt-Anweisungen.md`,
`cowork_custom_instructions.md`.

Falls du eine echte Architektur-Klärung brauchst (Charter-Prinzip-10-STOPP,
Mapping-Lücke, unklare Begründung), darfst du Charter/LOG/Backlog lazy
nachladen — das ist legitime Klärung. Im Lauf-Bericht dokumentieren.

---

## 2. Pipeline-Stages

| Stage | Was |
|---|---|
| 1 | Input erkennen & laden (Modus aus Trigger: Crawl/Drive/Excel/PDF/Mail/Hybrid) |
| 2 | Daten extrahieren — **vollständiger Lieferanten-Datensatz** (E80: für Cross-Selling-Stage werden alle Produkte gebraucht, nicht nur Trigger-Modelle) |
| 3 | Daten normalisieren (Lieferanten-Format → 48-Spalten-Schema laut SPEC_KONSTANTEN Sektion 1) |
| **0.5** | **Pre-Run Scope-Analyse (NEU v1.15, E83):** Token/Wallclock-Schätzung für den geplanten Lauf eigenständig durchführen. Bei Schätzungen > 100k Output-Tokens oder > 8 Min Wallclock pro Stage: Batch-Aufteilung im Lauf-Bericht dokumentieren mit Begründung. **Familien-erhaltende Split-Regel (E84):** Outfit-Pair-Familien (gleicher Modell-Stamm + alle Farben + Top/Bottom) bleiben pro Batch zusammen. **E81-Autonomie:** Entscheidung autonom, keine User-Rückfrage. Im Bericht: Batch-Plan, geschätzte Tokens/Wallclock pro Batch, welche Familien in welchem Batch landen. Stage 5.8 Cross-Selling läuft im letzten Batch über alle bisher importierten Modelle vereint. |
| 4 | Pricing berechnen — siehe Sektion 8 unten |
| 5 | Mehrsprachige Felder ableiten (DE-Quelle → EN/FR/IT/ES via E58-Sprach-Lookup in SPEC_KONSTANTEN Sektion 6). **Farb-Lokalisierung KORRIGIERT v1.18 (E92):** Marketing-Farben mit DE-Pendant ins Deutsche übersetzen (Teal→Türkis, Sky→Himmelblau, Cherry→Kirschrot, Emerald→Smaragdgrün, Lime→Limettengrün). Marketing-Farben ohne DE-Pendant bleiben identisch in allen 5 Sprachen (Nude, Mauve, Tan, Skin). |
| 5.5 | HTML-Texte für Attribute (markentext, artikeldetails, material_and_care, size_and_fit) generieren gemäß Stil-Briefing Sektion 9. **material_and_care clean Pattern (E78, NEU v1.14): 2 Paragraphen, P1 Stoffzusammensetzung, P2 Pflegehinweise — kein E74-Stil hier.** |
| 5.6 | **Bildpipeline-Sub-Process aufrufen (REAKTIVIERT v1.21, E93):** `cowork_anweisung_bildpipeline.md` v2.1 starten, Map `{artikelnummer: [bild_urls]}` zurückbekommen. R2-Upload für Verarbeitete + Originale, Crop nach Lieferanten-`crop_profile`, Pose-Sortierung nach `pose_sort`. Lieferanten-Drive-`_Eingang` als alternative Quelle bei manuellen Uploads. |
| 5.7 | Bild-URLs aus Map in Stammdaten-CSV Spalten Bild 1-10 einbetten. Auf Vater UND alle Kinder duplizieren (E34/E46). Bei <10 Bildern: übrige Spalten leer (B30 weiter unverifiziert, aber im aktuellen Verhalten unproblematisch). |
| 5.8 | **Cross-Selling-Beziehungen ableiten (E80, erweitert v1.15):** „Vervollständige Dein Outfit" (Top↔Bottom gleiche Farbe) + „Ähnliche Artikel" (gleiches Modell, andere Farbe). **Linke Spalte (Artikelnummer) wird auf Vater UND alle Kinder repliziert; rechte Spalte (Cross-Seller) bleibt strikt Vater.** Beide Richtungen (A↔B). Voller Datensatz aus Stage 2. Modell-Stamm-Schlüssel bei Farbvarianten: `(modell_basis, farbe_im_namen)` — nicht nur `modell_basis`. Details: SPEC_KONSTANTEN Sektion 12. |
| 6 | Validierung: **16-Punkte-Self-Check** aus SPEC_KONSTANTEN Sektion 9 (12 alte + Punkt 13 Originalitäts-Check (E77) + Punkte 14-16 Cross-Selling-Check, **Punkt 15 + 16 neu formuliert v1.15** für Kinder-Replikation). Bei Fehler: STOPP + User. |
| 7 | **5 CSVs** im Workspace schreiben (Stammdaten/Variationen/Merkmale/Attribute/CrossSelling) mit Datei-Naming-Konvention (AP11, v1.15), keine leeren CSVs ausgeben (AP12, v1.15), Lauf-Bericht erstellen, via `present_files` ausgeben |

---

## 3. Globale CSV-Format-Regeln (für alle 5 CSVs)

| Setting | Wert |
|---|---|
| Encoding | **UTF-8 mit BOM** |
| Trennzeichen | `;` (Semikolon) |
| Quote-Zeichen | `"` (Doppel-Anführungszeichen) |
| Quoting | minimal für Stammdaten/Variationen/Merkmale/CrossSelling; **`QUOTE_ALL`** für Attribute (HTML mit Sonderzeichen) |
| Zeilenende | **CRLF** (`\r\n`) |
| Dezimaltrennzeichen | **Komma** (`12,50` nicht `12.50`) — DE-Locale |
| Datei-Endung | `.csv` |

Abweichungen produzieren reproduzierbar Import-Fehler.

---

## 4. Reihenfolge der Imports (für den Lauf-Bericht relevant)

Die 5 CSVs werden in WaWi in genau dieser Reihenfolge importiert. Sie müssen
in dieser Reihenfolge generierbar sein:

1. **Stammdaten** (Artikel > Artikeldaten) — inkl. Lieferantenblock und 10 Bild-Spalten
2. **Variationen** (Artikel > Variationen) — Sprach-Werte für Größe
3. **Merkmale** (Artikel > Artikelmerkmale) — Filter-Werte (Farbe, Größe, Style)
4. **Attribute** (Artikel > Artikelattribute) — HTML-Reichtext in 5 Sprachen
5. **Cross-Selling** (Artikel > Cross-Selling-Artikel — eigener Import-Typ, NEU v1.14) — 3 Spalten: `Artikelnummer;Artikelnummer Cross-Seller;Cross-Selling-Gruppe`. **Linke Spalte: Vater UND alle Kinder (v1.15-Erweiterung E80). Rechte Spalte: strikt Vater.** Details: SPEC_KONSTANTEN Sektion 12.

Stammdaten-Schema = 48 Spalten, kanonisch in SPEC_KONSTANTEN.md Sektion 1.

**Datei-Naming-Konvention (AP11, NEU v1.15):** `<NR>_<Typ>_<LIEFERANT>_<YYYY-MM-DD_HHMM>.csv`. Beispiele:
- `1_Stammdaten_HotCakes_Batch1_2026-05-17_1500.csv`
- `2_Variationen_HotCakes_Batch1_2026-05-17_1500.csv`
- `3_Merkmale_HotCakes_Batch1_2026-05-17_1500.csv`
- `4_Attribute_HotCakes_Batch1_2026-05-17_1500.csv`
- `5_CrossSelling_HotCakes_Batch1_2026-05-17_1500.csv`

Bei Batch-Aufteilung im Dateinamen einbauen (`Batch1`, `Batch2`). Reihenfolge-Nummer 1-5 zwingend als erstes Element.

---

## 5. CSV 2: Variationen (12 Spalten)

```
Artikelnummer;Variationsname;Darstellungsform;Variationswertname;
Global-Englisch: Variationsname;Global-Englisch: Variationswertname;
Global-Französisch: Variationsname;Global-Französisch: Variationswertname;
Global-Italienisch: Variationsname;Global-Italienisch: Variationswertname;
Global-Spanisch: Variationsname;Global-Spanisch: Variationswertname
```

- Eine Zeile pro Größen-Variante (= pro Kind-Artikelnummer-Suffix)
- `Artikelnummer` = **Vater-Artikelnummer** (z.B. `HC-Hekate-Bodysuit`, ohne Größen-Suffix)
- `Darstellungsform` = `DROPDOWN`
- Variationsname-Übersetzung: Größe / Size / Taille / Taglia / Talla
- Variationswerte (XS, S, M, L, XL) sind universal — werden trotzdem in allen 5 Sprachen explizit gepflegt

---

## 6. CSV 3: Merkmale (4 Spalten)

```
Lieferant;Artikelnummer (Lieferant);Merkmalname;Merkmalwertname 1
```

- Mehrere Zeilen pro Artikel (eine pro Merkmal-Wert)
- **Auf Vater UND alle Kinder explizit dupliziert** (E34 — JTL erbt nichts implizit)
- Nur Deutsch in der CSV. Übersetzungen liegen an WaWi-Merkmalwert-Stammdaten

**Erlaubte Merkmalnamen für Kleidung (4 in WaWi belegt):**

| Merkmalname | Wer hat ihn | Erlaubte Werte |
|---|---|---|
| `Farbe Kleidung` | Vater + alle Kinder | Beige, Blau, Braun, Gelb, Gold, Grau, Grün, Lila, Pink, Rot, Schwarz, Silber, Weiß |
| `Größe Kleidung` | nur Kinder | XS, S, M, L, XL, 2XL |
| `Style Tops` | Vater + alle Kinder (bei Top oder Bodysuit) | Bodysuit, Crop Top, High Neck, Open Back, Riemchentop, Rundausschnitt, T-Shirt, Triangle Ausschnitt. Mehrere Werte → mehrere Zeilen |
| `Style Shorts` | Vater + alle Kinder (bei Shorts/Bottoms) | Cheeky, Classic Hot Pants, High Leg, High Waist, Leggings, Low Waist, Mid Waist, Riemchenshorts. Mehrere Werte → mehrere Zeilen |

**Wichtig:** `Style Bodysuits` und `Style Leggings` existieren NICHT als Merkmalsnamen.
Bodysuits → `Style Tops` mit Wert "Bodysuit" plus weitere Top-Style-Werte. Leggings →
`Style Shorts` mit Wert "Leggings".

**Größen-Konvention pro Lieferant** (aus `lieferanten_mapping.yaml` Feld `groessen_konvention`):
- `standard`: jede Größe einzeln
- `kombi_reduziert_auf_kleinste` (HotCakes, E27): Kombi-Größe wird auf kleinste reduziert (XS/S → XS, S/M → S)

**Merkmalwert außerhalb erlaubter Liste** → Lauf abbrechen, User-Frage. Keine neuen
Werte autonom anlegen.

---

## 7. CSV 4: Attribute (8 Spalten, alle Felder gequotet)

```
Lieferant;Artikelnummer (Lieferant);Attributname;Attributwert;
Englisch: Attributwert;Französisch: Attributwert;Italienisch: Attributwert;Spanisch: Attributwert
```

**Quoting:** `csv.QUOTE_ALL` — jedes Feld in `"..."`. Pflicht, weil Werte HTML mit
Sonderzeichen und Anführungszeichen enthalten.

**Eine Zeile pro Artikel × Attribut, auf Vater UND alle Kinder dupliziert** (E34).
Ein Stamm aus 1 Vater + 5 Kindern mit 4 Attributen → 24 Zeilen.

**Mindest-Set pro Artikel:** `markentext`, `artikeldetails`, `material_and_care`,
`size_and_fit`. Übrige je nach Produkt-Relevanz.

| Attributname | Inhalt | Format | **Stil-Modus** |
|---|---|---|---|
| `markentext` | Brand-Pitch (80-150 Wörter, evergreen) | `<h2>Marke</h2><p>Story</p>` | **E74-aspirational** (E72/E79 Caching im Mapping) |
| `artikeldetails` | Tagline + Fließtext + Features (100-300 Wörter) | siehe Stil-Briefing Sektion 9 | **E74-aspirational** |
| `material_and_care` | **2 Paragraphen: P1 Stoffzusammensetzung, P2 Pflegehinweise** | `<p>...</p><p>...</p>` | **clean/funktional (E78, NEU v1.14)** |
| `size_and_fit` | Passform + Modellgröße + Tragehöhe. **Modelname aus Crawl-Body (F5/B58, v1.16):** statt „Unser Model trägt..." → `<Modelname> trägt Größe S bei 1,72 m...` (z.B. Yifan, Vika, Elena bei HotCakes). Bei mehreren Models: erstes Model im Crawl-Body. Bei null Modelname: „Das Model trägt..." oder Phrase weglassen. **Keine Größentabelle** | Plaintext oder leichtes HTML | E74-aspirational gemäßigt |
| `anwendung` | 3-8 Imperativ-Schritte (wenn relevant) | `<ul class="check"><li>Schritt</li></ul>` | klar/funktional |
| `faqs` | mehrere Blöcke à 30-80 Wörter (wenn relevant) | wiederholte `<h3>Frage?</h3><p>Antwort</p>` | warm-funktional |
| `inhaltsstoffe` | Komma-Liste (wenn relevant) | `<p>` | clean |

**`material_and_care` clean Pattern (E78, NEU v1.14)** — Pflicht-Aufbau:
```html
<p>85% Polyamid, 15% Elasthan.</p>
<p>Handwäsche bei 30°C, nicht bleichen, nicht in den Trockner, nicht bügeln, nicht chemisch reinigen.</p>
```
P1 = Stoffzusammensetzung (EU-Pflicht), P2 = Pflegehinweise. **Kein E74-Stil hier** — keine sinnlichen Adjektive, keine Verkaufs-Hinweise, keine Begründungen. Nur Fakten + Anweisungen. Du-Form oder förmlicher Imperativ, pro Lieferant konsistent.

**Mehrsprachigkeit:** alle 5 Sprachen voll ausformuliert (E73). Eigennamen (Modellnamen, Print-Familien, „Crop Top", „High Waist") unverändert.

---

## 7.1 CSV 5: Cross-Selling (3 Spalten, NEU v1.14, E80, erweitert v1.15)

```
Artikelnummer;Artikelnummer Cross-Seller;Cross-Selling-Gruppe
```

**JTL-Ameise-Import-Typ:** „Cross-Selling-Artikel" (eigener Import, NICHT Teil von Artikeldaten).

**Eine Zeile pro Beziehung × Identifizierungs-ID.** Symmetrie: jede Beziehung beidseitig (A↔B + B↔A in zwei Zeilen).

**v1.15-Erweiterung (E80):** Die linke Spalte `Artikelnummer` wird **auf Vater UND alle Kinder repliziert**. Die rechte Spalte `Artikelnummer Cross-Seller` bleibt **strikt Vater**. Das bewirkt: ein Kunde, der ein Kind-Artikel (Größe S, M, L...) anschaut, bekommt im Shop dieselben Cross-Selling-Vorschläge wie auf dem Vater-Artikel — und der Verweis geht immer auf die Vater-Karte, nicht auf eine Kind-Größe.

Pro bidirektionale Beziehung also nicht 2 Zeilen sondern **2 × (1 Vater + 4 Kinder) = 10 Zeilen**. Bei 21 Modellen mit Outfit-Pair-Beziehungen kommt man rechnerisch auf etwa 180 statt 36 Zeilen.

**Cross-Selling-Gruppen (Stand 2026-05-17, existieren in WaWi):**

| Gruppen-Name (exakter Wert) | Algorithmus |
|---|---|
| `Vervollständige Dein Outfit` | gleicher Modell-Stamm + gegensätzlicher Typ (Top↔Bottom) + gleiche Farbe |
| `Ähnliche Artikel` | gleicher Modell-Stamm + gleicher Typ + andere Farbe |

**Modell-Stamm-Schlüssel** (Algorithmus-Präzisierung v1.15): `(modell_basis, farbe_im_namen)` bei Farbvarianten, nicht nur `modell_basis`. Bug-Beleg: Batch 2 Iter. 1 fand für Outfit-Pair-Stamm „Savanna" nur 14 statt 20 Zeilen, weil 3 Farb-Geschwister (Black/Skin/Emerald) zusammengefasst als ein Stamm gewertet wurden. Mit Farbe als Teil des Schlüssels: jedes (Savanna, Black) Top hat exakt einen Bottom-Match in (Savanna, Black) und nicht in (Savanna, Skin).

**Voller Datensatz nötig:** Stage 2 muss den vollen Lieferanten-Crawl gehalten haben (z.B. alle 124 HotCakes-Produkte), nicht nur die Trigger-Modelle — sonst werden Beziehungen zu nicht-getriggerten Schwester-Artikeln verpasst.

**Beispiel-CSV (3 Modelle aus voller Lieferung mit Schwester-Farbe, mit Kinder-Replikation v1.15):**
```csv
Artikelnummer;Artikelnummer Cross-Seller;Cross-Selling-Gruppe
HC-Peonies-Top-Nude;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Top-Nude_XS;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Top-Nude_S;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Top-Nude_M;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Top-Nude_L;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude_XS;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude_S;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude_M;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude_L;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
```
10 Zeilen für 1 bidirektionale Outfit-Pair-Beziehung (2 Richtungen × 5 IDs pro Vater-Familie). Bei „Ähnliche Artikel"-Beziehung gilt das gleiche Muster.

Details: SPEC_KONSTANTEN Sektion 12.

---

## 8. Pricing-Berechnung (Pilot-Vereinfachung, E25)

Pro Artikel:
- **Netto-EK** = EK des Modells aus Lieferanten-Rechnung (Unit Price). Im Trigger explizit pro Modell angegeben.
- **Brutto-VK** = `EK × Aufschlagsfaktor`, dann **kaufmännische Rundung auf X,90**.
  - Aufschlagsfaktor Pilot: **2.0** (kanonisch in SPEC_KONSTANTEN.md falls dort verankert; sonst hardcoded für Pilot)
  - Rundungs-Regel: Ergebnis wird auf nächstes ,90 gerundet. Bsp: 27 × 2.0 = 54.00 → 53,90. Bsp: 21 × 2.0 = 42.00 → 41,90.
- **EK Netto (für GLD)** = Netto-EK (gleicher Wert, manuelles Ameise-Mapping E28/E38)

Bei fehlendem EK im Trigger: STOPP + User-Frage.

---

## 9. Stil-Briefing für `artikeldetails` und HTML-Konventionen (E53 + E74-Pivot + E82, NEU v1.13/v1.15)

### Zielgruppe (NEU, kanonisch ab v1.13)

Frauen 25-35, fashionbegeistert, Pole-Dance-Performer oder -Lifestyle-Anhängerinnen. Wollen Outfits, die im Studio glänzen UND im Alltag funktionieren. Keine Spec-Käufer — aspirational ansprechen.

### polesportshop-DNA (E74-Pivot)

- **Du-Form konsequent** (Frauen-Zielgruppe direkt, nie objektifizierend)
- **Aspirational zuerst, Funktional zweite Stimme:** emotionaler Hook → Funktionalität (Halt, Grip, Bewegungsfreiheit, Material, Schnitt) konkret nachliefern. Kein Spec-Datenblatt-Ton.
- **Performance- + Fashion-Vokabular gemischt:** „sitzt", „performt", „verlängert optisch die Beine", „Statement-Piece", „von Studio zu Brunch"
- **Mit Esprit, selbstbewusst, ohne Pathos:** wohl gewählte starke Adjektive OK, Marketing-Schreierei nicht
- **Pole als Sport UND Lifestyle** — nicht nur Sportgerät, aber auch kein Sex-Sell

### Sprach-Pflicht (E73, NEU v1.13)

**Alle 5 Sprachen (DE, EN, FR, IT, ES) im `artikeldetails` werden VOLL ausformuliert.** Keine „leichten Übersetzungen mit Eigennamen unverändert" mehr. Pro Sprache eigene Tonalität-Treffer:
- DE: warm-funktional mit Esprit
- EN: cool-confident
- FR: sinnlicher
- IT: lebhafter
- ES: warm-direkt

Eigennamen (Brand, Modell, Print-Familien) unverändert lassen — siehe E58.

### Pole-Junkie-Cross-Reference (E49 + E70 zulässig, E77 geschärft v1.14)

- Strukturelle Reduktions-Vorbild bei dünnen Hersteller-Texten
- Auch als Feature-Cross-Reference erlaubt (E70)
- **Eigenformulierung in polesportshop-DNA Pflicht — NEU DENKEN, nicht paraphrasieren** (E77, NEU v1.14): nicht paraphrasieren (anderes Wort, gleiche Satz-Struktur), nicht synonymisieren (gleicher Inhalt, andere Wörter), nicht umstellen. Frage dich: was würde polesportshop diesem Produkt sagen, wenn Hersteller-Body und Pole-Junkie-Seite gar nicht existierten? Pole-Junkie liefert max. Struktur-Idee + Feature-Bestätigung, nie Wording.

### Verbotene Konstrukte

- `<strong>` HTML-Tag (Tjorben-Direktive)
- `<p class="h5 bold">` als Sub-Header (weglassen, Features in `<ul class="check">` einbetten)
- Adjektive: „sexy", „verführerisch", „aufreizend", „provokant", „atemberaubend", „einzigartig", „verlockend", „erotisch"
- **Em-Dashes (—) im Fließtext** — ersetzen mit `,` (KI-Marker, E74)
- **Doppelpunkt (`:`) im Fließtext (NEU v1.15, E82, verschärft E74)** — Doppelpunkt war in E74 als Em-Dash-Ersatz erlaubt. Mit E82 jetzt auch verboten in Fließtext und `<h2>`-Taglines. Stattdessen umformulieren (zwei Sätze, oder Hauptsatz mit Komma). Beispiel: `<h2>Marble-Print Mesh-Bodysuit: dein Statement-Piece</h2>` → `<h2>Marble-Print Mesh-Bodysuit, dein Statement-Piece</h2>` oder `<h2>Marble-Print Mesh-Bodysuit für ein Statement</h2>`.
- **Meta-Einleitungs-Sätze (NEU v1.15, E82)** — kein „Die Maße:", „Die Pflege:", „Das Material:" als Aufzählungs-Einleitung. Direkt zum Inhalt. Beispiel: `<p>Die Maße: Yifan trägt Größe S bei 1,72 m...</p>` → `<p>Yifan trägt Größe S bei 1,72 m...</p>` (Modelname aus Crawl-Body, F5/B58 v1.16).
- Pathos-Adjektiv-Kaskaden („atemberaubend, einzigartig, exklusiv und absolut traumhaft")
- Eingedeutschte Anglizismen — „Polewear", „Pole Dance", „Cheeky" bleiben
- Marketing-Imperative: „shop now", „jetzt kaufen", „greif zu"
- Hashtags, Emojis
- **„Bottom" im deutschen Freitext (NEU v1.14, E76)** — immer „Shorts" verwenden. „Pole Dance Shorts" ist zentrales SEO-Keyword. EN/FR/IT/ES nutzen ihre etablierten Begriffe.
- **Strukturelle Plagiate (NEU v1.14, E77)** — wörtliche 5-Wörter-Sequenzen aus Hersteller-Body, 1:1-Übernahme der Sub-Satz-Reihenfolge, Pole-Junkie-Tagline-Imitationen. Hinweis E77-Plagiats-Scan v1.15: bei Bullet-Listen synthetischer Separator zwischen `<li>`-Items beim Normalisieren, damit der 5-Wort-N-Gramm-Scan keine Bullet-Concat-Artefakte als Plagiat meldet (Bug-Beleg: 6/6 E77-Funde in Batch 2 Iter. 1 waren Bullet-Concat-Artefakte).

### Erlaubte Konstrukte

- `<ul class="check">` mit goldenen Häkchen (polesportshop-CI)
- `<h2>` als Tagline (max 8-10 Wörter, konkret, **ohne Doppelpunkt v1.15**). **`<h1>` wird NIE verwendet** (kollidiert mit Website-SEO)
- `<h3>` für FAQ-Fragen
- `<p>` für Fließtext (max 2-3 Sätze pro Absatz)
- Fashion-Vokabular („Statement-Piece", „Wardrobe Essential", „Eyecatcher")
- Pole-Insider-Begriffe („Floor Work", „Climb", „Grip", „Aerial Hoop")
- Sinnliche Wendungen mit Maß („Stoff, der sich anschmiegt wie eine zweite Haut")

### Template-Beispiel (Bodysuit, E74/E82-Stil)

```html
<h2>Marble-Print Mesh-Bodysuit mit Athletic-Back</h2>
<p>Ein Statement-Piece, das im Studio glänzt und auf der Bühne unvergessen
bleibt. Der Marble-Print spielt Licht und Schatten gegeneinander aus, der
offene Rücken gibt dir freie Schultern für jeden Climb.</p>
<ul class="check">
  <li>Mesh-Stoff mit Marmor-Print</li>
  <li>Tiefer V-Ausschnitt vorn</li>
  <li>Open-Back-Design für Schulter-Mobilität</li>
  <li>Bodysuit-Schnitt, hält ohne zu verrutschen</li>
</ul>
```

### HTML-Regeln
- **HTML-Entities NUR für Zeichen außerhalb Latin-1** (v1.16-Korrektur F4/B57): z.B. ✓ = `&#10004;`, ➔ = `&#10148;`, ✦ = `&#10022;`. **Latin-1-Zeichen (ß, ä, ö, ü, é, à, ñ, ç etc.) bleiben Unicode** im UTF-8-Output. Beispiel falsch (Regression v1.15): `gro&szlig;e Auswahl` → richtig: `große Auswahl`. SPEC_KONSTANTEN Sektion 5 + AP7 sind kanonisch.
- Custom-CSS-Klassen: nur `check`

---

## 10. Spalten-Mapping in Ameise (für Lauf-Bericht / User-Hinweise)

Allgemein (E30): Spaltennamen müssen nicht zwanghaft JTL-Feldnamen treffen.
Pro Lieferant einmal mappen + Vorlage speichern, dann klonen.

**Stammdaten-Spezifika:**
- `Brutto-VK` → Auto-Mapping greift
- `EK Netto (für GLD)` → manuelle Zuordnung auf JTL-Feld „Ø Einkaufspreis (netto)" nötig (E28/E38)
- `Identifizierungsspalte Vaterartikel` → JTL-Feld „Vaterartikel ID-Feld"
- Vaterartikel identifizieren anhand: `Artikelnummer`
- Varkombi: „Variationen und Werte im Vaterartikel erstellen"
- Lieferantenblock-Spalten unter „Lieferanteneinstellungen des Artikels"; Standardwert „Währung" in Vorlage setzen (z.B. EUR für HotCakes), nicht als CSV-Spalte (E36)
- **Standardlieferant in der Vorlage (Pflicht, klargestellt v1.15):** im Standardwerte-Bereich „Lieferant" explizit auf den Lieferanten setzen (z.B. „HotCakes Polewear"). Bug-Beleg 2026-05-17: HotCakes-Attribute-Vorlage hatte Standardlieferanten auf „nicht gewählt", Import schlug mit 220 Warnungen „Lieferant HOTCAKES existiert nicht" fehl. Gilt für ALLE 5 Vorlagen pro Lieferant.
- **Artikelgewicht + Versandgewicht (F3/B56, NEU v1.16):** Default `0,05` (50 g) pro Kleidungsstück in die Spalten `Artikelgewicht` und `Versandgewicht` schreiben. Komma-Dezimal (DE-Locale). Override pro Artikel möglich wenn echtes Gewicht aus Lieferanten-Daten bekannt. Maße (Länge/Breite/Höhe) bleiben leer (pro Kleidungsstück variabel, kein sinnvoller Pauschal-Default).
- **TARIC-Code (F6/B59, NEU v1.16):** Default `62114390` für Pole-Bekleidung aus `lieferanten_mapping.yaml` Feld `taric_code` ziehen → Spalte `TARIC` in Stammdaten-CSV. Sonstiges-Reiter in WaWi wird damit gefüllt.
- Bild-Spalten `Bild 1` bis `Bild 10` → JTL-Felder `Bild Pfad/URL 1` bis `Bild Pfad/URL 10`
- Reiter „Bilder/Plattformen": alle 11 Plattform-Häkchen in der Vorlage gesetzt (B5-Lösung)
- **Multi-Kategorie (E92 verfeinert E89, KORRIGIERT v1.18 nach Trial 2026-05-18):** Pro Artikel **3 CSV-Zeilen** mit gleicher Artikelnummer: (a) Oberkategorie `Pole Dance Kleidung` (Ebene 2 leer), (b) Unterkategorie `Pole Dance Kleidung` + spezifische Subkategorie (`Pole Dance Tops` / `Pole Dance Shorts` / `Bodysuits` / `Leggings` / `Legwarmer` / `Shirts`), (c) Sara-Pflicht-Zuweisung `Intern` + `Neue Artikel für Sara` (WaWi-Key 546). **Korrektur:** v1.16/E89-Annahme „WaWi resolved Pfad selbst" war falsch — Trial-Lauf 2026-05-18 21:06 zeigte fehlende Oberkategorie im Shop. Zurück zum E57-Doppel-Pattern + Sara-Zeile. Vorlagen-Setting unverändert: „Kategorieverknüpfungen des Artikels aktualisieren" = „Neue Kategorien beim jeweiligen Artikel hinzuimportieren".
- Reiter „Verkaufskanal aktiv": Häkchen in Vorlage entfernt + Vorlage gespeichert (E37/B21)

**Reiter „Weitere Texte" (E31):** pro Sprache (EN/FR/IT/ES) → CSV `Global-{Sprache}: Artikelname`, `Global-{Sprache}: Titel-Tag`, `Global-{Sprache}: Meta-Description`.

**Cross-Selling-Vorlage (NEU v1.14):** 3 Spalten mappen — `Artikelnummer`, `Artikelnummer Cross-Seller`, `Cross-Selling-Gruppe`. Slot-Konvention: `_5_CrossSelling` (siehe `lieferanten_mapping.yaml` Schema-Doku). Standardlieferant in der Vorlage NICHT relevant für diesen Import-Typ (es geht um Artikel-Beziehungen, nicht um Lieferanten-Zuordnung).

---

## 11. Fehler-Handling (Tabelle)

| Situation | Verhalten |
|---|---|
| Lieferantenname nicht im Mapping | Halten, User-Frage |
| Pflichtfelder im Mapping null | Halten, fehlende Werte abfragen |
| `groessen_konvention` fehlt | Default `standard`, im Bericht warnen |
| Input-Modus nicht eindeutig | Halten, klären |
| Crawl-Trigger mit Shopify-Detektion erfolgreich (E48 Pfad B) | Crawl durchführen via Code-Execution + Storefront-JSON. Im Bericht E48-Pfad markieren. |
| Pole-Junkie-Crawl (E49 Owner-Direktive) | Crawl ohne Halt durchführen. Im Bericht E49-Verweis. Bei Cease-and-Desist sofort eskalieren und pausieren. |
| Übersetzung scheitert bei einzelnem Feld | Artikel in `_Review/`, andere weiter |
| Pflichtfeld fehlt (Material, Preise, Farbe) | Lauf abbrechen, präzise melden |
| Merkmalwert außerhalb erlaubter Liste | Lauf abbrechen + User-Frage |
| Self-Check (Stage 6) scheitert | STOPP + User. Keine partielle Ausgabe. |
| Validierung scheitert | Lauf abbrechen |
| Cloud-Storage-Link (Dropbox/WeTransfer) | NICHT blind fetchen — Connector prüfen oder User um lokalen Download bitten |
| **Token/Wallclock-Schätzung > Limit (NEU v1.15, E83)** | **NICHT halten — Batch-Aufteilung autonom entscheiden (E81), Plan im Bericht dokumentieren, Stage 0.5 ausführen** |

---

## 12. Was Cowork DARF und NICHT DARF (Kurzliste)

### DARF
- Files anlegen/lesen/kopieren im Workspace
- Wissens-Files via GitHub-Raw lesen (`https://raw.githubusercontent.com/verticalogmbh/polesportshop-wissen/<tag>/<file>`, E87/E91 v1.20). Drive-Connector nur noch für Lieferanten-Drive-Ordner (Drive-Upload-Input-Modus).
- Übersetzungen erstellen (außer Eigennamen und SEO-Templates, siehe NICHT DARF)
- HTML-Snippets nach Sektion 9 generieren
- CSVs validieren und schreiben
- Mid-Run-GitHub-Raw-Read für Charter/LOG/Backlog bei echter Architektur-Klärung (legitime Klärung, kein E62-Verstoß)
- **Workflow-Entscheidungen autonom treffen (NEU v1.15, E81):** Batch-Splitting, Batch-Größen, Token-Budget-Management, Stage-Reihenfolge bei Tool-Limits. STOPP + User-Frage bleibt strikt für: fehlende Daten, unbekannte Sprach-Begriffe, Goldstandard-Abweichungen, Mapping-`null`-Pflichtfelder.

### NICHT DARF
- Dateien permanent löschen
- WaWi schreibend ändern
- Importvorlagen in Ameise verändern
- A-Nummern vergeben
- `lieferanten_mapping.yaml` ohne User-Bestätigung schreiben
- API-Keys/Credentials im Chat ausgeben oder akzeptieren (E33)
- **Bild-Spalten in Stammdaten-CSV mit Hersteller-CDN-URLs befüllen** (E44 — Validierung Stage 6 bricht ab). Bild-URLs müssen R2-Public-URLs sein (E43/E44), aus der Bildpipeline-Sub-Process-Map. **NEU v1.18 (E93):** Bildpipeline ist wieder aktiv, Stage 5.6 + 5.7 erzeugen die R2-URLs. Nicht mehr leer wie in E63-Phase.
- **Produkt-spezifische Meta-Descriptions oder Titel-Tags erfinden** (E55, AP3 — Templates aus SPEC_KONSTANTEN sind hardcoded, einzige Variable ist `{name}`). LLM-Generation für SEO strikt verboten.
- **Sprach-Namen außerhalb der E58-Lookup-Tabellen erfinden** (AP8) — STOPP, User-Frage
- **Eigennamen übersetzen** (Modell-Namen, Brand-Namen wie „Hekate", „Arachne", „HotCakes")
- **Schema-Spalten-Reihenfolge umorganisieren** — Schema ist append-only (E54, AP4)
- **Kategorie-Werte außerhalb der E51-Tabelle nutzen** (AP1 — „Damen" und „Limited Editions" sind keine gültigen Kategorien)
- **Multi-Kategorie ohne separate Zeilen umsetzen** (E57, AP6). **🔒 Anti-Confusion (E75, v1.13):** wenn jemand „doppelte Größen" als Bug meldet → KEIN Spec-Fix. Erst Vorlagen-Setting `Kategorieverknüpfungen des Artikels aktualisieren = Neue Kategorien beim jeweiligen Artikel hinzuimportieren` in WaWi prüfen. **KORRIGIERT v1.18 (E92, kehrt E89-Annahme zurück):** Pro Artikel 3 Zeilen — Oberkategorie + Subkategorie + Sara-546. Nicht nur Subkategorie (WaWi resolved den Pfad NICHT automatisch — Trial-Lauf 2026-05-18 zeigte fehlende Oberkategorie im Shop).
- **Kind-Artikelname ohne Größen-Suffix lassen** (E56, AP5 — Kind-Name = Vater-Sprachname + Leerzeichen + Variationswert)
- **SEO-Felder auf Kind-Zeilen befüllen** (E56 — Titel-Tag und Meta-Description leben nur auf Vater-Zeilen)
- **Workflow-Frage statt autonomer Entscheidung (NEU v1.15, AP9)** — Batch-Splitting, Token-Budget, Stage-Reihenfolge gehören zur Autonomie (E81). Cowork entscheidet, dokumentiert im Bericht, fragt nicht.
- **CSV/Lauf-Bericht nach Drive uploaden (NEU v1.15, AP10)** — E52/E69 verbietet das, AP10 verschärft. CSVs bleiben im Workspace, Tjorben lädt manuell wenn er archivieren will. Bug-Beleg: 3 korrupte Uploads in `2026-05-17_HOTCAKES_batch1/` Drive-Ordner.
- **Datei-Naming ohne Nummer-Präfix (NEU v1.15, AP11)** — Konvention `<NR>_<Typ>_<LIEFERANT>_<YYYY-MM-DD_HHMM>.csv` mit Reihenfolge-Nummer 1-5. Ohne Nummer-Präfix kann Tjorben die Import-Reihenfolge nicht visuell prüfen.
- **Leere CSV mit nur Header (NEU v1.15, AP12)** — wenn 0 Daten-Zeilen, NICHT ausgeben. Im Bericht stattdessen vermerken („Cross-Selling-CSV nicht ausgegeben, 0 Beziehungen gefunden").

---

## 13. Output-Konvention für diesen Lauf

- **5 CSVs** im Cowork-Workspace `/home/claude/outputs/` (E52/E69 — kein Drive-Upload, AP10). Inkl. der neuen `5_CrossSelling_*.csv` ab v1.14 (E80).
- **Datei-Naming-Konvention (AP11, v1.15):** `<NR>_<Typ>_<LIEFERANT>_<YYYY-MM-DD_HHMM>.csv` mit Reihenfolge-Nummer 1-5. Beispiele:
  - `1_Stammdaten_HotCakes_Batch1_2026-05-17_1500.csv`
  - `5_CrossSelling_HotCakes_Batch2_2026-05-17_1700.csv`
- **Keine leeren CSVs** (AP12, v1.15): wenn 0 Daten-Zeilen, NICHT ausgeben sondern im Lauf-Bericht vermerken.
- Lauf-Bericht `run_<YYYY-MM-DD_HHMM>_<lieferant>.md` daneben im Workspace
- Alle Output-Files via `present_files`-Pattern an Tjorben ausgeben
- Lauf-Bericht enthält: **Stage 0.5 Scope-Analyse mit Batch-Plan (NEU v1.15, E83)**, Stages mit Wallclock + Tokens, **Self-Check-Ergebnis (16 Punkte)**, Credit-Verbrauch, ggf. Anomalien, ggf. Pole-Junkie-Stil-Inspirations-Hinweise (E49/E53/E70), ggf. lazy-geladene Files mit Begründung, **Eigeninterpretationen explizit markiert (E70)**. Bei Cross-Selling-Stage 5.8 zusätzlich: Anzahl der gefundenen Beziehungen pro Gruppe, Anzahl Schwester-Farben pro Modell-Stamm (Datenpunkt für die Algorithmus-Validierung), Anzahl Kinder-Zeilen vs. Vater-Zeilen (Datenpunkt für E80-Erweiterung-Validierung v1.15).

---

## 14. Verhältnis zum Snapshot

Dieser Brief ist **offizieller Teil des Snapshots ab v1.12** (E68 verankert), aktualisiert in v1.15.
Bei Änderungen an `WAWI-IMPORT-WISSEN.md` oder
`cowork_anweisung_datenimports.md` muss der Run-Brief in Cycle 4 des
nächsten Wissens-Updates mitgepflegt werden — sonst zeigt Cowork veraltetes
operatives Verhalten gegenüber der vollständigen Spec.

Output-Konvention für CSVs und Lauf-Bericht: **lokal im Cowork-Workspace
`/home/claude/outputs/` + `present_files`-Pattern**, KEIN Drive-Upload
(E52 final, E69 Drift behoben, A6 final gelöst mit v1.12, AP10 verschärft v1.15).

Wenn dieser Brief im Widerspruch zu deinen Custom Instructions oder zu
SPEC_KONSTANTEN.md steht: SPEC_KONSTANTEN gewinnt für Konstanten,
Custom Instructions gewinnen für deine Identität und Sicherheit, **dieser
Brief gewinnt für die operative Stage-Sequenz und Spec-Lade-Regel jedes
Daten-Laufs**.
