
> **🗄️ DEPRECATED v1.22 — COLD STORAGE.** Diese Cowork-Spec ist seit dem Code-Pivot (v1.22) **nicht mehr der Primärpfad**. Die Artikelanlage läuft als lokaler Code in `pipeline/` (siehe `CLAUDE.md` + `pipeline/README.md`). Dieses Dokument bleibt als **Cowork-Fallback + Historie** erhalten (voller Stand auch im git-Tag `v1.21`). Nicht für die tägliche Arbeit lesen.
> **🗄️ DEPRECATED ab v1.22 (2026-06-15).** Die Artikelanlage läuft jetzt als lokaler Code (`pipeline/`, siehe `pipeline/README.md`). Diese Datei ist **historische / Fallback-Referenz für die Cowork-Ausführung** und wird nicht mehr aktiv synchron gehalten — nicht für aktuelle Läufe verwenden. Das Schema bleibt kanonisch in `SPEC_KONSTANTEN.md`.

# Cowork-Anweisung: Daten-Pipeline (Stammdaten + Variationen + Merkmale + Attribute + Cross-Selling)

**Stand:** v2.1, 2026-05-18 (Minor-Update im v1.21-Refactor E92+E93: Multi-Kategorie zurück auf 3-Zeilen-Pattern (Oberkategorie + Subkategorie + Sara-546), Farb-Lokalisierung DE für Marketing-Farben mit DE-Pendant, Stage 5.6+5.7 Bildpipeline wieder aktiv). · **Vorheriger Stand:** v2.0, 2026-05-18 (Major-Verschlankung v1.20). · **Vor-vorheriger Stand:** v1.15.1, 2026-05-18 (vor Verschlankung).

> **Zweck dieser Datei:** vollständige operative Spec für Daten-Pipeline-Läufe in Cowork. **NICHT in Stage 0 für reguläre Läufe geladen** (E68: dort lädst du `run_brief_daten.md`). Diese Datei wird lazy-geladen bei tiefen Architektur-Klärungen, Onboarding-Detailfragen, oder beim ersten Setup eines neuen Lieferanten.

> **Konstanten (Schema, SEO-Templates, Sprach-Lookup, Merkmalwerte, Self-Check, Anti-Patterns):** kanonisch in `SPEC_KONSTANTEN.md`. Diese Datei verweist nur dorthin, definiert nicht.

---

## 1. Zweck

Diese Spec definiert die **operative Mechanik** der Daten-Pipeline für die Artikelanlage in JTL-WaWi via JTL-Ameise-CSV-Imports. Ausgabe pro Lauf: **5 CSVs** (Stammdaten, Variationen, Merkmale, Attribute, Cross-Selling) im Cowork-Workspace, via `present_files` an Tjorben. Tjorben importiert in Ameise in der in Sektion 8 dokumentierten Reihenfolge.

**Charter-Bezug:** Cowork ist Produktions-Engine (E1), kein Review-Gate vor CSV (E2), 5 separate CSVs für JTL-Ameise-Native (E5). Volle Architektur-Prinzipien siehe `PROJEKT-CHARTER.md`.

---

## 2. Trigger & Input-Modi

### 2.1 Trigger-Erkennung

Trigger-Phrasen die diese Pipeline aktivieren:
- „Verarbeite neue Artikel von <LIEFERANT>..."
- „Lege neue Artikel von <LIEFERANT> an..."
- „Importiere Lieferung von <LIEFERANT>..."

Bei Trigger ohne `<LIEFERANT>`: STOPP, User-Frage.

### 2.2 Input-Modi (E4, 6 Modi)

Cowork erkennt den Input-Modus pro Lauf aus dem Trigger:

1. **Crawl-Modus** — Lieferanten-Shop-URL (z.B. Shopify). Aktuelle Mechanik: E48 Pfad B (Code-Execution + Storefront-JSON).
2. **Drive-Upload-Modus** — Tjorben legt Lieferanten-Files (CSV/Excel/PDF) in Lieferanten-Drive-Ordner.
3. **Excel/CSV-Direkteingabe** — Trigger enthält Pfad zu Excel/CSV.
4. **PDF-Modus** — Lieferanten-Rechnung/-Katalog als PDF.
5. **Mail-Modus** — Lieferanten-Mail-Anhang.
6. **Hybrid** — Kombination (z.B. PDF-Rechnung + Crawl-Body für Texte).

Im Pilot 2026-05 aktiv: Crawl (HotCakes Shopify) + Drive-Upload (POLE ADDICT). Andere Modi je nach Lieferant. Firecrawl-Connector ist nicht in Anthropic-Registry (E41, B25); Crawl-Modus läuft im Pilot via E48 Pfad B für Shopify-Lieferanten.

### 2.3 Trigger-Beispiele

```
Verarbeite neue Artikel von HotCakes: Crawl Modus, alle Polewear-Artikel.
Verarbeite neue Artikel von POLE ADDICT: Excel im Drive-Ordner _Eingang.
Verarbeite neue Artikel von HotCakes: 3 Modelle aus Lieferung 2026-05-17:
  - Hekate Bodysuit Black, EK 27 EUR
  - Arachne Top Teal, EK 21 EUR
  - Arachne Bottom Teal, EK 21 EUR
```

### 2.4 Crawl-Mechanik (E48, Shopify-Storefront-JSON)

Für Shopify-Lieferanten (HotCakes, Pole Junkie): Code-Execution + `curl/requests` mit Browser-User-Agent gegen `<shop>/products.json` oder `<shop>/products/<handle>.json`. Liefert vollständige Produkt-Liste mit Varianten, Tags, Body-HTML, Bild-URLs. Validiert mit Arachne Top Black 2026-05-15 (HTTP 200, 124 Produkte). Pole-Junkie-Crawl ist mit E49 explizit freigegeben (Owner-Direktive).

Lieferanten-spezifische Crawl-Mechanik gepflegt in `lieferanten_mapping.yaml` Feld `crawl_mechanik` (`shopify_json` | `null`).

---

## 3. Lieferantenkontext laden

Stage 1 nach Trigger-Parse: lese `lieferanten_mapping.yaml` (Stage-0-Pflicht-File, Cache via E62) und suche den Lieferanten-Block.

**Wenn Lieferant nicht im Mapping:** STOPP, „Bitte erst Onboarding durchführen — siehe `LIEFERANTEN-ONBOARDING.md`". Kein Ad-hoc-Lauf für unbekannte Lieferanten.

**Wenn Pflichtfelder null:** STOPP, fehlende Werte abfragen. Pflichtfelder pro Lieferant: `anzeigename`, `kuerzel`, `hersteller`, `marke_kurz`, `herkunftsland`, `waehrung`, `shop_url`, `r2_prefix`, `ameise_vorlagen.stammdaten`, `ameise_vorlagen.variationen`, `ameise_vorlagen.merkmale`, `ameise_vorlagen.attribute`, `ameise_vorlagen.cross_selling`, `brand_story_de/en/fr/it/es` (E72/E79). Optionale Felder mit Defaults: `groessen_konvention` (`standard`), `category` (`fashion`), `crop_profile` (`fashion`), `pose_sort` (`auto_vision`), `max_groesse` (`null`), `article_weight_kg` (`0.05`), `taric_code` (`'62114390'`).

Schema-Doku am Ende der YAML pflegt die vollständige Feld-Liste. Bei Schema-Änderung: Änderung in YAML, dann diese Spec mitziehen.

---

## 4. Pipeline-Stages

**Operative Stage-Sequenz (kompakte Übersicht in `run_brief_daten.md` Sektion 2). Diese Sektion gibt die detaillierte Mechanik pro Stage.**

### STOPP-Trigger (E81, harte Liste)

Cowork stoppt sofort + fragt User bei:
- Fehlende Pflicht-Daten (EK fehlt, Modellname fehlt, Farbe fehlt)
- Mapping-Pflichtfeld `null` für den Lieferanten
- Unbekannter Sprach-Begriff (außerhalb SPEC_KONSTANTEN Sektion 6 Lookup-Tabellen)
- Goldstandard-Abweichung (SPEC_KONSTANTEN Sektion 8) ohne Mapping-Eintrag
- Connector down (Drive nicht erreichbar, GitHub-Raw nicht erreichbar)
- Self-Check (Stage 6) findet harten Fail

**NICHT-STOPP (autonom entscheiden, E81):** Batch-Splitting, Batch-Größen, Token-Budget-Management, Stage-Reihenfolge bei Tool-Limits.

### Stage 0: Snapshot-Resolution + Spec-Caching

GitHub-Raw-Resolution (E87/E91): jüngsten `vX.Y`-Tag holen, dann via `https://raw.githubusercontent.com/verticalogmbh/polesportshop-wissen/<tag>/<file>` die 3 Stage-0-Files laden:

1. `run_brief_daten.md`
2. `SPEC_KONSTANTEN.md`
3. `lieferanten_mapping.yaml`

Cache lokal in `/home/claude/wissens_cache/`. Drift-Verdacht („Snapshot wurde gerade aktualisiert"): Lauf abbrechen, neu starten — kein Mid-Run-Reload.

### Stage 0.5: Pre-Run Scope-Analyse (E83, NEU v1.15)

Autonom Token + Wallclock schätzen für den geplanten Scope. Bei Schätzung > 100k Output-Tokens oder > 8 Min pro Stage: Batch-Aufteilung dokumentieren. **Familien-erhaltende Split-Regel (E84):** Outfit-Pair-Familien (gleicher Modell-Stamm + alle Farben + Top/Bottom) bleiben pro Batch zusammen. Cross-Selling-Stage 5.8 läuft im letzten Batch über alle bisher importierten Modelle vereint.

Im Lauf-Bericht dokumentieren: Batch-Plan, geschätzte Tokens/Wallclock pro Batch, welche Familien in welchem Batch landen.

### Stage 1: Input erkennen & laden

Input-Modus aus Trigger ableiten (siehe 2.2). Crawl: Storefront-JSON laden. Drive: Lieferanten-Ordner listen. Excel/CSV: File parsen. Bei Hybrid: alle Quellen laden und im weiteren Lauf konsolidieren.

### Stage 2: Daten extrahieren

**Voller Lieferanten-Datensatz laden** — E80 für Cross-Selling-Stage 5.8 nötig (alle Produkte des Lieferanten, nicht nur Trigger-Modelle). Bei großen Lieferanten in Token-Budget aufteilen, aber Familie-Erhaltung achten.

Felder pro Artikel extrahieren: Modellname, Farben, Größen, Material, Print, Style-Tags, Bild-URLs (für Stammdaten-Bild-Spalten — leer mit E63), EK pro Modell aus Trigger, Body-HTML als Quelle für Features.

### Stage 3: Daten normalisieren

Lieferanten-Format → 48-Spalten-Schema laut SPEC_KONSTANTEN Sektion 1. Größen-Konvention pro Lieferant via Mapping (`standard` | `kombi_reduziert_auf_kleinste`). Farb-Normalisierung gegen SPEC_KONSTANTEN Sektion 7 (Farbe Kleidung — 13 erlaubte Werte, 2-stufige Logik mit Lieferanten-Farbe als Tag).

### Stage 4: Pricing-Berechnung (E25)

Pro Artikel:
- **Netto-EK:** aus Trigger pro Modell.
- **Brutto-VK:** `EK × Aufschlagsfaktor` (Pilot: 2.0), kaufmännische Rundung auf `,90`. Bsp.: `27 × 2.0 = 54 → 53,90`.
- **EK Netto (für GLD):** = Netto-EK (manuelles Ameise-Mapping E28/E38).

Bei fehlendem EK: STOPP, User-Frage.

### Stage 5: Mehrsprachige Felder ableiten (E58)

DE-Quelle → EN/FR/IT/ES via Lookup-Tabellen in SPEC_KONSTANTEN Sektion 6. Eigennamen (Modellnamen, Print-Familien, „Crop Top", „High Waist") unverändert. Bei Begriff außerhalb Lookup-Tabelle: STOPP, User-Frage (AP8, E59). Niemals erfinden.

Artikelname-Konvention (E26, E56): Vater = lokalisiertes Substantiv + Modell + Farbe. Kind = Vater-Name + Leerzeichen + Größe.

SEO-Felder (Titel-Tag, Meta-Description) deterministisch nach E55-Template aus SPEC_KONSTANTEN Sektion 5, NUR auf Vater-Zeilen, leer auf Kindern (E56). HTML-Entities NUR für Zeichen außerhalb Latin-1 (✓ = `&#10004;`, ➔ = `&#10148;`); Umlaute (ß, ä, ö, ü, é, à) bleiben Unicode (F4/B57 v1.16).

### Stage 5.5: Attribut-HTML generieren (E22/E53/E74/E78/E82-Stil)

Pflicht-Set: `markentext`, `artikeldetails`, `material_and_care`, `size_and_fit`. Optional: `anwendung`, `faqs`, `inhaltsstoffe`. Pro Attribut + pro Sprache (5 Sprachen voll, E73) HTML-Snippet generieren.

**Stil-Differenzierung pro Feld (SPEC_KONSTANTEN Sektion 11):**
- `markentext` + `artikeldetails`: E74-aspirational (Zielgruppe Frauen 25-35, Du-Form, Performance-+Fashion-Vokabular).
- `material_and_care`: clean/funktional (E78) — 2 HTML-Paragraphen, P1 Stoffzusammensetzung, P2 Pflegehinweise. Keine Verkaufs-Adjektive.
- `size_and_fit`: aspirational gemäßigt + Modelname aus Crawl-Body (F5/B58 v1.16). Statt „Unser Model trägt..." → `<Modelname> trägt Größe S bei 1,72 m...` (z.B. Yifan, Vika, Elena bei HotCakes). Bei mehreren Models: erstes Model im Crawl-Body. Bei null Modelname: „Das Model trägt..." oder Phrase weglassen.

`markentext` wird primär aus `lieferanten_mapping.yaml` Felder `brand_story_<lang>` gezogen (E72/E79, Caching). Wenn `null`: Cowork generiert pro Lauf und markiert als E70 (Eigeninterpretation).

**Verbote im Fließtext (E74/E76/E82):**
- HTML-Tag `<strong>` (Tjorben-Direktive)
- Em-Dash (—)
- Doppelpunkt im Fließtext und `<h2>`-Taglines (E82, NEU v1.15)
- Meta-Einleitungs-Sätze („Die Maße:", „Die Pflege:")
- Adjektive: „sexy", „verführerisch", „aufreizend", „provokant", „atemberaubend", „einzigartig", „verlockend", „erotisch"
- Im deutschen Freitext: „Bottom" (E76, immer „Shorts")
- Eigennamen übersetzen (Brand, Modell, Print-Familien)

**Originalitäts-Pflicht (E77):** Kein 5-Wort-N-Gramm aus Hersteller-Body. Pole-Junkie-Stil-Inspiration erlaubt (E49+E53+E70), aber Eigenformulierung in polesportshop-DNA — nicht paraphrasieren, nicht synonymisieren.

### Stage 5.6: Bildpipeline-Sub-Process aufrufen (REAKTIVIERT v1.21, E93)

Cowork ruft `cowork_anweisung_bildpipeline.md` v2.1 als Sub-Process auf und erhält die Map `{artikelnummer: [bild_urls]}` zurück. Pro Vater wird die Bild-Quelle aus Crawl-Body / Drive-`_Eingang` / Hersteller-Site nach Anti-Bot-Fallback-Reihenfolge geladen, durch Crop-Profil (`crop_profile` aus Mapping: `fashion` 2:3 1000×1500 oder `tech` 1:1 1200×1200) verarbeitet, per Vision auf Pose klassifiziert (`pose_sort` aus Mapping: `auto_vision` für Fashion mit Hero/Back/Side-Reihenfolge, oder `manufacturer_order` / `none`), auf R2 hochgeladen unter `<r2_prefix>/<filename>.jpg` (verarbeitetes Shop-Bild) und `originals/<r2_prefix>/<filename>.<ext>` (Magic-Byte-detektiertes Original, A2-Pattern).

### Stage 5.7: Bild-URLs in Stammdaten-CSV einbetten (REAKTIVIERT v1.21)

Aus der Bildpipeline-Map die ersten 10 URLs pro Artikel in die Stammdaten-CSV-Spalten `Bild 1` bis `Bild 10` schreiben. Auf Vater UND alle Kinder duplizieren (E34/E46). Bei <10 Bildern pro Artikel: übrige Spalten leer (Re-Import-Verhalten siehe Stage 10 Konventionen).

**Ameise-Vorlage-Voraussetzungen** (Stammdaten-Vorlage):
- 10 Bild-Spalten `Bild 1` bis `Bild 10` auf JTL-Felder `Bild Pfad/URL 1` bis `Bild Pfad/URL 10` gemappt
- Reiter „Bilder/Plattformen": alle 11 Plattform-Häkchen gesetzt (E46/B5 — automatische Plattform-Aktivierung)

### Stage 5.8: Cross-Selling-Beziehungen (E80 v1.14, Kinder-Replikation v1.15)

Algorithmen:
- **`Vervollständige Dein Outfit`:** gleicher Modell-Stamm + gegensätzlicher Typ (Top↔Bottom) + gleiche Farbe.
- **`Ähnliche Artikel`:** gleicher Modell-Stamm + gleicher Typ + andere Farbe.

**Modell-Stamm-Schlüssel** (v1.15-Präzisierung): `(modell_basis, farbe_im_namen)` bei Farbvarianten — nicht nur `modell_basis`.

**Kinder-Replikation (v1.15-Erweiterung E80):** Linke Spalte `Artikelnummer` enthält Vater UND alle Kinder. Rechte Spalte `Artikelnummer Cross-Seller` bleibt strikt Vater. Pro bidirektionale Beziehung: 2 × (1 Vater + N Kinder) Zeilen.

Symmetrie: Beziehung beidseitig (A↔B in zwei Zeilen, plus Kinder-Replikation).

Voller Datensatz aus Stage 2 nötig.

Details: SPEC_KONSTANTEN Sektion 12.

### Stage 6: Validierung

**16-Punkte-Self-Check** aus SPEC_KONSTANTEN Sektion 9. Bei Fail eines Punkts: STOPP, eindeutig benennen, User-Frage formulieren. Self-Check-Output im Lauf-Bericht: `[#N] [✓/✗] <Punkt> — <Detail>`.

### Stage 7: CSVs schreiben

5 CSVs im Cowork-Workspace `/home/claude/outputs/`. Format-Regeln in SPEC_KONSTANTEN (Sektion 1 für Stammdaten, Sektion 12 für Cross-Selling) bzw. `run_brief_daten.md` Sektion 3.

**Datei-Naming-Konvention (AP11):** `<NR>_<Typ>_<LIEFERANT>_<YYYY-MM-DD_HHMM>.csv`. Reihenfolge-Nummer 1-5 zwingend.

**Leere CSVs NICHT ausgeben (AP12):** im Lauf-Bericht stattdessen vermerken.

Lauf-Bericht `run_<YYYY-MM-DD_HHMM>_<lieferant>.md` daneben im Workspace. Alle Files via `present_files` an Tjorben.

---

## 5. CSV-Schemas

**Schema-Details kanonisch in SPEC_KONSTANTEN.md.** Diese Sektion gibt nur Übersicht + Pointer.

### 5.1 Stammdaten (48 Spalten, v3.1 nach E54)

→ SPEC_KONSTANTEN Sektion 1.

Pflichtfelder pro Vater: Artikelnummer, Sprach-Artikelnamen, Brutto-VK, EK Netto, Steuersatz, Hersteller, Lieferantenblock-Spalten, TARIC-Code (`taric_code` aus Mapping, NEU v1.16), Artikelgewicht + Versandgewicht (`article_weight_kg` aus Mapping, NEU v1.16, DE-Komma), 10 Bild-Spalten (leer ab E63).

Multi-Kategorie (E57 + E92 korrigiert E89, v1.21): pro Artikel **3 CSV-Zeilen** mit gleicher Artikelnummer:
- (a) Oberkategorie-Zuweisung: `Pole Dance Kleidung` (Ebene 2 leer)
- (b) Unterkategorie-Zuweisung: `Pole Dance Kleidung` + spezifische Subkategorie (`Pole Dance Tops` / `Pole Dance Shorts` / `Bodysuits` / `Leggings` / `Legwarmer` / `Shirts`)
- (c) Sara-Review-Pflicht-Zuweisung: `Intern` + `Neue Artikel für Sara` (WaWi-Kategorie-Key `546`)

**Korrektur v1.21 (E92):** v1.19-E89-Annahme „WaWi resolved Pfad selbst" war falsch (Trial-Lauf 2026-05-18 21:06 zeigte fehlende Oberkategorie). E57-Doppel-Pattern bleibt gültig, Sara als 3. Zeile ergänzt.

Vorlagen-Setting unverändert: „Kategorieverknüpfungen des Artikels aktualisieren" = „Neue Kategorien beim jeweiligen Artikel hinzuimportieren".

### 5.2 Variationen (12 Spalten)

```
Artikelnummer;Variationsname;Darstellungsform;Variationswertname;
Global-Englisch: Variationsname;Global-Englisch: Variationswertname;
... (analog FR/IT/ES)
```

Eine Zeile pro Größen-Variante. `Artikelnummer` = Vater-Artikelnummer. `Darstellungsform` = `DROPDOWN`. Variationsname: Größe / Size / Taille / Taglia / Talla.

### 5.3 Merkmale (4 Spalten)

→ Werte: SPEC_KONSTANTEN Sektion 7.

```
Lieferant;Artikelnummer (Lieferant);Merkmalname;Merkmalwertname 1
```

Auf Vater UND alle Kinder explizit dupliziert (E34). Nur Deutsch in der CSV.

### 5.4 Attribute (8 Spalten, alle Felder gequotet)

```
Lieferant;Artikelnummer (Lieferant);Attributname;Attributwert;
Englisch: Attributwert;Französisch: Attributwert;Italienisch: Attributwert;Spanisch: Attributwert
```

`csv.QUOTE_ALL` — jedes Feld in `"..."`. Auf Vater UND alle Kinder dupliziert (E34).

### 5.5 Cross-Selling (3 Spalten, E80, Kinder-Replikation v1.15)

→ SPEC_KONSTANTEN Sektion 12.

```
Artikelnummer;Artikelnummer Cross-Seller;Cross-Selling-Gruppe
```

### 5.6 Bilder — als Spalten in Stammdaten-CSV (E46), Pipeline-Generierung REAKTIVIERT v1.21 (E93)

Bild-URLs sind 10 Spalten am Ende der Stammdaten-CSV (`Bild 1` bis `Bild 10`). Generierung läuft via Bildpipeline-Sub-Process (Stage 5.6 + 5.7), R2-Public-URLs nach E43/E44-Mechanik. Crop-Profile pro Lieferant (E45), Pose-Sortierung via Vision (E45). Spec-Details: `cowork_anweisung_bildpipeline.md` v2.1.

### 5.7 Feature-Erfassungs-Quellen (E70)

Style-, Material-, Farb-Features kommen text-basiert aus Lieferanten-Body-HTML, nicht Vision-API (B44 deferred). Bei dünnem Hersteller-Text: Pole-Junkie-Cross-Reference erlaubt (E49+E53+E70), Eigenformulierung Pflicht (E77).

---

## 6. Ameise-Vorlagen-Naming + Standardlieferant

→ Detaillierter Onboarding-Prozess: `LIEFERANTEN-ONBOARDING.md`.

Naming-Konvention (E29, ab v1.14 = 5 Vorlagen pro Lieferant): `{Lieferantenname}_{Nr}_{Import-Typ}`. Slot-Reihenfolge: `_1_Stammdaten`, `_2_Variationen`, `_3_Merkmale`, `_4_Attribute`, `_5_CrossSelling`. Slot-Nummern sind pro Import-Typ eindeutig (siehe Schema-Doku in `lieferanten_mapping.yaml`).

**Standardlieferant in jeder Vorlage (Pflicht, klargestellt v1.15 nach Bug):** im Standardwerte-Bereich „Lieferant" explizit auf Lieferanten setzen. Bug-Beleg 2026-05-17: HotCakes-Attribute-Vorlage hatte Standardlieferanten auf „nicht gewählt", Import schlug mit 220 Warnungen fehl.

Stammdaten-Vorlage: alle 10 Bild-Spalten mappen + alle 11 Plattform-Häkchen im Reiter „Bilder/Plattformen" setzen (E46/B5).

---

## 7. Spalten-Mapping in Ameise

Allgemein (E30): Spaltennamen müssen nicht zwanghaft JTL-Feldnamen treffen. Pro Lieferant einmal mappen + Vorlage speichern, dann klonen.

**Stammdaten-Spezifika:**
- `Brutto-VK` → Auto-Mapping greift
- `EK Netto (für GLD)` → manuelle Zuordnung auf JTL-Feld „Ø Einkaufspreis (netto)" nötig (E28/E38)
- `Identifizierungsspalte Vaterartikel` → JTL-Feld „Vaterartikel ID-Feld"
- Vaterartikel identifizieren anhand: `Artikelnummer`
- Varkombi: „Variationen und Werte im Vaterartikel erstellen"
- Lieferantenblock unter „Lieferanteneinstellungen des Artikels"; Standardwert „Währung" in Vorlage setzen (E36)
- Bild-Spalten `Bild 1` bis `Bild 10` → JTL-Felder `Bild Pfad/URL 1` bis `Bild Pfad/URL 10`
- Reiter „Bilder/Plattformen": alle 11 Plattform-Häkchen gesetzt (B5)
- Multi-Kategorie (E57/E89): „Kategorieverknüpfungen des Artikels aktualisieren" = „Neue Kategorien beim jeweiligen Artikel hinzuimportieren"
- Reiter „Verkaufskanal aktiv": Häkchen in Vorlage entfernt + Vorlage gespeichert (E37/B21)

**Reiter „Weitere Texte" (E31):** pro Sprache (EN/FR/IT/ES) → CSV `Global-{Sprache}: Artikelname`, `Global-{Sprache}: Titel-Tag`, `Global-{Sprache}: Meta-Description`.

**Cross-Selling-Vorlage:** 3 Spalten — `Artikelnummer`, `Artikelnummer Cross-Seller`, `Cross-Selling-Gruppe`. Standardlieferant nicht relevant für diesen Import-Typ.

---

## 8. Reihenfolge der Imports

Die 5 CSVs werden in WaWi in dieser Reihenfolge importiert (Vorlagen-Slots `_1_` bis `_5_`):

1. **Stammdaten** (Artikel > Artikeldaten) — inkl. Lieferantenblock und 10 Bild-Spalten
2. **Variationen** (Artikel > Variationen) — Sprach-Werte für Größe
3. **Merkmale** (Artikel > Artikelmerkmale)
4. **Attribute** (Artikel > Artikelattribute)
5. **Cross-Selling** (Artikel > Cross-Selling-Artikel — eigener Import-Typ)

---

## 9. Fehler-Handling (Tabelle)

| Situation | Verhalten |
|---|---|
| Lieferantenname nicht im Mapping | STOPP, Verweis auf `LIEFERANTEN-ONBOARDING.md` |
| Pflichtfelder im Mapping null | STOPP, fehlende Werte abfragen |
| Input-Modus nicht eindeutig | STOPP, klären |
| Crawl-Trigger mit Shopify-Detektion erfolgreich | Crawl durchführen via E48 Pfad B. Im Bericht markieren. |
| Pole-Junkie-Crawl (E49 Owner-Direktive) | Ohne Halt durchführen. Im Bericht E49-Verweis. Bei Cease-and-Desist sofort eskalieren und pausieren. |
| Übersetzung scheitert bei einzelnem Feld | Artikel in `_Review/`, andere weiter |
| Pflichtfeld fehlt (Material, Preise, Farbe) | Lauf abbrechen, präzise melden |
| Merkmalwert außerhalb erlaubter Liste | Lauf abbrechen + User-Frage (AP1) |
| Self-Check (Stage 6) scheitert | STOPP, keine partielle Ausgabe |
| Cloud-Storage-Link (Dropbox/WeTransfer) | NICHT blind fetchen — Connector prüfen oder User um lokalen Download bitten |
| Token/Wallclock-Schätzung > Limit (E83) | NICHT halten — Batch-Aufteilung autonom entscheiden (E81), Plan im Bericht dokumentieren |

---

## 10. Konventionen

### Was Cowork DARF
- Files anlegen/lesen/kopieren im Workspace
- GitHub-Raw-Read für Wissens-Files (E87/E91 v1.20)
- Drive-Connector für Lieferanten-Drive-Ordner (Crawl-Input-Modus)
- Übersetzungen erstellen (außer Eigennamen und SEO-Templates)
- HTML-Snippets nach Stil-Briefing generieren
- CSVs validieren und schreiben
- Mid-Run-Read für Charter/LOG/Backlog bei echter Architektur-Klärung (legitim, kein E62-Verstoß)
- Workflow-Entscheidungen autonom treffen (E81): Batch-Splitting, Token-Budget, Stage-Reihenfolge bei Tool-Limits

### Was Cowork NICHT DARF
- Dateien permanent löschen
- WaWi schreibend ändern (Charter Prinzip 3)
- Importvorlagen in Ameise verändern
- A-Nummern vergeben
- `lieferanten_mapping.yaml` ohne User-Bestätigung schreiben
- API-Keys/Credentials im Chat ausgeben oder akzeptieren (E33)
- Bild-Spalten in Stammdaten-CSV mit Hersteller-CDN-URLs befüllen (E44 — nur R2-Public-URLs erlaubt, aus Bildpipeline-Map)
- Produkt-spezifische Meta-Descriptions/Titel-Tags erfinden (E55, AP3)
- Sprach-Namen außerhalb E58-Lookup erfinden (AP8)
- Eigennamen übersetzen (Modellnamen, Brand-Namen)
- Schema-Spalten-Reihenfolge umorganisieren (E54, AP4)
- Kategorie-Werte außerhalb der E51-Tabelle nutzen (AP1)
- Multi-Kategorie-Pattern brechen (E57/E89, siehe Sektion 5.1 und SPEC_KONSTANTEN Self-Check #4)
- Kind-Artikelname ohne Größen-Suffix (E56, AP5)
- SEO-Felder auf Kind-Zeilen befüllen (E56)
- Workflow-Frage statt autonomer Entscheidung (AP9)
- CSV/Lauf-Bericht nach Drive uploaden (AP10, E52/E69)
- Datei-Naming ohne Nummer-Präfix (AP11)
- Leere CSV mit nur Header ausgeben (AP12)

**Vollständige AP1-AP12-Definitionen mit Symptomen + Mitigation:** SPEC_KONSTANTEN Sektion 10.

### Datenstrategien (aktueller Stand)
- **CSVs lokal, kein Drive-Upload** (E52, E69, AP10).
- **Artikelnummer = Lieferantenartikelnummer** (E6, A-Nummer aufgeschoben, B4).
- **Bilder integriert in Stammdaten** (E46), Pipeline deaktiviert (E63).
- **Cross-Selling als 5. CSV** mit Kinder-Replikation (E80 v1.15).
- **Wissens-Backbone Git/GitHub** (E87, ab v1.19).

### Idempotenz
Pro Trigger ein eigener Lauf — keine implizite Wiederholungs-Logik. Re-Import durch Tjorben in WaWi (gleiche CSV erneut) ist außerhalb des Cowork-Scopes.

### Re-Import-Verhalten bei leeren Bild-Spalten (UNVERIFIZIERT — B30, akut ab v1.21)
Mit Bildpipeline-Reaktivierung (E93) wieder relevant: bei Re-Import mit <10 Bildern hinterlässt Cowork die Spalten Bild N..10 leer. Ob JTL die leeren Spalten als „kein Update" oder „aktiv leeren" interpretiert ist UNVERIFIZIERT. Risiko: manuell gepflegte Bilder werden überschrieben. Vor erstem produktiven Re-Import auf bebilderte Artikel: Test-Lauf mit kontrolliertem Artikel.

### Re-Import-Verhalten bei Cross-Selling (TEILVALIDIERT — B49)
Initial-Import validiert in Live-Trial Batch 1+2 2026-05-17 (16/16 Self-Check grün). Re-Import auf bestehende Cross-Selling-Beziehungen NOCH NICHT validiert. Vor erstem produktivem Re-Import: in WaWi alle Cross-Selling-Beziehungen des betroffenen Lieferanten manuell löschen, dann frischer Import.

---

## 11. Credentials und externe Services

Zwei zulässige Mechanismen (E33):

1. **Connector-Setup in Cowork-UI** — Google Drive, Cloudflare Developer Platform, künftige Firecrawl-Aufnahme.
2. **Drive-Credentials-File mit eingeschränktem Zugriff** — `_Credentials/r2_credentials.json`. Im Pilot mit E63 für Daten-Läufe nicht aktiv.

Strikt verboten: API-Keys im Chat, erfundene Mechanismen, Local MCP via `claude_desktop_config.json` als Bridge (E42).

---

## 12. Verwandte Dokumente

- `run_brief_daten.md` — kompakte operative Spec (Stage-0-Pflicht)
- `SPEC_KONSTANTEN.md` — alle Konstanten (Schema, SEO, Sprach-Lookup, Merkmalwerte, Self-Check, AP1-AP12)
- `lieferanten_mapping.yaml` — Lieferanten-Metadaten
- `LIEFERANTEN-ONBOARDING.md` — Onboarding-Prozess (NEU v1.20)
- `CLAUDE.md` — Daily-Workflow für Wissens-Management-Seite (Claude Code lokal)
- `PROJEKT-CHARTER.md` — Architektur-Prinzipien, Trade-offs
- `WAWI-IMPORT-WISSEN.md` — Pilot-Wissen aus echten Ameise-Imports
- `ENTSCHEIDUNGS-LOG-*.md` — Architektur-Entscheidungen pro Cluster (Index in SPEC_KONSTANTEN Sektion 14)
- `BACKLOG.md` — aktive Risiken, neue Findings (erledigte in `BACKLOG-ARCHIV.md`)
