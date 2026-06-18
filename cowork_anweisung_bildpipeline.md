
> **🗄️ DEPRECATED v1.22 — COLD STORAGE.** Diese Cowork-Spec ist seit dem Code-Pivot (v1.22) **nicht mehr der Primärpfad**. Die Artikelanlage läuft als lokaler Code in `pipeline/` (siehe `CLAUDE.md` + `pipeline/README.md`). Dieses Dokument bleibt als **Cowork-Fallback + Historie** erhalten (voller Stand auch im git-Tag `v1.21`). Nicht für die tägliche Arbeit lesen.
> **🗄️ DEPRECATED ab v1.22 (2026-06-15).** Die Bildpipeline läuft jetzt als lokaler Code (`pipeline/images/`, siehe `pipeline/README.md`). Diese Datei ist **historische / Fallback-Referenz für die Cowork-Ausführung** und wird nicht mehr aktiv synchron gehalten — nicht für aktuelle Läufe verwenden.

# Cowork-Anweisung: Bildpipeline polesports

> ## 🟢 AKTIV — reaktiviert mit v1.21 (E93, 2026-05-18)
>
> Die Bildpipeline ist nach E63-Archivierungs-Phase (2026-05-16 bis 2026-05-18) wieder aktiv. **Trigger 2026-05-18:** HotCakes End-to-End-Trial 21:06 (Lauf-Bericht v1.20) hatte 25 Min Wallclock für 21 Modelle — das Token/Wallclock-Verhältnis macht Bilder-Inklusion wirtschaftlich. R2-Architektur (E43), Crop-Profile (E45), Vision-Pose-Sortierung (E45) sind unverändert verfügbar. Mit der Reaktivierung kehrt sich der manuelle Bilder-Pflege-Workflow um.
>
> **Operative Auswirkung:**
> - Stage 5.6 + 5.7 in `cowork_anweisung_datenimports.md` sind **wieder aktiv**.
> - Bild-Spalten 1-10 in der Stammdaten-CSV werden mit R2-URLs befüllt (E46 Mechanik unverändert).
> - Tjorben pflegt Bilder **nicht mehr** manuell in WaWi — Cowork crawlt + verarbeitet + lädt R2 hoch + bettet ein.
> - R2-Bucket-Lifecycle unverändert, Originale + Verarbeitete bleiben unter `<lieferant>/` und `originals/<lieferant>/`.
>
> **Bezug:** E93 (Reaktivierung), E63 (vorherige Archivierung), E43 (R2-Mechanik), E45 (Crop + Pose), E46 (Bilder in Stammdaten-CSV), E87 (Wissens-Resolution via Git), E91 (Cowork-Resolver auf GitHub-Raw).

---


**Version:** v2.1 (Stand 2026-05-18 — Reaktivierung im v1.21-Refactor E93). · **Vorheriger Stand:** v1.6 (Stand 2026-05-15 Abend, dann v2.0 als Stub in v1.20)
**Änderungen ggü. v1.5:**
- **Originalbilder-HTML-Index in R2 (B34, NEU Stage 6.5):** Pro Lieferant generiert Cowork nach jedem Bildpipeline-Lauf eine HTML-Index-Seite unter `originals/<lieferant>/_index.html`. Die Seite listet alle Originale chronologisch (neueste oben) mit Thumbnail-Preview, Dateiname, Upload-Datum und Direkt-Download-Link. Public-URL: `https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev/originals/<lieferant>/_index.html` — dient Tjorbens Social-Media-Bearbeiterin als Ordner-artiger Zugriff.
- **Sekundengenauer Timestamp im Filename:** Filename-Konvention verschärft auf `<base>_<NN>_<LIEFERANT>_<YYYY-MM-DD_HHMMSS>.<ext>` statt `<base>_<NN>_<LIEFERANT>_<YYYY-MM-DD>.<ext>`. Damit funktioniert chronologische Sortierung auch bei mehreren Läufen am selben Tag.
- **Within-Pose-Sortierung formell verankert (B28-Folge, Stage 5.5):** bei mehreren `back`-Aufnahmen → full-body vor crop. Konvention aus den 4 HotCakes-Modellen gewonnen, ab v1.6 Spec.
- **`manufacturer_first_vision_audit` für HotCakes verworfen (B28-Lösung):** mit 1/4 Konsistenz (manuf-Order = pose-sortiert in nur 1 von 4 Modellen) lohnt sich die Audit-Optimierung nicht. Thumbnail-Vision (Faktor 10 Token-Reduktion) bleibt der richtige Pfad.

**Änderungen ggü. v1.4 (Übernahme aus v1.5):**
- **Bildpipeline-Parallelisierung** (E48-Lessons): ThreadPoolExecutor(max_workers=8) ab 8 Bildern.
- **Vision-Klassifikation auf Thumbnails** (E48-Lessons): 384×576-Thumbnail statt Full-Res. Faktor 10 Token-Reduktion.
- **Magic-Byte-Detection als Pflicht:** A2-Pattern unverändert.

**Änderungen ggü. v1.3:**
- **Snapshot-Resolution-Strategie (ab v2.1/E91, ersetzt E47-Drive-Pattern):** Cowork resolved den jüngsten Git-Tag `vX.Y` im Repo `verticalogmbh/polesportshop-wissen` und liest `lieferanten_mapping.yaml` via GitHub-Raw-URL. Details siehe Sektion „Lieferantenkontext" unten und `cowork_custom_instructions.md` v2.0.

**Änderungen ggü. v1.2 (Übernahme aus v1.3):**
- **R2 als vollständiger Bild-Storage** (E44): Originale wandern von Drive (`_Originale/YYYY-MM/`) nach R2 unter Prefix `originals/<lieferant>/`. Drive-Archiv für Originale entfällt; pro Bild werden zwei PUT-Objects (verarbeitetes Shop-Bild + Original) im selben S3-Client-Lauf geschrieben.
- **Crop-Profile pro Produkttyp** (E45): `fashion` (2:3, 1000×1500, top_bias 0.3) für Kleidung, `tech` (1:1, 1200×1200, top_bias 0.0) für Technik. Profil-Auswahl pro Lieferant über das Mapping-Feld `crop_profile`.
- **Vision-basierte Pose-Sortierung für Fashion** (E45): Cowork klassifiziert pro Bild eine von sieben Posen (front/back/side/detail/lifestyle/group/unknown), sortiert die Bild-URLs für die Map-Rückgabe nach Hero-Prioritäten (Bild 1 = front, Bild 2 = back, Bild 3 = side, danach detail/lifestyle/group). Steuerung pro Lieferant über `pose_sort` (`auto_vision` | `manufacturer_order` | `none`).
- **Magic-Byte-Detection** für Original-Extension: URL-Endung und Content-Type-Header sind bei Shopify-CDN-Quellen nicht verlässlich (siehe Anomalie A2 im BACKLOG). Cowork erkennt das echte Format aus den ersten Bytes des Response-Body und benennt entsprechend (z.B. `.jpg` vs. `.webp` vs. `.png`).
- **Output-Format geändert** (E46): Schritt 8 (Bilder-CSV generieren) entfällt. Statt einer Bilder-CSV gibt die Bildpipeline eine Map `{artikelnummer: [bild_urls]}` an die aufrufende Daten-Pipeline zurück. Bei direktem User-Trigger (kein Sub-Process) wird die Map als JSON-Datei im Logs-Ordner abgelegt und im Bericht referenziert.
- **Egress-Allowlist-Workaround** dokumentiert (B29): Pilot-Default ist „All domains" wegen Anthropic-Bug bei „Package managers only" — die Additional-Liste wird in dem Modus silent ignoriert.
- **R2-Lifecycle:** keine Auto-Delete-Regel für `<lieferant>/` oder `originals/<lieferant>/` (E44 — Storage-Kosten vernachlässigbar, ~2 Cent/Monat bei 1,2 GB für 50 Lieferanten). Default-Multipart-Abort nach 7 Tagen bleibt unverändert.

Operative Anweisung für die automatisierte Verarbeitung von Lieferantenbildern für die WaWi-Artikelanlage.

## Zweck

Diese Pipeline verarbeitet eingehende Originalbilder eines Lieferanten und stellt sie für den JTL-Ameise Stammdaten-Import bereit. Pro Bild zwei R2-PUT-Objects: das verarbeitete Shop-Bild (gecroppt, skaliert, komprimiert) unter `<r2_prefix>/<dateiname>.jpg` und das Original (Magic-Byte-Detected) unter `originals/<r2_prefix>/<dateiname>.<orig-ext>`. Für Fashion-Lieferanten wird die Reihenfolge der zurückgegebenen URLs nach Pose sortiert (Bild 1 = Hero-Front, Bild 2 = Rück für Mouse-Hover, Bild 3 = Seite, weitere nach Priorität).

## Trigger

Zwei Auslösungswege:

**A) Direkter User-Trigger** im Chat:

> "Verarbeite Bilder von `<Lieferant>`"
> oder mit explizitem Input:
> "Verarbeite Bilder von `<Lieferant>`, hier `<Quelle>`: `<URLs/Drive-Link/Anhang>`"

Beispiele:
- "Verarbeite Bilder von POLE ADDICT" (Cowork schaut in den `_Eingang`-Drive-Ordner)
- "Verarbeite Bilder von POLE ADDICT, hier die URLs: https://..." (Cowork lädt aus den URLs)
- "Verarbeite Bilder von Lunalae, hier der Drive-Link mit allen Bildern: https://drive.google.com/..." (Cowork holt aus dem Drive-Ordner)

Output bei direktem Trigger: JSON-Map als Logs-Datei plus Markdown-Bericht im Chat.

**B) Sub-Process-Aufruf aus der Daten-Pipeline:**

Wenn `cowork_anweisung_datenimports.md` v2.1 in Stage 5.6 die Bildpipeline aufruft, wird die Map `{artikelnummer: [bild_urls]}` direkt zurückgegeben — kein zusätzlicher User-Trigger nötig. Die Daten-Pipeline bettet die URLs in die Stammdaten-CSV-Spalten `Bild 1` bis `Bild 10` ein (E46). Stage 5.6 + 5.7 sind ab v1.21 (E93) wieder aktiv.

Kein Auto-Trigger und kein Polling. Der Mensch entscheidet bewusst pro Lauf.

## Konfiguration

### Drive-IDs (geteilte Ablage `Artikelanlage Bilder Pipeline`)
- Drive Root: `0AHwtragXAY-wUk9PVA`
- ~~Zentraler `_Originale`-Ordner: `1OutNtX0xmjwPXXOELlA7vflI4SNvpkCg`~~ — wird mit E44 nicht mehr aktiv genutzt (Drive-Originale-Archiv entfällt); Ordner bleibt als historisches Archiv für Originale vor 2026-05-15 stehen, neue Läufe schreiben dorthin nichts mehr
- `_PIPELINE/_Review`: `1NmMRLfPf_DLiSYFFpvryGQa6-eaKgOqA`
- `_PIPELINE/_Logs`: `1s4q8hBMB50p-Ip3tM0-INWVBLZHz6fNt`
- **`_Credentials`** Sub-Ordner mit Permissions nur für Tjorben (kein Sharing). Enthält `r2_credentials.json` (Datei-ID `1r8dSh1qh72ABuFlfjsEXZ8f3W3oWtIXc`).
- Pro Lieferant: aus `lieferanten_mapping.yaml`, Felder `drive_ordner_id` und `drive_eingang_id`

### Cloudflare R2 (S3-kompatibel, vollständiger Storage nach E44)
- Endpoint: `https://d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com`
- Region: `auto`
- Bucket: `polesportshop-images`
- Public Base URL: `https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev`
- **Bucket-Struktur (E44):**
  - `<r2_prefix>/<dateiname>.jpg` — verarbeitete Shop-Bilder (r2_prefix aus `lieferanten_mapping.yaml`)
  - `originals/<r2_prefix>/<dateiname>.<orig-ext>` — Original-Bytes (Extension via Magic-Byte-Detection)
- **R2-Lifecycle (E44):** keine Auto-Delete-Regel auf den Lieferanten-Prefixen. Default-Bucket-Regel „Multipart Abort nach 7 Tagen" bleibt aktiv (Cleanup für hängengebliebene Uploads, kein Object-Delete).

### Upload-Mechanik (E43)

R2-Upload läuft über Code-Execution + boto3 + Drive-File-Credentials. Kein nativer MCP-Connector für Object-Operations.

**Schritte pro Lauf:**

1. **Network-Egress** prüfen: Cowork-Settings → Capabilities → „Additional allowed domains" muss enthalten:
   - `d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com`
   - `pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev`
   - Hersteller-CDN-Domains je Lieferant (z.B. `cdn.shopify.com`)

   **Pilot-Stand (B29):** Allowlist-Modus „All domains" wegen Anthropic-Bug (Issues #38984, #51400 — der granulare „Package managers only"-Modus ignoriert die Additional-Liste silent). Wenn der Modus auf „Package managers only" steht und die granulare Liste nicht greift: Lauf abbrechen, User auf B29-Workaround verweisen.

2. **Bucket-Pre-Check** über Cloudflare Developer Platform Connector (`r2_bucket_get(name='polesportshop-images')`). Bei Fehler: Lauf abbrechen.

3. **Credentials laden** aus Drive-File `_Credentials/r2_credentials.json` (Google Drive Connector → `read_file_content` mit Datei-ID `1r8dSh1qh72ABuFlfjsEXZ8f3W3oWtIXc`). Erwartetes Schema:
   ```json
   {
     "access_key_id": "...",
     "secret_access_key": "...",
     "endpoint": "https://d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com",
     "bucket": "polesportshop-images",
     "region": "auto"
   }
   ```
   Werte als ENV-Vars in die Code-Execution-Sandbox einspeisen — niemals in Chat, Logs, Berichten oder CSVs spiegeln (E33).

4. **boto3 installieren** in der Sandbox (`pip install boto3`).

5. **S3-Client erzeugen** mit den ENV-Vars (Endpoint + Region + Keys).

6. **PUT-Object pro Bild — ZWEIMAL (E44):**
   - **Verarbeitetes Shop-Bild** mit:
     - Key: `<r2_prefix>/<neuer-dateiname>.jpg`
     - ContentType: `image/jpeg`
     - CacheControl: `public, max-age=2592000`
   - **Original-Bytes** mit:
     - Key: `originals/<r2_prefix>/<neuer-dateiname>.<orig-ext>` (orig-ext aus Magic-Byte-Detection)
     - ContentType: passend zum Original-Format (`image/jpeg`, `image/png`, `image/webp`, `image/heic`)
     - CacheControl: `public, max-age=2592000`
   - Bei Fehler: bis zu 3 Retries pro PUT mit Exponential Backoff (1s, 2s, 4s). Dann harter Abbruch.

7. **Public-URL bilden** für die verarbeiteten Bilder als `<Public Base URL>/<r2_prefix>/<dateiname>.jpg` — das ist die URL, die in die Map-Rückgabe wandert.

8. **Sandbox-Cleanup:** ENV-Vars am Ende des Laufs explizit löschen, temporäre boto3-Cache-Files aus `/tmp` entfernen.

**Fallback-Verbot:** Wenn Egress, Bucket-Pre-Check, Credentials oder PUT-Operationen scheitern, bricht der Lauf ab. **Keine** Fallback-Map mit direkten Hersteller-CDN-URLs — die einmalige Übergangslösung aus dem 2026-05-14er Versuch ist mit E43 explizit beendet (siehe E40 in Ablösung).

### Magic-Byte-Detection für Original-Extension (NEU mit E44, Anomalie A2)

URL-Endung ist nicht verlässlich (Shopify-CDN liefert WebP unter `.jpg`-URLs), Content-Type-Header ist auch nicht verlässlich. Vor dem R2-PUT für das Original werden die ersten 12 Bytes des Response-Body geprüft:

| Bytes (Hex) | Format | Extension |
|---|---|---|
| `FF D8 FF` | JPEG | `.jpg` |
| `89 50 4E 47 0D 0A 1A 0A` | PNG | `.png` |
| `52 49 46 46 ?? ?? ?? ?? 57 45 42 50` | WebP (RIFF/WEBP) | `.webp` |
| `00 00 00 ?? 66 74 79 70 68 65 69 63` | HEIC | `.heic` |
| `00 00 00 ?? 66 74 79 70 6D 69 66 31` | HEIF | `.heif` |
| `47 49 46 38 (37\|39) 61` | GIF | `.gif` |

Bei Unbekannt: Fallback auf `.bin`, im Bericht protokollieren.

**Accept-Header beim Download:** Cowork sendet `image/jpeg, image/png, image/webp;q=0.5, */*;q=0.1` damit Shopify-CDN in vielen Fällen ein echtes JPEG liefert statt WebP-Verhandlung.

### Bildverarbeitungsparameter — Crop-Profile (E45)

> **Cap-Enforcement-Hinweis (NEU mit v1.9, E60/B35):** Der 100-KB-Cap pro verarbeitetes Bild ist **verpflichtend**. Im 3-Modell-Pilot-Lauf 2026-05-14 wurden Bilder mit 150-175 KB hochgeladen — Tjorben hat das beim Stammdaten-Import bemerkt. Konsequenz: ab v1.9 muss jeder Lauf-Bericht pro Bild **Final-Quality + Final-Filegröße** ausweisen. Bei Quality-Floor-Hit (Q=30 erreicht und Bild trotzdem > 100 KB): Warnung im Bericht, Lauf nicht abbrechen. Im nächsten v2.0-Bildpipeline-Update wird die Quality-Iteration noch angepasst (Initial 85, Floor 70 als Alternative-Vorschlag aus E60 — Implementierung steht aus). **Bestehende R2-Bilder der 3 Pilot-Modelle (Hekate, Arachne Bottom Teal, Savanna Original Top) müssen beim nächsten Bildpipeline-Lauf re-encodiert werden** — URLs bleiben gleich (R2 überschreibt nach Key), Stammdaten-CSV muss nicht neu generiert werden.

Profil pro Lieferant aus `lieferanten_mapping.yaml`-Feld `crop_profile`:

| Profil | Aspect | Auflösung | top_bias | JPEG-Qualität | Max-Größe | Anwendung |
|---|---|---|---|---|---|---|
| `fashion` | 2:3 (Hochformat) | 1000 × 1500 | 0.3 (Beschnitt bevorzugt unten, Brust/Oberteil bleibt im Frame) | iterativ 95 → 30 | 100 KB | Kleidung, Bodysuits, Tops, Shorts |
| `tech` | 1:1 (Quadrat) | 1200 × 1200 | 0.0 (zentriert, kein Bias) | iterativ 95 → 30 | 100 KB | Pole-Stangen, Zubehör, Hardware |

- Zielformat (verarbeitet): JPEG
- JPEG-Qualität: iterativ von 95 abwärts in 5er-Schritten, bis Größe passt (Mindestqualität 30)
- Bei `top_bias`: HEIC bleibt bei 0.0 (kein Beschnitt von oben) wenn Lieferant Lifestyle/Setting-Shots liefert; Standardbild-Quelle nutzt das Profil-`top_bias`
- LANCZOS-Resampling für die Skalierung
- Default bei fehlendem `crop_profile` im Mapping: `fashion` (häufigster Fall im Pilot)

### Pose-Klassifikation und Sortier-Priorität (NEU mit E45)

Steuerung pro Lieferant über das Mapping-Feld `pose_sort`:

| Wert | Bedeutung |
|---|---|
| `auto_vision` | Cowork klassifiziert mit interner Vision-Capability (Default für Fashion) |
| `manufacturer_order` | Hersteller-Reihenfolge der Bild-URLs ist verlässlich, keine Vision nötig (z.B. wenn Hersteller-CDN semantische Namen wie `_1_front.jpg` liefert) |
| `none` | Keine Pose-Sortierung; Reihenfolge bleibt zufällig (Default für `tech`) |

**Bei `auto_vision`** klassifiziert Cowork jedes Bild in genau eine Kategorie mit Confidence-Score (0.0-1.0):

| Kategorie | Beschreibung |
|---|---|
| `front` | Model frontal, gesamter Look sichtbar (Hero-Aufnahme) |
| `back` | Model von hinten, gesamter Look von der Rückseite |
| `side` | Model im Profil oder 3/4-Ansicht |
| `detail` | Nahaufnahme von Material, Naht, Verschluss, Branding |
| `lifestyle` | Model in Bewegung oder dynamischer Pose, oft Setting |
| `group` | Mehrere Models oder Looks im selben Bild |
| `unknown` | Vision unsicher (Confidence < 0.7), Fallback nötig |

**Sortier-Priorität für die Map-Rückgabe (E45):**
- Bild 1 = `front` (höchste Confidence)
- Bild 2 = `back` (für Mouse-Hover-Image im Shop)
- Bild 3 = `side`
- Bild 4+ = `detail`, `lifestyle`, `group` in dieser Priorität
- Innerhalb derselben Kategorie: sortiert nach Vision-Confidence absteigend

**Fallback bei `unknown`-Klassifikationen:** Cowork hält den Lauf an, meldet die nicht-klassifizierten Bilder mit R2-Public-URL-Vorschau und Confidence-Score an den User. User sortiert manuell ("Bild 2 ist Front, Bild 4 ist Rück"), Cowork übernimmt die Reihenfolge und führt den Lauf zu Ende.

### Dateinamen-Konvention (v1.6 mit Sekunden-Timestamp)

Verarbeitete Bilder (R2) **und Originale** (R2 unter `originals/`):
```
LIEFERANTENARTIKELNUMMER_BILDNUMMER_LIEFERANTENKÜRZEL_YYYY-MM-DD_HHMMSS.<ext>
```

Wichtig: **Sekundengenaue Auflösung** (`HHMMSS`) — damit bei mehreren Läufen am gleichen Tag die chronologische Sortierung sauber funktioniert. Der Timestamp ist der **Lauf-Start-Timestamp** (für alle Bilder eines Laufs identisch), nicht der Bild-spezifische Upload-Timestamp.

Beispiele (v1.6-Stil):
- Verarbeitet: `hotcakes/HC-Arachne-Bottom-Black_01_HOTCAKES_2026-05-15_203045.jpg`
- Original:    `originals/hotcakes/HC-Arachne-Bottom-Black_01_HOTCAKES_2026-05-15_203045.jpg` (Extension via Magic-Byte-Detection)
- POLE ADDICT: `pole-addict/PA-Aria-Black_01_POLE-ADDICT_2026-05-13_141022.jpg`
- Lunalae:     `lunalae/LL-Ramona-Cyan_01_LUNALAE_2026-05-14_091533.jpg`

Bildnummer: zweistellig (01, 02, 03...). Nach Pose-Sortierung ist Bild 01 immer der Hero (front bei `auto_vision`, sonst der erste Treffer aus Quell-Reihenfolge).

**Migration der alten Filename-Konvention:** bestehende Originale ohne `HHMMSS`-Suffix bleiben unverändert (kein Rename in R2). Der Index baut sich aus `LastModified`-Header der R2-Objects, daher funktioniert chronologische Sortierung auch für alte Files.

## Lieferantenkontext

Lieferanten-Metadaten kommen aus `lieferanten_mapping.yaml` im **jüngsten Git-Tag** im Repo `verticalogmbh/polesportshop-wissen`.

**Resolution-Strategie** (ab E91, v1.20, ersetzt das alte Drive-Pattern aus E47):

1. Jüngsten `vX.Y`-Tag via GitHub-API holen: `https://api.github.com/repos/verticalogmbh/polesportshop-wissen/tags`. Falls Repo privat: Auth-Token-Mechanik via Drive-Credentials-File E33, oder Tjorben gibt im Trigger den Tag explizit an.
2. Lade `lieferanten_mapping.yaml` via `https://raw.githubusercontent.com/verticalogmbh/polesportshop-wissen/<tag>/lieferanten_mapping.yaml` mit `web_fetch` oder `curl/requests`.
3. Cache lokal in `/home/claude/wissens_cache/` zusammen mit den Daten-Pipeline-Files (E62 Spec-Caching-Pflicht).
4. **Drive-Übergang als Fallback:** falls GitHub-Raw nicht erreichbar (z.B. Repo privat ohne Auth), nutzt Tjorben den temporären Drive-Folder als Brücke — siehe `cowork_custom_instructions.md` v2.0 für Resolution-Logik.

Schema und Pflichtfelder sind in dem `lieferanten_mapping.yaml` dokumentiert. Cowork resolved den Lieferanten anhand des Anzeigenamens aus dem Trigger und liest:
- `kuerzel`, `r2_prefix`, `drive_eingang_id`, `drive_ordner_id`, `lieferantennummer_wawi`, `shop_url`, `fallback_retailer_url`
- **`category`** (`fashion` / `tech`) — informativ, beeinflusst keine Verarbeitung direkt
- **`crop_profile`** (`fashion` / `tech`) — Auswahl der Bildverarbeitungsparameter
- **`pose_sort`** (`auto_vision` / `manufacturer_order` / `none`) — Sortier-Strategie für die Map-Rückgabe

Wenn ein Lieferant noch nicht im Mapping ist oder Pflichtfelder null sind: halten, beim User nachfragen.

## Anti-Bot-Strategie und Fallback-Reihenfolge

Hintergrund: Shopify-basierte Lieferanten-Shops (HotCakes, Pole Junkie) blocken WebFetch-User-Agents an einzelnen Produktseiten — andere Seiten desselben Shops gehen problemlos durch. Symptom: leerer Response oder Anti-Bot-Challenge-HTML statt Produktdaten. Schema-Erkennung in Cowork: WebFetch liefert <500 Zeichen Body oder enthält Keywords wie `cf-challenge`, `Just a moment`, `Checking your browser`.

**Wichtig (Anomalie A3 im BACKLOG):** Sandbox-Egress-Tunnel-Blocks können sich als Anti-Bot-Treffer tarnen — bei Fehlern erst Egress-Allowlist und Sandbox-Netz prüfen, dann erst Anti-Bot annehmen.

**Fallback-Reihenfolge pro Produktseite:**

1. **Default: WebFetch.** Schneller, kein Credit-Verbrauch. Antwort gegen Anti-Bot-Heuristik prüfen.
2. **Falls Anti-Bot getroffen: Retailer/Hersteller-Alternative (E20).** Wenn `fallback_retailer_url` im Mapping gesetzt ist: dort dasselbe Modell suchen. Bei Hersteller-Site primär blockiert: Retailer-Site probieren; bei Retailer-Site blockiert: Hersteller-Site probieren.
3. **Halt mit User-Klärung.** Im Pilot 2026-05-15 ist Firecrawl-MCP **nicht** als nativer Cowork-Connector verfügbar (E41/B25). Frühere v1.1-Stufe „Firecrawl-MCP über `/v2/scrape`" entfällt damit. Stattdessen: Lauf für diese Produktseite halten, User-Klärung anfordern (manuelle Bild-Beschaffung via Drive `_Eingang` oder einzelne URL liefern oder Produktseite überspringen).

Sobald Firecrawl als Connector verfügbar wird (B25), wird die Stufe wieder eingezogen. Bis dahin: Halt statt Spoofing — kein User-Agent-Faking, kein Proxy-Trick (E21-Geist).

## Prozess

### Schritt 1: Lieferantenkontext laden
- Lieferantenname aus Trigger → Eintrag in `lieferanten_mapping.yaml` finden
- `kuerzel`, `r2_prefix`, `drive_eingang_id`, `shop_url`, `fallback_retailer_url` extrahieren
- **`category`, `crop_profile`, `pose_sort` extrahieren** (E45 — Defaults `fashion`/`fashion`/`auto_vision`)
- Wenn nicht gefunden oder Pflichtfeld null: halten, User fragen

### Schritt 2: Bilder einsammeln

Cowork erkennt aus dem Trigger-Kontext, woher die Bilder kommen:

**Quelle A — Drive `_Eingang`** (Default bei "Verarbeite Bilder von X" ohne weitere Angabe):
- Drive-Inhalt von `<Lieferant>/_Eingang/` listen (über `drive_eingang_id` aus dem Mapping)
- Mime-Types filtern: `image/jpeg`, `image/png`, `image/heif`, `image/heic`
- Bereits verarbeitete Bilder (Prefix `verarbeitet_`) überspringen

**Quelle B — URLs** (User gibt URLs an, oder Aufruf aus Daten-Pipeline mit Bild-URL-Liste):
- Jede URL herunterladen (Content-Type prüfen, max. 20 MB pro Bild). Accept-Header siehe oben.
- Bei Anti-Bot-Treffer beim Download: Fallback-Reihenfolge (siehe oben). Anti-Bot kann auch auf Bild-URLs selbst greifen, nicht nur auf Produktseiten.
- Temporär in Sandbox ablegen für die Verarbeitung
- Bei Crawl-Output: URL kommt aus dem `bild_urls`-Array der Produkt-Extraktion

**Quelle C — Drive-Link** (User gibt Drive-Ordner-/Datei-Link):
- Drive-Tools nutzen, Inhalte listen
- Bilder analog Quelle A behandeln
- **Beachten Anomalie A1 (Drive-MCP-Size-Limit):** Bei großen Files (>~130 KB) kann `download_file_content` an Token-Budget scheitern. Workaround: User-Hinweis, dass das Original direkt auf R2 hochgeladen wird; oder Bilder von Drive nach Sandbox via Code-Execution-S3-Download (Public-Drive-URL) holen, dann verarbeiten.

**Quelle D — Chat-Anhang** (User hängt Bilder direkt in der Nachricht an):
- Anhänge aus dem Chat lesen
- Analog weiterverarbeiten

Wenn Quelle leer / keine Bilder: Lauf abbrechen mit Hinweis "Keine Bilder gefunden, Quelle: `<Quelle>`".

### Schritt 3: Artikeldaten für Matching laden

Hängt von der Bild-Quelle ab:

- **Quelle B + Sub-Process von Daten-Pipeline:** Mapping ist bereits bekannt (Daten-Pipeline liefert pro Artikel die `bild_urls` zusammen mit `lieferantenartikelnummer`). Matching-Stage 4 wird übersprungen.
- **Quelle B/C/D mit explizitem User-Mapping:** User gibt Mapping im Trigger an ("Diese 3 URLs gehören zu PA-Aria-Black"). Matching-Stage 4 wird übersprungen.
- **Quelle A (Drive `_Eingang`) ohne Mapping:** Cowork muss matchen. Lädt dafür aus WaWi (via Datenbank oder Export) alle aktiven Artikel des Lieferanten: Lieferantenartikelnummer, Artikelname, Farbe, Style, Größenvarianten. Dieser Datensatz dient als Referenz für das KI-Vision-Matching in Schritt 4.

### Schritt 4: KI-Vision-Matching (nur wenn Schritt 3 nötig war)
Für jedes Bild aus `_Eingang`:
- Bildinhalt analysieren (Farbe, Style, Form, sichtbare Details)
- Gegen Artikelliste matchen
- Confidence-Score (0-100) berechnen
- Bei mehreren Bildern desselben Artikels: Bildnummer-Vergabe erfolgt erst nach Pose-Sortierung in Schritt 5.5

Confidence-Schwellen:
- ≥90%: automatische Zuordnung
- 70-89%: automatische Zuordnung mit Logging-Eintrag (Hinweis im Bericht)
- <70%: Bild in `_PIPELINE/_Review/` ablegen mit Hinweisdatei (Begründung + Vorschläge), aus Pipeline nehmen

### Schritt 5: Bildverarbeitung (Crop-Profil-getrieben, E45)
Für jedes erfolgreich gematchte Bild:
1. Original aus Drive/URL/Anhang in Sandbox laden
2. **Crop-Profil aus Mapping anwenden** (E45):
   - Aspect-Ratio (2:3 für fashion, 1:1 für tech)
   - top_bias (0.3 für fashion, 0.0 für tech)
   - Bei Bild breiter als Ziel-Aspect → seitlich beschneiden (zentriert)
   - Bei Bild höher als Ziel-Aspect → `top_bias` anwenden
3. Auf Profil-Zielauflösung skalieren (LANCZOS-Filter)
4. Als JPEG mit iterativer Qualitätsreduktion speichern, Ziel <100 KB
5. Bei Qualität ≤30 und immer noch >100 KB: in `_Review` ablegen mit Hinweis "Zielqualität nicht erreicht"

### Schritt 5.5: Pose-Klassifikation und Sortierung (NEU mit E45, nur bei `pose_sort: auto_vision`)

Für jedes verarbeitete Bild pro Artikel:

1. **Thumbnail-Generierung für Vision (v1.5, E48-Lessons):** aus dem Original ein 384×576-JPEG-Thumbnail erzeugen (Pillow, `Image.thumbnail` mit `Image.LANCZOS`). Das Thumbnail wird ausschließlich für den Vision-Call genutzt, nicht für die R2-Ablage. Faktor 10 Token-Reduktion ggü. der vollen 1000×1500-Auflösung ohne nachweisbare Genauigkeits-Einbuße bei Pose-Klassen.

2. **Pose-Klassifikation via Cowork-Vision-Capability:** Thumbnail gegen die 7 Kategorien (front/back/side/detail/lifestyle/group/unknown) klassifizieren mit Confidence-Score.

3. **Fallback auf Full-Res bei kritischer Klassifikation:** wenn Klassifikation `detail` UND Confidence < 0.85 → zusätzlicher Vision-Call mit dem vollen 1000×1500-JPEG. Detail-Aufnahmen können vom Thumbnail aus zu schwer beurteilbar sein (Material-Textur, Schnitt-Details). Bei allen anderen Klassen reicht das Thumbnail.

4. **Pro Artikel:** Bilder nach Sortier-Priorität sortieren — Bild 1 = front (höchste Confidence), Bild 2 = back, Bild 3 = side, dann detail/lifestyle/group in der Priorität, innerhalb gleicher Kategorie nach Confidence absteigend.

5. **Within-Pose-Sortierung (v1.5, B28-Beobachtung):** bei mehreren Bildern derselben Kategorie (z.B. zwei `back`-Aufnahmen — full-body und crop) → **full-body vor crop** sortieren. Konvention aus dem ersten Praxis-Lauf 2026-05-15.

6. **Bei `unknown`-Treffern:**
   - Lauf für diesen Artikel halten.
   - Cowork meldet im Chat: Lieferantenartikelnummer, betroffene Bilder mit Public-URL-Vorschau (nach Verarbeitung schon auf R2), Confidence-Score je Bild.
   - User antwortet mit gewünschter Reihenfolge ("Bild 02 ist Front, Bild 04 ist Rück, Rest egal").
   - Cowork übernimmt die Reihenfolge, vergibt Bildnummern (01, 02, ...) und fährt fort.

7. **Bildnummer-Vergabe nach Sortierung:** zweistellig 01-NN, in der finalisierten Sortier-Reihenfolge.

**Bei `pose_sort: manufacturer_order`:** Reihenfolge der Bild-URLs aus dem Crawl/Drive bleibt erhalten. Bildnummer-Vergabe in dieser Reihenfolge. Keine Vision-Calls — Token-Ersparnis ~100 %.

**Bei `pose_sort: none`:** keine Sortierung, Bildnummer-Vergabe nach Eingangs-Reihenfolge (für Tech akzeptabel).

**Erste-Datenpunkt-Beobachtung 2026-05-15 (B28):** HotCakes Arachne Top Black — 4/4 Bilder klassifiziert ohne `unknown`-Fallback, Confidence-Verteilung 0.80-0.95. Klassifikations-Reihenfolge stimmte mit manueller Erwartung überein. Studio-Hintergrund (neutral grau) ist offenbar entscheidender Marker für `back` vs. `lifestyle`. Dynamische Posen mit erhobenen Armen drücken die Confidence ohne die Klasse zu verschieben.

### Schritt 5.6: Parallel-Execution der Bild-Stages (v1.5, E48-Lessons)

Für Läufe mit ≥8 Bildern (typisch ab 2 Artikeln × 4 Bildern) gelten alle Bild-Verarbeitungs-Stages (Download → Crop+Resize+JPEG-Optimierung → R2-Upload) als parallelisierbar via `ThreadPoolExecutor(max_workers=8)`. Validierte Latenz-Verbesserung: ~110 s sequenziell → ~15 s parallelisiert für 80 Bilder eines 20-Artikel-Laufs.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_one_image(artikelnummer, image_url, crop_profile, r2_prefix):
    # download → magic-byte-detect → crop → resize → JPEG-optimize
    # → R2-PUT verarbeitet + R2-PUT original
    # return URL-pair + metadata
    ...

with ThreadPoolExecutor(max_workers=8) as ex:
    futures = {
        ex.submit(process_one_image, art, url, profile, prefix): (art, idx)
        for art, urls in articles.items()
        for idx, url in enumerate(urls)
    }
    results = {}
    for future in as_completed(futures):
        art, idx = futures[future]
        results.setdefault(art, [])[idx:idx] = [future.result()]
```

**Pose-Klassifikation läuft NACH der parallel-verarbeiteten Bild-Stage** (auf den fertigen verarbeiteten Bildern bzw. ihren Thumbnails), nicht innerhalb des ThreadPool. Grund: Vision-Calls werden vom übergeordneten Cowork-Vision-Tool serialisiert, Parallelisierung würde keinen Latenz-Gewinn bringen.

**HTTP-Connection-Reuse:** innerhalb der Worker-Threads `requests.Session()` statt fresh requests pro Bild — spart TLS-Handshake-Zeit (~30-50 % weniger Download-Zeit pro Bild).

**Bei <8 Bildern** sequenziell verarbeiten — der ThreadPool-Overhead lohnt sich erst bei nennenswerter Bilderzahl.

### Schritt 6: Upload auf Cloudflare R2 — verarbeitet + Original (E43, E44)

Mechanik gemäß Sektion „Upload-Mechanik (E43)" oben, jetzt mit Doppel-PUT pro Bild (E44):
1. Egress-Allowlist + Bucket-Pre-Check vor dem ersten Upload (einmal pro Lauf).
2. Credentials aus Drive-File laden, in ENV-Vars setzen.
3. boto3-S3-Client erzeugen.
4. **Magic-Byte-Detection** für jedes Original bestimmt die Original-Extension.
5. **Pro Bild zwei PUT-Objects:**
   - Verarbeitetes Bild: Key `<r2_prefix>/<dateiname>.jpg`, ContentType `image/jpeg`, CacheControl `public, max-age=2592000`. Bis zu 3 Retries.
   - Original: Key `originals/<r2_prefix>/<dateiname>.<orig-ext>`, ContentType passend zum Magic-Byte-Format, CacheControl `public, max-age=2592000`. Bis zu 3 Retries.
6. Erfolgreiche Uploads in Log aufnehmen; Fehlschläge nach Retry-Limit in `_Review` mit Fehlermeldung.
7. Sandbox-Cleanup am Ende.

**Bei R2-Setup-Ausfall** (fehlende Egress-Allowlist, fehlende Credentials, Bucket-Pre-Check failure) oder bei dauerhaftem Upload-Fehler: Lauf abbrechen. Keine Fallback-Map mit direkten Hersteller-URLs (E40 in Ablösung, B22).

### Schritt 7: ~~Originale archivieren in Drive~~ — entfällt mit E44

Bisherige Drive-Archivierung in `_Originale/YYYY-MM/` entfällt. Originale werden in Schritt 6 direkt auf R2 unter `originals/<r2_prefix>/` hochgeladen — keine zweite Archivierung in Drive nötig.

**Source-spezifisches Cleanup bleibt:**
- Quelle A (Drive `_Eingang`): Original umbenennen mit Prefix `verarbeitet_` (z.B. `verarbeitet_IMG_1156.heic`), nicht löschen
- Quelle B (URLs): keine Aktion nötig, URLs bleiben im Aufrufkontext
- Quelle C (Drive-Link): nicht umbenennen (Lieferanten-Ordner!), keine weitere Aktion
- Quelle D (Chat-Anhang): keine Aktion nötig

### Schritt 8: ~~Bilder-CSV generieren~~ — entfällt mit E46

Bisherige Bilder-CSV (`5_Bilder_<LIEFERANT>_<TS>.csv`) entfällt. Stattdessen wird eine Map zurückgegeben:

**Output-Format der Bildpipeline (Map):**
```python
{
  "HC-Hekate-Bodysuit": [
    "https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev/hotcakes/HC-Hekate-Bodysuit_01_HOTCAKES_2026-05-15.jpg",
    "https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev/hotcakes/HC-Hekate-Bodysuit_02_HOTCAKES_2026-05-15.jpg",
    "https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev/hotcakes/HC-Hekate-Bodysuit_03_HOTCAKES_2026-05-15.jpg"
  ],
  ...
}
```

- Schlüssel: Lieferantenartikelnummer (Vater-Ebene; die Daten-Pipeline dupliziert auf alle Kinder, E34/E46-Stage 5.7)
- Werte: Liste von R2-Public-URLs der verarbeiteten Bilder, in finalisierter Reihenfolge (nach Pose-Sortierung bei `auto_vision`, sonst nach Quell-Reihenfolge)
- Maximal-Länge der Liste: nicht hartkodiert; die Daten-Pipeline schreibt die ersten 10 URLs in die Stammdaten-Spalten `Bild 1` bis `Bild 10`, weitere werden im Bericht protokolliert aber nicht in die CSV übernommen

**Bei direktem User-Trigger** (kein Sub-Process): Map als JSON-Datei in `_PIPELINE/_Logs/<YYYY-MM-DD>_<LIEFERANT>/bilder_map.json` ablegen; im Markdown-Bericht referenzieren.

**Bei Sub-Process-Aufruf aus Daten-Pipeline:** Map als Python-Dict zurückgeben; die Daten-Pipeline persistiert nichts.

### Schritt 8.5: R2-HTML-Index für Bearbeiterin (NEU v1.6, B34)

Cowork generiert nach jedem Pipeline-Lauf eine HTML-Index-Seite unter dem R2-Pfad `originals/<lieferant>/_index.html`. Die Seite dient Tjorbens Social-Media-Bearbeiterin als Ordner-artiger Zugriff auf alle Originale eines Lieferanten, sortiert nach Upload-Datum desc.

**Mechanik:**

1. Cowork listet alle Objekte in R2 unter Prefix `originals/<lieferant>/` via `list_objects_v2` (S3-API), bekommt `LastModified` pro Object
2. Sortiert nach `LastModified` desc (neueste oben)
3. Generiert HTML mit einer Tabelle: Thumbnail-Preview (via Public-URL) + Dateiname + Upload-Datum + Direkt-Download-Link
4. PUT das HTML als `originals/<lieferant>/_index.html` (überschreibt bestehende Version)
5. Public-URL: `https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev/originals/<lieferant>/_index.html`

**HTML-Template (Beispiel-Skelett):**

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>Originale HotCakes — polesportshop</title>
  <style>
    body { font-family: sans-serif; max-width: 1200px; margin: 2em auto; padding: 0 1em; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 0.5em; border-bottom: 1px solid #eee; }
    img { max-width: 150px; max-height: 200px; object-fit: cover; }
    a { color: #b8860b; text-decoration: none; }
  </style>
</head>
<body>
  <h1>Originale HotCakes</h1>
  <p>Stand: 2026-05-15 22:30 — sortiert nach Upload-Datum, neueste zuerst.</p>
  <table>
    <thead><tr><th>Vorschau</th><th>Dateiname</th><th>Upload</th><th>Download</th></tr></thead>
    <tbody>
      <tr>
        <td><img src="HC-Savanna-Sky-Top_01_HOTCAKES_2026-05-15_223045.jpg" loading="lazy"></td>
        <td>HC-Savanna-Sky-Top_01_HOTCAKES_2026-05-15_223045.jpg</td>
        <td>2026-05-15 22:30</td>
        <td><a href="HC-Savanna-Sky-Top_01_HOTCAKES_2026-05-15_223045.jpg" download>↓</a></td>
      </tr>
      ... (alle Files chronologisch sortiert)
    </tbody>
  </table>
</body>
</html>
```

**Wichtig zur Cache-Steuerung:** beim PUT der `_index.html` den Header `Cache-Control: no-cache, must-revalidate` setzen, damit die Bearbeiterin immer den aktuellen Stand sieht ohne Browser-Cache-Probleme.

**Performance:** R2-LIST mit Prefix-Filter ist eine Einzeloperation (~50ms), HTML-Generation in Python <1s, R2-PUT <200ms. Gesamt-Stage <1s pro Lieferant.

### Schritt 9: Ergebnisbericht
Markdown-Bericht in `_PIPELINE/_Logs/run_<YYYY-MM-DD_HHMM>_<lieferant>.md` mit:
- Lieferant, Zeitstempel, Crop-Profil, Pose-Strategie
- Anzahl Bilder im Eingang
- Anzahl erfolgreich verarbeitet (Vater-Ebene, da Daten-Pipeline auf Kinder dupliziert)
- **Pose-Klassifikations-Statistik (bei `auto_vision`):** Verteilung über Kategorien, Anzahl `unknown`-Fälle und User-Korrekturen
- Anzahl in Review-Queue (mit Gründen)
- Anzahl Fehler
- Pfad zur generierten Map-JSON (bei direktem Trigger)
- Confidence-Score-Verteilung (Matching + Pose)
- R2-Upload-Statistik: Erfolge / Retries / Fehler, getrennt nach „verarbeitet" und „original"
- **Magic-Byte-Detection-Statistik:** wie viele Originale wurden als jpeg / png / webp / heic / unknown erkannt
- Fallback-Statistik (wie viele Bilder über WebFetch, wie viele über Retailer-Fallback, wie viele in Halt gelaufen)
- **Credentials-Footprint:** Bestätigung, dass keine Credential-Werte in Logs/Bericht/Map/Chat aufgetaucht sind

Zusammenfassung im Chat ausgeben mit:
- 1-Satz-Status ("✅ 24 Bilder verarbeitet" oder "⚠️ 20 erfolgreich, 4 in Review, 2 unknown-pose")
- Bei direktem Trigger: Link zur generierten Map-JSON
- Bei Sub-Process-Aufruf: Übergabe der Map an die Daten-Pipeline

## Fehler-Handling

| Situation | Verhalten |
|---|---|
| Keine Bilder in `_Eingang` | Lauf abbrechen, kurzer Hinweis im Chat |
| Lieferantenname nicht in `lieferanten_mapping.yaml` | Lauf abbrechen, Liste verfügbarer Lieferanten zeigen |
| Pflichtfelder im Mapping sind null | Halten, beim User die fehlenden Werte abfragen |
| **`crop_profile` / `pose_sort` fehlen** | Defaults `fashion`/`auto_vision` annehmen, im Bericht warnen |
| WaWi-Daten nicht verfügbar | Lauf abbrechen, technischen Fehler melden |
| **Network-Egress nicht für R2-Domains freigeschaltet** | Lauf abbrechen, User auf Settings → Capabilities verweisen (siehe B29 zum „All domains"-Workaround) |
| **`_Credentials/r2_credentials.json` nicht lesbar oder Schema falsch** | Lauf abbrechen, User auf Drive-File-Setup verweisen |
| **Bucket-Pre-Check (`r2_bucket_get`) schlägt fehl** | Lauf abbrechen, Cloudflare-Connector-Status prüfen |
| R2-Upload (verarbeitet ODER original) fehlschlägt nach 3 Retries | Lauf abbrechen — kein CDN-Fallback. Im Bericht protokollieren. |
| **Magic-Byte-Detection liefert `unknown` für Original** | Original mit `.bin`-Extension hochladen, im Bericht protokollieren, Lauf nicht abbrechen |
| Anti-Bot-Treffer bei WebFetch | Fallback-Reihenfolge starten (siehe oben), Anomalie A3 beachten |
| Anti-Bot bleibt nach Retailer/Hersteller-Stufe | Halt mit User-Klärung (Firecrawl-Stufe im Pilot nicht verfügbar, E41/B25) |
| **Pose-Klassifikation `unknown` für Bild bei `auto_vision`** | Lauf halten, User für manuelle Sortierung anfragen, mit fixierter Reihenfolge weiterfahren |
| Einzelnes Bild matcht <70% | In `_Review` ablegen, mit Pipeline weiter (kein Abbruch) |
| Bildverarbeitung fehlschlägt (z.B. korruptes Bild) | In `_Review` ablegen mit Fehlermeldung, mit Pipeline weiter |
| **Drive-MCP `download_file_content` schlägt mit Token-Overflow fehl** | Anomalie A1: Workaround via Code-Execution-Download über Public-Drive-URL, oder User-Hinweis dass Bild manuell ins `_Eingang` gelegt werden muss |

## Konventionen & Regeln

### Was Cowork DARF
- Ordner anlegen, Dateien anlegen, Dateien kopieren, Dateien umbenennen (durch copy + neuer Titel)
- R2-Uploads über Code-Execution + boto3 mit Credentials aus dem Drive-File (E43), zwei PUTs pro Bild (verarbeitet + original, E44)
- Cloudflare Developer Platform Connector für Bucket-Pre-Checks (`r2_bucket_get`)
- Interne Vision-Capability für Pose-Klassifikation nutzen (E45)
- WaWi lesen
- Map als Sub-Process-Return-Wert an aufrufende Daten-Pipeline weitergeben (E46)
- `lieferanten_mapping.yaml` lesen
- `_Credentials/r2_credentials.json` lesen (im Rahmen der Upload-Mechanik)

### Was Cowork NICHT DARF
- Dateien permanent löschen (auch nicht im Papierkorb)
- WaWi schreibend ändern (Ameise-Import macht der User)
- Berechtigungen verändern (Drive-Sharing, Bucket-Permissions, `_Credentials`-Ordner-Permissions)
- Neue Lieferantenordner ohne explizite Anweisung anlegen
- `lieferanten_mapping.yaml` ohne explizite User-Bestätigung erweitern
- R2-Bucket-Konfiguration ändern (auch nicht via Cloudflare-Connector — der ist read/lifecycle, kein Config-Wrencher)
- R2-Lifecycle-Regel für `<lieferant>/` oder `originals/<lieferant>/` anlegen oder ändern (E44 — keine Auto-Delete)
- Bilder-Map mit direkten Hersteller-CDN-URLs ausliefern, wenn R2-Upload nicht funktioniert hat (E40 in Ablösung, hartkodiert in der Validierung der Daten-Pipeline Stage 6)
- User-Agent-Spoofing oder andere Anti-Bot-Umgehungsversuche
- Credential-Werte (Access Key, Secret) in Logs, Berichten, Maps oder Chat-Output spiegeln (E33)
- API-Keys aus Chat-Inputs akzeptieren oder als Trigger-Parameter setzen lassen

### Idempotenz
- Wird derselbe Lauf mehrfach getriggert, soll nichts kaputtgehen
- Bereits hochgeladene Bilder auf R2 werden überschrieben (gewollt — neuere Version, gilt für verarbeitete und Originale)
- Bereits verarbeitete Originale in `_Eingang` erkennen am `verarbeitet_`-Prefix und überspringen
- Doppelte Einträge in der Map vermeiden (eindeutig pro Artikelnummer × Bildnummer)

## Zukunfts-Pfade (Beobachtung, nicht jetzt umsetzen)

- **B26 — Cloudflare-Code-Mode-MCP** (`mcp.cloudflare.com/mcp` mit `search()`+`execute()`-Tools, deckt R2-Object-Ops via JavaScript-Snippets ab). Falls in der Anthropic-Cowork-Registry verfügbar wird: Schritt 6 könnte vollständig auf den Connector umziehen, boto3-Sandbox-Mechanik entfällt.
- **B27 — Cloudflare-Worker-Proxy.** Wenn die Pipeline auf >5 Lieferanten oder Multi-User skaliert: Worker mit R2-Binding aufsetzen, Cowork ruft Worker mit Bearer-Token. R2-Credentials leben dann nur im Worker, nicht mehr in Drive.
- **B25 — Firecrawl als nativer Cowork-Connector.** Sobald in der Registry: Anti-Bot-Fallback-Stufe „Firecrawl /v2/scrape" wieder einziehen, vor „Halt mit User-Klärung".
- **B28 — Vision-Klassifikations-Verifikation.** Erster echter Fashion-Lauf mit Pose-Sortierung verifiziert die Klassifikations-Genauigkeit; bei systematischen Fehlern Klassifikations-Prompt schärfen oder Default-Strategie umstellen.
- **B29 — Anthropic-Allowlist-Bug.** Beobachten, ob „Package managers only" + Additional-Liste in einer kommenden Anthropic-Version wieder funktioniert; dann granularen Modus reaktivieren.
- **B30 — Re-Import-Verhalten bei leeren Bild-Spalten.** Stammdaten-Re-Import mit weniger als 10 Bildern testen, JTL-Verhalten verifizieren.

## Verwandte Dokumente

- `cowork_anweisung_datenimports.md` v1.5 — operative Anweisung für die parallele Daten-Pipeline; ruft die Bildpipeline programmatisch in Stage 5.6 auf
- `lieferanten_mapping.yaml` — Single Source of Truth Lieferanten-Metadaten (jetzt mit `category`/`crop_profile`/`pose_sort`)
- `WAWI-IMPORT-WISSEN.md` — operatives Pilot-Wissen (Stammdaten-Schema mit Bild-Spalten, Mapping-Detail)
- `ENTSCHEIDUNGS-LOG.md` — E10-E12 (Bilder-Pipeline), E19/E34 (Erbung-Verbot), E20 (Hersteller bevorzugen), E24 (Konfig-Auslagerung), E29 (Vorlagen-Naming, jetzt 4 Vorlagen), E33 (Credential-Mechanismen), E40 (CDN-URLs in Ablösung), E41 (Crawl-Tool-Marktcheck), E42 (Local MCP Bridge tot), E43 (R2-Upload-Mechanik), E44 (R2 vollständiger Storage), E45 (Crop-Profile + Pose-Sortierung), E46 (Bilder in Stammdaten, Output-Format Map)
- `BACKLOG.md` — B5 GELÖST (Plattform-Aktivierung über E46), B16 (Cloud-Storage-Connector), B22 TEILGELÖST (R2-Migration Arachne Bottom Black erfolgreich), B23 (MCP-Connector-Inventur erledigt), B25 (Firecrawl-Registry beobachten), B26 (Cloudflare-Code-Mode beobachten), B27 (Worker-Proxy als Reserve), B28 (Vision-Klassifikations-Verifikation), B29 (Allowlist-Bug-Tracker), B30 (Re-Import-Verhalten bei leeren Bild-Spalten)
