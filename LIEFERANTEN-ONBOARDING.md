# Lieferanten-Onboarding — Standard-Prozess

**Stand:** v1.23, 2026-06-18 (auf Code-Pipeline aktualisiert; Ausführung lokal in Claude Code, nicht mehr Cowork)
**Zweck:** Zentraler Spec für das Onboarding eines neuen Lieferanten (Skalierung auf ~50). Konsolidiert Mapping-Schema, Code-Artefakte und Ameise-Vorlagen-Anlage.
**Trigger im Claude-Code-Chat:** „Onboarde Lieferant <NAME>" (Mapping + Brand-Story in Claude Code), dann „Verarbeite neue Artikel von <NAME>: Probe-Lauf" — **lokaler Code-Lauf** (`pipeline/orchestrator`), kein Cowork.

> **Skalierungs-Kern:** Ein Lieferant = Dateien in **festen Fächern** (siehe „Code-Artefakte pro Lieferant" unten) + ein Mapping-Eintrag + 5 Ameise-Vorlagen. Der Pipeline-Kern und die Wissens-Docs wachsen dadurch **nicht** — sie wachsen nur mit neuen Mechaniken. So bleiben 50 Lieferanten handhabbar.

---

## Wann dieser Spec greift

Vor dem ersten produktiven Daten-Pipeline-Lauf für einen neuen Lieferanten. Lieferanten 2–21 folgen alle diesem Prozess; Lieferanten 0+1 (POLE_ADDICT, HOTCAKES) liefen vor v1.20 ad-hoc und behalten ihre historischen Besonderheiten (POLE ADDICT alte Vorlagen-Naming, HotCakes hat 2 Legacy-Vorlagen aus E35/E46).

Nicht relevant bei: Refresh-Läufen (neue Lieferung eines bekannten Lieferanten), Re-Imports auf bestehende Artikel, Cross-Selling-Family-Refresh.

---

## Code-Artefakte pro Lieferant (feste Slots)

Neben dem Mapping-Eintrag legt ein neuer Lieferant Dateien in diese festen Fächer:

| Slot | Datei | Pflicht? |
|---|---|---|
| Mapping/Config + Brand-Story | `lieferanten_mapping.yaml` (1 Eintrag) | ja (Schritt 1) |
| Content (Merkmale/Style + Attribut-Texte, 5 Sprachen) | `pipeline/content/<kuerzel>_content.json` | ja |
| Barcodes (UTC/EAN pro Größe) | `pipeline/content/ean_<kuerzel>.csv` (`modell_basis;garment_type;farbe;groesse;ean`) | nur wenn Lieferant Barcodes liefert (E95) |
| Crawl-Builder (Nicht-Shopify) | `pipeline/suppliers/<kuerzel>.py` mit `build_vaeter()` | nur Nicht-Shopify (Shopify → `builder: None`, Crawl automatisch) |
| EK + Bestell-Mengen (aus Rechnung) | `EK_input/ek_<x>.csv`, `EK_input/menge_<x>.csv` (gitignored) | pro Lauf |
| Registry-Eintrag | `orchestrator.SUPPLIERS` (`key`, `ek`, `content`, `builder`, ggf. `ean`, `scope`) | ja |

Mapping-Währung steuert den Margen-Aufschlag (E98: EUR → +1€ EK, sonst +5€ VK) und ob EK umgerechnet wird (`fx_to_eur`). `lieferzeit_tage` nur fürs Lieferdatum der Bestellung.

## Pflicht-Checkliste (5 Schritte, in dieser Reihenfolge)

### Schritt 1 — Mapping-Eintrag in `lieferanten_mapping.yaml`

Pflichtfelder pro Lieferant (Cowork bricht ab bei `null`):
- `anzeigename` — voller Name wie im Trigger gesprochen
- `kuerzel` — für Dateinamen (z.B. `POLE-ADDICT`)
- `hersteller` — Marken-/Herstellername für Stammdaten (lange Form)
- `marke_kurz` — Kurzform für Artikelnamen (Goldstandard-Konvention E59). Wenn keine Kurzform existiert: identisch zu `hersteller`.
- `herkunftsland` — ISO-2-Code (PT, GR, DE, US, ...)
- `waehrung` — ISO-3-Code (EUR, USD, GBP)
- `steuerklasse` — JTL-Steuerklassen-Anzeigename. Pilot-Default: `"OSS2-undefiniert - Standard alle Länder"`
- `shop_url` — primäre Crawl-Quelle (Hersteller bevorzugt, E20)
- `r2_prefix` — Bucket-Pfad-Prefix in Cloudflare R2 (auch wenn Bildpipeline mit E63 archiviert ist — Feld bleibt für Reaktivierung)
- `ameise_vorlagen.stammdaten` / `.variationen` / `.merkmale` / `.attribute` / `.cross_selling` — Vorlagen-Namen in WaWi (siehe Schritt 2)
- `brand_story_de` / `_en` / `_fr` / `_it` / `_es` — Brand-Story in allen 5 Sprachen (siehe Schritt 3)

Defaults pro Lieferant (NEU v1.16):
- `article_weight_kg: 0.05` (50 g pro Kleidungsstück, F3/B56)
- `taric_code: '62114390'` (TARIC für Pole-Bekleidung, F6/B59 — als String gequotet, sonst interpretiert YAML als Int)

Optional:
- `fallback_retailer_url` — wenn Hersteller-Site unvollständig
- `drive_ordner_id`, `drive_eingang_id` — Lieferanten-Drive-Ordner (für Drive-Upload-Input-Modus)
- `lieferantennummer_wawi` — interne WaWi-Lieferantennummer
- `groessen_konvention` — `standard` (jede Größe einzeln) oder `kombi_reduziert_auf_kleinste` (XS/S → XS, E27 für HotCakes)
- `max_groesse` — Default-Größen-Cap (`S` | `M` | `L` | `XL` | `XXL` | `null`)
- `category` — `fashion` (Default) | `tech`
- `crop_profile` — `fashion` (2:3, 1000×1500) | `tech` (1:1, 1200×1200). Eingefroren mit E63, bleibt für Reaktivierung.
- `pose_sort` — `auto_vision` (Default für fashion) | `manufacturer_order` | `none`. Eingefroren mit E63.
- `crawl_mechanik` — `shopify_json` | `null`. Beim Onboarding detektieren (z.B. via `curl https://<shop>/products.json` Test).
- `stil_inspiration: true` — wenn Lieferant zusätzlich Stil-Inspirations-Quelle ist (Pole Junkie nutzt das, E49/E53).

Volle Schema-Doku am Ende von `lieferanten_mapping.yaml`.

### Schritt 2 — 5 Ameise-Vorlagen in JTL-WaWi anlegen

**Naming-Konvention (E29):** `{Lieferantenname}_{Reihenfolge}_{Import-Typ}` mit Underscores als Element-Trenner, Leerzeichen nur innerhalb des Lieferantennamens.

**Empfohlene Slot-Reihenfolge** (für alle neuen Lieferanten — Legacy bei POLE ADDICT und HotCakes-_3_Lieferantendaten/_5_Bilder ist eingefroren):
1. `{Lieferantenname}_1_Stammdaten` (Import-Typ: Artikel > Artikeldaten)
2. `{Lieferantenname}_2_Variationen` (Artikel > Variationen)
3. `{Lieferantenname}_3_Merkmale` (Artikel > Artikelmerkmale)
4. `{Lieferantenname}_4_Attribute` (Artikel > Artikelattribute)
5. `{Lieferantenname}_5_CrossSelling` (Cross-Selling-Artikel — eigener Import-Typ)

**Slot-Konvention pro Import-Typ (NEU v1.15):** Slot-Nummern sind pro Import-Typ eindeutig, nicht lieferanten-weit. `_3_Merkmale` kollidiert NICHT mit `_3_Lieferantendaten` (anderer Import-Typ).

**Pro Vorlage einrichten:**
- **Spalten-Mapping** auf JTL-Felder (E30: sprechende CSV-Spaltennamen OK, Auto-Mapping greift teilweise; pro Vorlage einmal manuell mappen + speichern, dann pro neuem Lieferanten klonen). Details in `WAWI-IMPORT-WISSEN.md` Sektion 10 (Cheat-Sheet) und `cowork_anweisung_datenimports.md` Sektion 7.
- **Standardlieferant explizit setzen (Pflicht ab v1.15 nach Bug-Beleg):** im Standardwerte-Bereich „Lieferant" explizit auf den Lieferanten setzen. Bug-Beleg HotCakes 2026-05-17: `_4_Attribute`-Vorlage hatte „nicht gewählt" → 220 Warnungen „Lieferant existiert nicht". Gilt für ALLE 5 Vorlagen.
- **Stammdaten-Vorlage zusätzlich:**
  - 10 Bild-Spalten `Bild 1`–`Bild 10` auf JTL-Felder `Bild Pfad/URL 1`–`Bild Pfad/URL 10` mappen (E46/B5).
  - Reiter „Bilder/Plattformen": alle 11 Plattform-Häkchen setzen.
  - Reiter „Verkaufskanal aktiv": Häkchen entfernen + Vorlage speichern (E37/B21).
  - Multi-Kategorie-Setting: „Kategorieverknüpfungen des Artikels aktualisieren" = „Neue Kategorien beim jeweiligen Artikel hinzuimportieren" (E57).
  - Lieferantenblock-Spalten unter „Lieferanteneinstellungen des Artikels" mappen + Währungs-Standardwert setzen (E36).
  - GLD manuell auf „Ø Einkaufspreis (netto)" mappen (E28/E38).
- **Attribute-Vorlage zusätzlich:** alle Felder gequotet (`csv.QUOTE_ALL`).
- **Cross-Selling-Vorlage zusätzlich:** Import-Typ „Cross-Selling-Artikel" wählen, 3 Spalten zuordnen (`Artikelnummer` → Identifizierungsspalte, `Artikelnummer Cross-Seller` → Artikel-IDs-Cross-Selling-Artikel, `Cross-Selling-Gruppe` → Cross-Selling). Cross-Selling-Gruppen müssen vorab in WaWi existieren (bei polesportshop sind „Vervollständige Dein Outfit" und „Ähnliche Artikel" angelegt — bei Bedarf für Lieferant erweitern).

### Schritt 3 — Brand-Story pro Lieferant pflegen (E72/E79)

Brand-Story-Caching ist die Default-Mechanik für `markentext`-Attribut (statt pro Lauf neu generieren).

**Pro Sprache** (`brand_story_de`, `brand_story_en`, `brand_story_fr`, `brand_story_it`, `brand_story_es`):
- 80–150 Wörter
- Aspirational (E74-Stil), Zielgruppe Frauen 25–35
- Markenstimme + Persönlichkeit der Gründer:innen, wenn bekannt (E79-evergreen: keine Print-Serien-Erwähnungen, weil die wechseln)
- DE = Master, andere 4 Sprachen daraus abgeleitet — aber pro Sprache eigene Tonalität-Treffer (siehe `run_brief_daten.md` Sektion 9 für Sprach-Tonalitäten).

Recherche-Quelle: Hersteller-„About"-Seite, ggf. Wikipedia/Presse-Mitteilungen. Im Zweifel Tjorben fragen.

**Wenn null:** Cowork generiert Brand-Story pro Lauf neu und markiert als E70 (Eigeninterpretation). Akzeptabel als Übergang, aber ineffizient — beim Onboarding einmal richtig pflegen.

### Schritt 4 — Probe-Lauf (lokaler Code)

`orchestrator.run(supplier="<kuerzel>", with_images=...)` (bzw. `python -m pipeline.orchestrator --supplier <x> [--images]`). EK/Mengen vorher in `EK_input/` ablegen.

**Erwartetes Ergebnis (Go-Kriterien):**
- Pricing findet für jeden Vater einen EK (sonst STOPP, `missing`-Liste im Bericht).
- A-Nummern aus dem Nummernkreis vergeben (E94), EAN angereichert falls Referenz (E95).
- 5 CSVs (+ optional Bestellung) in `pipeline/outputs/<KUERZEL>_<stamp>/`, Lauf-Bericht daneben.
- Self-Check 16/16 grün.

**No-Go-Kriterien:**
- Cowork stoppt bei Sprach-Lookup-Lücke (AP8) → SPEC_KONSTANTEN Sektion 6 erweitern, Re-Lauf.
- Self-Check fail-t auf 1+ Punkt → Spec-Update oder Mapping-Anpassung, Re-Lauf.
- Mapping-Pflichtfeld `null` erkannt → Mapping ergänzen, Re-Lauf.
- Pole-Junkie-spezifisch: Cease-and-Desist-Erkennung → STOPP, eskalieren (E49).

### Schritt 5 — Ameise-Import + Shop-Review

Tjorben importiert die 5 CSVs in WaWi-Ameise in der Slot-Reihenfolge `_1_` bis `_5_`. Nach Import:
- WaWi-UI: Artikel-Liste prüfen — sind Vater/Kind-Strukturen korrekt? Sind Kategorien korrekt zugewiesen (inkl. Sara-546-Zuweisung, E89)?
- Shop-Review: Frontend prüfen — sehen Titel-Tags + Meta-Description korrekt aus? Stimmt der Stil? Sind 5 Sprachen befüllt?
- Sara (Social-Media-Manager) reviewt im WaWi-Filter „Intern > Neue Artikel für Sara" (Kategorie-Key 546) und entfernt die Zuweisung nach Approval (E89-Workflow).
- Bilder: kommen automatisch aus der Pipeline (R2-URLs in Stammdaten `Bild 1`–`Bild 10`, E46/E93) — kein manuelles Pflegen.

Findings: in `BACKLOG.md` aufnehmen oder direkt in den nächsten Wissens-Update-Build mitnehmen.

---

## Onboarding-Commit-Pattern

Nach Schritt 1+3 (Mapping + Brand-Story) commited Claude Code typischerweise so:

```
git -C ~/Documents/polesportshop-wissen add lieferanten_mapping.yaml
git -C ~/Documents/polesportshop-wissen commit -m "lieferanten_mapping: <KÜRZEL> Onboarding (B<x>)"
git -C ~/Documents/polesportshop-wissen push
```

**Kein Tag-Bump für Onboarding-Commits.** Onboarding-Sammel-Commits gehen ohne Tag durch; der nächste reguläre Wissens-Update-Build zieht sie ein. Bei kritischem Onboarding (z.B. neuer Lieferant mit komplett neuem Crawl-Pattern, der Spec-Updates braucht): zusammen mit Spec-Updates als `v1.X+1`-Build verpacken.

## Skalierungs-Hinweis (für Lieferant 6+)

`lieferanten_mapping.yaml` wächst linear mit der Anzahl Lieferanten. Brand-Stories sind dabei der Hauptgewichts-Faktor (~3 KB pro Lieferant in 5 Sprachen). Bei N≥5 aktive Lieferanten: Brand-Story-Split in separate Files (z.B. `brand-stories/<kuerzel>.yaml`) prüfen — Entscheidung deferred bis dahin, siehe BACKLOG B64.

## Onboarding-Templates / Goldstandard

- **HotCakes** als Goldstandard-Referenz (E59): voller `brand_story_*`-Set, alle Defaults gesetzt, alle 5 Vorlagen Live-Trial-validiert. Beim Onboarding eines neuen Shopify-Lieferanten: HotCakes-Block als Template nehmen, anpassen.
- **POLE ADDICT** als Goldstandard-Referenz für nicht-Shopify (Drive-Upload-Modus): historische Vorlagen-Naming, ein nützliches Spiegelbild für „wenn Lieferant eigene CSV/Excel liefert".

---

## Verwandte Dokumente

- `lieferanten_mapping.yaml` — Schema-Doku am Ende der Datei
- `WAWI-IMPORT-WISSEN.md` Sektion 9 — Detailpräzisierung der Ameise-Vorlagen-Anlage + HotCakes-Goldstandard
- `cowork_anweisung_datenimports.md` Sektion 6 + 7 — Spalten-Mapping in Ameise
- `SPEC_KONSTANTEN.md` Sektion 7 — Merkmalwerte (Pflicht beim Onboarding zu prüfen, ob neue Werte nötig)
- `SPEC_KONSTANTEN.md` Sektion 8 — Goldstandard-Referenz-Artikel
- `PROJEKT-CHARTER.md` Prinzip 10 — WaWi-Mapping als Fels nicht Treibsand
