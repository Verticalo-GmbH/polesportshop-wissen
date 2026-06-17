# WaWi-Import-Wissen

> ## 🔒 KANONISCH — IN STEIN GEMEIßELT
>
> Dieses Dokument enthält das **gefrorene** WaWi-Mapping-Wissen. Jedes Detail ist aus echten Ameise-Imports empirisch validiert. Trial-and-Error-Kosten dieser Erkenntnisse sind bekannt (Stunden bis Tage pro Erkenntnis, über mehrere Pilot-Läufe gesammelt). 
>
> **Niemals durch generierte Plausibilität ersetzen.** Bei Konflikt zwischen einer LLM-Generation und einem Eintrag in dieser Datei: diese Datei gewinnt. Bei Lücke (kein Eintrag zur Frage): **STOPP + User-Frage**, statt zu erfinden.
>
> **Diese Datei ändert sich selten.** Updates kommen nur durch echte WaWi-Import-Läufe (nicht durch Spekulation), durch JTL-WaWi-Version-Updates (alle 12+ Monate), oder durch dokumentierte Verifikation eines bisher unverifizierten Verhaltens (z.B. B30).
>
> **Hinweis ab v1.22 (Code-Pivot):** Ausführende Engine ist jetzt die Code-Pipeline (`pipeline/`), nicht mehr Cowork. Wo unten der Begriff Cowork in einer **Regel** steht, gilt sie für die Pipeline; **historische Beispiele** behalten den Begriff. Diese Datei ist **Schema-/WaWi-Referenz** und wird vom Code konsultiert; der 16-Punkte-Self-Check ist als `pipeline/selfcheck.py` verpflichtend (Charter-Prinzip 10, E59).
>
> **Goldstandard-Referenz-Artikel** (E59): die drei HotCakes-Pilot-Artikel Hekate Bodysuit, Arachne Bottom Teal, Savanna Original Top. Strukturelle Abweichungen davon ohne Lieferanten-Mapping-Eintrag = STOPP + User-Frage.

**Stand:** 2026-05-18 (v1.16 — v1.20-Refactor E91: Onboarding-Hinweise jetzt auf `LIEFERANTEN-ONBOARDING.md` zentralisiert, Drive-Verweise auf Git-Pattern aktualisiert. Inhaltlich keine WaWi-Mechanik-Änderung). · **Vorheriger Stand:** 2026-05-17 (Snapshot v1.15) · **Vor-vorheriger Stand:** 2026-05-16 (v1.10) · **Validiert mit:** POLE ADDICT Pilot (2026-05-13) + HotCakes vollständiger Pilot-Lauf (2026-05-14, 3 Väter + 13 Kinder erfolgreich für Stammdaten + Variationen + Merkmale + Attribute) + JTL-Export Artikelmerkmale 13.05.2026 (1709 Zeilen, 478 Artikel, 80 Vater-Kind-Stämme) + Cowork-Setup-Session 2026-05-15 vormittags (R2-Upload-Mechanik fixiert auf Code-Execution + boto3, siehe E43) + HotCakes Arachne-Bottom-Black Bild-Migration 2026-05-15 nachmittags (4 Bilder + 4 Originale auf R2, Re-Import über Stammdaten-CSV mit Bild-Spalten — Plattform-Aktivierung automatisch, B5 gelöst, E46) + JTL-Export Artikelstammdaten 2026-05-15 abends (802 Datenzeilen, 297 mit allen 5 Sprach-Feldern, SEO-Template-Pattern und Sprach-Lokalisierungs-Konvention abgeleitet, E55+E58) + v3.1-Pre-22-Test 2026-05-15 spät (Multi-Kategorie-Mechanik E57 verifiziert, Kind-Name-mit-Größe E56 fixiert) + **HotCakes Live-Trial-Runs Batch 1 + Batch 2 (2026-05-17): 21 Modelle (10 + 11), 16/16 Self-Check grün, Cross-Selling-CSV mit Kinder-Replikation produktiv importiert (180 Zeilen Batch 2)**

> **Änderungen v1.15 (2026-05-17):**
> - **Sektion 9 (Ameise-Vorlagen-Übersicht): HotCakes-Vorlagen-Slots final fixiert** nach Live-Trial Batch 1+2. `merkmale=_3_Merkmale` (korrigiert von `_4_Merkmale`), `attribute=_4_Attribute` (gesetzt), `cross_selling=_5_CrossSelling` (gesetzt). Onboarding pro Lieferant ab v1.14: **5 Vorlagen Pflicht** (4 Artikel + 1 Cross-Selling).
> - **Slot-Konvention pro Import-Typ klargestellt** (neuer Block in Sektion 9): Slot-Nummern sind eindeutig **pro Import-Typ**, NICHT lieferanten-weit. `_3_Merkmale` (Merkmale-Import) ≠ `_3_Lieferantendaten` (Stammdaten-Legacy bei POLE ADDICT); `_5_CrossSelling` (Cross-Selling-Import) ≠ `_5_Bilder` (Stammdaten-Legacy bei HotCakes). Empfohlene Slot-Reihenfolge für neue Lieferanten: `_1_Stammdaten`, `_2_Variationen`, `_3_Merkmale`, `_4_Attribute`, `_5_CrossSelling`. Legacy bei POLE ADDICT + HotCakes-Bilder/Lieferantendaten bleibt aus historischen Gründen, hat keine Funktion mehr.
> - **Standardlieferant in jeder Vorlage Pflicht** (Bug-Beleg Live-Trial Batch 1 Attribute-Import 2026-05-17): 220 Warnungen „Lieferant HOTCAKES existiert nicht" weil `_4_Attribute`-Vorlage Standardlieferanten auf „nicht gewählt" hatte. Lösung: **in jeder der 5 Ameise-Vorlagen muss der Standardlieferant explizit gesetzt sein**, auch wenn die CSV den Lieferanten als Spalte mitliefert. Cowork-Onboarding-Checkliste und Sektion 9 entsprechend verschärft.
> - **Architektur-Header: 4 CSVs → 5 CSVs** (Cross-Selling als 5. CSV seit v1.14, E80). War in v1.14 noch inkonsistent dokumentiert.
>
> **Änderungen v1.10 (2026-05-16):**
> - **Sektion 10.5 (Anti-Patterns AP1-AP8) gewandert in `SPEC_KONSTANTEN.md` Sektion 10.** Begründung: Konstanten-Auslagerung gemäß E61/Charter-Prinzip 11. AP1-AP8 sind harte Lookup-Konstanten und gehören zur kanonischen Konstanten-Datei. Cowork konsultiert sie aus `SPEC_KONSTANTEN.md`, nicht mehr aus dieser Datei.
> - **`SPEC_KONSTANTEN.md` ist ab v1.10 kanonisch für alle Konstanten** (48-Spalten-Schema, SEO-Templates, Sprach-Lookup, Merkmalwerte, Kategorien, Self-Check 12-Punkte, AP1-AP8 — v1.15: erweitert auf AP1-AP12). Diese Datei (`WAWI-IMPORT-WISSEN.md`) bleibt operative Wahrheit für Stolperfallen, Pilot-Erfahrungen und das *Wie* der Imports — bei Konflikt zwischen SPEC_KONSTANTEN und WAWI-IMPORT-WISSEN: STOPP + User-Frage (siehe Konflikt-Auflösung in SPEC_KONSTANTEN.md).

Dieses Dokument bündelt das gesamte operative Wissen über die Daten-Übergabe von CSVs an JTL-WaWi via Ameise. Alles, was hier steht, ist im echten Pilot-Lauf erprobt und funktioniert. Wer in einem neuen Chat weiterarbeitet, kann sich auf diese Konventionen verlassen — sie sind hart erkämpft.

> **Wichtiger Hinweis Stand 2026-05-14 (nach HotCakes-Pilot, historisch):** Die Pipeline hatte sich auf 5 CSVs stabilisiert: Stammdaten (inkl. Lieferantenblock-Spalten) + Variationen + Merkmale + Attribute + Bilder. Die in v1.2 zusätzlich vorgesehene separate Lieferantendaten-CSV wurde abgeschafft (E35) — ihre Felder leben seitdem direkt in der Stammdaten-CSV (E36, 38 Spalten). Attribute sind Standard (E39). Bilder werden auf Vater UND alle Kinder dupliziert (E34, gleicher Mechanismus wie Merkmale).

> **Wichtiger Hinweis Stand 2026-05-15 vormittags (nach Cowork-Setup-Session, historisch):** Die R2-Upload-Mechanik für Bilder ist final fixiert (E43, Pfad b): Code-Execution + boto3 + Network-Egress-Allowlist + Credentials aus Drive-File. Kein nativer R2-MCP-Connector — der Cloudflare Developer Platform Connector deckt nur Bucket-Lifecycle ab. Praktisch ändert sich am CSV-Schema dieser Datei nichts; die R2-URLs sehen aus wie zuvor. Die Mechanik dahinter ist Sache der Bildpipeline-Spec (`cowork_anweisung_bildpipeline.md`).

> **Wichtiger Hinweis Stand 2026-05-15 nachmittags (Pivot-Tag — der wichtigste Eintrag in diesem Dokument):** Die Pipeline ist auf **4 CSVs** reduziert (E46): Stammdaten + Variationen + Merkmale + Attribute. Die separate Bilder-CSV ist **abgeschafft**. Bild-URLs leben jetzt als 10 zusätzliche Spalten `Bild 1` bis `Bild 10` direkt in der Stammdaten-CSV (Schema v3, 48 Spalten = 38 + 10). Plattform-Aktivierung läuft automatisch über den Stammdaten-Import: die Ameise-Vorlage hat im Reiter „Bilder/Plattformen" alle 11 Plattform-Häkchen gesetzt, und alle Bilder werden beim Stammdaten-Import sofort für alle Plattformen aktiviert. Damit ist B5 (Plattform-Aktivierung) automatisch gelöst — keine manuellen „Alle aktivieren"-Klicks mehr nötig. Validiert mit Arachne-Bottom-Black-Re-Import am 2026-05-15: alle 9 Plattform-Häkchen automatisch gesetzt, Shop-Bilder sichtbar auf allen Verkaufskanälen. R2 ist außerdem vollständiger Bild-Storage geworden (E44): Originale liegen auf `originals/<lieferant>/` mit Magic-Byte-erkannter Extension, Verarbeitete auf `<lieferant>/`. Drive-Archiv für Originale entfällt. Plus neue Crop-Profile pro Produkttyp und Vision-basierte Pose-Sortierung (E45) — operativ unsichtbar, bezieht sich nur auf die Bildpipeline.

> **Wichtiger Hinweis Stand 2026-05-17 (Live-Trial Batch 1+2):** 5-CSV-Architektur mit Cross-Selling produktiv erprobt. 21 Modelle (10 + 11) erfolgreich importiert, 16/16 Self-Check grün in beiden Batches, Cross-Selling-CSV mit Kinder-Replikation (E80-Erweiterung) lief problemlos durch. Vorlagen-Setup bei Tjorbens HotCakes ist final: 5 aktive Vorlagen (`_1_Stammdaten`, `_2_Variationen`, `_3_Merkmale`, `_4_Attribute`, `_5_CrossSelling`), plus 2 Legacy ohne Funktion (`_3_Lieferantendaten` aus alter Naming-Konvention von vor E35, `_5_Bilder` aus alter Pipeline von vor E46 — gleiche Slot-Nummer wie aktuelles Cross-Selling, weil Slots pro Import-Typ unterschiedlich sind). Bug-Beleg: Im Batch-1-Attribute-Import gab es 220 Warnungen „Lieferant HOTCAKES existiert nicht", weil die `_4_Attribute`-Vorlage Standardlieferanten auf „nicht gewählt" hatte. Konsequenz: in jeder der 5 Vorlagen Standardlieferanten explizit setzen.

## 1. Architektur in einem Absatz

JTL-WaWi 1.10.15.0 ist das Warenwirtschafts-Backend. **JTL-Ameise** ist das CSV-Import-Tool von JTL, mit dem strukturierte Daten in WaWi reinkommen. Die Pipeline produziert pro Lieferanten-Lauf **fünf CSVs** (Stammdaten mit integriertem Lieferantenblock und 10 Bild-URL-Spalten, Variationen, Merkmale, Attribute, Cross-Selling — Cross-Selling seit v1.14, E80), die in einer bestimmten Reihenfolge in Ameise importiert werden. Jede CSV hat ihr eigenes Ameise-Vorlagen-Profil mit spezifischem Spalten-Mapping und Identifikator-Setting. Die Pipeline generiert die CSVs, der Einkäufer führt die Ameise-Imports manuell durch — die Pipeline schreibt nicht selbst in WaWi. Die Bildpipeline läuft als eigenständiger Sub-Process (E12), gibt aber keine separate CSV mehr aus, sondern eine Map `{artikelnummer: [bild_urls]}`, die die Daten-Pipeline in die 10 Bild-Spalten der Stammdaten-CSV einbettet.

## 2. Globale CSV-Format-Regeln (für alle fünf CSVs gleich)

| Parameter | Wert | Warum |
|---|---|---|
| **Encoding** | UTF-8 **mit** BOM (`utf-8-sig` in Python) | Ohne BOM liest Ameise den ersten Spaltennamen falsch (`\ufeffArtikelnummer` statt `Artikelnummer`) → Mapping bricht |
| **Trennzeichen** | Semikolon `;` | DE-Locale-Standard, Komma kollidiert mit Dezimal-Komma in Preisen |
| **Quote-Zeichen** | doppeltes Anführungszeichen `"` | Ameise-Default |
| **Quoting-Strategie** | minimal für Stammdaten/Variationen/Merkmale/Cross-Selling; **alle Felder** für Attribute | Attribute enthalten HTML mit Sonderzeichen, daher `csv.QUOTE_ALL` |
| **Zeilenende** | CRLF (`\r\n`) | Windows-Standard, Ameise erwartet das |
| **Dezimaltrennzeichen** | Komma (`12,50` nicht `12.50`) | DE-Locale, sonst werden Preise als String interpretiert |
| **Datei-Endung** | `.csv` | Ameise erkennt am Namen, nicht am Mime-Type |

Diese Regeln gelten universell. Abweichungen produzieren reproduzierbar Import-Fehler.

## 3. Reihenfolge der Imports (kritisch)

Die fünf CSVs müssen in dieser Reihenfolge importiert werden, weil jeder folgende Import auf den vorherigen verweist:

1. **Stammdaten** zuerst — Artikel muss in WaWi existieren, bevor irgendetwas auf ihn verweisen kann (Import-Typ: *Artikel > Artikeldaten*). Inkl. Lieferantenblock-Spalten (Netto-EK, Ist Standardlieferant, Lieferzeit in Tagen) **und 10 Bild-URL-Spalten `Bild 1` bis `Bild 10`**. Plattform-Aktivierung der Bilder läuft beim Stammdaten-Import automatisch durch konfigurierte Häkchen im Reiter „Bilder/Plattformen" der Vorlage.
2. **Variationen** — pflegt die Sprach-Varianten von Variationsname und Variationswertname (Import-Typ: *Artikel > Variationen*)
3. **Merkmale** — referenziert die Artikel via Lieferantenartikelnummer (Import-Typ: *Artikel > Artikelmerkmale*)
4. **Attribute** — Reichtext-Inhalte in 5 Sprachen (Import-Typ: *Artikel > Artikelattribute*)
5. **Cross-Selling** — Beziehungen zwischen Artikeln (Import-Typ: *Cross-Selling-Artikel*, eigene Sektion im Ameise-Menü, NICHT Teil von „Artikeldaten"). Seit v1.14 / E80.

Wenn Schritt 1 fehlschlägt, alle anderen abbrechen. Wenn Schritte 2-5 fehlschlagen, der Artikel ist im Shop, aber unvollständig — manuelle Nacharbeit in WaWi nötig.

> **Historische Hinweise:**
> - Bis 2026-05-14 stand zwischen Variationen und Merkmalen eine separate Lieferantendaten-CSV (Import-Typ *Artikel > Artikeldaten des Lieferanten*). Mit E35 ist dieser Schritt entfallen — Lieferantenfelder kommen mit der Stammdaten-CSV mit. Die HotCakes-Vorlage `HotCakes Polewear_3_Lieferantendaten` bleibt als Legacy in WaWi ohne Funktion.
> - Bis 2026-05-15 vormittags stand nach Attributen ein separater Bilder-Import (Import-Typ *Bilder > Artikelbilder pro Plattform*). Mit E46 (2026-05-15 nachmittags) ist dieser Schritt entfallen — Bild-URLs kommen mit der Stammdaten-CSV mit, Plattform-Aktivierung läuft automatisch über die Vorlage. Die HotCakes-Vorlage `HotCakes Polewear_5_Bilder` bleibt als Legacy in WaWi ohne Funktion. Drei Schreibversuche für eine separate Bilder-CSV mit Plattform-Aktivierung (Pattern 1 = mehrere Zeilen pro Artikel, Pattern 2 = Verknüpfungs-Import, Pattern 3 = manuelles „Alle aktivieren") sind alle verworfen — die Lösung kam aus der JTL-Doku selbst (siehe Anomalie A4 in BACKLOG).
> - Bis 2026-05-16 (v1.13) war Cross-Selling manuelle Pflege in der WaWi-Artikelmaske. Mit E80 (v1.14) als 5. CSV automatisiert. **Bei Live-Trial Batch 1+2 2026-05-17 erstmals produktiv eingesetzt.**

---

## 4. CSV 1: Stammdaten

### Schema (48 Spalten — Stand 2026-05-15 v3 nach E46)

Spalten in der Reihenfolge, die sich im HotCakes-Lauf etabliert hat. Vollständige Liste:

**Identifikation (4):** `Artikelnummer; Artikelnummer (Lieferant); HAN; Identifizierungsspalte Vaterartikel`
**Hauptdaten DE (4):** `Artikelname; Hersteller; Steuerklasse; TARIC-Code`
**Variation (2):** `Variationsname 1; Variationswert 1`
**Kategorie (2):** `Kategorie Ebene 1; Kategorie Ebene 2`
**Preise (2):** `EK Netto (für GLD); Brutto-VK`
**Lieferantenblock (3) — NEU mit E36:** `Netto-EK; Ist Standardlieferant; Lieferzeit in Tagen (Lieferant)`
**Lager & Status (3):** `Bestandsführung aktiv; Neu im Sortiment; Neu im Sortiment seit`
**Gewicht & Versand (4):** `Artikelgewicht; Versandgewicht; Versandklasse; Herkunftsland`
**Sprach-Artikelnamen (4):** `Global-Englisch: Artikelname; Global-Französisch: Artikelname; Global-Italienisch: Artikelname; Global-Spanisch: Artikelname` — gemappt über Reiter "Weitere Texte"
**Meta-Daten DE (2, nur Vater):** `Titel-Tag (SEO); Meta-Description (SEO)`
**Meta-Daten Sprachen (8, nur Vater):** `Global-Englisch: Titel-Tag; Global-Englisch: Meta-Description` + analog für FR/IT/ES — gemappt über Reiter "Weitere Texte"
**Bilder (10) — NEU mit E46:** `Bild 1; Bild 2; Bild 3; Bild 4; Bild 5; Bild 6; Bild 7; Bild 8; Bild 9; Bild 10` — Public-R2-URLs, leere Strings bei weniger Bildern. Plattform-Aktivierung läuft beim Import automatisch über die im Reiter „Bilder/Plattformen" der Vorlage konfigurierten 11 Plattform-Häkchen.

### Vater-Kind-Logik

Pro Modell+Farbe gibt es **eine Vater-Zeile** plus **eine Kind-Zeile pro Größenvariante**. Mit Multi-Kategorie-Zuweisung (E57) werden alle diese Zeilen verdoppelt — eine pro Kategorie-Zuweisung. Die Vater-Zeilen werden zuerst geschrieben, dann die zugehörigen Kinder direkt darunter.

> **🔢 E94 (ab 2026-06-17) — Artikelnummer aus dem WaWi-Nummernkreis (Weg B):** Die `Artikelnummer` ist seit E94 die **numerische A-Nummer** aus dem fortlaufenden WaWi-Nummernkreis (`A` + laufende Nummer, z.B. `A1009262`; Kinder `A1009262-001`…), **vorab** von der Pipeline vergeben (`pipeline/numbering.py`, Zähler in `pipeline/state/nummernkreis.json`). Grund: Der Lager-Scan identifiziert über die Artikelnummer; sprechende Schlüssel waren nicht scannbar. Der sprechende Schlüssel (`HC-Hekate-Bodysuit`) lebt weiter in `Artikelnummer (Lieferant)`. Verknüpfung Vater-Kind + Cross-Selling laufen über die A-Nummer; Merkmale/Attribute weiter über `Artikelnummer (Lieferant)`. **Ameise-Vorlagen unverändert** (Identifikator = Artikelnummer, Auto-Vergabe AUS). In den folgenden Beispielen steht weiterhin `HC-Hekate-Bodysuit` zur Illustration der Struktur — der reale Wert in `Artikelnummer` ist die A-Nummer, in `Artikelnummer (Lieferant)` der sprechende Schlüssel.

**Vater-Zeile:**
- `Artikelnummer` = **A-Nummer aus WaWi-Nummernkreis (E94)**, z.B. `A1009262` — vorab vergeben
- `Artikelnummer (Lieferant)` = **sprechender Schlüssel** `HC-Hekate-Bodysuit` (Identifikator Merkmale/Attribute; Mapping-Strategie Abschnitt 8)
- `HAN` = leer (reserviert für echte Hersteller-/Barcode-Nummern vom Lieferanten)
- `Identifizierungsspalte Vaterartikel` = **leer** (das ist das Signal "ich bin der Vater")
- `Artikelname` = Format `{Hersteller} {Produkttyp} {Modell} {Farbe}`, z.B. `HotCakes Bodysuit Hekate Schwarz` — **ohne Größe** (E56, Konvention siehe E26)
- `Variationsname 1` = `Größe`
- `Variationswert 1` = **leer** (Vater hat selbst keinen Variantenwert)
- `Kategorie Ebene 1` = `Pole Dance Kleidung` (für Kleidungs-Pilot, E51)
- `Kategorie Ebene 2` = entweder leer (Oberkategorie-Zeile) oder Unterkategorie wie `Bodysuits` / `Pole Dance Tops` / `Pole Dance Shorts` (E51) — mit Multi-Kategorie-Mechanik (E57) gibt es **zwei Vater-Zeilen** pro Modell, eine mit leer und eine mit Unterkategorie
- `Steuerklasse` = `OSS2-undefiniert - Standard alle Länder` (Kleidung-Default)
- `TARIC-Code` = `62114390` (Kleidung-Default)
- `Artikelgewicht` = `0,05` (Kleidung-Default, in kg)
- `Versandgewicht` = `0,05`
- `Versandklasse` = `standard`
- `Bestandsführung aktiv` = `Y`
- `Neu im Sortiment` = `Y`
- `Neu im Sortiment seit` = Lauf-Datum (Format `DD.MM.YYYY`, z.B. `14.05.2026`)
- **Lieferantenblock** befüllt: `Netto-EK` in Originalwährung (z.B. `39,00`), `Ist Standardlieferant` = `Y`, `Lieferzeit in Tagen (Lieferant)` = `0` (Pilot-Default)
- **Bilder** (`Bild 1` bis `Bild 10`): R2-Public-URLs für alle Bilder des Artikels in der von der Bildpipeline gelieferten Reihenfolge; `Bild N+1` bis `Bild 10` leer
- **Sprach-Artikelnamen (4):** lokalisiert nach E58-Konvention — Brand + Eigennamen unverändert, Produkt-Substantive nach Übersetzungstabelle, Farb-Adjektive konsequent lokalisiert
- **SEO-Felder (Titel-Tag + Meta-Description in allen 5 Sprachen):** befüllt nach E55-Template — **nur auf Vater-Zeilen**, mit Vater-Namen ohne Größe als `{name}`-Variable. Bei Multi-Kategorie-Doppelzeilen sind die SEO-Felder auf **beiden** Vater-Zeilen identisch (es ist der gleiche Artikel).

**Kind-Zeile:**
- `Artikelnummer` = **Vater-A-Nummer + `-001`, `-002`** … aufsteigend nach Größe (E94), z.B. `A1009262-001` (XS)
- `Artikelnummer (Lieferant)` = sprechender Kind-Schlüssel (Vater-Schlüssel + `_<Größe>`, z.B. `HC-Hekate-Bodysuit_XS`) — Identifikator für Merkmale/Attribute
- `Identifizierungsspalte Vaterartikel` = **Vater-A-Nummer** (z.B. `A1009262`) — das ist die Verknüpfung (E94: über A-Nummer, nicht mehr über den sprechenden Schlüssel)
- `Artikelname` (alle 5 Sprachen) = Vater-Name + Leerzeichen + Variationswert (E56) — z.B. DE `HotCakes Bodysuit Hekate Schwarz XS`, FR `HotCakes Body Hekate Noir XS`, IT `HotCakes Body Hekate Nero XS`. Die Größe ist in allen 5 Sprachen identisch (XS/S/M/L/XL/2XL universal).
- `Variationsname 1` = `Größe`
- `Variationswert 1` = Variantenwert, z.B. `XS`
- Alle anderen Felder (Hersteller, Steuerklasse, TARIC, Preise, Gewichte etc.) identisch zum Vater
- **Lieferantenblock** identisch zum Vater (gleicher Lieferant, gleicher Netto-EK, gleiche Lieferzeit)
- **Bilder** (`Bild 1` bis `Bild 10`): **identische URLs wie Vater** (E34/E46-Duplizierung, JTL erbt Bilder nicht implizit zu Kindern)
- **SEO-Felder (Titel-Tag, Meta-Description in allen 5 Sprachen):** **leer auf Kindern** (E56 — Best-Practice aus polesportshop-Bestand, validiert im Export)
- Kategorie-Zuweisung: identisch zur Multi-Kategorie-Logik des Vaters — pro Kind ebenfalls **zwei Zeilen** (eine Oberkategorie, eine Unterkategorie) bei aktiver Multi-Kategorie (E57)

### Multi-Kategorie-Mechanik (E57)

**🔒 Anti-Confusion-Note (E75, NEU v1.13): wenn jemand „doppelte Größen", „Stammdaten-Zeilen doppelt vorhanden" oder „Bug in der CSV" meldet — KEIN Spec-Eingriff in E57. Die Doppelzeilen sind ARCHITEKTUR, nicht Bug. Erst dieses Vorlagen-Setting in WaWi prüfen:**

> **„Kategorieverknüpfungen des Artikels aktualisieren" = „Neue Kategorien beim jeweiligen Artikel hinzuimportieren"**

**Default ist „Nicht aktualisieren" — dann sind die Doppelzeilen funktionslos und Ameise verhält sich, als wären es Duplikate.** Wenn das Setting nicht stimmt: Setting fixen, Vorlage speichern, originale CSV nochmal importieren. **Niemals eine „gefixte" CSV mit halbierter Zeilenzahl bauen, ohne diesen Cross-Check durchgeführt zu haben.** Goldstandard-Referenz: `1_Stammdaten_HotCakes_2026-05-16.csv` (im Pilot-Hauptordner) — funktioniert mit Doppelzeilen + korrektem Setting sauber.

Dieser Hinweis steht hier weil im Klärungs-Chat 2026-05-16 die Diagnose voreilig in Richtung „Spec-Bug" lief und beinahe eine korrekte Architektur gekippt worden wäre. Charter-Prinzip-10 + Spec-Cross-Check vor jedem Fix-Vorschlag.

**v1.15-Validierung:** Live-Trial Batch 1+2 (2026-05-17) hat E57-Doppelzeilen erneut produktiv bestätigt — 21 Modelle mit Multi-Kategorie-Mechanik, alle Artikel landen sowohl in Oberkategorie als auch in passender Unterkategorie. Doppelzeilen-Architektur ist endgültig stabil.

**Update v1.16/E92 (2026-05-18): 3-Zeilen-Pattern ab v1.21.** Zusätzlich zu den E57-Doppelzeilen (Oberkategorie + Unterkategorie) kommt seit E89/E92 eine **3. Zeile** pro Artikel für den Sara-Review-Workflow: `Kategorie Ebene 1 = Intern`, `Kategorie Ebene 2 = Neue Artikel für Sara` (WaWi-Key 546). Sara prüft, entfernt die 546-Zuweisung nach Approval manuell. Hintergrund: v1.19/E89 hatte fälschlich angenommen, dass eine einzige Subkategorie-Zeile reicht (WaWi resolved Pfad selbst) — Trial-Lauf 2026-05-18 21:06 zeigte fehlende Oberkategorie im Shop, E57-Doppel-Pattern bleibt also gültig, Sara als 3. Zeile ergänzt.

---

JTL-Ameise bietet **keine zusätzlichen Kategorie-Spalten** in der Stammdaten-CSV. Multi-Kategorie pro Artikel geht ausschließlich über **doppelte Zeilen** mit gleicher Artikelnummer:

```
Zeile A — Oberkategorie-Zuweisung:
   Artikelnummer = HC-Hekate-Bodysuit
   ...
   Kategorie Ebene 1 = Pole Dance Kleidung
   Kategorie Ebene 2 = (leer)
   SEO-Felder = befüllt (Vater)

Zeile B — Unterkategorie-Zuweisung:
   Artikelnummer = HC-Hekate-Bodysuit
   ...
   Kategorie Ebene 1 = Pole Dance Kleidung
   Kategorie Ebene 2 = Bodysuits
   SEO-Felder = befüllt (Vater, identisch zu Zeile A)
```

Gilt **sowohl für Vater als auch für jedes Kind**. Pro Modell mit N Kind-Größen entstehen also `2 × (1 + N)` Zeilen.

**Ameise-Vorlagen-Setting (verpflichtend, einmalig pro Lieferanten-Vorlage):**
- Einstellung: **„Kategorieverknüpfungen des Artikels aktualisieren"**
- Wert: **„Neue Kategorien beim jeweiligen Artikel hinzuimportieren"**
- Default ist „Nicht aktualisieren" — dann werden die zweite und alle weiteren Kategorie-Zuweisungen ignoriert.
- Vorlage anschließend speichern, gilt session-übergreifend.

**Setting-Name in Tjorbens Ameise-Version (1.10.15.0):** „Kategorieverknüpfungen des Artikels aktualisieren". In älterer Forum-Doku auch als „Aktualisierung von Kategorien eines Artikels" bezeichnet — funktional identisch.

### SEO-Templates pro Sprache (E55)

**Deterministisches Pattern aus polesportshop-Bestand** (im JTL-Export 2026-05-15 über 30 Stichproben verifiziert, 100 % konsistent). Einzige Variable: `{name}` = Vater-Artikelname **ohne Größe**.

**Titel-Tag pro Sprache:**

| Sprache | Format |
|---|---|
| DE | `{name} \| polesportshop.de` |
| EN | `{name} \| polesportshop.de` (nicht `.com`) |
| FR | `{name} \| polesports.fr` |
| IT | `{name} \| polesports.it` |
| ES | `{name} \| polesports.es` |

**Meta-Description pro Sprache** (HTML-Entities: `&#10004;` = ✓, `&#10148;` = ➜, **direkt so verwenden — keine Unicode-Zeichen einsetzen**):

| Sprache | Format |
|---|---|
| DE | `{name} &#10004; große Auswahl &#10004; TOP Preise &#10004; Schneller Versand &#10148; jetzt hier online bestellen!` |
| EN | `{name} &#10004; Five star customer support &#10004; Top quality and price &#10004; Instant shipping &#10148; order now!` |
| FR | `{name} &#10004; Support client cinq étoiles &#10004; Qualité et prix au top &#10004; Expédition instantanée &#10148; commandez maintenant !` |
| IT | `{name} &#10004; Assistenza clienti a cinque stelle &#10004; Qualità e prezzo al top &#10004; Spedizione immediata &#10148; ordina ora!` |
| ES | `{name} &#10004; Soporte al cliente de cinco estrellas &#10004; Calidad y precio superiores &#10004; Envío instantáneo &#10148; ¡Ordénalo ahora!` |

**SEO-Felder leben ausschließlich auf Vater-Zeilen** (siehe Kind-Zeile oben). Auf allen Kind-Zeilen sind alle 10 SEO-Spalten (DE + 4 Sprachen × 2 Felder) leer.

**Verbot:** keine produkt-spezifische Meta-Description erfinden („Mesh-Bodysuit mit Marmor-Print, tiefem Ausschnitt..." — Cowork-Erfindung aus 3-Modell-Batch). Die produktspezifische Beschreibung lebt im Attribut `artikeldetails` mit E53-Stil, klar getrennt von SEO-Metadaten.

### Sprach-Lokalisierungs-Konvention für Artikelnamen (E58)

Aus polesportshop-Bestand abgeleitet (30 Stichproben über mehrere Brands):

| Element | Behandlung | Beispiele |
|---|---|---|
| Brand-Name | unverändert in allen 5 Sprachen | HotCakes, FANNA, Polerina, Pole Addict, Shark Polewear, Dragonfly, Lunalae, Paradise Chick, Bandurska |
| Eigennamen (Modell-Namen) | unverändert | Hekate, Arachne, Savanna, Emma, Carla, Monica, Isla, „Bali Grape", „X Spark Edition" |
| Produkt-Substantiv | meist lokalisiert (Tabelle unten) | Bodysuit → Body (FR/IT/ES); Shorts → Short (FR), Pantalones Cortos (ES); Top → Haut (FR) |
| Material/Style-Substantiv | meist lokalisiert | Mesh → Maille/Maglia/Malla; Velvet bleibt überall |
| Farb-Adjektiv | konsequent lokalisiert | Schwarz/Black/Noir/Nero/Negro; Türkis/Teal/Turquoise/Turchese/Turquesa |
| Größen-Suffix | identisch in allen Sprachen | XS, S, M, L, XL, 2XL (universal) |

**Produkt-Substantiv-Tabelle (explizit, weil häufig falsch):**

| DE | EN | FR | IT | ES |
|---|---|---|---|---|
| Bodysuit | Bodysuit | Body | Body | Body |
| Shorts | Shorts | Short | Shorts | Pantalones Cortos |
| Top | Top | Haut | Top | Top |
| Leggings | Leggings | Legging | Leggings | Leggings |

**Farb-Tabelle (häufig in Pole-Wear, explizit):**

| DE | EN | FR | IT | ES |
|---|---|---|---|---|
| Schwarz | Black | Noir | Nero | Negro |
| Weiß | White | Blanc | Bianco | Blanco |
| Türkis | Teal | Turquoise | Turchese | Turquesa |
| Pink | Pink | Rose | Rosa | Rosa |
| Burgundrot | Burgundy | Bordeaux | Borgogna | Burdeos |
| Beige | Beige | Beige | Beige | Beige |

Die Pipeline hat damit eine geschlossene Lookup-Tabelle für Standard-Vokabular — keine LLM-Übersetzung für die gängigen Pole-Wear-Begriffe. Bei seltenen/neuen Begriffen darf die Pipeline übersetzen, muss das aber im Lauf-Bericht markieren.

**Verbot:** keine Sprach-Namen erfinden. Konkrete Vorfälle aus 3-Modell-Batch:
- „Arachne Blau" (EN) statt „Arachne Teal" — falsche Farb-Übersetzung
- DE-Begriff im EN-Slot belassen (z.B. „Burgundrot" statt „Burgundy")

### Ameise-Import-Settings

| Setting | Wert |
|---|---|
| Vorlage | `{Lieferantenname}_1_Stammdaten` (pro Lieferant einmal angelegt, neue Naming-Konvention E29) |
| Import-Typ | Artikel > Artikeldaten |
| Encoding | UTF-8 mit BOM |
| Trennzeichen | `;` |
| Quote | `"` |
| Identifikator | `Artikelnummer` |
| Vaterartikel identifizieren anhand | `Artikelnummer` |
| Vaterartikel-ID-Feld ist | `Artikelnummer` |
| Varkombi-Behandlung | "Variationen und Werte im Vaterartikel erstellen" |
| **Kategorieverknüpfungen des Artikels aktualisieren (E57)** | **„Neue Kategorien beim jeweiligen Artikel hinzuimportieren"** — Pflicht für Multi-Kategorie-Doppelzeilen, Default ist „Nicht aktualisieren" |
| **Standardlieferant (v1.15, NEU Pflicht)** | **explizit auf den Lieferanten setzen** (z.B. HOTCAKES für HotCakes Polewear) — Pflicht in jeder Vorlage, auch wenn CSV den Lieferanten als Spalte mitliefert. Bug-Beleg: Live-Trial Batch 1 Attribute-Import 2026-05-17 mit 220 Warnungen wegen `_4_Attribute`-Vorlage mit Standardlieferant „nicht gewählt" |

**Wichtig — Reiter "Weitere Texte"** (unten in Ameise, zwischen "Sonderpreise" und "Verkaufskanal aktiv"): hier werden alle Sprach-Spalten zugewiesen. Tabelle mit drei Spalten *Datenfeld / Sprache / Spalte in Importdatei*. Pro Sprache (Englisch, Französisch, Italienisch, Spanisch) jeweils:
- "Artikelname, {Sprache}" → CSV-Spalte `Global-{Sprache}: Artikelname`
- "Titel-Tag, {Sprache}" → CSV-Spalte `Global-{Sprache}: Titel-Tag`
- "Meta-Description, {Sprache}" → CSV-Spalte `Global-{Sprache}: Meta-Description`

**Wichtig — Verkaufskanal aktiv** (rechts oben im Standardwerte-Bereich): defaultmäßig sind alle Häkchen gesetzt (polesportshop.de, poledanceshop.de, Mobile Kasse). **Bei Vorlagen-Anlage Häkchen entfernen und Vorlage speichern** (E37) — sonst gehen Artikel sofort online beim Import.

**Wichtig — Lieferantenblock-Spalten** (E36): Die drei neuen Spalten werden im Bereich "Lieferanteneinstellungen des Artikels" der Vorlage zugeordnet. **Standardwert "Währung"** in der Vorlage auf den Lieferanten-Wert setzen (z.B. EUR für HotCakes) — nicht als CSV-Spalte führen, da pro Lieferant konstant.

**Wichtig — Bilder-Spalten (NEU mit E46):** Die 10 Bild-Spalten der CSV werden auf die JTL-Felder `Bild Pfad/URL 1` bis `Bild Pfad/URL 10` gemappt. Zusätzlich im Reiter „Bilder/Plattformen" der Vorlage alle 11 Plattform-Häkchen setzen (polesportshop.de, poledanceshop.de, alle 7 Amazon-Marktplätze, plus die zwei weiteren Plattform-Einträge in der HotCakes-Vorlage) — dadurch werden die Bilder beim Stammdaten-Import sofort für alle Plattformen aktiviert. Manuelle „Alle aktivieren"-Klicks pro Artikel entfallen damit komplett (B5 gelöst).

### GLD manuell setzen via Stammdaten-CSV

Der Wert in der CSV-Spalte `EK Netto (für GLD)` greift im Artikeldaten-Import **wenn die Spalte beim Mapping manuell zugeordnet wird** auf das JTL-Feld "Ø Einkaufspreis (netto)". Das Auto-Mapping über den Spaltennamen greift bei `EK Netto (für GLD)` nicht zuverlässig — manuelle Zuordnung in der Vorlage löst das Problem dauerhaft (Vorlage speichern, E38).

Hintergrund: GLD = "Gleitender Durchschnitt", der "Ø Einkaufspreis (netto)" in der Artikel-Ansicht. JTL-Default-Mechanik berechnet ihn aus Eingangsrechnungen. Wir setzen ihn manuell pro Stück nach E23-Formel: `GLD = EK_Rechnung + Zoll + Versand` (aus Referenztabellen). Bei HotCakes alle Werte = EK_Rechnung (Zoll 0, Versand 0).

**Verworfener Workaround:** ein separater "Preise/Bestände (QuickSync)"-Import — nicht nötig, manuelle Mapping-Zuordnung im Stammdaten-Import reicht.

### Stolperfallen
- **`Identifizierungsspalte Vaterartikel` leer beim Kind** → Kind wird als eigenständiger Artikel angelegt, kein Vater-Kind-Verhältnis
- **HAN gefüllt mit Hilfsdaten** → bricht später, wenn echte Barcodes vom Lieferanten kommen; HAN reserviert lassen
- **Kategorie-Ebenen leer** → Artikel landet ohne Kategorie, ist im Shop unsichtbar
- **Multi-Kategorie ohne Doppelzeilen** → Artikel landet nur in einer der gewünschten Kategorien (E57)
- **Multi-Kategorie-Doppelzeilen aber Ameise-Setting auf „Nicht aktualisieren"** → zweite Zuweisung wird ignoriert, Effekt identisch zu Einzelzeile (E57)
- **Kind-Artikelname ohne Größen-Suffix** → WaWi-UI zeigt alle Größen mit identischem Namen, keine Unterscheidung in Listen (E56)
- **SEO-Felder auch auf Kind-Zeilen gefüllt** → unnötige Duplikation; im polesportshop-Bestand liegen SEO-Felder grundsätzlich nur auf Vater (E56, validiert in 297 Bestand-Artikeln)
- **Eigene Meta-Description statt E55-Template** → Cowork-Erfindung, inkompatibel mit historischem Shop-Pattern; produzierte Probleme im 3-Modell-Batch (E55, E59)
- **HTML-Entities `&#10004;` durch Unicode `✓` ersetzt** → SEO-Templates erwarten die Entities so wie sie historisch im Shop sind (E55)
- **EN-Titel-Tag mit `polesportshop.com`** → falsch; EN nutzt auch `polesportshop.de` (E55, im Export bestätigt)
- **Sprach-Namen mit DE-Begriffen belassen** (z.B. „Burgundrot" im EN-Slot) → E58-Verstoß, falsche Lokalisierung
- **Eigennamen übersetzt** (z.B. „Hekate" zu „Hecate") → E58-Verstoß, Eigennamen bleiben unverändert
- **Verkaufskanal-Häkchen in Vorlage gesetzt** → Artikel gehen sofort online (E37/B21)
- **EK Netto (für GLD) wird nicht durchgreifen** → manuelle Mapping-Zuordnung beim Import (E38, Auto-Mapping greift nicht zuverlässig)
- **Reiter "Weitere Texte" nicht öffnen** → Sprach-Spalten werden nicht importiert, Artikel hat nur DE-Texte
- **Lieferantenblock-Spalten nicht gemappt** → Netto-EK, Standardlieferant-Flag und Lieferzeit nicht am Artikel, manuelle Nacharbeit nötig
- **„Bilder/Plattformen"-Häkchen in der Vorlage nicht gesetzt** → Bilder werden zwar am Artikel angehängt, aber nicht für die Shop-Plattformen aktiviert (B5 fällt zurück auf alten Pilot-Workaround). Beim Anlegen einer neuen Lieferanten-Stammdaten-Vorlage explizit prüfen.
- **Bild-Spalten nicht gemappt** → Bilder bleiben am Artikel komplett aus, Detailseite hat keine Bilder
- **Re-Import mit leeren Bild-Spalten auf einen Artikel, der bereits Bilder hat** → Verhalten **unverifiziert** (B30): unklar, ob bestehende Bilder gelöscht oder behalten werden. Pilot-Konvention bis zur Verifikation: immer alle 10 Spalten ausgeben (auch wenn weniger Bilder vorhanden, dann mit leeren Strings); keine Re-Imports auf bestehende Artikel mit weniger als der bisher gepflegten Bilderanzahl
- **Standardlieferant in Vorlage „nicht gewählt"** (NEU v1.15) → Ameise gibt 220+ Warnungen „Lieferant XYZ existiert nicht" beim Import, weil die CSV den Lieferanten als Spalte mitliefert, aber Ameise das Default-Setting der Vorlage erwartet. **Pflicht: in jeder Vorlage Standardlieferanten explizit setzen** (Bug-Beleg Live-Trial Batch 1 Attribute-Import 2026-05-17)

---

## 4.5 CSV 2: Variationen

Separate CSV für die Variations-Sprachen (Variationsname und Variationswertname pro Sprache).

### Schema (12 Spalten)

```
Artikelnummer; Variationsname; Darstellungsform; Variationswertname;
Global-Englisch: Variationsname; Global-Englisch: Variationswertname;
Global-Französisch: Variationsname; Global-Französisch: Variationswertname;
Global-Italienisch: Variationsname; Global-Italienisch: Variationswertname;
Global-Spanisch: Variationsname; Global-Spanisch: Variationswertname
```

Eine Zeile pro Größen-Variante. `Artikelnummer` = **Vater-Artikelnummer** (z.B. `HC-Hekate-Bodysuit`). `Darstellungsform` = `DROPDOWN`. Übersetzungstabelle Variationsname: Größe / Size / Taille / Taglia / Talla. Variationswerte (XS, S, M, L, XL) sind universal — werden aber explizit in allen 5 Sprachen gepflegt.

### Ameise-Import-Settings

| Setting | Wert |
|---|---|
| Vorlage | `{Lieferantenname}_2_Variationen` |
| Import-Typ | Artikel > Variationen |
| Identifikator | `Artikelnummer` |
| Encoding | UTF-8 mit BOM |
| Trennzeichen | `;` |
| **Standardlieferant (v1.15)** | **explizit auf den Lieferanten setzen** (Pflicht in jeder Vorlage) |

Sprach-Spalten via Reiter "Weitere Texte" analog Stammdaten-Import.

---

## 5. CSV 3: Merkmale

### Schema (4 Spalten)

```
Lieferant;Artikelnummer (Lieferant);Merkmalname;Merkmalwertname 1
```

**Wichtig (E19/E34):** Pro Artikel-Stamm kommen mehrere Zeilen — eine pro Merkmal-Wert. **Merkmale werden auf Vater UND auf jedem Kind explizit gepflegt.** JTL erbt zwischen Vater und Kind generell nichts implizit — diese Regel gilt für Merkmale, Attribute und Bilder gleichermaßen (E34). Validierungsquelle: JTL-Export Artikelmerkmale vom 13.05.2026. Beispiel A1009118 *Paradise Chick Top Gigi Active Schwarz*: Vater mit Farbe="Schwarz" und Style Tops="Open Back"+"Rundausschnitt"; alle 5 Kinder (-001 bis -005) haben dieselben Farbe+Style-Werte plus eigene Größen-Werte.

### Welche Merkmale, in welchen Fällen (Stand 2026-05-14, validiert am JTL-Export)

In WaWi existieren genau **4 belegte Merkmalsnamen** für Kleidung:

| Merkmalname | Wer hat ihn | Wertbildung |
|---|---|---|
| `Farbe Kleidung` | Vater UND alle Kinder | Farbe auf Deutsch, eine Zeile pro Artikel. Erlaubte Werte: Beige, Blau, Braun, Gelb, Gold, Grau, Grün, Lila, Pink, Rot, Schwarz, Silber, Weiß |
| `Größe Kleidung` | nur Kinder | Größe pro Kind. Erlaubte Werte: XS, S, M, L, XL, 2XL |
| `Style Tops` | Vater UND alle Kinder | Wenn Produkttyp = Top oder Bodysuit. Mehrere Werte möglich (je Feature eine Zeile). Belegte Werte: Bodysuit, Crop Top, High Neck, Open Back, Riemchentop, Rundausschnitt, T-Shirt, Triangle Ausschnitt. UI-Extras (definiert, noch unbelegt): Langärmlig, One Shoulder, Samt |
| `Style Shorts` | Vater UND alle Kinder | Wenn Produkttyp = Shorts. Belegte Werte: Cheeky, Classic Hot Pants, High Leg, High Waist, Leggings, Low Waist, Mid Waist, Riemchenshorts. UI-Extras: Samt, Bike Shorts, Strumpfhose |

**Wichtige Korrektur:** `Style Bodysuits` und `Style Leggings` existieren **nicht** als Merkmalsnamen in WaWi. Bodysuits werden über `Style Tops` mit Wert "Bodysuit" plus weitere Top-Style-Werte gepflegt (z.B. Hekate Bodysuit: Style Tops = Bodysuit + Open Back + Rundausschnitt).

### Größen-Konvention pro Lieferant

Wenn ein Lieferant Kombi-Größen liefert (z.B. `XS/S` als eine SKU), gilt die `groessen_konvention` aus `lieferanten_mapping.yaml`:
- `standard`: jede Größe einzeln, keine Expansion nötig
- `kombi_reduziert_auf_kleinste` (HotCakes-Konvention, E27): Kombi-Größe wird auf kleinste reduziert (XS/S → XS). Kein Filter-Match auf die größere Größe, dafür stabile SKU-Logik.

### Mehrsprachigkeit

**Nur Deutsch in der CSV.** Die Übersetzungen liegen in WaWi an den Merkmal-Wert-Stammdaten und werden zentral gepflegt. Beim Anlegen eines neuen Merkmalwerts in der CSV (z.B. eine neue Farbe) wird dieser zunächst nur auf DE existieren — die anderen Sprachen müssen einmalig in WaWi nachgetragen werden.

### Ameise-Import-Settings

| Setting | Wert |
|---|---|
| Vorlage | `{Lieferantenname}_3_Merkmale` (Slot 3 pro Import-Typ Merkmale; **HotCakes-Vorlage heißt final `HotCakes Polewear_3_Merkmale`** — korrigiert v1.15, war vorher fälschlich als `_4_Merkmale` dokumentiert) |
| Import-Typ | Artikel > Artikelmerkmale |
| Encoding | UTF-8 mit BOM |
| Trennzeichen | `;` |
| Quote | `"` |
| Identifikator | `Artikelnummer (Lieferant)` |
| **Standardlieferant (v1.15)** | **explizit auf den Lieferanten setzen** (Pflicht in jeder Vorlage) |

### Stolperfallen
- **Merkmal nur auf Vater gepflegt** → Filter-Suche findet die Kinder nicht (E19-Falle)
- **`Style Bodysuits`/`Style Leggings` als Merkmalsname verwenden** → existiert nicht in WaWi, Import bricht oder legt neue Merkmalsnamen an (unsauber)
- **Merkmalwert außerhalb der erlaubten Liste** → Werte werden zwar angelegt, aber kein UI-Filter-Eintrag in WaWi. B19 (`wawi_merkmalswerte.yaml` als Validierungsquelle) soll das künftig vorab abfangen
- **Standardlieferant in Vorlage „nicht gewählt"** (NEU v1.15) → 220+ Warnungen wie bei Attribute-Import

---

## 6. CSV 4: Attribute

Stand: HotCakes-Pilot 2026-05-14 mit 16 Zeilen erfolgreich importiert (4 Attribute × 4 Artikel im Test-Scope; auf Vater + Kinder duplizieren ergibt im Vollscope 64 Zeilen für 16 Artikel × 4 Attribute). Attribute sind jetzt Standard, nicht mehr optional (E39). **v1.15-Validierung:** Live-Trial Batch 1+2 (2026-05-17) hat 21 Modelle × 6 Artikel/Modell × 6 Attribute × 5 Sprachen produktiv importiert (Batch 1: 10 Modelle, Batch 2: 11 Modelle), 16/16 Self-Check grün.

### Schema (8 Spalten, alle Felder gequotet)

```
Lieferant;Artikelnummer (Lieferant);Attributname;Attributwert;Englisch: Attributwert;Französisch: Attributwert;Italienisch: Attributwert;Spanisch: Attributwert
```

**Quoting:** `csv.QUOTE_ALL` — jedes Feld in `"..."`. Das ist Pflicht, weil die Werte HTML mit Sonderzeichen, Anführungszeichen und Zeilenumbrüchen enthalten.

**Eine Zeile pro Artikel × Attribut — auf Vater UND alle Kinder dupliziert (E34):** Wie bei Merkmalen erbt JTL Attribute nicht implizit zu den Kindern. Ein HotCakes-Hekate-Bodysuit-Stamm (1 Vater + 5 Kinder) mit 4 Attributen erzeugt also 24 Zeilen (6 Artikel × 4 Attribute), nicht 4 Zeilen (nur Vater).

### Die Attribute pro Artikel

Pro Artikel mehrere Zeilen, je Attributname eine Zeile. Der Pipeline-Scope (E22, Stilprofil) sieht aktuell folgende Attribute vor:

| Attributname | Inhalt | Format |
|---|---|---|
| `markentext` | Brand-Pitch des Lieferanten (50-100 Wörter) | `<h2>Marke</h2><p>Story</p>` |
| `artikeldetails` | Tagline + Fließtext + Features (100-300 Wörter) | `<h2>Tagline</h2><p>Fließtext</p><p class="h5 bold">Sub-Header</p><ul class="check"><li>Feature</li></ul>` — H1 wird **nicht** verwendet (kollidiert mit Website-SEO) |
| `anwendung` | 3-8 Imperativ-Schritte (wenn relevant) | `<ul class="check"><li>Schritt</li></ul>` |
| `faqs` | mehrere Blöcke à 30-80 Wörter (wenn relevant) | wiederholtes `<h3>Frage?</h3><p>Antwort</p>` |
| `material_and_care` | Material-Zusammensetzung + Pflegehinweis | `<p>` oder `<ul class="check">` |
| `inhaltsstoffe` | Komma-Liste (wenn relevant) | `<p>` |
| `size_and_fit` | Passform-Beschreibung + Modellgröße + Tragehöhe. **Keine Größentabelle** mehr — die ist zentral im Shop-Template (siehe E22 v2026-05-14) | Plaintext oder leichtes HTML |

**Mindest-Set pro Artikel:** `markentext`, `artikeldetails`, `material_and_care`, `size_and_fit`. Übrige je nach Produkt-Relevanz.

**Stilregel (E82, verschärft v1.15):** 
- Em-Dashes (—) werden im Output **nicht** verwendet (KI-Marker). Im Fließtext durch `,` ersetzen.
- **Doppelpunkte im Fließtext und in `<h2>`-Taglines verboten** (E82, NEU v1.15). Statt `Material: Mesh` → `Mesh-Material`. Statt `Pflege:` als Sub-Header → konkretes Substantiv oder als prose.
- **Meta-Einleitungs-Sätze verboten:** „Die Maße:", „Die Pflege:", „Die Features:" — direkt mit dem Inhalt beginnen.

### Mehrsprachigkeit

Alle fünf Sprachen werden direkt in der CSV mitgeliefert — anders als bei Merkmalen. Eigennamen (Modellnamen, Branchen-Features wie "Crop Top", "High Waist") bleiben unübersetzt. Marketing-Texte werden inhaltlich-stilistisch übertragen, nicht wortwörtlich.

### Ameise-Import-Settings

| Setting | Wert |
|---|---|
| Vorlage | `{Lieferantenname}_4_Attribute` (Slot 4 pro Import-Typ Attribute; **HotCakes-Vorlage heißt final `HotCakes Polewear_4_Attribute`** — fixiert v1.15 nach Live-Trial Batch 1) |
| Import-Typ | Artikel > Artikelattribute |
| Encoding | UTF-8 mit BOM |
| Trennzeichen | `;` |
| Quote | `"` |
| Identifikator | `Artikelnummer (Lieferant)` |
| **Standardlieferant (v1.15)** | **explizit auf den Lieferanten setzen** (Pflicht — Bug-Beleg Live-Trial Batch 1 mit 220 Warnungen wegen fehlendem Default) |

### Stolperfallen
- **Quoting `MINIMAL` statt `QUOTE_ALL`** → wenn HTML ein `;` enthält, bricht die Zeile mittendrin
- **Anführungszeichen im HTML nicht escapet** → Standardbehandlung: `"` im Wert wird zu `""` (CSV-Verdoppelung)
- **Sprach-Spalte leer** → Ameise legt das Attribut nur auf DE an, andere Sprachen bleiben leer im Shop
- **H1 im HTML** → kollidiert mit Website-SEO, nur H2 oder tiefer verwenden
- **Em-Dashes im Text** → wirken KI-generiert, ersetzen durch `,`
- **Doppelpunkte in Taglines oder Fließtext** (NEU v1.15) → E82-Verstoß, Self-Check Punkt 13 prüft das
- **Meta-Einleitungs-Sätze** wie „Die Maße:" (NEU v1.15) → E82-Verstoß
- **Attribute nur auf Vater** → Kinder haben leere Detailseiten-Inhalte (E34-Falle)
- **Standardlieferant in Vorlage „nicht gewählt"** (NEU v1.15) → 220+ Warnungen beim Import. **Bug-Beleg-Quelle für diesen Eintrag.**

---

## 7. Bilder — integriert in die Stammdaten-CSV (kein separater Import mehr)

> **Pivot 2026-05-15 (E46):** Bis zur Mittags-Session des 2026-05-15 gab es einen separaten Bilder-Import als 5. CSV mit Import-Typ *Bilder > Artikelbilder pro Plattform*. Drei Versuche, die Plattform-Aktivierung über genau diesen Import hinzubekommen, sind alle gescheitert (siehe Anomalie A4 in BACKLOG): Pattern 1 mit mehreren Zeilen pro Artikel aktivierte Plattformen nur für die zuletzt gelesene Zeile (JTL-Multi-Row-Quirk), Pattern 2 mit Verknüpfungs-Import braucht vorher aktivierte Quellplattform-Bilder und skaliert nicht, Pattern 3 mit manuellem „Alle aktivieren"-Klick pro Artikel blockiert die Automation. Die Lösung kam aus der JTL-Doku selbst: bei „Bilder auf allen Plattformen gleich" werden Bilder als Spalten in die Stammdaten-CSV gelegt und die Vorlage trägt im Reiter „Bilder/Plattformen" alle Plattform-Häkchen. Damit läuft Plattform-Aktivierung automatisch beim Stammdaten-Import.

### Wo die Bild-URLs jetzt leben

In der Stammdaten-CSV (siehe Abschnitt 4) als 10 Spalten am Ende: `Bild 1` bis `Bild 10`. Eine URL pro Spalte, leere Strings bei weniger als 10 Bildern. Reihenfolge bestimmt die Anzeige-Reihenfolge im Shop (Bild 1 = Hauptbild). Die Reihenfolge kommt aus der Bildpipeline-Pose-Sortierung (siehe `cowork_anweisung_bildpipeline.md` und E45): bei Fashion-Artikeln steht das Front-Bild auf Position 1, das Back-Bild auf Position 2 (Mouse-Hover-Effekt), dann Side, dann Detail/Lifestyle/Group.

### Vater + Kind: identische URLs

Bild-URLs werden auf Vater UND alle Kinder dupliziert (E34/E46). Ein HotCakes-Hekate-Bodysuit-Stamm (1 Vater + 5 Kinder) mit 4 Bildern erzeugt 6 Stammdaten-Zeilen, jeweils mit denselben 4 URLs in `Bild 1` bis `Bild 4` und leeren Strings in `Bild 5` bis `Bild 10`.

### Wo die URLs herkommen

Aus dem Cloudflare-R2-Bucket `polesportshop-images`. R2 ist seit 2026-05-15 (E44) vollständiger Bild-Storage geworden — sowohl Verarbeitete als auch Originale liegen dort:

- **Verarbeitete** (das, was in die CSV kommt): `<lieferantenkuerzel>/<dateiname>.jpg`
- **Originale** (Archiv): `originals/<lieferantenkuerzel>/<dateiname>.<ext>` — Extension wird per Magic-Byte-Detection beim Download bestimmt (Shopify-CDN macht Content-Negotiation, deshalb keine verlässliche Endung in der URL)

Public-URL-Schema (für die CSV-Spalten):
```
https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev/<lieferantenkuerzel>/<dateiname>.jpg
```

Die R2-URLs sind dauerhaft erreichbar — wenn das Bucket umzieht, müssen alle WaWi-Bilder neu importiert werden (Risiko siehe BACKLOG B10).

> **Übergangs-Hinweis ist erledigt (Stand 2026-05-15 nachmittags):** Beim HotCakes-Bildpipeline-Versuch am 2026-05-14 wurden direkte HotCakes-CDN-URLs in die CSV geschrieben statt R2-URLs (E40, Übergangslösung). Mit der Arachne-Bottom-Black-Migration am 2026-05-15 ist diese Übergangslösung abgelöst — alle 4 HotCakes-Arachne-Bottom-Black-Bilder liegen jetzt auf R2 (Verarbeitete + Originale), und das Re-Import-CSV mit den R2-URLs in den Bild-Spalten lief erfolgreich durch (Plattform-Häkchen automatisch). Der nächste Schritt ist die Migration der restlichen 5 HotCakes-Artikel-Stämme von CDN-URLs auf R2-URLs (B22 in Umsetzung, jetzt mit dem neuen Stammdaten-Re-Import-Mechanismus statt Bilder-Import).

### Plattform-Aktivierung läuft automatisch über die Vorlage (B5 gelöst)

In der Stammdaten-Vorlage muss der Reiter „Bilder/Plattformen" alle 11 Plattform-Häkchen aktiviert haben (polesportshop.de, poledanceshop.de, alle 7 Amazon-Marktplätze, plus die zwei weiteren Plattform-Einträge in der HotCakes-Vorlage — Bestand auflisten in der jeweiligen Lieferanten-Vorlage). Beim Anlegen einer neuen Lieferanten-Stammdaten-Vorlage **explizit prüfen, dass alle Häkchen gesetzt sind**, sonst bleibt B5 ungelöst trotz der neuen Mechanik. Vorlage speichern.

**Was du jetzt nicht mehr machen musst:** Pro Artikel in WaWi den Bilder-Tab öffnen und „Alle aktivieren" drücken. Pro Artikel × 4 Klicks × n Artikel waren das früher; mit dem neuen Mechanismus null Klicks.

### Stolperfallen
- **„Bilder/Plattformen"-Häkchen in der Vorlage nicht gesetzt** → Bilder hängen am Artikel, aber sind nicht für Shop-Plattformen aktiviert → kein Bild im Shop sichtbar. Vorlage prüfen.
- **R2-URL nicht öffentlich erreichbar** → testen vor Import (`curl -I <url>` muss `200 OK` liefern)
- **Reihenfolge der Bilder in CSV egal annehmen** → falsch, die Spalten-Reihenfolge `Bild 1`, `Bild 2`, ... bestimmt die Anzeige-Reihenfolge im Shop
- **Bilder nur auf Vater** → Kinder haben keine Detailseiten-Bilder im Shop (E34-Falle)
- **Hersteller-CDN-URLs in der CSV** → Übergang abgelöst (E40 historisch); R2-URLs sind seit 2026-05-15 verpflichtend (E44)
- **Re-Import mit weniger Bild-Spalten als bisher gepflegt** → Verhalten **unverifiziert** (B30), Risiko von Bilder-Verlust. Konvention: immer alle 10 Spalten ausgeben, fehlende Bilder als leere Strings

---

## 7.5 CSV 5: Cross-Selling (NEU v1.14, E80 — produktiv v1.15)

> **Pivot 2026-05-16 (E80):** Cross-Selling-Beziehungen wurden bis v1.13 manuell pro Artikel in der WaWi-Artikelmaske (Reiter „Sonstiges" → „Cross-Selling-Gruppen zuweisen") gepflegt. Bei wachsendem Lieferanten-Volumen wird die manuelle Pflege zum Engpass. Die Pipeline erzeugt ab v1.14 eine 5. CSV pro Lauf, die JTL-Ameise über den Import-Typ „Cross-Selling-Artikel" automatisch in WaWi anlegt.

> **v1.15-Erweiterung (E80-Erweiterung):** Mit Live-Trial Batch 1+2 wurde die Erweiterung produktiv erprobt:
> - **Cross-Selling auf Vater UND alle Kinder:** linke Spalte (ArtNr) listet Vater + alle Kind-Größen (5 Zeilen pro Vater bei 4 Größen + Vater), rechte Spalte (Cross-Seller) strikt Vater. Bei 21 Modellen × 2 bidir. Beziehungen × 5 Zeilen Replikation → 180 Zeilen statt 36.
> - **Modell-Stamm-Schlüssel inkludiert Farbe:** `(modell_basis, farbe_im_namen)` statt nur `modell_basis`. Verhindert falsche Outfit-Paarungen wie Arachne-Top-Black mit Arachne-Bottom-Teal.
> - **Family-Refresh-Modus** als optionaler Trigger (Re-Lauf wenn Schwester-Artikel angelegt werden, z.B. neue Farben einer bestehenden Modell-Familie).

### CSV-Schema

3 Spalten in genau dieser Reihenfolge:

```
Artikelnummer; Artikelnummer Cross-Seller; Cross-Selling-Gruppe
```

Eine Zeile pro Beziehung. Mehrere Beziehungen pro Artikel = mehrere Zeilen mit gleicher `Artikelnummer`. Mit Kinder-Replikation (v1.15) wachsen die Zeilen pro Beziehung um Faktor 5.

### Ameise-Setup

- **Import-Typ:** `Cross-Selling-Artikel` (im Ameise-Menü „Artikel" eigene Sektion, **nicht** Teil von „Artikeldaten")
- **Identifizierungsspalte:** `Artikelnummer` → Artikelnummer
- **Artikel-IDs Cross-Selling-Artikel:** `Artikelnummer Cross-Seller` → Artikelnummer
- **Cross-Selling:** `Cross-Selling-Gruppe` → Cross-Selling-Gruppe
- **Encoding:** UTF-8 (BOM optional, Ameise erkennt automatisch)
- **Spaltenbegrenzer:** `;`
- **Kopfzeile enthalten:** Ja
- **Ab Zeile:** 2
- **Standardlieferant (v1.15)** → **explizit auf den Lieferanten setzen** (Pflicht in jeder Vorlage)

### Cross-Selling-Gruppen (Stand 2026-05-17)

Die Cross-Selling-Gruppen müssen **vorab in WaWi existieren**, sonst bricht der Import ab. Pflege-Ort: Artikel-Maske → Reiter „Sonstiges" → „Cross-Selling-Gruppen zuweisen" → Schaltfläche „Hinzufügen" zeigt alle existierenden Gruppen.

Im Bestand bei polesportshop bereits angelegt (Screenshot 2026-05-16):

| Gruppen-Name | Pipeline-Nutzung | Semantik |
|---|---|---|
| `Vervollständige Dein Outfit` | ✓ aktiv (E80) | Top↔Bottom in gleicher Farbe |
| `Ähnliche Artikel` | ✓ aktiv (E80) | gleiches Modell in anderen Farben |
| `Reinigungsmittle` | manuell | Reinigungsmittel-Empfehlung für Pole-Stangen |
| `High Heels Zubehör` | manuell | Begleitende Heels-Artikel |
| `Garantieverlängerung` | manuell | Garantie-Add-Ons |
| `Unsere Zubehör-Empfehlung` | manuell | generisches Zubehör |
| `Zusätzliche Farbauswahl` | manuell | Farbvarianten-Hinweis |
| `Weitere Studio-Poles` | manuell | Pole-Stangen-Vergleich |

### Vorlagen-Anlage pro Lieferant

Beim Onboarding eines neuen Lieferanten (oder Nachrüsten eines Bestands-Lieferanten):

1. Im Ameise-Menü „Artikel" → „Cross-Selling-Artikel" auswählen
2. CSV laden (eine vorhandene CSV als Spalten-Vorlage öffnen)
3. Die 3 Spalten wie oben zuordnen
4. **Standardlieferant explizit setzen** (v1.15, Pflicht)
5. Auf „Vorlage speichern" → Name nach Konvention: `{Lieferantenname}_5_CrossSelling` bzw. nächster freier Slot bei Lieferanten mit Legacy-Vorlagen (bei HotCakes Polewear z.B. weiterhin `HotCakes Polewear_5_CrossSelling` möglich, weil `_5_Bilder` als Legacy belegt ist — aber **andere Import-Typen, also kein Konflikt**)
6. Bei der nächsten Pipeline-Lieferung steht der Name in der `_MANIFEST`-Ausgabe drin und muss ins `lieferanten_mapping.yaml` Feld `ameise_vorlagen.cross_selling` übertragen werden

### Bidirektionalität und Vater-only

Die Pipeline schreibt **jede Beziehung zweimal** (A→B und B→A in zwei Zeilen). WaWi sollte das eigentlich bidirektional auflösen, aber zur Sicherheit doppelt geschrieben — falls die Bidirektionalität in einer WaWi-Version anders aufgelöst wird, bleibt die Shop-Anzeige beidseitig korrekt.

**Mit v1.15-Kinder-Replikation:** Cross-Selling-Beziehungen nutzen in der rechten Spalte (`Artikelnummer Cross-Seller`) **nur Vater-Artikelnummern**, niemals Kind-IDs mit Größen-Suffix. In der linken Spalte (`Artikelnummer`) werden Vater + alle Kinder repliziert. Kind-Größen erscheinen sonst als eigenständige Cross-Selling-Empfehlung im Shop, was die Anzeige zerschießt.

### Achtung Datenbank-Backup

Die JTL-Doku empfiehlt explizit eine **Datenbanksicherung vor jedem Cross-Selling-Import**. Bei polesportshop läuft das Backup automatisch nightly über die WaWi-Backup-Funktion — für manuelle Sicherheit kann vor dem ersten produktiven Cross-Selling-Import-Lauf einmalig ein ad-hoc-Backup angestoßen werden.

**v1.15-Validierung:** Live-Trial Batch 1 (10 Modelle) + Batch 2 (11 Modelle, 180 Cross-Selling-Zeilen mit Kinder-Replikation) erfolgreich importiert, 16/16 Self-Check grün in beiden Batches. Re-Import-Verhalten (Verdopplung-Risiko) noch nicht validiert (siehe BACKLOG B49).

---

## 8. Mapping-Strategien & A-Nummer-Logik

Die Pipeline arbeitet aktuell mit:

> **Artikelnummer = Artikelnummer (Lieferant) = Lieferantenartikelnummer**

Das heißt: dieselbe ID erscheint in mehreren Spalten der Stammdaten-CSV, weil sie sowohl als interner Identifier als auch als Lieferanten-SKU dient. Das ist eine bewusste Vereinfachung für den Pilot (siehe ENTSCHEIDUNGS-LOG E6).

### Konsequenzen für die Imports

- **Stammdaten-Import:** Identifikator `Artikelnummer`, die Lieferantenartikelnummer wird zur JTL-Hauptartikelnummer. Bilder werden im selben Import über die 10 Bild-Spalten mitgegeben (E46).
- **Variationen-Import:** Identifikator `Artikelnummer` (= Vater-Artikelnummer)
- **Merkmale-Import:** Identifikator `Artikelnummer (Lieferant)` — funktioniert weil identisch
- **Attribute-Import:** Identifikator `Artikelnummer (Lieferant)` — funktioniert weil identisch
- **Cross-Selling-Import:** Identifikator `Artikelnummer` (= Vater-Artikelnummer, nie Kind-ID)

> **Historischer Hinweis:** Bis 2026-05-15 vormittags gab es einen separaten Bilder-Import mit dem berüchtigten „falschen Mapping" (CSV-Spalte `Artikelnummer (Lieferant)` → JTL-Feld `Artikelnummer`) — das ist mit E46 entfallen, weil Bilder jetzt im Stammdaten-Import mit dem normalen `Artikelnummer`-Mapping kommen.

### Bei späterer Umstellung auf eigene A-Nummern

Wenn die Pipeline umgestellt wird auf separate WaWi-A-Nummern (z.B. `A12345`), ändert sich ausschließlich die `Artikelnummer`-Spalte in den Stammdaten. Alle anderen CSVs nutzen `Artikelnummer (Lieferant)` als Identifikator und bleiben unverändert. Die Bild-Spalten in der Stammdaten-CSV bleiben sowohl beim Layout als auch beim Mapping unverändert.

Migration bestehender Artikel: extra Schritt, vermutlich Bulk-Update via WaWi-DB oder Ameise-Reimport. Beim Strategiewechsel rechtzeitig planen.

---

## 9. Ameise-Vorlagen-Übersicht

Pro Lieferant werden **5 Ameise-Vorlagen** einmalig manuell angelegt (Stammdaten inkl. Bildern, Variationen, Merkmale, Attribute, Cross-Selling — Pflicht ab v1.14, produktiv-validiert v1.15). Naming-Konvention (etabliert mit HotCakes 2026-05-14, E29; verschärft v1.15):

`{Lieferantenname}_{Reihenfolge}_{Import-Typ}`

— Underscores als Element-Trenner, Leerzeichen nur innerhalb des Lieferantennamens.

### Slot-Konvention pro Import-Typ (NEU v1.15)

**Slot-Nummern sind eindeutig pro Import-Typ, NICHT lieferanten-weit.** Eine `_3_Merkmale`-Vorlage hat denselben Slot wie eine `_3_Lieferantendaten`-Vorlage, aber unterschiedlichen Import-Typ — das ist OK, weil Ameise pro Import-Typ filtert. Das bedeutet bei HotCakes mit historischer Vorlagen-Anlage:

- `_3_Lieferantendaten` (Stammdaten-Legacy, vor E35 angelegt, ohne Funktion seit E35) — Slot 3 im Import-Typ „Artikeldaten des Lieferanten"
- `_3_Merkmale` (aktuell, Slot 3 im Import-Typ „Artikelmerkmale")
- `_5_Bilder` (Stammdaten-Legacy, vor E46 angelegt, ohne Funktion seit E46) — Slot 5 im Import-Typ „Artikelbilder pro Plattform"
- `_5_CrossSelling` (aktuell, Slot 5 im Import-Typ „Cross-Selling-Artikel")

**Empfohlene Slot-Reihenfolge für NEUE Lieferanten** (kein Legacy):
- `_1_Stammdaten`
- `_2_Variationen`
- `_3_Merkmale`
- `_4_Attribute`
- `_5_CrossSelling`

Bestehende Lieferanten (HotCakes, POLE ADDICT) behalten ihre historische Naming-Konvention — Legacy-Vorlagen NICHT umnumerieren (Aufwand vs. Nutzen).

### Vorlagen-Übersicht

| Vorlage | Skopus | Anlage |
|---|---|---|
| `{Lieferantenname}_1_Stammdaten` | pro Lieferant | manuell in Ameise einmalig, dann pro neuen Lieferanten klonen. Verkaufskanal-Häkchen raus (E37), GLD-Spalte manuell mappen (E38), Lieferantenblock im Lieferanten-Bereich mappen, Währungs-Standardwert setzen, **Standardlieferant explizit setzen (v1.15 Pflicht)**, **10 Bild-Spalten auf `Bild Pfad/URL 1-10` mappen, alle 11 Plattform-Häkchen im Reiter „Bilder/Plattformen" setzen (E46/B5)** |
| `{Lieferantenname}_2_Variationen` | pro Lieferant | klonen + Sprach-Mapping in "Weitere Texte" prüfen + **Standardlieferant setzen** |
| `{Lieferantenname}_3_Merkmale` | pro Lieferant | klonen + **Standardlieferant setzen** |
| `{Lieferantenname}_4_Attribute` | pro Lieferant | klonen aus JTL-Standard, alle Felder gequotet + **Standardlieferant setzen (v1.15 Pflicht — Bug-Beleg Live-Trial Batch 1 mit 220 Warnungen)** |
| `{Lieferantenname}_5_CrossSelling` | pro Lieferant | klonen, Import-Typ „Cross-Selling-Artikel" wählen, 3 Spalten zuordnen, **Standardlieferant setzen** |

### HotCakes Polewear — finaler Stand v1.15 (nach Live-Trial 2026-05-17)

Bei HotCakes hat sich folgende Vorlagen-Belegung als final stabilisiert (5 aktive + 2 Legacy):

| Vorlage | Status | Import-Typ |
|---|---|---|
| `HotCakes Polewear_1_Stammdaten` | ✓ aktiv | Artikel > Artikeldaten |
| `HotCakes Polewear_2_Variationen` | ✓ aktiv | Artikel > Variationen |
| `HotCakes Polewear_3_Lieferantendaten` | ⚠ Legacy (vor E35) | Artikel > Artikeldaten des Lieferanten — nicht mehr benutzt |
| `HotCakes Polewear_3_Merkmale` | ✓ aktiv (korrigiert v1.15, war vorher fälschlich als `_4_Merkmale` dokumentiert) | Artikel > Artikelmerkmale |
| `HotCakes Polewear_4_Attribute` | ✓ aktiv | Artikel > Artikelattribute |
| `HotCakes Polewear_5_Bilder` | ⚠ Legacy (vor E46) | Bilder > Artikelbilder pro Plattform — nicht mehr benutzt |
| `HotCakes Polewear_5_CrossSelling` | ✓ aktiv (v1.14, produktiv v1.15) | Cross-Selling-Artikel |

Die Stammdaten-Vorlage wurde am 2026-05-15 erweitert: Bild-Mapping für `Bild 1` bis `Bild 4` (Ausbau auf `Bild 1` bis `Bild 10` steht an) und alle 11 Plattform-Häkchen im Reiter „Bilder/Plattformen". Bestehende Vorlagen nicht umnummerieren (Aufwand vs. Nutzen).

### Bestand POLE ADDICT

Folgt noch alter Naming-Konvention (`POLE ADDICT Stammdaten Import` etc.). Nicht umbenennen. Beim Onboarding ist POLE ADDICT historisch ohne Cross-Selling-Vorlage — Nachrüstung bei nächstem POLE-ADDICT-Lauf.

### Onboarding eines neuen Lieferanten

→ **Vollständiger Onboarding-Prozess: `LIEFERANTEN-ONBOARDING.md` (NEU v1.20).**

Kurzfassung: **5 Vorlagen** kopieren von einem anderen Lieferanten, Namen anpassen, **Standardlieferant in jeder der 5 Vorlagen explizit setzen (v1.15 Pflicht)**, Spalten-Mapping prüfen (sollte identisch sein, weil CSV-Schemas identisch sind), bei der Stammdaten-Vorlage alle 11 Plattform-Häkchen im Reiter „Bilder/Plattformen" setzen. Cross-Selling-Gruppen müssen vorab in WaWi existieren (bei polesportshop sind „Vervollständige Dein Outfit" und „Ähnliche Artikel" schon angelegt). Weitere Pflichtschritte (Mapping-YAML-Eintrag, Brand-Story-Pflege, Probe-Lauf, Go/No-Go-Checkliste) im Onboarding-Spec.

**Wichtig zum Spalten-Mapping (E30):** Spaltennamen in den CSVs müssen nicht zwanghaft die JTL-Feldnamen treffen — Auto-Mapping ist ein Bonus, kein Muss. Pro Lieferant einmal manuell mappen + Vorlage speichern, danach pro neuem Lieferanten Vorlage klonen. Sprechende Spaltennamen sind dadurch OK.

---

## 10. Cheat-Sheet: Ameise-Settings auf einen Blick

| CSV | Vorlage | Import-Typ | Identifikator | Besonderheit |
|---|---|---|---|---|
| 1 Stammdaten | `{Lieferant}_1_Stammdaten` | Artikel > Artikeldaten | `Artikelnummer` | Sprach-Spalten via "Weitere Texte"; Verkaufskanal-Häkchen raus (E37); GLD-Spalte manuell mappen (E38); Lieferantenblock-Spalten im Lieferanten-Bereich mappen + Währungs-Standardwert setzen (E36); **10 Bild-Spalten auf `Bild Pfad/URL 1-10` mappen + alle 11 Plattform-Häkchen im Reiter „Bilder/Plattformen" setzen (E46/B5)**; **Standardlieferant explizit setzen (v1.15)** |
| 2 Variationen | `{Lieferant}_2_Variationen` | Artikel > Variationen | `Artikelnummer` | Sprach-Spalten via "Weitere Texte"; **Standardlieferant setzen (v1.15)** |
| 3 Merkmale | `{Lieferant}_3_Merkmale` | Artikel > Artikelmerkmale | `Artikelnummer (Lieferant)` | Auf Vater UND Kind, Werte aus erlaubter Liste; **Standardlieferant setzen (v1.15)** |
| 4 Attribute | `{Lieferant}_4_Attribute` | Artikel > Artikelattribute | `Artikelnummer (Lieferant)` | Alle Felder gequotet (`QUOTE_ALL`), HTML-Templates aus E22, auf Vater UND Kind (E34); **Standardlieferant setzen (v1.15 Pflicht — Bug-Beleg)** |
| 5 Cross-Selling | `{Lieferant}_5_CrossSelling` | Cross-Selling-Artikel | `Artikelnummer` | Vater-only in `Cross-Seller`-Spalte; bidirektional doppelt; **Kinder-Replikation in linker Spalte (v1.15)**; Datenbank-Backup empfohlen; **Standardlieferant setzen (v1.15)** |

Für alle: UTF-8 BOM, `;`, `"`, CRLF.

---

## 10.5 Anti-Patterns: Cowork-Erfindungen — siehe `SPEC_KONSTANTEN.md` Sektion 10

Die Anti-Pattern-Liste AP1-AP12 ist mit v1.10 (E61) in die kanonische Konstanten-Datei `SPEC_KONSTANTEN.md` (Sektion 10) gewandert. Sie bleibt verpflichtende Lese-Pflicht vor jeder Stammdaten-CSV-Generation. Begründung: harte Lookup-Konstante, gehört zur Konstanten-Datei-Architektur (Charter-Prinzip 11).

**v1.15-Erweiterung:** AP9-AP12 sind in SPEC_KONSTANTEN.md ergänzt (AP9 Drive-CSV-Upload-Verbot, AP10 Lokal-Datei-Schreib-Pflicht, AP11 Datei-Naming `<NR>_<Typ>_<LIEFERANT>_<DATUM>.csv`, AP12 keine leeren CSVs).

**Generelle Regel (E59, unverändert):** Wenn die Pipeline eine Generation überlegt, bei der ein WaWi-Feld nicht aus einer Lookup-Tabelle, einem E-Eintrag oder einer Lieferanten-Mapping-Zeile direkt abgeleitet werden kann → **STOPP + User-Frage**, niemals durch generierte Plausibilität füllen.

---

## 11. Stolperfallen-Gesamtliste

Konsolidiert über alle CSVs, in Reihenfolge der Wahrscheinlichkeit:

1. **BOM vergessen** → erste Spalte wird nicht erkannt, ganzer Import bricht
2. **Bilder-Mapping fehlt** (Bild-Spalten nicht auf `Bild Pfad/URL 1-10` in der Stammdaten-Vorlage gemappt) → Bilder kommen nicht am Artikel an (E46-Falle)
3. **„Bilder/Plattformen"-Häkchen in der Stammdaten-Vorlage nicht gesetzt** → Bilder hängen am Artikel, aber sind nicht für Shop-Plattformen aktiviert → unsichtbar im Shop (E46-Falle, B5-Regression)
4. **Dezimal-Punkt statt -Komma in Preisen** → Preise werden als Text interpretiert, im Shop steht `0,00 €`
5. **Kind-Artikel ohne `Identifizierungsspalte Vaterartikel`** → eigenständiger Artikel statt Variante
6. **Verkaufskanal-Häkchen in Stammdaten-Vorlage gesetzt** → Artikel gehen sofort online statt im Review (E37)
7. **`EK Netto (für GLD)` nicht manuell gemappt** → GLD bleibt leer beim Artikel, weil Auto-Mapping nicht greift (E38)
8. **Reiter "Weitere Texte" nicht geöffnet** → Sprach-Spalten nicht importiert, nur DE im Shop
9. **Merkmal nur auf Vater statt Vater+Kind** → Filter-Suche findet die Kinder nicht (E19/E34)
10. **Attribute nur auf Vater statt Vater+Kind** → Kind-Detailseiten leer (E34)
11. **Bild-URLs nur auf Vater statt Vater+Kind** → Kind-Detailseiten haben keine Bilder (E34/E46)
12. **`Style Bodysuits` als Merkmalsname verwendet** → existiert nicht, Bodysuits laufen über `Style Tops`
13. **Quoting `MINIMAL` bei Attributen** → HTML mit `;` bricht die Zeile
14. **HAN mit Pseudo-Daten gefüllt** → bricht bei späterem echtem Barcode-Import
15. **Kategorie-Ebenen leer** → Artikel landet kategorielos, im Shop unsichtbar
16. **R2-URL nicht erreichbar** → Bild lädt nicht, Artikel hat Platzhalter
17. **Hersteller-CDN-URLs in Bild-Spalten** → Übergang abgelöst (E40 historisch), R2-URLs sind seit 2026-05-15 verpflichtend (E44)
18. **Re-Import mit weniger Bild-Spalten als bisher gepflegt** → Verhalten **unverifiziert** (B30) — Risiko von Bilder-Verlust; immer alle 10 Spalten ausgeben mit leeren Strings für fehlende Bilder
19. **Sprach-Spalte in Attribut-CSV leer** → Attribut existiert nur auf DE
20. **Import in falscher Reihenfolge** (z.B. Variationen vor Stammdaten, oder Cross-Selling vor Stammdaten) → "Artikel nicht gefunden"-Fehler
21. **H1 im Attribut-HTML** → kollidiert mit Website-SEO, nur H2 oder tiefer verwenden
22. **Em-Dashes (—) im Text** → wirken KI-generiert, ersetzen durch `,` oder `:`
23. **Lieferantenblock-Spalten nicht im Lieferanten-Bereich der Vorlage gemappt** → Netto-EK, Lieferzeit etc. landen nicht beim Artikel (E36)
24. **Doppelpunkte in Attribut-Taglines oder Fließtext** (NEU v1.15) → E82-Verstoß
25. **Meta-Einleitungs-Sätze** wie „Die Maße:" oder „Die Pflege:" (NEU v1.15) → E82-Verstoß
26. **Standardlieferant in Vorlage „nicht gewählt"** (NEU v1.15, häufig) → 220+ Warnungen „Lieferant XYZ existiert nicht" beim Import. **Pflicht in jeder der 5 Vorlagen explizit setzen**. Bug-Beleg: Live-Trial Batch 1 Attribute-Import 2026-05-17.
27. **Cross-Selling-CSV mit Kind-IDs in `Artikelnummer Cross-Seller`-Spalte** (NEU v1.15) → Kind-Größen erscheinen als eigenständige Cross-Selling-Empfehlung im Shop, zerschießt die Anzeige. Rechte Spalte strikt Vater.
28. **Cross-Selling-CSV ohne Kinder-Replikation in linker Spalte** (NEU v1.15) → Cross-Selling-Anzeige greift nur auf Vater, nicht auf Kindern. Pflicht: linke Spalte listet Vater + alle Kinder.

---

## 12. Pilot-Erkenntnisse

### POLE ADDICT (2026-05-13)
- Drei Vater-Artikel + zehn Kind-Artikel über eine Stammdaten-CSV importiert
- Variationsname/Variationswert-Mechanik in JTL korrekt erkannt
- Größen-Expansion bei kombinierten Größen funktioniert filter-seitig
- Alle vier Attribute pro Vater inklusive Mehrsprachigkeit korrekt angelegt
- Bilder via R2-URL importiert, hängen an den drei Artikeln
- HEIC-Originale lassen sich verarbeiten (Smart-Crop, Resize, JPEG-Konvertierung)

### HotCakes Polewear (2026-05-14)
- 3 Vater-Artikel (Hekate Bodysuit, Arachne Top, Arachne Shorts) + 13 Kinder importiert
- Stammdaten-CSV in zwei Versionen: v1 mit 35 Spalten, v2 mit 38 Spalten (Lieferantenblock integriert, E36) — v2 erfolgreich
- Brutto-VK greift Auto-Mapping über Spaltennamen
- `EK Netto (für GLD)` greift nur über manuelle Mapping-Zuordnung — Vorlage speichert das danach dauerhaft (E38)
- Sprach-Spalten via "Weitere Texte" zugewiesen — funktioniert
- Verkaufskanal-Häkchen mussten in Vorlage entfernt werden, sonst gingen Artikel sofort online (E37)
- Importvorlagen-Naming `HotCakes Polewear_1_Stammdaten` etabliert für künftige Lieferanten
- Merkmale-CSV (67 Zeilen) auf Vater + alle Kinder erfolgreich (E19)
- Attribute-CSV (64 Zeilen, 16 Artikel × 4 Attribute) auf Vater + alle Kinder erfolgreich (E34)
- Bildpipeline-Versuch mit direkten HotCakes-CDN-URLs (R2-Connector im Cowork-Projekt nicht installiert) — als Übergangslösung markiert (E40), R2-Upload-Mechanik 2026-05-15 final definiert (E43 — Code-Execution + boto3)

### Cowork-Setup-Session (2026-05-15 vormittags)
- R2-Upload-Mechanik fixiert auf Code-Execution + boto3 (E43, Pfad b)
- Credentials-Strategie via Drive-File mit Tjorben-only-Permissions (E33 erweitert)
- Network-Egress-Allowlist im Pilot zunächst auf „All domains" wegen Anthropic-Bug bei „Package managers only" (B29) — reversibel sobald Bug gefixt

### HotCakes Arachne-Bottom-Black Bild-Migration (2026-05-15 nachmittags)
- 4 verarbeitete Shop-Bilder auf R2 unter `hotcakes/HC-Arachne-Bottom-Black_NN_HOTCAKES_2026-05-15.jpg` hochgeladen
- 4 Originale auf R2 unter `originals/hotcakes/HC-Arachne-Bottom-Black_NN_HOTCAKES_2026-05-15.jpg` hochgeladen (alle als JPEG erkannt via Magic-Byte-Detection, weil Shopify-CDN Content-Negotiation macht und die URL-Endung nicht verlässlich ist)
- Mini-Stammdaten-CSV-Re-Import mit den 4 R2-URLs in den Spalten `Bild 1` bis `Bild 4` erfolgreich (alle 9 Plattform-Häkchen automatisch gesetzt durch konfigurierte Häkchen in der Stammdaten-Vorlage)
- Validierungs-Bestätigung für E46: Bilder-Integration in Stammdaten-CSV + Plattform-Aktivierung via Vorlage funktioniert; B5 ist damit für alle künftigen Stammdaten-Imports gelöst
- Pivot der Pipeline-Architektur von 5 auf 4 CSVs bestätigt

### v3.1-Pre-22-Test — Stammdaten-Stabilisierung (2026-05-15 spätabends)

Die drei HotCakes-Pilot-Modelle (Hekate Bodysuit, Arachne Bottom Teal, Savanna Original Top) über mehrere CSV-Iterationen in WaWi re-importiert. Erkenntnisse:

- **Schema v3.1 (E54)** funktioniert für Vorlagen-Kontinuität — die ersten 38 Spalten der ALT-Vorlage blieben unverändert kompatibel, nur die 10 Bild-Spalten mussten neu gemappt werden. Bestätigung der Append-only-Konvention für künftige Schema-Bumps.
- **SEO-Template-Pattern (E55)** aus dem JTL-Export 2026-05-15 abends verifiziert über 30 Stichproben hinweg, 100 % konsistent. Cowork-Erfindungen aus 3-Modell-Batch (produkt-spezifische Meta-Descriptions) sind anti-pattern — werden ab v1.9 strikt durch das Template ersetzt.
- **Kind-Artikelname mit Größen-Suffix (E56)** validiert — Pattern-Check im JTL-Export: 453 Artikel haben Größe am Namens-Ende, 349 ohne (Väter mit Variation + One-Size-Artikel). Konvention eindeutig.
- **Multi-Kategorie via Doppelzeilen (E57)** im Forum recherchiert (5 Forum-Threads übereinstimmend) und im Re-Import validiert. Pflicht-Setting in der Tjorben-Ameise-Vorlage: „Kategorieverknüpfungen des Artikels aktualisieren = Neue Kategorien beim jeweiligen Artikel hinzuimportieren" — gilt session-übergreifend nach einmaligem Vorlagen-Speichern. Effekt: jeder Artikel landet sowohl in der Oberkategorie „Pole Dance Kleidung" als auch in der passenden Unterkategorie.
- **Sprach-Lokalisierungs-Konvention (E58)** aus 297 Bestand-Artikeln abgeleitet: Brand+Eigennamen unverändert, Produkt-Substantive nach Lookup-Tabelle, Farb-Adjektive konsequent lokalisiert. Cowork hat damit eine geschlossene Tabelle für Pole-Wear-Standard-Vokabular.
- **Wissens-Schutz-Mechanik (E59)** als Reaktion auf 6 dokumentierte Cowork-Erfindungen über 2 Stammdaten-Sessions: Charter-Prinzip 10 (neu), kanonische 🔒-Markierung dieser Datei, Mapping-Bibel-Self-Check-Checkliste in der Cowork-Anweisung Sektion 6, Goldstandard-Referenz-Artikel (Hekate Bodysuit, Arachne Bottom Teal, Savanna Original Top).

### HotCakes Live-Trial Batch 1 + Batch 2 (2026-05-17) — Cross-Selling produktiv

**Batch 1 (10 Modelle, 16/16 Self-Check grün):**
- Stammdaten-CSV: 10 Modelle × Multi-Kategorie-Doppelzeilen × (Vater + Größen-Kinder) erfolgreich importiert
- Variationen-CSV: 10 Variationsnamen × 5 Sprachen erfolgreich
- Merkmale-CSV: alle 4 Merkmalsnamen auf Vater + Kindern korrekt
- Attribute-CSV: **220 Warnungen „Lieferant HOTCAKES existiert nicht"** wegen `_4_Attribute`-Vorlage mit Standardlieferant „nicht gewählt" → Tjorben hat Standardlieferant in Vorlage gesetzt und gespeichert. **v1.15-AP12-Sektion 9-Verschärfung** als Konsequenz.
- Cross-Selling-CSV: Bidirektional, mit Kinder-Replikation, „Vervollständige Dein Outfit" + „Ähnliche Artikel" erfolgreich
- **3 korrupte CSV-Uploads in Drive** (AP10-Verstoß) → B51 als Drive-Cleanup-Workaround

**Batch 2 (11 Modelle, 16/16 Self-Check grün):**
- Selbe Mechanik wie Batch 1, plus Cross-Selling-Beziehungen über Batch-1+Batch-2 hinweg
- **Cross-Selling-CSV: 180 Zeilen** mit Kinder-Replikation (E80-Erweiterung — Vater + 4 Kinder pro bidir. Beziehung, also 10 Zeilen pro Outfit-Pair-Beziehung statt 2)
- E84 Familien-erhaltende Split-Regel hat funktioniert (Outfit-Pair-Familien blieben pro Batch zusammen, Cross-Selling Stage 5.8 lief im letzten Batch über alle 21 Modelle vereint)
- E83 Pre-Run Scope-Analyse hat funktional gegriffen (Cowork hat autonom Batch-Aufteilung dokumentiert)

**Was funktioniert hat (v1.15-Validierungen):**
- E80-Erweiterung Kinder-Replikation (linke Spalte Vater + alle Kinder, rechte Spalte strikt Vater)
- E80-Erweiterung Modell-Stamm-Schlüssel mit Farbe (Bug-Fix aus Batch 2 Iter. 1: 14 statt 20 Outfit-Pair-Zeilen vor Fix)
- E81 Autonomie für Workflow-Entscheidungen (Cowork hat selbständig Batch-Splitting und Stage-Reihenfolge entschieden)
- E82 Stil-Verschärfung (Doppelpunkt-Verbot + Meta-Einleitungs-Verbot in Attributen)
- E83 Pre-Run Scope-Analyse als Stage 0.5
- E84 Familien-erhaltende Split-Regel

**Was nachgebessert wurde post-Lauf:**
- Standardlieferant in jeder Vorlage Pflicht (AP12-Sektion 9-Update, v1.15)
- HotCakes-Vorlagen-Slots final dokumentiert (`_3_Merkmale` korrigiert von `_4_Merkmale`)
- Slot-Konvention pro Import-Typ als Schema-Doku-Block in Sektion 9

### Wo manuell nachgearbeitet wurde (und jetzt nicht mehr nötig)
- ~~"Alle aktivieren" im Bilder-Tab pro Artikel (Plattform-Aktivierung, B5)~~ — gelöst durch E46
- Kategorie-Zuordnung in WaWi (Pilot-Default `Intern/Automatisierung Artikelanlage` durch echte Kategorie ersetzen) — noch manuell
- Verkaufskanal-Häkchen pro Artikel (B21 künftig über CSV) — noch manuell

### Was noch nicht validiert ist
- Re-Import-Verhalten bei leeren oder gekürzten Bild-Spalten auf bestehende Artikel (B30) — Konvention bis dahin: immer 10 Spalten ausgeben
- Cross-Selling-Re-Import-Verhalten auf bereits importierte Beziehungen (B49) — Verdopplung-Risiko ungeprüft
- Vision-Pose-Klassifikations-Genauigkeit über Lieferanten (B28) — bei Lunalae noch nicht erprobt
- Mehrsprachigkeits-Qualität durch Native-Reviewer (siehe BACKLOG B6)
- Skalierung Batches >15 Modelle (B53) — Batch 1+2 hatten je 10/11

---

## 13. Nutzung dieses Dokuments

Im neuen Chat anhängen, wenn:
- Eine CSV-Spezifikation diskutiert wird ("warum sind die Bild-URLs in der Stammdaten-CSV?")
- Ein Import-Fehler debuggt werden muss ("Artikel hat keine Bilder im Shop trotz erfolgreichem Stammdaten-Import" → diese Datei zeigt die wahrscheinlichen Ursachen)
- Eine neue Lieferanten-Vorlage in Ameise angelegt wird (Schemas und Settings sind hier definitiv, inkl. der 11 Plattform-Häkchen im Reiter „Bilder/Plattformen" der Stammdaten-Vorlage und Standardlieferant-Pflicht in jeder Vorlage)
- Die A-Nummer-Strategie diskutiert oder umgestellt wird (Konsequenzen sind hier aufgelistet)
- Ein neues Attribut, Merkmal oder eine neue Spalte ergänzt werden soll (Format-Regeln und Quoting-Logik sind hier fix)
- Die Bild-Integration in der Stammdaten-CSV erweitert oder angepasst wird (Spalten-Layout, Plattform-Häkchen, Mapping)
- Eine Cross-Selling-Vorlage neu angelegt wird oder die Cross-Selling-Mechanik diskutiert wird

Nicht nötig, wenn:
- Reine Pipeline-Architektur-Diskussion (dann PROJEKT-CHARTER + ENTSCHEIDUNGS-LOG)
- Bild-Verarbeitungs-Details — Crop-Profile, Pose-Sortierung, R2-Upload-Mechanik (dann cowork_anweisung_bildpipeline)
- Crawl- oder Input-Logik (dann cowork_anweisung_datenimports)

Dieses Dokument ändert sich, wenn neue Erkenntnisse aus echten Import-Läufen entstehen oder wenn das WaWi-/Ameise-Verhalten sich ändert (Version-Update, neue Standardvorlage o.ä.). Im Gegensatz zu den `cowork_anweisung_*.md`-Files folgt es **einer v1.X-Versionierung gleichgeschaltet mit den anderen Snapshot-Dateien ab v1.15** (vorher datums-getragen) — der Stand wird sowohl über die Versions-Markierung oben als auch über das Datum geführt.
