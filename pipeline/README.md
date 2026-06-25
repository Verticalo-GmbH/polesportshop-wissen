# pipeline/ — Artikelanlage-Pipeline (lokal, Claude Code)

Erzeugt aus Lieferanten-Daten die **5 JTL-Ameise-CSVs** (Stammdaten, Variationen,
Merkmale, Attribute, Cross-Selling) + **Bildpipeline** (Crop/Kompression → Cloudflare R2).
Lokale Python-Portierung der früheren Cowork-Pipeline (Snapshot-Wissen v1.21).

**Wichtig:** Dieses Runbook macht das Repo selbst-bedienbar — eine neue Claude-Code-Session
oder ein neuer Laptop braucht nur `git clone` + die Schritte unten. Aller Code, alle
generierten Texte und das Mapping liegen im Repo; nur Secrets, EK-Listen, venv und Outputs
sind lokal (siehe unten).

---

## Setup (neuer Rechner / neue Session)

```bash
git clone https://github.com/verticalogmbh/polesportshop-wissen
cd polesportshop-wissen/pipeline
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

## Was du pro Lauf bereitstellst (nicht im Repo, bewusst)

1. **EK-Liste / Rechnung** → `pipeline/EK_input/ek_<lieferant>_<nr>.csv`
   Format (Semikolon): `modell;typ;farbe;ek_netto` — eine Zeile je Vater (Farbe leer, wenn keine).
   Beispiel siehe `orchestrator.py` Konstante `EK_FILE`.
2. **R2-Credentials** (nur für Bilder) → `pipeline/.secrets/r2_credentials.json`
   ```json
   { "access_key_id": "...", "secret_access_key": "..." }
   ```
   Quelle: Cloudflare → R2 → Manage R2 API Tokens → **Object Read & Write** auf Bucket
   `polesportshop-images`. Endpoint/Bucket/Public-URL stehen schon in `config.py`.
   Wird nie geloggt/committet (gitignored).

## Lauf

```bash
cd polesportshop-wissen
./pipeline/.venv/bin/python -m pipeline.orchestrator            # 5 CSVs (Bild-Spalten leer)
./pipeline/.venv/bin/python -m pipeline.orchestrator --images   # zusätzlich Bilder -> R2 -> URLs in Stammdaten
```
Output: `pipeline/outputs/HOTCAKES_<timestamp>/` (5 CSVs + Lauf-Bericht, Self-Check 16/16).

## Review & WaWi-Import (JTL-Ameise)

Import-Reihenfolge: `1_Stammdaten` → `2_Variationen` → `3_Merkmale` → `4_Attribute`,
`5_CrossSelling` separat (Import-Typ „Cross-Selling-Artikel").

**Zwei Vorlagen-Stolperfallen (einmalig pro Ameise-Importvorlage mappen):**
- **Variationen:** Spalten `Sortiernummer Variation` + `Sortiernummer Variationswert`
  zuordnen — sonst sortiert JTL 1.11 die Größen alphabetisch (L,M,S,XS).
- **Stammdaten:** Spalten `Bild 1`–`Bild 10` zuordnen, sonst kommen die Bilder nicht in den Shop.

---

## Konfiguration & Module

- **Scope/Lieferant:** `lieferanten_mapping.yaml` (Repo-Root) — Shop-URL, `crawl_mechanik`,
  `crop_profile`, `pose_sort`, `r2_prefix`, TARIC, Brand-Story. Neuer Lieferant = hier eintragen.
- **Konstanten/Schema:** `spec.py` (SPEC_KONSTANTEN §1–§7 verbatim), `constants.py`.
- **Pipeline-Stages:**
  `crawl/shopify_json.py` (Crawl) → `extract.py` (Modell/Farbe/Typ-Split, Scope-Filter)
  → `pricing.py` (Netto-VK = EK netto ×2, dann MwSt ×1,19 → ,90) → `content.py`/`content/<lieferant>_content.json`
  (Merkmale-Farbe/Style + Attribut-Texte, in `content_build.py` autoriert)
  → `csv/*` (5 CSV-Writer) → `selfcheck.py` (16 Punkte) → `orchestrator.py`.
- **Bilder:** `images/process.py` (Crop fashion 2:3 1000×1500, <100 KB),
  `images/r2.py` (boto3 → R2, idempotent).
- **Content neu bauen** (nach Text-/Farb-Änderung): `python -m pipeline.content_build`.

## Artikel-Ledger (E102) — zentraler Stand aller Artikel

`pipeline/state/artikel_ledger.json` (committet) hält **immer nur den letzten Stand**
jedes angelegten Artikels, gekeyt auf die A-Nummer — wie ein Git-Working-Tree. Die
**Historie liefert git** über die Commits dieser Datei (kein Durchsuchen alter
`outputs/`-Ordner mehr). Pro Vater: Lieferant + WaWi-Nr, sprechender Schlüssel, Name,
Modell/Typ/Farbe, Währung + fx, EK (original + EUR), GLD, Brutto-VK, Herkunftsland,
Kinder `{A-Nummer: Größe}`, EAN je Größe, Quelle, Stand-Datum. Jeder **kanonische Lauf**
(`persist_counter=True`) ruft `ledger.upsert(...)` und überschreibt die betroffenen
A-Nummern. Modul: `ledger.py`.

## Betriebs-Modus

- **Daten-Run (Normalfall):** EK-Liste rein → `orchestrator` laufen → reviewen → importieren.
  Kein Wissens-Build, keine Zeremonie. Commit nur, wenn Mapping/Content sich ändert.
- **Logik-/Wissens-Update:** Regel-Änderung = Code-Änderung in `pipeline/` (+ betroffene
  Spec-Markdown synchron halten) → commit + push. Tag `vX.Y` bei sinnvollem Meilenstein.

## Gitignored (lokal, nicht im Repo)
`pipeline/.venv/` · `pipeline/outputs/` · `pipeline/EK_input/` · `pipeline/.secrets/` · Secrets.
Die R2-Bilder selbst liegen in Cloudflare (cloud), unabhängig vom Rechner.
