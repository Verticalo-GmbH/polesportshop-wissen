# SPEC_KONSTANTEN — Kanonische Wissens-Konstanten

**🔒 KANONISCH — IN STEIN GEMEISSELT** (Charter-Prinzipien 10 + 11, E61)

**Stand:** v1.19, 2026-05-18 · **Spec-Bezug:** v1.21-Snapshot (Git-Tag) · **Quelle:** verbatim aus v1.9-Snapshot Version_2026-05-15_233800, iterativ erweitert v1.13-v1.17, v1.18 (Skalierungs-Refactor v1.20), **v1.19 (Trial-Findings v1.21: Sektion 4 + Self-Check #4 korrigiert auf 3-Zeilen-Multi-Kategorie inkl. Oberkategorie + Sara-546 — E89 verfeinert durch E92; Sektion 6 Farb-Lokalisierung Teal/Sky/Emerald/Lime/Kirschrot ins DE übersetzt — E92; Sektion 14 um E92/E93)**

---

## Zweck dieser Datei

Diese Datei ist der **alleinige Speicherort** aller harten Konstanten der Daten-Pipeline: Schemata, Templates, Lookup-Tabellen, Mapping-Listen, Self-Check-Vorgaben, Anti-Patterns. Sie wurde mit E61 (2026-05-16) aus `cowork_anweisung_datenimports.md` und `WAWI-IMPORT-WISSEN.md` extrahiert, weil Cowork beim Versuch, diese Konstanten pro Lauf aus den großen Spec-Dateien zu extrahieren, ~50K Tokens nur fürs Lesen verbrannte und Stage 0 nie hinter sich brachte.

**Charter-Prinzip 11 (Konstanten-Datei-Architektur, E61):** Konstanten leben in einer einzigen Datei und werden vom ausführenden Code 1:1 gespiegelt (`pipeline/spec.py`). Wenn eine Konstante sich ändert, ändert sie sich **hier** — und im Code, nirgends sonst.

> **Hinweis ab v1.22 (Code-Pivot):** Ausführende Engine ist jetzt die lokale **Code-Pipeline** (`pipeline/`), nicht mehr Cowork. Wo unten „Cowork" in einer **Anweisung/Regel** steht, gilt sie sinngemäß für die Pipeline (der Code spiegelt diese Konstanten, `pipeline/spec.py`). **Historische Beispiele** (Anti-Patterns AP1–AP12, E-Nummer-Index) behalten „Cowork" bewusst — sie berichten, was damals passiert ist.

**Charter-Prinzip 10 (E59, weiter gültig):** WaWi-Mapping ist gefrorenes Wissen — niemals erfinden, immer konsultieren. Bei Unsicherheit über ein Feld, einen Standardwert, eine Spalten-Reihenfolge oder ein Sprach-Pattern: **STOPP + User-Frage**, niemals durch generierte Plausibilität füllen.

## Konflikt-Auflösung

Bei Widerspruch zwischen Quellen gilt die Hierarchie:

1. **SPEC_KONSTANTEN.md** (diese Datei) — kanonische Quelle für alle Konstanten ab v1.10.
2. **WAWI-IMPORT-WISSEN.md** — operatives Pilot-Wissen aus echten Ameise-Imports. Wenn hier ein Widerspruch zu SPEC_KONSTANTEN entsteht, ist das ein **Bug** in SPEC_KONSTANTEN und muss korrigiert werden — niemals umgekehrt durch generierte Plausibilität gefüllt.
3. **cowork_anweisung_datenimports.md** — beschreibt das *Was und Warum* (Stages, Lieferantenkontext, Output-Konventionen). Verweist für Konstanten auf SPEC_KONSTANTEN.md.
4. **ENTSCHEIDUNGS-LOG.md / PROJEKT-CHARTER.md** — Begründung und Architektur-Hintergrund.

Bei Drift zwischen SPEC_KONSTANTEN und WAWI-IMPORT-WISSEN: STOPP + User-Frage in den Lauf-Bericht. Niemals durch eine der beiden Versionen entscheiden, ohne Tjorben zu fragen.

## Versionshinweis

Diese Datei ist nicht versioniert mit Major/Minor (kein v1.X-Header). Stattdessen wird sie pro Snapshot mitversioniert — der gültige Stand ist immer der aus dem jüngsten kompletten Snapshot. Änderungen werden im jeweiligen Snapshot-Manifest und in den `ENTSCHEIDUNGS-LOG-*`-Cluster-Files dokumentiert (E-Nummer → Cluster-File-Zuordnung in Sektion 14 dieser Datei, `ENTSCHEIDUNGSLOG_E_NUMMER_INDEX`). Seit v1.17 ist der Master-LOG in 6 Themen-Cluster gesplittet; ARCHIV bleibt separat als `ENTSCHEIDUNGS-LOG-ARCHIV.md`.

---

## 1. Stammdaten-Schema (49 Spalten, v3.2 nach E95 — EAN ans Ende; v3.1 nach E54)

**WICHTIG (E54, 2026-05-15 Abend):** Diese Spalten-Reihenfolge ist explizit so gewählt, dass bestehende Lieferanten-Vorlagen aus der v2-Ära (vor E46) für die ersten 38 Spalten **unverändert** funktionieren. Die Pipeline generiert die CSV **strikt in dieser Reihenfolge**. Nur die 10 Bild-Spalten (39-48) müssen einmalig pro Lieferanten-Vorlage neu gemappt werden. Append-only-Konvention für künftige Schema-Bumps.

**Spalten-Reihenfolge (exakt):**

```
Position 1-12 — Identifikation + Hauptdaten + Variation + Kategorie:
   1.  Artikelnummer
   2.  Artikelnummer (Lieferant)
   3.  HAN
   4.  Identifizierungsspalte Vaterartikel
   5.  Artikelname
   6.  Hersteller
   7.  Steuerklasse
   8.  TARIC-Code
   9.  Variationsname 1
   10. Variationswert 1
   11. Kategorie Ebene 1
   12. Kategorie Ebene 2

Position 13-14 — Preise (Hauptpreise):
   13. EK Netto (für GLD)
   14. Brutto-VK

Position 15-17 — Lager & Status:
   15. Bestandsführung aktiv
   16. Neu im Sortiment
   17. Neu im Sortiment seit

Position 18-21 — Gewicht & Versand:
   18. Artikelgewicht
   19. Versandgewicht
   20. Versandklasse
   21. Herkunftsland

Position 22-25 — Sprach-Artikelnamen:
   22. Global-Englisch: Artikelname
   23. Global-Französisch: Artikelname
   24. Global-Italienisch: Artikelname
   25. Global-Spanisch: Artikelname

Position 26-27 — Meta-Daten DE (nur Vater):
   26. Titel-Tag (SEO)
   27. Meta-Description (SEO)

Position 28-35 — Sprach-SEO-Daten (8 Spalten, nur Vater):
   28. Global-Englisch: Titel-Tag
   29. Global-Englisch: Meta-Description
   30. Global-Französisch: Titel-Tag
   31. Global-Französisch: Meta-Description
   32. Global-Italienisch: Titel-Tag
   33. Global-Italienisch: Meta-Description
   34. Global-Spanisch: Titel-Tag
   35. Global-Spanisch: Meta-Description

Position 36-38 — Lieferantenblock (am Ende der 38 alten Spalten):
   36. Netto-EK
   37. Ist Standardlieferant
   38. Lieferzeit in Tagen (Lieferant)

Position 39-48 — Bild-URLs (E46 angehängt):
   39. Bild 1
   40. Bild 2
   41. Bild 3
   42. Bild 4
   43. Bild 5
   44. Bild 6
   45. Bild 7
   46. Bild 8
   47. Bild 9
   48. Bild 10
   49. EAN                  (NEU E95 — GTIN/UTC-Barcode pro Größe; nur Kind-Zeilen befüllt, sonst leer)
```

**Hinweis zu Bild-Spalten (v1.10+):** Die 10 Bild-Spalten bleiben im Schema verpflichtend, werden aber in v1.10 **standardmäßig leer ausgegeben**, weil die Bildpipeline archiviert ist (E63). Tjorben pflegt Bilder bis auf Weiteres manuell in WaWi. Die Spalten sind nicht optional — alle 10 müssen mit leeren Strings in jeder Zeile vorhanden sein, um Schema-Konformität für Ameise zu wahren.

## 2. Standardwerte für Kleidung-Pilot

- `Steuerklasse` = `OSS2-undefiniert - Standard alle Länder`
- `TARIC-Code` = `62114390`
- `Artikelgewicht` = `Versandgewicht` = `0,05` (kg)
- `Versandklasse` = `standard`
- `Herkunftsland` aus Mapping
- `Bestandsführung aktiv` = `Y`
- `Neu im Sortiment` = `Y`, `Neu im Sortiment seit` = Lauf-Datum (`DD.MM.YYYY`)
- `Ist Standardlieferant` = `Y` (Default, Pilot: 1 Lieferant pro Artikel)
- `Lieferzeit in Tagen (Lieferant)` = `0` (Default)

## 3. Kategorie-Mapping (E51, 2026-05-15 Abend) — pro Kleidungstyp fest

| Kleidungstyp | Kategorie Ebene 1 | Kategorie Ebene 2 |
|---|---|---|
| Top | Pole Dance Kleidung | Pole Dance Tops |
| Bottom / Shorts | Pole Dance Kleidung | Pole Dance Shorts |
| Bodysuit | Pole Dance Kleidung | Bodysuits |
| Leggings | Pole Dance Kleidung | Leggings |
| Legwarmer | Pole Dance Kleidung | Legwarmer |
| Shirt | Pole Dance Kleidung | Shirts |

**WICHTIG:** Einzelnamen pro Spalte, **nicht** Pfad-Notation mit `->` (JTL-Ameise-Konvention, recherchiert 2026-05-15). Pfad-Notation ist nur die WaWi-UI-Darstellung. `Damen` ist KEINE gültige Kategorie — nicht verwenden. `Limited Editions` wird ebenfalls nicht verwendet (Kategorie wird gelöscht).

## 4. Vater-Kind-Konventionen

**Vater-Zeile:**
- `Artikelnummer` = Basis (z.B. `HC-Hekate-Bodysuit`)
- `Identifizierungsspalte Vaterartikel` = leer
- `Artikelname` = ohne Größe (Konvention E26): `{Hersteller} {Produkttyp} {Modell} {Farbe}`
- `Variationswert 1` = leer
- **Multi-Kategorie (E57 + E89, korrigiert v1.21/E92):** Pro Vater **drei Zeilen** mit gleicher Artikelnummer:
  - **Zeile A (Oberkategorie-Zuweisung):** `Kategorie Ebene 1` = `Pole Dance Kleidung`, `Kategorie Ebene 2` leer.
  - **Zeile B (Unterkategorie-Zuweisung):** `Kategorie Ebene 1` = `Pole Dance Kleidung`, `Kategorie Ebene 2` = spezifische Subkategorie (`Pole Dance Tops` / `Pole Dance Shorts` / `Bodysuits` / `Leggings` / `Legwarmer` / `Shirts`).
  - **Zeile C (Sara-Review-Pflicht-Zuweisung):** `Kategorie Ebene 1` = `Intern`, `Kategorie Ebene 2` = `Neue Artikel für Sara` (WaWi-Key 546).

  **Warum drei Zeilen:** Lauf-Bericht 2026-05-18 21:06 zeigte: WaWi resolved die Hierarchie NICHT automatisch über die Subkategorie — Oberkategorie fehlte im Shop. Korrektur v1.21/E92: Oberkategorie muss explizit als eigene Zeile gesetzt sein (E57-Doppel-Pattern), zusätzlich Sara-Pflicht-Zeile (E89 verfeinert).
- **SEO-Felder (E55):** Titel-Tag und Meta-Description in allen 5 Sprachen befüllt nach **deterministischem Template** (siehe Sektion 5 unten). Identisch auf beiden Multi-Kategorie-Vater-Zeilen.
- **Sprach-Artikelnamen (E58):** Brand+Eigennamen unverändert, Produkt-Substantive nach Übersetzungstabelle, Farb-Adjektive konsequent lokalisiert (siehe Sektion 6 unten).
- Lieferantenblock befüllt (Netto-EK in Originalwährung)
- **Bild 1 bis Bild 10:** standardmäßig leer in v1.10 (Bildpipeline archiviert, E63). Manueller Bild-Pflege durch Tjorben.

**Kind-Zeile:**
- `Artikelnummer` = Vater + `-001`, `-002`, ...
- `Identifizierungsspalte Vaterartikel` = Vater-Artikelnummer
- `Variationswert 1` = Größe (nach `groessen_konvention` bereits reduziert)
- **Artikelname (E56)** in allen 5 Sprachen = **Vater-Sprachname + Leerzeichen + Variationswert**. Beispiel Kind XS:
  - DE: `HotCakes Bodysuit Hekate Schwarz XS`
  - EN: `HotCakes Bodysuit Hekate Black XS`
  - FR: `HotCakes Body Hekate Noir XS`
  - IT: `HotCakes Body Hekate Nero XS`
  - ES: `HotCakes Body Hekate Negro XS`
- **Multi-Kategorie (E57):** Analog zum Vater — pro Kind zwei Zeilen mit gleicher Artikelnummer (eine Oberkategorie, eine Unterkategorie).
- **SEO-Felder: leer auf allen Kind-Zeilen** (E56) — Titel-Tag und Meta-Description sind ausschließlich auf Vater-Zeilen.
- Lieferantenblock befüllt (identisch zum Vater)
- **Bild 1 bis Bild 10:** standardmäßig leer in v1.10 (analog Vater).

## 5. SEO-Templates pro Sprache (E55) — DETERMINISTISCH

**Verbot (AP3 aus Sektion 10 unten):** keine produkt-spezifischen Meta-Descriptions erfinden. Einzige Variable im Template: `{name}` = Vater-Artikelname **ohne Größe**.

**Titel-Tag pro Sprache:**

```
DE: {name} | polesportshop.de
EN: {name} | polesportshop.de   ← .de, nicht .com
FR: {name} | polesports.fr
IT: {name} | polesports.it
ES: {name} | polesports.es
```

**Meta-Description pro Sprache** (HTML-Entities **direkt so** verwenden, keine Unicode-Zeichen):

```
DE: {name} &#10004; große Auswahl &#10004; TOP Preise &#10004; Schneller Versand &#10148; jetzt hier online bestellen!
EN: {name} &#10004; Five star customer support &#10004; Top quality and price &#10004; Instant shipping &#10148; order now!
FR: {name} &#10004; Support client cinq étoiles &#10004; Qualité et prix au top &#10004; Expédition instantanée &#10148; commandez maintenant !
IT: {name} &#10004; Assistenza clienti a cinque stelle &#10004; Qualità e prezzo al top &#10004; Spedizione immediata &#10148; ordina ora!
ES: {name} &#10004; Soporte al cliente de cinco estrellas &#10004; Calidad y precio superiores &#10004; Envío instantáneo &#10148; ¡Ordénalo ahora!
```

Hard-coded in der Pipeline (Python). Keine LLM-Generation für SEO-Felder.

## 6. Sprach-Lokalisierungs-Konvention (E58) — Lookup-Tabellen

**Verbot (AP8 aus Sektion 10 unten):** keine Sprach-Namen erfinden. Bei Begriff außerhalb der Tabellen: STOPP + User-Frage in den Lauf-Bericht.

**Produkt-Substantiv (immer lokalisieren):**

| DE | EN | FR | IT | ES |
|---|---|---|---|---|
| Bodysuit | Bodysuit | Body | Body | Body |
| Shorts | Shorts | Short | Shorts | Pantalones Cortos |
| Top | Top | Haut | Top | Top |
| Leggings | Leggings | Legging | Leggings | Leggings |

**Farb-Adjektiv (immer lokalisieren — KORRIGIERT v1.21/E92 nach Trial-Lauf 2026-05-18 21:06):**

Tjorben-Direktive 2026-05-18: „Wir haben die Konvention für deutsche Artikelnamen, dass wir da auch immer die deutsche Farbe nehmen." Die alte v1.15-Liste „Niemals lokalisieren (Marketing-Farben)" wurde damit teilweise ausser Kraft gesetzt — wo ein deutsches Wort existiert, wird es verwendet. Englische Marketing-Begriffe bleiben nur dort, wo es **kein** etabliertes DE-Pendant gibt.

**Standard-Tabelle (alle Standard-Farben + lokalisierte Marketing-Farben):**

| DE | EN | FR | IT | ES | Merkmal-Hauptfarbe (Sektion 7) |
|---|---|---|---|---|---|
| Schwarz | Black | Noir | Nero | Negro | Schwarz |
| Weiß | White | Blanc | Bianco | Blanco | Weiß |
| Türkis | Teal | Turquoise | Turchese | Turquesa | Blau |
| Himmelblau | Sky | Bleu Ciel | Azzurro Cielo | Azul Cielo | Blau |
| Smaragdgrün | Emerald | Émeraude | Smeraldo | Esmeralda | Grün |
| Limettengrün | Lime | Vert Citron | Verde Lime | Verde Lima | Grün |
| Kirschrot | Cherry | Cerise | Ciliegia | Cereza | Rot |
| Pink | Pink | Rose | Rosa | Rosa | Pink |
| Burgundrot | Burgundy | Bordeaux | Borgogna | Burdeos | Rot |
| Beige | Beige | Beige | Beige | Beige | Beige |
| Grau | Grey | Gris | Grigio | Gris | Grau |
| Braun | Brown | Marron | Marrone | Marrón | Braun |
| Rot | Red | Rouge | Rosso | Rojo | Rot |
| Blau | Blue | Bleu | Blu | Azul | Blau |
| Gelb | Yellow | Jaune | Giallo | Amarillo | Gelb |
| Grün | Green | Vert | Verde | Verde | Grün |

**Niemals lokalisieren** (kein etabliertes DE-Pendant existiert, Marketing-Begriff ist im DE eingebürgert — bleibt in allen 5 Sprachen identisch inkl. DE):

| Marketing-Farbe | Bleibt in allen Sprachen | Merkmal-Hauptfarbe |
|---|---|---|
| Nude | Nude | Beige |
| Mauve | Mauve | Lila |
| Tan | Tan | Beige |
| Skin | Skin | Beige |

Plus identisch in allen Sprachen (keine Farbe, sondern Eigenname/Print-Variante/Material):
- Brand-Namen: HotCakes, FANNA, Polerina, Pole Addict, Shark Polewear, etc.
- Modell-Eigennamen: Hekate, Arachne, Savanna, Bali Grape, X Spark Edition, etc.
- Print-Familien-Namen: Original, Heat, Lynx-Print etc. (Merkmal-Hauptfarbe folgt dominanter Druckfarbe oder `Bunt`)
- Größen-Suffix: XS, S, M, L, XL, 2XL
- Material-Eigennamen: Velvet (bleibt überall)

**Begründung Tjorben-Direktive 2026-05-18:** „HotCakes Top Arachne Teal" (DE) im Trial-Lauf war falsch. Korrekt: „HotCakes Top Arachne Türkis" (DE). Bei Sky analog: „HotCakes Top Savanna Himmelblau" statt „Savanna Sky". Bei Mauve/Nude/Tan/Skin: keine sinnvolle DE-Übersetzung existiert (Altrosa für Mauve wäre nicht gleich semantisch) — bleibt englisch.

**Bei neuen Marketing-Begriffen außerhalb der zwei Tabellen oben:** STOPP, User-Frage, **niemals raten**. Tjorben entscheidet pro neuer Marketing-Farbe ob lokalisieren oder identisch belassen.

### 6.1 Hartkodierte DE-Konventionen (NEU v1.14, E76)

Begriffe, die im **deutschen Freitext** (alle HTML-Attribute, Meta-Description, etc.) **niemals** verwendet werden, sondern immer durch ihr deutsches Pendant ersetzt sind. Diese Regel gilt nur für Deutsch — die anderen 4 Sprachen behalten ihre Anglizismen.

| Verboten im DE-Freitext | Immer verwenden | Grund |
|---|---|---|
| Bottom | Shorts | „Pole Dance Shorts" ist zentrales SEO-Keyword für polesportshop (E76). |

**Anti-Pattern (E76):** Wenn der Hersteller-Body „Bottom" sagt, übernimm das nicht ins DE — schreib „Shorts". Im Strukturfeld „Artikelname" war's eh schon durch E58 richtig — diese Regel wirkt zusätzlich auf den Freitext.

## 7. Merkmalwerte (E50, statische WaWi-Listen)

Schema der Merkmale-CSV: `Lieferant; Artikelnummer (Lieferant); Merkmalname; Merkmalwertname 1` (4 Spalten).

**Pro Artikel mehrere Zeilen — auf Vater UND Kind explizit gepflegt** (E19, validiert JTL-Export 13.05.2026).

**Sprache: NUR Deutsch in der CSV.** WaWi pflegt die Übersetzungen statisch pro Merkmalwert intern. Die Pipeline generiert AUSSCHLIESSLICH die deutschen Werte. Keine Mehrsprachigkeit in den Merkmale-CSV-Spalten.

**Statische WaWi-Merkmalwert-Listen (E50, Stand 2026-05-15 aus WaWi-Screenshots):**

| Merkmalname | Wer hat ihn | Erlaubte Werte (statisch in WaWi gepflegt — die Pipeline wählt aus diesen) |
|---|---|---|
| `Farbe Kleidung` | Vater UND alle Kinder | **(15)** Bunt, Gold, Schwarz, Weiß, Braun, Beige, Grau, Blau, Grün, Gelb, Orange, Rot, Pink, Lila, Silber |
| `Größe Kleidung` | nur Kinder | XS, S, M, L, XL, 2XL |
| `Style Tops` | Vater UND alle Kinder (Top/Bodysuit) | **(11)** Crop Top, Open Back, Rundausschnitt, Bodysuit, High Neck, Langärmlig, One Shoulder, Riemchentop, Samt, T-Shirt, Triangle Ausschnitt |
| `Style Shorts` | Vater UND alle Kinder (Shorts) | **(11)** Cheeky, High Leg, High Waist, Low Waist, Mid Waist, Classic Hot Pants, Riemchenshorts, Samt, Leggings, Bike Shorts, Strumpfhose |

**Wichtig:** `Style Bodysuits` und `Style Leggings` existieren **nicht** als Merkmalsnamen. Bodysuits laufen über `Style Tops` mit Wert „Bodysuit" plus weitere Top-Style-Werte.

**Zweistufige Farb-Logik (zentral nach E50):**

Bei Farben die nicht 1:1 in der 15er-WaWi-Liste sind (z.B. Teal, Burgund, Nude, Petrol, Cognac, Mauve, Sky):

1. **Artikelname:** behält den **spezifischen Farbnamen** wie er marketing-üblich ist (Beispiel: `HotCakes Shorts Arachne Türkis`, `HotCakes Top Peonies Nude`, `HotCakes Top Bali Mauve`)
2. **Merkmalwert Farbe:** der **nächstpassende WaWi-Wert** aus den 15 erlaubten Werten (Beispiel: Türkis → `Blau`, Nude → `Beige`, Burgund → `Rot`, Mauve → `Lila`, Sky → `Blau`)

Bei Konflikt zwischen Hersteller-Wording und WaWi-Liste **gewinnt die WaWi-Liste beim Merkmal**. Der Artikelname kann die Hersteller-Wording behalten — er ist das Customer-Facing-Element.

**Mapping-Hilfe (häufige Sonderfälle):**

| Spezifischer Name (Artikelname) | WaWi-Wert (Merkmal) |
|---|---|
| Teal, Türkis, Petrol, Aqua, Mint | Blau |
| Nude, Sand, Creme, Vanilla | Beige |
| Burgund, Bordeaux, Weinrot, Kirsch | Rot |
| Mauve, Altrosa, Rosé | Pink oder Lila (je nach Helligkeit; Mauve eher Lila, Altrosa eher Pink) |
| Cognac, Camel, Karamell, Mocca | Braun |
| Anthrazit, Charcoal | Grau |
| Sky, Hellblau, Pastellblau | Blau |
| Marble-Print, Zebra-Print, Animal-Print | (Hauptfarbe des Prints; bei dezentem Multi-Farb-Print: Bunt) |
| Original (Print-Variante) | (dominante Druckfarbe; bei Multi-Print mit > 3 Farben: Bunt) |

**Falsches Pattern (aus 3-Modell-Lauf 2026-05-15):**
- ❌ `HotCakes Shorts Arachne Blau` (Cowork hat „Teal" zu „Blau" auch im Artikelnamen umbenannt)
- ✅ `HotCakes Shorts Arachne Türkis` (Name spezifisch) + Merkmal Farbe Kleidung `Blau` (nächster WaWi-Wert)

## 8. Goldstandard-Referenz-Artikel (E59)

Diese drei HotCakes-Pilot-Artikel sind die **strukturelle Referenz** für jeden neuen Artikel im Pilot:

- **Hekate Bodysuit** (Bodysuit, schwarz, Größen XS/S/M/L)
- **Arachne Bottom Teal** (Shorts, Türkis, Größen XS/S/M/L)
- **Savanna Original Top** (Top, Multicolor, Größen XS/S/M/L)

Jeder neue Artikel wird beim Self-Check (siehe Sektion 9) gegen diese drei abgeglichen. Strukturelle Abweichungen ohne Lieferanten-Mapping-Eintrag = **STOPP + User-Frage**. „Strukturell" meint: Anzahl Vater/Kind-Zeilen, Multi-Kategorie-Pattern, befüllte Felder, Sprach-Spalten — nicht den konkreten Inhalt (Farben, Modellnamen, Größen-Set).

## 9. Stage 6 Mapping-Bibel-Self-Check (E59, erweitert v1.15 auf 16 Punkte, Punkte 15+16 für Kinder-Replikation neu formuliert)

**Vor Stage 7 (CSV schreiben) muss die Pipeline diese 16-Punkte-Checkliste durchgehen und im Lauf-Bericht pro Punkt eine Ja/Nein-Bestätigung dokumentieren.** Bei Fail eines Punkts: Lauf abbrechen, Punkt eindeutig benennen, User-Frage formulieren.

| # | Self-Check-Punkt | Wo verankert | Fail-Symptom |
|---|---|---|---|
| 1 | Schema-Spalten-Reihenfolge entspricht 1:1 der 49-Spalten-Liste (Sektion 1, E95: + EAN) | E54, E95, Sektion 1 | CSV-Ameise-Import bricht oder mapped falsch |
| 2 | Kategorie Ebene 1 = `Pole Dance Kleidung` (für Kleidungs-Pilot) — niemals `Damen` oder `Limited Editions` | E51, AP1 | Artikel landet in falscher Shop-Kategorie |
| 3 | Kategorie Ebene 2 = nur die in Sektion 3 erlaubten Werte (`Bodysuits` / `Pole Dance Tops` / `Pole Dance Shorts` / `Leggings` / `Legwarmer` / `Shirts`) | E51 | Artikel in falscher Unterkategorie |
| 4 | **Multi-Kategorie-Pattern (KORRIGIERT v1.21, E92 verfeinert E89):** Pro Artikel **mindestens 3 Kategorie-Zeilen** in der CSV mit gleicher Artikelnummer: (a) Oberkategorie-Zuweisung `Pole Dance Kleidung` (Kategorie Ebene 2 leer); (b) Unterkategorie-Zuweisung `Pole Dance Kleidung` + spezifische Subkategorie (Pole Dance Tops/Shorts/Bodysuits/Leggings/etc.); (c) Sara-Review-Pflicht-Zuweisung `Intern` + `Neue Artikel für Sara` (WaWi-Key 546). **Korrektur:** v1.19/E89-Annahme „WaWi resolved Pfad selbst" war falsch — Lauf-Bericht 2026-05-18 21:06 zeigte fehlende Oberkategorie im Shop. Zurück zum E57-Doppel-Pattern, ergänzt um Sara-Zeile aus E89. Vorlagen-Setting unverändert: „Kategorieverknüpfungen des Artikels aktualisieren" = „Neue Kategorien beim jeweiligen Artikel hinzuimportieren". Anti-Confusion E75 weiter gültig. | E57, E89, E92, Sektion 4 | Artikel fehlt Oberkategorie im Shop, oder Sara-Workflow bricht weil 546-Zuweisung fehlt |
| 5 | Titel-Tag pro Sprache **exakt** nach E55-Template (kein produkt-spezifischer Spin, kein erfundener Domain-TLD) | E55, Sektion 5 | SEO inkonsistent zum Shop-Bestand |
| 6 | Meta-Description pro Sprache **exakt** nach E55-Template (HTML-Entities `&#10004;`/`&#10148;`, **nicht** Unicode `✓`/`➜`) | E55, AP3, AP7 | Shop zeigt falsche oder erfundene Meta-Beschreibung |
| 7 | SEO-Felder (Titel-Tag + Meta-Description in allen 5 Sprachen) **nur auf Vater-Zeilen**, leer auf Kindern | E56 | unnötige SEO-Duplikation auf Variantenebene |
| 8 | Kind-Artikelname in allen 5 Sprachen = Vater-Sprachname + Leerzeichen + Variationswert | E56, AP5 | WaWi-Liste zeigt alle Größen mit identischem Namen |
| 9 | Farb-Adjektiv in allen 5 Sprachen lokalisiert nach Tabelle in Sektion 6 (keine DE-Reste in EN/FR/IT/ES) | E58, AP8 | falsche Sprach-Anzeige im Shop |
| 10 | Produkt-Substantiv lokalisiert nach Tabelle in Sektion 6 (Bodysuit → Body in FR/IT/ES etc.) | E58 | falsche Sprach-Anzeige im Shop |
| 11 | Bei Begriff außerhalb Sektion-6-Tabellen: STOPP-Marker im Lauf-Bericht statt Erfindung | E58, E59 | falsche Übersetzung schleicht sich ein |
| 12 | Strukturelle Übereinstimmung mit Goldstandard-Referenz-Artikeln (Sektion 8) für gleichen Produkttyp | E59 | strukturelle Abweichung ohne Lieferanten-Mapping-Eintrag |
| 13 | **Originalitäts-Check (NEU v1.14, E77):** im deutschen Freitext kein „Bottom" (E76), keine wörtliche 5-Wörter-Sequenz aus Hersteller-Body übernommen, keine 1:1-Übernahme der Sub-Sätze-Reihenfolge. **NEU v1.15:** beim 5-Wort-N-Gramm-Scan synthetischen Separator (`||`) zwischen `<li>`-Items setzen, damit Bullet-Listen-Items nicht als zusammenhängender Text gescannt werden (Bug-Beleg: 6/6 E77-Funde in Batch 2 Iter. 1 waren Bullet-Concat-Artefakte). Zusätzlich (NEU v1.15, E82): keine Em-Dashes im Fließtext, kein Doppelpunkt im Fließtext und `<h2>`-Taglines, keine Meta-Einleitungs-Sätze („Die Maße:", „Die Pflege:"). | E76, E77, E82 | Hersteller-/Pole-Junkie-Stimme schimmert durch, KI-Marker erkennbar |
| 14 | **Cross-Selling-CSV 3-Spalten-Schema korrekt (NEU v1.14, E80):** `Artikelnummer; Artikelnummer Cross-Seller; Cross-Selling-Gruppe` exakt in dieser Reihenfolge, UTF-8 BOM, `;`, CRLF | E80 | Ameise-Cross-Selling-Import bricht |
| 15 | **Cross-Selling rechte Spalte nur Vater-Artikelnummern (NEU v1.15, E80-Erweiterung):** `Artikelnummer Cross-Seller` enthält keine Kind-IDs mit Größen-Suffix (`-001`, `-002` etc.). Linke Spalte `Artikelnummer` enthält **Vater UND alle Kinder** (Kinder-Replikation, v1.15-Mechanik) — das ist KEIN Fail-Symptom, sondern das gewollte Verhalten. | E80 (v1.15-Erweiterung) | Shop zeigt Größen-Varianten als Cross-Selling-Empfehlung (= rechte Spalte falsch) |
| 16 | **Cross-Selling-Symmetrie auf Vater-Ebene mit Kinder-Replikation (NEU v1.15, E80-Erweiterung):** jede bidirektionale Beziehung A↔B existiert in zwei Vater-Richtungen, plus für jede Richtung mit Kinder-Replikation auf der linken Spalte. Bei 1 Vater + 4 Kindern pro Stamm: 2 × 5 = 10 Zeilen pro bidirektionale Outfit-Pair-Beziehung. | E80 (v1.15-Erweiterung) | Shop-Empfehlung wirkt nur in eine Richtung, oder Kind-Artikel haben keine Cross-Selling-Anzeige |

**Self-Check-Output im Lauf-Bericht:** Format pro Punkt: `[#N] [✓/✗] <Punkt-Bezeichnung> — <Detail>`. Beispiel:
```
[#1] ✓ Schema-Reihenfolge — 49 Spalten, exakt nach v3.2-Layout (E95: + EAN ans Ende)
[#5] ✓ Titel-Tag — DE: "HotCakes Bodysuit Hekate Schwarz | polesportshop.de"; alle 5 Sprachen aus Template
[#12] ✓ Goldstandard-Abgleich — strukturell identisch zu HC-Hekate-Bodysuit (Vater + 4 Kinder, je 2 Kategorie-Zeilen)
[#13] ✓ Originalitäts-Check — kein "Bottom" im DE-Freitext, kein 5-Wörter-Plagiat (Bullet-Separator-Scan greift), keine E82-Verletzung (keine Em-Dashes, keine Doppelpunkte im Fließtext, keine Meta-Einleitungen)
[#14] ✓ Cross-Selling-Schema — 3 Spalten, UTF-8 BOM, CRLF korrekt
[#15] ✓ Cross-Selling rechts Vater-only — alle Cross-Seller-IDs sind Vater-IDs ohne Größen-Suffix; linke Spalte enthält Vater + Kinder (gewollt, v1.15)
[#16] ✓ Cross-Selling-Symmetrie + Kinder-Replikation — 12 Outfit-Pairs × 10 + 6 Ähnliche × 10 = 180 Zeilen beidseitig vorhanden
```

**Bei Fail eines Punkts:** Lauf-Bericht enthält explizit:
```
[#N] ✗ <Punkt> — <Detail des Fehlschlags>
   STOPP-Grund: <was die Pipeline unsicher ist>
   User-Frage: <konkrete Frage an Tjorben>
```

**Cross-Ref (NEU v1.16, E85):** Für Wissens-Build-Self-Check (WSC-1 bis WSC-17) siehe `WISSENS-UPDATE-PLAYBOOK.md` Sektion 6. Dieser Sektion-9-Self-Check gilt nur für Daten-Pipeline-Läufe und bleibt davon separat.

## 10. Anti-Patterns (AP1-AP12, E59 + v1.15-Erweiterung) — Cowork-Erfindungen, die nicht passieren dürfen

Diese Liste sammelt **konkrete Cowork-Generations-Fehler aus realen Pilot-Sessions**. Sie sind nicht hypothetisch — sie sind passiert. Jeder Eintrag ist eine reproduzierbare Falle, die Cowork bei der nächsten CSV-Generation aktiv vermeiden muss.

Cowork-Pflicht: vor jeder Stammdaten-CSV-Generation diese Liste durchgehen und im Lauf-Bericht bestätigen.

| # | Vorfall | Was passierte | Richtige Behandlung |
|---|---|---|---|
| AP1 | **Kategorie „Damen" erfunden** | 3-Modell-Batch: Cowork schrieb `Kategorie Ebene 1 = Damen` statt `Pole Dance Kleidung`. Im Shop: Artikel landete in falscher Kategorie. | E51-Mapping verbindlich abrufen, **immer** `Pole Dance Kleidung` als Ebene 1 für Kleidungs-Pilot. „Damen" ist keine gültige Kategorie. |
| AP2 | **Artikelname „Blau" statt „Türkis"** | 3-Modell-Batch: Cowork schrieb für Arachne-Teal `HotCakes Shorts Arachne Blau` (zweistufige Farb-Logik gebrochen). | E50 zweistufige Farb-Logik: spezifischer Name (`Türkis`) im Artikelnamen, nächster WaWi-Wert (`Blau`) im Farb-Merkmal. Beide stehen in verschiedenen Feldern. |
| AP3 | **Eigene Meta-Description erfunden** | 3-Modell-Batch: Cowork schrieb produkt-spezifische Texte wie „Mesh-Bodysuit mit Marmor-Print, tiefem Ausschnitt und athletischem Rücken." statt das deterministische Template aus dem Bestand. | E55-Template **strikt** anwenden, einzige Variable ist `{name}` = Vater-Name ohne Größe. Produkt-spezifische Beschreibung lebt im Attribut `artikeldetails`, nicht in der Meta-Description. |
| AP4 | **Spalten-Reihenfolge umorganisiert** | v3-Spec: Cowork verschob den Lieferantenblock auf Position 16-17 statt 36-38 (ALT-Vorlagen-Reihenfolge gebrochen). Tjorbens Vorlage zerschossen, kompletter Re-Mapping-Aufwand. | E54-Schema-Reihenfolge ist **append-only** — neue Spalten immer am Ende anhängen, niemals bestehende Bereiche umorganisieren. |
| AP5 | **Kind-Artikelname ohne Größe** | v3.1-Pre-22-Test 2026-05-15: Cowork generierte alle 4 Kinder von `HC-Hekate-Bodysuit` mit identischem Namen `HotCakes Bodysuit Hekate Schwarz`. WaWi-Liste unbrauchbar. | E56: Kind-Name = Vater-Name + Leerzeichen + Variationswert, in **allen 5 Sprachen**. |
| AP6 | **Multi-Kategorie nicht implementiert** | v3.1-Pre-22-Test: Cowork generierte nur eine Zeile pro Artikel mit Ebene 1 + 2 gefüllt → Artikel landete nur in der Unterkategorie. | E57: pro Artikel zwei Zeilen mit gleicher Artikelnummer (eine Oberkategorie-Zeile + eine Unterkategorie-Zeile). Plus Ameise-Setting „Kategorieverknüpfungen des Artikels aktualisieren = Neue Kategorien beim jeweiligen Artikel hinzuimportieren". |
| AP7 | **HTML-Entities durch Unicode ersetzt** | (Vermieden bisher, aber latentes Risiko bei String-Manipulation) — wenn Cowork die SEO-Templates aus String-Vorlagen baut und unterwegs `html.unescape()` o.ä. läuft, werden `&#10004;` zu `✓`. | Entities **direkt** im Template-String als ASCII-Sequenz lassen. Keine Unescape-Schritte in der Pipeline. |
| AP8 | **Sprach-Namen mit DE-Resten** | (Risiko erkannt, noch nicht passiert in Pilot) — z.B. Cowork lässt „Burgundrot" im EN-Slot stehen oder erfindet „Hecate" für „Hekate". | E58-Lookup-Tabellen verwenden. Bei seltenen Begriffen STOPP + User-Frage, nicht raten. Eigennamen niemals übersetzen. |
| AP9 | **Workflow-Frage statt autonomer Entscheidung (NEU v1.15, E81)** | Live-Trial-Runs Batch 1+2 HotCakes 2026-05-17: Cowork fragte Tjorben mehrfach zurück zu Batch-Splitting, Token-Budget-Management und Stage-Reihenfolge, statt diese operativen Entscheidungen autonom zu treffen. Lauf-Pausen, User-Reibung. | E81-Autonomie: Batch-Splitting, Batch-Größen, Token-Budget, Stage-Reihenfolge bei Tool-Limits werden selbständig getroffen — nicht zurück an Tjorben. Im Lauf-Bericht dokumentieren. STOPP + User-Frage bleibt strikt für: fehlende Daten, unbekannte Sprach-Begriffe, Goldstandard-Abweichungen, Mapping-`null`-Pflichtfelder. |
| AP10 | **CSV/Lauf-Bericht nach Drive uploaden (NEU v1.15, AP10 verschärft E52/E69)** | Live-Trial-Runs Batch 1 HotCakes 2026-05-17: Cowork lud 3 korrupte CSVs in `2026-05-17_HOTCAKES_batch1/`-Drive-Ordner hoch (entgegen E52/E69). Die korrupten Files lassen sich nicht mehr regulär löschen — Drive-Cleanup-Workaround in BACKLOG (B33). | E52/E69 verbietet Drive-Upload von CSVs und Lauf-Berichten. AP10 schärft: niemals upload, auch nicht zu „Archivzwecken". Tjorben lädt manuell wenn er archivieren will. |
| AP11 | **Datei-Naming ohne Nummer-Präfix (NEU v1.15)** | Live-Trial-Runs Batch 1+2 HotCakes 2026-05-17: Cowork generierte CSV-Namen ohne Reihenfolge-Nummer (`Stammdaten_HotCakes_2026-05-17.csv` statt `1_Stammdaten_HotCakes_2026-05-17.csv`). Tjorben konnte Import-Reihenfolge nicht visuell prüfen. | Konvention `<NR>_<Typ>_<LIEFERANT>_<YYYY-MM-DD_HHMM>.csv` mit Reihenfolge-Nummer 1-5 (1=Stammdaten, 2=Variationen, 3=Merkmale, 4=Attribute, 5=CrossSelling). Bei Batch-Aufteilung Batch-Index im Lieferanten-Teil einbauen: `1_Stammdaten_HotCakes_Batch1_2026-05-17_1500.csv`. |
| AP12 | **Leere CSV mit nur Header (NEU v1.15)** | Live-Trial-Runs Batch 1 HotCakes 2026-05-17: Cowork generierte eine `5_CrossSelling`-CSV mit nur Header-Zeile (0 Daten-Zeilen), weil Batch 1 zu früh ohne den vollen Lieferanten-Crawl lief. Tjorben importierte das CSV-File und WaWi meldete „kein Datensatz importiert" — unklar ob Bug oder OK. | Wenn 0 Daten-Zeilen, CSV NICHT ausgeben sondern im Lauf-Bericht vermerken („Cross-Selling-CSV nicht ausgegeben, 0 Beziehungen gefunden — Grund: voller Lieferanten-Crawl fehlte"). |

**Generelle Regel (E59):** Wenn die Pipeline eine Generation überlegt, bei der ein WaWi-Feld nicht aus einer Lookup-Tabelle, einem E-Eintrag oder einer Lieferanten-Mapping-Zeile direkt abgeleitet werden kann → **STOPP + User-Frage**, niemals durch generierte Plausibilität füllen.

---

## 11. Attribute-Stil-Differenzierung pro Feld (NEU v1.14, E74 + E78)

**Wichtig:** der E74-Stil-Pivot (aspirational + Esprit, Zielgruppe Frauen 25-35) gilt nicht für alle Attribut-Felder gleich. Pro Feld unterschiedliche Tonalitäts-Anforderung.

| Attribut-Feld | Stil-Modus | Begründung |
|---|---|---|
| `markentext` | **E74-aspirational** | Storytelling, Bindung zur Marke aufbauen, Persönlichkeit der Gründer:innen sichtbar machen. Brand-Story-Caching (E72/E79). |
| `artikeldetails` | **E74-aspirational** | Kern-Verkaufstext pro Artikel, Zielgruppe direkt ansprechen, Funktion als zweite Stimme nach dem Hook. |
| `material_and_care` | **clean/funktional (E78)** | Regulatorisch-funktionales Feld (EU-Textilkennzeichnungs-Pflicht). Kein Verkaufs-Text. |
| `size_and_fit` | **E74-aspirational (gemäßigt) + Modelname aus Crawl (F5/B58, NEU v1.17)** | Passform ist Verkaufsthema („eng anliegend für freie Pole-Bewegung"). Funktion ist hier prominenter als bei `artikeldetails`, aber die Stimme bleibt warm/aspirational. **Modelname-Konvention:** statt „Unser Model trägt..." → `<Modelname> trägt Größe S bei 1,72 m...` (z.B. Yifan, Vika, Elena bei HotCakes). Modelname aus Crawl-Body-Metadaten ziehen. Bei mehreren Models pro Artikel: erstes Model im Crawl-Body. Bei null Modelname im Crawl: neutrale Formulierung („Das Model trägt...") oder Phrase weglassen. |

### 11.1 `material_and_care` Struktur (E78)

Zwei klare HTML-Paragraphen, in dieser Reihenfolge:

**Paragraph 1: Stoffzusammensetzung** — EU-Textilkennzeichnungs-Pflicht, reine Material-Angabe in Prozent.

```html
<p>85% Polyamid, 15% Elasthan.</p>
```

**Paragraph 2: Pflegehinweise** — funktionale Aufzählung.

```html
<p>Handwäsche bei 30°C, nicht bleichen, nicht in den Trockner, nicht bügeln, nicht chemisch reinigen.</p>
```

**Verboten in `material_and_care`** (Abweichung vom E74-Stil-Pivot — gilt nur für dieses Feld):
- Sinnliche Adjektive („zarte Pflege", „samtige Berührung")
- Verkaufsförderliche Hinweise („damit der Glanz erhalten bleibt")
- Beschreibende Begründungen („weil das Material besonders empfindlich ist")
- E74-Wendungen wie „geht von Studio zu Brunch" — hier komplett fehl am Platz

**Erlaubt:** Du-Form (z.B. „Wasche bei 30°C") oder förmlicher Imperativ („Bei 30°C waschen"). Die Pipeline wählt eine Variante und hält sie pro Lieferant konsistent.

---

## 12. Cross-Selling-CSV-Schema (NEU v1.14, E80, erweitert v1.15) — 5. CSV-Output pro Lauf

**JTL-Ameise Import-Typ:** „Cross-Selling-Artikel" (eigener Import, nicht Teil der Artikeldaten).

**3-Spalten-Schema (exakte Reihenfolge):**

| # | Spalte | Inhalt | Beispiel |
|---|---|---|---|
| 1 | `Artikelnummer` | Identifizierungs-ID des Artikels, dem die Cross-Selling-Empfehlung zugeordnet wird. **NEU v1.15:** Vater UND alle Kinder werden hier aufgeführt (Kinder-Replikation). | `HC-Peonies-Top-Nude` oder `HC-Peonies-Top-Nude-001` (Kind) |
| 2 | `Artikelnummer Cross-Seller` | Vater-Artikelnummer des empfohlenen Artikels. Hier strikt nur Väter, niemals Kinder. | `HC-Peonies-Bottom-Nude` |
| 3 | `Cross-Selling-Gruppe` | exakter Name der Cross-Selling-Gruppe (muss in WaWi vorab existieren) | `Vervollständige Dein Outfit` |

**Eine Zeile pro Beziehung × Identifizierungs-ID.** Mehrere Cross-Selling-Beziehungen pro Artikel = mehrere Zeilen mit gleicher `Artikelnummer`. Außerdem pro Beziehung Replikation auf die Kind-IDs (siehe 12.1).

**Aktuell genutzte Cross-Selling-Gruppen (Stand 2026-05-17):**

| Gruppen-Name | Semantik | Algorithmus |
|---|---|---|
| `Vervollständige Dein Outfit` | exaktes Top-Bottom-Pendant in gleicher Farbe | gleicher Modell-Stamm + Farbe + gegensätzlicher Typ (Top↔Bottom) |
| `Ähnliche Artikel` | gleiches Modell in anderen Farben | gleicher Modell-Stamm (ohne Farbe) + gleicher Typ + andere Farbe |

**Andere existierende Gruppen in WaWi (nicht Pipeline-relevant aktuell):** `Reinigungsmittle`, `High Heels Zubehör`, `Garantieverlängerung`, `Unsere Zubehör-Empfehlung`, `Zusätzliche Farbauswahl`, `Weitere Studio-Poles`. Diese werden manuell gepflegt.

### 12.1 Cross-Selling-Algorithmus (pro Lauf)

1. **Vollständiger Lieferanten-Crawl:** Die Pipeline lädt den vollen Shopify-`/products.json`-Datensatz (nicht nur die Trigger-Modelle). Bei HotCakes: 124 Produkte.

2. **Modell-Stamm-Schlüssel (Algorithmus-Präzisierung NEU v1.15):** Für Outfit-Pair und Ähnliche-Artikel-Suche wird der Modell-Stamm-Schlüssel **inklusive Farbe** verwendet, nicht nur das Basis-Modell. Konkret:
   - Für **„Vervollständige Dein Outfit"**: Schlüssel `(modell_basis, farbe_im_namen)` — Top und Bottom müssen sowohl im Modell-Stamm als auch in der Farbe übereinstimmen. Beispiel: `(Savanna, Black)` Top matched nur mit `(Savanna, Black)` Bottom, nicht mit `(Savanna, Skin)` Bottom.
   - Für **„Ähnliche Artikel"**: Schlüssel `(modell_basis, typ)` ohne Farbe — gleicher Modell-Stamm und Typ, andere Farbe.

   **Bug-Beleg (Batch 2 Iter. 1, 2026-05-17):** Erste Implementierung nutzte nur `modell_basis` als Schlüssel für Outfit-Pairs, was Savanna-Top-Black fälschlich mit Savanna-Bottom-Skin und Savanna-Bottom-Emerald gematcht hätte. Mit der Farbe als Teil des Schlüssels: jede `(Savanna, Farbe)`-Familie ist eindeutig.

3. **Pro Vater-Artikel der Lieferung** (= Trigger-Modelle): identifiziere
   - Modell-Familie (z.B. „Peonies Top", „Savanna Top")
   - Farb-Variante (z.B. „Nude", „Mauve", „Black")
   - Typ (Top / Bottom / Bodysuit)

4. **Berechne Beziehungen** aus dem vollen Datensatz:
   - **„Vervollständige Dein Outfit":** Suche nach gleichem `(modell_basis, farbe_im_namen)` mit gegensätzlichem Typ. Bei Treffer: bidirektional eine Vater-Vater-Beziehung.
   - **„Ähnliche Artikel":** Suche nach gleichem `(modell_basis, typ)` mit anderer Farbe. Eine Vater-Vater-Beziehung pro Paar-Richtung. Bei drei Farb-Geschwistern: 3×2 = 6 Vater-Vater-Zeilen.

5. **Kinder-Replikation (NEU v1.15, E80-Erweiterung):** Für jede Vater-Vater-Beziehung wird die linke Spalte (`Artikelnummer`) zusätzlich für jede Kind-ID des Vaters dupliziert. Bei 1 Vater + 4 Kindern pro Stamm: 5 Zeilen pro Vater-Richtung. Eine bidirektionale Outfit-Pair-Beziehung = 2 × 5 = **10 Zeilen** statt 2. Die rechte Spalte (`Artikelnummer Cross-Seller`) bleibt **strikt Vater** — keine Kind-IDs in der rechten Spalte.

6. **CSV-Format:** UTF-8 BOM, `;`, CRLF, Quote `MINIMAL`.

7. **Cross-Selling-Family-Refresh-Modus (NEU v1.15, E80-Erweiterung 3 — optionaler Trigger-Modus):** Bei späterem Nachzug von Schwester-Artikeln (z.B. wenn Tjorben weitere Farbgeschwister Arachne Tan/Cherry, Savanna Black/Skin/Emerald/Lime/Heat oder Peonies-Bodysuit-skin-tones anlegt), kann die Pipeline in einem Refresh-Lauf für betroffene Modell-Familien das komplette Cross-Selling neu berechnen statt nur die neuen Artikel. Trigger: `Verarbeite Cross-Selling-Refresh für Lieferant X, Modell-Stamm Y`. Output: nur CSV 5, andere CSVs nicht ausgegeben (AP12 — keine leeren CSVs).

### 12.2 Beispiel-CSV-Output (mit Kinder-Replikation v1.15)

Angenommen Lieferung enthält 6 HotCakes-Modelle: Peonies Top Nude, Peonies Bottom Nude, Peonies Top Beige (Schwester-Farbe), Dark Roast Top, Dark Roast Bottom, Hekate Bodysuit. Jeder Vater hat 4 Kinder (Größen XS/S/M/L), Artikelnummer-Schema `<Vater>-<NNN>` (001-004).

Outfit-Pair-Beziehung **Peonies Top Nude ↔ Peonies Bottom Nude** (10 Zeilen, bidirektional × 5 IDs pro Vater-Familie):

```csv
Artikelnummer;Artikelnummer Cross-Seller;Cross-Selling-Gruppe
HC-Peonies-Top-Nude;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Top-Nude-001;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Top-Nude-002;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Top-Nude-003;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Top-Nude-004;HC-Peonies-Bottom-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude-001;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude-002;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude-003;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
HC-Peonies-Bottom-Nude-004;HC-Peonies-Top-Nude;Vervollständige Dein Outfit
```

Ähnliche-Artikel-Beziehung **Peonies Top Nude ↔ Peonies Top Beige** (10 Zeilen, analog):

```csv
HC-Peonies-Top-Nude;HC-Peonies-Top-Beige;Ähnliche Artikel
HC-Peonies-Top-Nude-001;HC-Peonies-Top-Beige;Ähnliche Artikel
HC-Peonies-Top-Nude-002;HC-Peonies-Top-Beige;Ähnliche Artikel
HC-Peonies-Top-Nude-003;HC-Peonies-Top-Beige;Ähnliche Artikel
HC-Peonies-Top-Nude-004;HC-Peonies-Top-Beige;Ähnliche Artikel
HC-Peonies-Top-Beige;HC-Peonies-Top-Nude;Ähnliche Artikel
HC-Peonies-Top-Beige-001;HC-Peonies-Top-Nude;Ähnliche Artikel
HC-Peonies-Top-Beige-002;HC-Peonies-Top-Nude;Ähnliche Artikel
HC-Peonies-Top-Beige-003;HC-Peonies-Top-Nude;Ähnliche Artikel
HC-Peonies-Top-Beige-004;HC-Peonies-Top-Nude;Ähnliche Artikel
```

Dark Roast Top ↔ Dark Roast Bottom: analog 10 Zeilen Outfit-Pair.

Hekate Bodysuit hat keine Outfit-Pair-Beziehung (Bodysuit ist Solo-Typ) und in diesem Beispiel keine Farb-Geschwister — daher keine Cross-Selling-Zeilen für Hekate.

**Beispiel-Summe:** 3 bidirektionale Beziehungen × 10 = **30 Zeilen** für 6 Modelle. Bei 21 Modellen mit ähnlicher Beziehungs-Dichte wie HotCakes Live-Trial Batch 1+2 (18 bidirektionale Beziehungen): 18 × 10 = **180 Zeilen** statt 36.

---

## 13. SNAPSHOT_KNOWLEDGE_FILES (v1.18 — Git-Tag-Pattern)

**Zweck:** Single Source of Truth für die Liste aller Wissens-Files, die in einem kompletten Snapshot vorhanden sein müssen. Resolver-Specs (`cowork_anweisung_datenimports.md`, `cowork_custom_instructions.md`, `Projekt-Anweisungen.md`, `run_brief_daten.md`) referenzieren diese Liste, statt eigene File-Listen zu führen — Drift-Schutz auf Ebene 1.

**Snapshot-Konzept ab v1.20 (E87 + E91):** Ein Snapshot ist ein **Git-Tag** auf `main` im Repo `https://github.com/verticalogmbh/polesportshop-wissen`. Die Liste unten beschreibt die Files, die im Repo-Root unter dem Tag liegen müssen. Drive-Sub-Folder-Snapshots (v1.0–v1.18) sind Read-Only-Archiv und nicht mehr aktualisiert.

**Bedeutung der Spalten:**
- `Datei`: Dateiname im Repo-Root (case-sensitive).
- `MaxKB`: Soft-Limit für die Dateigröße (50 KB). Architektur-Ziel: ≤ 40 KB pro File (Build-Target). In der Git-Welt ist >50 KB kein Tool-Limit-Killer mehr (E87), nur ein Lesbarkeits-Hinweis.
- `STATUS`: `OK` wenn aktuell unter 50 KB; `KNOWN_EXCEPTION` wenn überschritten und der Split bewusst aufgeschoben ist (mit Begründung).

**Konvention:** Self-Check (WSC-3 + WSC-1) liest diese Liste, vergleicht mit tatsächlichem Repo-Inhalt und prüft Größen. `KNOWN_EXCEPTION`-Files sind kein Fail, sondern informational Warning.

| Datei | MaxKB | STATUS |
|---|---|---|
| PROJEKT-CHARTER.md | 50 | OK |
| CLAUDE.md | 50 | OK (NEU v1.20 — Daily-Workflow-Cheatsheet für Claude Code) |
| LIEFERANTEN-ONBOARDING.md | 50 | OK (NEU v1.20 — Standard-Prozess für Lieferant 2-21) |
| WISSENS-UPDATE-PLAYBOOK.md | 50 | OK |
| Projekt-Anweisungen.md | 50 | OK |
| cowork_custom_instructions.md | 50 | OK |
| SPEC_KONSTANTEN.md | 50 | OK (knapp >50 KB nach v1.19, monitoring) |
| run_brief_daten.md | 50 | OK |
| cowork_anweisung_datenimports.md | 50 | OK (ab v2.0 v1.20 verschlankt — Konstanten + Self-Check + AP1-AP12 ausgelagert nach SPEC_KONSTANTEN) |
| cowork_anweisung_bildpipeline.md | 50 | KNOWN_EXCEPTION — Voll-Spec wieder aktiv ab v2.1/E93 (ca. 43 KB knapp unter 50 KB; Reaktivierung der Bildpipeline aus v1.19-Tag rekonstruiert) |
| WAWI-IMPORT-WISSEN.md | 50 | KNOWN_EXCEPTION — operatives Pilot-Wissen, Verschlankung bei B61-Trigger |
| lieferanten_mapping.yaml | 50 | OK (linear-skalierend; bei N≥5 Lieferanten Brand-Story-Split per B64) |
| BACKLOG.md | 50 | KNOWN_EXCEPTION — Pflege-Datei; erledigte Einträge in BACKLOG-ARCHIV.md ausgegliedert ab v1.20 |
| BACKLOG-ARCHIV.md | 50 | OK (NEU v1.20 — erledigte und deferred B-Einträge) |
| ENTSCHEIDUNGS-LOG-ARCHIV.md | 50 | OK |
| ENTSCHEIDUNGS-LOG-CRAWLING-DATEN.md | 50 | OK |
| ENTSCHEIDUNGS-LOG-COWORK-INFRA.md | 50 | OK |
| ENTSCHEIDUNGS-LOG-BILDPIPELINE.md | 50 | OK |
| ENTSCHEIDUNGS-LOG-STIL-CONTENT-A.md | 50 | OK |
| ENTSCHEIDUNGS-LOG-STIL-CONTENT-B.md | 50 | OK |
| ENTSCHEIDUNGS-LOG-LIVE-TRIAL.md | 50 | OK |
| _MANIFEST.md | 50 | OK |

**Gesamt: 22 Files pro kompletter Snapshot (21 Wissens-Files + 1 Manifest).** Änderungen ggü. v1.19 (19 Files): 3 neue Files (CLAUDE.md, LIEFERANTEN-ONBOARDING.md, BACKLOG-ARCHIV.md).

Repo-Meta-Files NICHT im Snapshot-Count: `README.md` (GitHub-Visitor-Doku), `.gitignore` (Worktree-Ausnahmen).

**Reihenfolge der Resolver-Ladung** (Cowork-Stage-0 oder Claude-Code-Klärungs-Sessions, je nach Trigger-Typ):

**Daten-Lauf-Trigger** („Verarbeite neue Artikel von …"):
1. `run_brief_daten.md` (kompakte operative Spec — E68)
2. `SPEC_KONSTANTEN.md` (diese Datei)
3. `lieferanten_mapping.yaml`

**Wissens-Update-Trigger** („Verarbeite Wissens-Update für v…"):
1. `WISSENS-UPDATE-PLAYBOOK.md`
2. `PROJEKT-CHARTER.md`
3. `BACKLOG.md` (aktive Risiken, neue Findings)
4. Betroffene Cluster-Files je nach Scope

**Onboarding-Trigger** („Onboarde neuen Lieferanten …", NEU v1.20):
1. `LIEFERANTEN-ONBOARDING.md`
2. `lieferanten_mapping.yaml`
3. `SPEC_KONSTANTEN.md` (Sektion 7 Merkmalwerte, Sektion 8 Goldstandard-Referenz)

**Klärungs-Chat** (Architektur-Fragen, kein Pipeline-Lauf):
- `CLAUDE.md` für Daily-Workflow-Fragen
- Bei Substanz: `PROJEKT-CHARTER.md` + relevantes `ENTSCHEIDUNGS-LOG-*.md` via E-Nummer-Index in Sektion 14
- Historische E-Nummern: `ENTSCHEIDUNGS-LOG-ARCHIV.md`

**Append-File-Verbot:** Wissens-Files dürfen NIE als `*_Append.md` oder `*_Patch.md` existieren — alle Änderungen werden im Master-File konsolidiert. Self-Check fail-t bei Pattern `*_Append*` oder `*_Patch*` im Repo-Root.

---

## 14. ENTSCHEIDUNGSLOG_E_NUMMER_INDEX (NEU v1.17)

**Zweck:** Master-Index für die E-Nummer → Cluster-File-Zuordnung nach dem v1.17-Split der ursprünglichen `ENTSCHEIDUNGS-LOG.md`. Resolver schlägt hier nach, wenn Cross-Referenzen zu E-Nummern aufgelöst werden müssen.

**Lese-Hinweis:** E-Nummern ohne Eintrag in der Tabelle liegen im ARCHIV (`ENTSCHEIDUNGS-LOG-ARCHIV.md`). Aktuell archiviert: E14, E20, E35, E36, E40, E42.

| E-Nr | Cluster-File | Titel-Kurzform |
|---|---|---|
| E1 | COWORK-INFRA | Cowork als Produktions-Engine, Claude.ai als Planungs-Engine |
| E2 | COWORK-INFRA | Lineare Pipeline ohne User-Review-Gate vor CSV-Output |
| E3 | COWORK-INFRA | Manueller Tages-Trigger durch Einkäufer |
| E4 | COWORK-INFRA | Multi-Input-Trigger (6 Modi) |
| E5 | CRAWLING-DATEN | Mehrere separate CSVs statt einer (initial vier, später fünf, ab v1.15 wieder vier) |
| E6 | CRAWLING-DATEN | Artikelnummer = Lieferantenartikelnummer |
| E7 | CRAWLING-DATEN | Vater-Kind-Struktur über Identifizierungsspalte Vaterartikel |
| E8 | CRAWLING-DATEN | Kombinierte Größen (XS/S) = ein Kind + Merkmal-Expansion |
| E9 | CRAWLING-DATEN | Mehrsprachigkeit: Attribute via Spalten-Suffix, Merkmale nur Deutsch |
| E10 | BILDPIPELINE | Cloudflare R2 für Bild-Hosting, Ameise-URL-Import |
| E11 | BILDPIPELINE | 2:3-Format, 1000×1500, JPEG <100 KB (Default-Profil `fashion_portrait_2x3`) |
| E12 | BILDPIPELINE | Bild-Pipeline separat aber als Sub-Process aufrufbar |
| E13 | CRAWLING-DATEN | Crawling von Pole Junkie (Wettbewerber) erlaubt, mit Auflagen |
| E15 | COWORK-INFRA | service@polesportshop.de für alle Pipeline-Services |
| E16 | STIL-CONTENT-A | Standard-Fallbacks für Pflegehinweise und Passform-Defaults |
| E17 | COWORK-INFRA | Plattform-Aktivierung als bewusstes Backlog-Item |
| E18 | STIL-CONTENT-A | Iterativer Quality-Loop in der Pilot-Phase |
| E19 | CRAWLING-DATEN | Merkmal-Logik bei Variantenartikeln: Farbe+Style auf Vater UND Kind, Größe nur auf Kind |
| E21 | CRAWLING-DATEN | Cloud-Storage-Links brauchen separates Handling |
| E22 | STIL-CONTENT-A | HTML- und Stilprofil-Definition für Pipeline-Output |
| E23 | STIL-CONTENT-A | Pricing-Architektur mit zwei Referenztabellen |
| E24 | COWORK-INFRA | Konfigurationsdaten als separate Files, getrennt von Anweisungs-Specs |
| E25 | STIL-CONTENT-A | Pricing-Vereinfachung für Pilot-Phase (Konstante 2.0) |
| E26 | STIL-CONTENT-A | Artikelname-Konvention mit Übersetzungstabellen |
| E27 | STIL-CONTENT-A | HotCakes-Größen-Konvention: Kombi-Größen auf kleinste reduzieren |
| E28 | STIL-CONTENT-A | GLD manuell setzbar via Stammdaten-CSV |
| E29 | STIL-CONTENT-A | Importvorlagen-Naming-Konvention |
| E30 | STIL-CONTENT-A | Spalten-Mapping: sprechende Namen OK, einmaliges manuelles Mapping reicht |
| E31 | STIL-CONTENT-A | Mehrsprachigkeit via „Weitere Texte"-Reiter mit Global-{Sprache}:-Präfix |
| E32 | COWORK-INFRA | Cowork-Setup, Drive Wichtig: Claude Backup/ als Brücke |
| E33 | COWORK-INFRA | Credential-Mechanismen für externe Services in Cowork |
| E34 | STIL-CONTENT-A | JTL-Erbung-Verbot universalisiert |
| E37 | STIL-CONTENT-A | Verkaufskanal-Häkchen aus Ameise-Importvorlage entfernt |
| E38 | STIL-CONTENT-A | GLD-Spalte muss manuell im Ameise-Mapping zugeordnet werden |
| E39 | STIL-CONTENT-A | Attribute als Standard-CSV (nicht mehr optional) |
| E41 | COWORK-INFRA | Crawl-Tool-Marktcheck 2026-05: Firecrawl bleibt strategische Wahl |
| E43 | COWORK-INFRA | R2-Upload-Mechanik: boto3 + Egress-Allowlist + Drive-File-Credentials |
| E44 | BILDPIPELINE | R2 als vollständiger Bild-Storage: Originale von Drive nach R2 |
| E45 | BILDPIPELINE | Crop-Profile pro Produkttyp + Vision-basierte Pose-Sortierung |
| E46 | BILDPIPELINE | Bilder integriert in Stammdaten-CSV, separater Bilder-Import abgeschafft |
| E47 | COWORK-INFRA | Wissens-Architektur: Immutable Snapshots in Drive |
| E48 | CRAWLING-DATEN | Crawl-Modus B: Code-Execution + Browser-UA gegen Shopify-Storefront-JSON |
| E49 | CRAWLING-DATEN | Pole Junkie Crawl-Freigabe: Owner-Direktive mit Verantwortungs-Übernahme |
| E50 | CRAWLING-DATEN | WaWi-Merkmalwerte: statische deutsche Liste mit zweistufiger Farb-Logik |
| E51 | CRAWLING-DATEN | Kategoriebaum-Mapping: Pole Dance Kleidung als Ebene 1 |
| E52 | CRAWLING-DATEN | A6-Pivot: CSVs nur lokal im Cowork-Workspace, kein Drive-Upload |
| E53 | STIL-CONTENT-B | Eigene polesportshop-Stilidentität, Pole Junkie als Reduktion-Vorbild |
| E54 | CRAWLING-DATEN | Stammdaten-CSV-Schema-Layout: 38 alte Spalten + 10 Bilder am Ende |
| E55 | STIL-CONTENT-A | SEO-Templates pro Sprache deterministisch aus festem Pattern |
| E56 | STIL-CONTENT-A | Kind-Artikelname mit Größen-Suffix in allen 5 Sprachen |
| E57 | CRAWLING-DATEN | Multi-Kategorie-Zuweisung via mehrfache CSV-Zeilen mit gleicher Artikelnummer |
| E58 | STIL-CONTENT-A | Sprach-Lokalisierungs-Konvention für Artikelnamen |
| E59 | STIL-CONTENT-A | WaWi-Mapping-Wissen als Fels nicht Treibsand |
| E60 | BILDPIPELINE | Bild-Größen-Cap <100 KB im JPEG-Encoding mit Quality-Iteration |
| E61 | COWORK-INFRA | Konstanten-Auslagerung in SPEC_KONSTANTEN.md |
| E62 | COWORK-INFRA | Spec-Caching-Konvention (Stage-0-Pflicht) |
| E63 | BILDPIPELINE | Bildpipeline archiviert, manueller Bilder-Workflow im Pilot |
| E64 | COWORK-INFRA | Lokaler Workflow als Default für Wissens-Updates |
| E65 | COWORK-INFRA | Stückelung in Prompt-Cycles als Default für mehrstufige Wissens-Updates |
| E66 | COWORK-INFRA | Build-Strategie: create_file vs. str_replace nach Änderungs-Volumen |
| E67 | COWORK-INFRA | Tag-Neustart-Disziplin als Context-Window-Resilienz |
| E68 | COWORK-INFRA | Selective Spec-Loading in Stage 0 + Pre-Compiled Run-Brief |
| E69 | CRAWLING-DATEN | E52-Implementation in Cowork-CI und Datenimports-Spec verankern |
| E70 | BILDPIPELINE | Feature-Erfassung text-basiert, Vision-API-Extraktion bewusst aufgeschoben |
| E71 | STIL-CONTENT-B | PO-Nummer komplett aus der Daten-Pipeline raus |
| E72 | STIL-CONTENT-A | Brand-Story-Caching pro Lieferant im lieferanten_mapping.yaml |
| E73 | STIL-CONTENT-A | Artikeldetails immer alle 5 Sprachen voll, keine leichten Übersetzungen |
| E74 | STIL-CONTENT-B | Attribute-Stil-Pivot: Zielgruppe Frauen 25-35, aspirational |
| E75 | STIL-CONTENT-B | Anti-Confusion-Note: E57-Doppelzeilen sind kein Bug, sondern bewusstes Pattern |
| E76 | STIL-CONTENT-B | „Bottom" im deutschen Freitext verboten, immer „Shorts" verwenden |
| E77 | STIL-CONTENT-B | Anti-Plagiarism / Originalitäts-Pflicht + Self-Check-Punkt 13 |
| E78 | STIL-CONTENT-B | material_and_care clean & funktional, zwei klare Paragraphen |
| E79 | STIL-CONTENT-B | Neue HotCakes-Brand-Story als Evergreen mit Gründerinnen-Persönlichkeit |
| E80 | STIL-CONTENT-B | Cross-Selling-Architektur als 5. CSV-Output („Vervollständige Dein Outfit" + „Ähnliche Artikel"); inkl. Erweiterung 2026-05-17 |
| E81 | LIVE-TRIAL | Autonomie-Hoheit für Workflow-Entscheidungen |
| E82 | LIVE-TRIAL | Stil-Verschärfung — Doppelpunkt-Verbot und Meta-Einleitungs-Verbot |
| E83 | LIVE-TRIAL | Pre-Run Scope-Analyse als Stage 0.5 |
| E84 | LIVE-TRIAL | Familien-erhaltende Split-Regel |
| E85 | COWORK-INFRA | Wissens-Update-Build-Pattern als Standard-Playbook |
| E86 | COWORK-INFRA | File-Header-Versionierungs-Konvention (SemVer für Snapshot-Disziplin) |
| E87 | COWORK-INFRA | Migration Drive → Git als Wissens-Backbone (Pattern-Pivot v1.19) |
| E89 | CRAWLING-DATEN | Category-Pattern + Sara-Review-Workflow (präzisiert E57, WaWi-Key 546) |
| E90 | CRAWLING-DATEN | F2-F6-Implementierung in v1.19 (Sammeleintrag: B55-B59 erledigt) |
| E91 | COWORK-INFRA | Skalierungs-Refactor v1.20 — Verschlankung, neue Anker, Cowork-Resolver auf GitHub-Raw (B63 erledigt) |
| E92 | CRAWLING-DATEN | Trial-Findings v1.20 — Multi-Kategorie auf 3-Zeilen-Pattern korrigiert (Oberkategorie + Subkategorie + Sara-546), Farb-Lokalisierung DE (Teal→Türkis, Sky→Himmelblau, Cherry→Kirschrot, Emerald→Smaragdgrün, Lime→Limettengrün) |
| E93 | BILDPIPELINE | Bildpipeline reaktiviert (kehrt E63 um) — Stage 5.6+5.7 wieder aktiv, R2-Architektur unverändert, Spec von Stub auf v2.1 voll-aktiv |
| E94 | CRAWLING-DATEN | Artikelnummer aus dem WaWi-Nummernkreis vorab vergeben (A-Nummern, „Weg B"; Kinder `-001`…) — aktiviert E6, weil Lager-Scan an der Artikelnummer hängt; sprechender Schlüssel bleibt in `Artikelnummer (Lieferant)` |
| E95 | CRAWLING-DATEN | EAN/GTIN-Spalte im Stammdaten-Schema (48→49, ans Ende/Position 49 per E54 append-only) + Barcode-Anreicherung pro Größe aus committeter Lieferanten-Referenz (`content/ean_<lieferant>.csv`); nur auf Kind-Ebene; Lunalae UTC-Barcodes |

**Cluster-File-Kurz-Lookup (Datei-Mapping zum Cluster-Namen oben):**

| Cluster-Name | Datei |
|---|---|
| CRAWLING-DATEN | ENTSCHEIDUNGS-LOG-CRAWLING-DATEN.md |
| COWORK-INFRA | ENTSCHEIDUNGS-LOG-COWORK-INFRA.md |
| BILDPIPELINE | ENTSCHEIDUNGS-LOG-BILDPIPELINE.md |
| STIL-CONTENT-A | ENTSCHEIDUNGS-LOG-STIL-CONTENT-A.md |
| STIL-CONTENT-B | ENTSCHEIDUNGS-LOG-STIL-CONTENT-B.md |
| LIVE-TRIAL | ENTSCHEIDUNGS-LOG-LIVE-TRIAL.md |

**Archivierte E-Nummern (in `ENTSCHEIDUNGS-LOG-ARCHIV.md`):** E14, E20, E35, E36, E40, E42.
