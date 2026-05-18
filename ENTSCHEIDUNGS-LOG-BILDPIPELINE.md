# ENTSCHEIDUNGS-LOG-BILDPIPELINE

**Cluster:** Bilder, R2-Storage, Crop, Pose, Vision — **reaktiviert mit E93 (v1.21, 2026-05-18)**, vorher archiviert seit E63 (2026-05-16)

**Stand:** v1.18, 2026-05-18 (neuer Eintrag E93: Bildpipeline reaktiviert, kehrt E63 um). · **Vorheriger Stand:** v1.17, 2026-05-17

**Bezug:** Dieser Cluster ist Teil des Splits der ursprünglichen `ENTSCHEIDUNGS-LOG.md` (v1.16, 165 KB → 6 Themen-Cluster ≤ 40 KB). Historische / abgelöste Einträge liegen weiterhin in `ENTSCHEIDUNGS-LOG-ARCHIV.md`. Cross-Cluster-Referenzen über E-Nummer; der Master-Index mit allen E-Nummern → Cluster-File-Zuordnung liegt in `SPEC_KONSTANTEN.md` unter `ENTSCHEIDUNGSLOG_E_NUMMER_INDEX`.

---

## Index

- **E10** — Cloudflare R2 für Bild-Hosting, Ameise-URL-Import
- **E11** — 2:3-Format, 1000×1500, JPEG <100 KB (Default-Profil, jetzt unter dem Namen `fashion`)
- **E12** — Bild-Pipeline separat aber als Sub-Process aufrufbar
- **E44** — R2 als vollständiger Bild-Storage: Originale wandern von Drive nach R2
- **E45** — Crop-Profile pro Produkttyp und Vision-basierte Pose-Sortierung für Fashion
- **E46** — Bilder integriert in Stammdaten-CSV, separater Bilder-Import abgeschafft
- **E60** — Bild-Größen-Cap < 100 KB im JPEG-Encoding mit Quality-Iteration und Floor
- **E63** — Bildpipeline archiviert, manueller Bilder-Workflow im Pilot — **REVERTIERT durch E93**
- **E70** — Feature-Erfassung text-basiert, Vision-API-Extraktion bewusst aufgeschoben
- **E93** — Bildpipeline reaktiviert (kehrt E63 um), NEU v1.21

---

**E10 — Cloudflare R2 für Bild-Hosting, Ameise-URL-Import.**
*Warum:* Stabile Public-URLs, schnelles CDN, niedrige Kosten, keine Auth-Komplexität.
*Verworfen:* Bilder direkt in JTL hochladen (lange Upload-Zeiten, keine externe URL für Re-Import). Drive-Shares (URLs instabil, nicht direkt embeddbar).
*Erweiterung 2026-05-15 (E44):* R2 ist jetzt vollständiger Bild-Storage — auch die Original-Bytes liegen auf R2 (Prefix `originals/<lieferant>/`) statt im Drive-Archiv. Begründung in E44.

**E11 — 2:3-Format, 1000×1500, JPEG <100 KB (Default-Profil, jetzt unter dem Namen `fashion`).**
*Warum:* Konsistenz im Shop, Performance, Bandbreite.
*Verworfen:* Originale 1:1 durchreichen (heterogene Formate, große Files).
*Erweiterung 2026-05-15 (E45):* Crop-Profile sind jetzt produkttyp-spezifisch — `fashion` (2:3, 1000×1500, top_bias 0.3) für Kleidung, `tech` (1:1, 1200×1200, top_bias 0.0) für Technik. Profil-Auswahl pro Lieferant über das Feld `crop_profile` im Lieferanten-Mapping. Begründung in E45.

**E12 — Bild-Pipeline separat aber als Sub-Process aufrufbar.**
*Warum:* Bilder können separat anfallen (Update vom Lieferanten ohne Daten-Änderung), aber typischerweise im Daten-Pipeline-Lauf mitgeneriert.
*Verworfen:* Bilder in Daten-Pipeline integriert (Monolith, nicht separat triggerbar).
*Klarstellung 2026-05-15 (E46):* Die Bildpipeline bleibt als separater Sub-Process bestehen — sie ist eigenständig triggerbar. Ihr Output ändert sich aber: statt einer eigenen Bilder-CSV gibt sie eine `{artikelnummer: [bild_urls]}`-Map zurück, die die Daten-Pipeline in die Stammdaten-CSV einbettet. Die Trennung der Pipelines bleibt, das Übergabe-Format ändert sich.

**E44 — R2 als vollständiger Bild-Storage: Originale wandern von Drive nach R2.**
*Stand:* 2026-05-15. Bezug: E10, E43.
*Warum:* Bei der HotCakes-Arachne-Bottom-Black-Migration 2026-05-15 stießen wir an das Größen-Limit der Drive-MCP-`download_file_content`-Toolchain: JPEG-Originale zwischen 130 und 500 KB sprengten das Token-Budget der Drive-Connector-Calls, weil die Datei base64-codiert in den Tool-Response geladen wird. Workaround „Drive-Connector durch Code-Execution + boto3-S3-Download via Public Drive-URL" wäre wieder eine eigene Mechanik nur fürs Original-Holen.

Die saubere Lösung: Originale gehen direkt nach R2, im selben Bucket unter dem Prefix `originals/<lieferant>/`. Cowork verarbeitet pro Bild gleichzeitig zwei PUT-Objects (verarbeitetes Shop-Bild + Original) im selben S3-Client-Lauf. Der Drive-Ordner `_Originale/` entfällt als Archiv-Ziel.

*Operative Konsequenzen:*
- **Bucket-Struktur erweitert:**
  - `<r2_prefix>/<dateiname>.jpg` — verarbeitete Shop-Bilder (bisher, unverändert)
  - `originals/<r2_prefix>/<dateiname>.<original-ext>` — Original-Bytes (neu)
- **Magic-Byte-Detection** für Original-Extension (siehe Bildpipeline-Spec): URL-Endung ist nicht verlässlich (Shopify-CDN liefert WebP unter `.jpg`-URLs), Content-Type-Header ist auch nicht verlässlich. Cowork erkennt das echte Format aus den ersten Bytes des Response-Body und benennt entsprechend.
- **R2-Lifecycle: keine Auto-Delete-Regel** für `<lieferant>/` oder `originals/<lieferant>/`. Storage-Kosten sind vernachlässigbar (~2 Cent/Monat bei 1,2 GB für 50 Lieferanten, R2-Tarif 0,015 USD/GB/Monat). Default-Bucket-Regel „Multipart Abort nach 7 Tagen" bleibt unverändert (Cleanup für hängengebliebene Uploads, kein Object-Delete).
- **Drive-Cleanup:** der Drive-Ordner `_Originale/2026-05/` (Drive-ID `1sigN8duqOgfHZvoF8nnf2yxR_QmsrciZ`) ist leer und kann von Tjorben gelöscht werden. Der übergeordnete `_Originale/`-Root-Ordner (`1OutNtX0xmjwPXXOELlA7vflI4SNvpkCg`) kann als historisches Archiv stehen bleiben — neue Läufe schreiben nicht mehr dorthin.

*Validierung:* HotCakes-Arachne-Bottom-Black-Migration 2026-05-15: alle 4 Originale erfolgreich auf R2 unter `originals/hotcakes/HC-Arachne-Bottom-Black_NN_HOTCAKES_2026-05-15.jpg` (alle als JPEG erkannt — Magic-Byte-Detection hat aus dem Shopify-Response echte `image/jpeg`-Bytes geholt, weil der zweite Lauf einen anderen Accept-Header schickte). Drive-Workspace-Folder `_Originale_pending_2026-05-15_hotcakes/` wurde geleert.

*Verworfen:*
- *Drive als Originale-Archiv beibehalten* — Drive-MCP-Size-Limit blockt die Pipeline, plus Doppel-Wartung von zwei Storage-Pfaden.
- *Originale nicht archivieren* — verliert die Audit-Spur, im Schadensfall (verlorene Bilder, falsche Verarbeitung) kein Rollback-Material.
- *Originale auf R2 mit kurzer Lifecycle-Regel (z.B. 90 Tage)* — Storage-Kosten so niedrig, dass Auto-Delete nur Komplexität ohne Mehrwert bringt. Wenn später Budget-Druck entsteht, kann eine Lifecycle-Regel nachgezogen werden.

*Folgeaufgaben:* keine — Mechanik ist mit dem Arachne-Bottom-Black-Lauf validiert. Restliche HotCakes-Artikel (Hekate Bodysuit + Arachne Top Black) durchlaufen denselben Pfad sobald Bild-Beschaffung läuft (B22 teilgelöst).

**E45 — Crop-Profile pro Produkttyp und Vision-basierte Pose-Sortierung für Fashion.**
*Stand:* 2026-05-15. Bezug: E11, E12.
*Warum:* Im HotCakes-Pilot 2026-05-15 hat sich gezeigt: das Default-Crop-Profil (2:3, 1000×1500) ist passend für Fashion-Produkte (Models im Hochformat, Brust/Oberteil als Fokus), aber nicht für Technik-Artikel (Pole-Stangen, Hardware, Zubehör — meist symmetrisch zentriert, kein „oben/unten"-Bias). Plus: die Sortierung der Bilder pro Artikel ist für Fashion verkaufsfördernd, weil der Shop ein Mouse-Hover-Image automatisch als zweites Bild anzeigt — Front → Rück → Seite ist Convention bei modernen Fashion-Shops.

*Crop-Profile (Definitionen in cowork_anweisung_bildpipeline.md v1.3):*

| Profil | Aspect | Auflösung | top_bias | Anwendung |
|---|---|---|---|---|
| `fashion` | 2:3 (Hochformat) | 1000×1500 | 0.3 (Beschnitt bevorzugt unten, Brust/Oberteil bleibt im Frame) | Kleidung, Bodysuits, Tops, Shorts |
| `tech` | 1:1 (Quadrat) | 1200×1200 | 0.0 (zentriert, kein Bias) | Pole-Stangen, Zubehör, Hardware |

Profil-Auswahl pro Lieferant über das neue Feld `crop_profile` im `lieferanten_mapping.yaml`. Default bei unbekanntem Lieferant: `fashion` (häufiger im Pilot).

*Pose-Sortierung für Fashion (Cowork-Vision-Mechanik):*

Cowork klassifiziert jedes Bild über interne Vision-Capability in genau eine Kategorie:

| Kategorie | Beschreibung |
|---|---|
| `front` | Model frontal, gesamter Look sichtbar (Hero-Aufnahme) |
| `back` | Model von hinten, gesamter Look von der Rückseite |
| `side` | Model im Profil oder 3/4-Ansicht |
| `detail` | Nahaufnahme von Material, Naht, Verschluss, Branding |
| `lifestyle` | Model in Bewegung oder dynamischer Pose, oft Setting |
| `group` | Mehrere Models oder Looks im selben Bild |
| `unknown` | Vision unsicher (Confidence < 0.7), Fallback nötig |

Sortier-Priorität:
- Bild 1 = `front` (höchste Confidence)
- Bild 2 = `back` (für Mouse-Hover-Image im Shop)
- Bild 3 = `side`
- Bild 4+ = `detail`, `lifestyle`, `group` in dieser Priorität
- Innerhalb derselben Kategorie: sortiert nach Vision-Confidence absteigend

Bei `unknown`-Klassifikation oder Vision-Versagen: Cowork hält den Lauf an und meldet die nicht-klassifizierten Bilder mit R2-Public-URL-Vorschau an den User. User sortiert manuell, Cowork übernimmt die Reihenfolge.

*Pose-Strategie pro Lieferant (neues Feld `pose_sort` im Mapping):*

| Wert | Bedeutung |
|---|---|
| `auto_vision` | Cowork klassifiziert mit Vision (Default für Fashion) |
| `manufacturer_order` | Hersteller-Reihenfolge der Bild-URLs ist verlässlich, keine Vision nötig |
| `none` | Keine Pose-Sortierung (Default für Tech) |

*Konsequenzen:*
- `lieferanten_mapping.yaml` bekommt drei neue Felder pro Lieferant: `category`, `crop_profile`, `pose_sort`. Default-Werte für die bestehenden Lieferanten (HotCakes, POLE ADDICT, Lunalae): `category: fashion`, `crop_profile: fashion`, `pose_sort: auto_vision`.
- Cowork-Bildpipeline-Stage 5 (Bildverarbeitung) liest pro Lauf das Profil aus dem Mapping und wendet entsprechende Crop-Parameter an.
- Cowork-Bildpipeline-Stage 5.5 (NEU) führt die Pose-Klassifikation und Sortierung nur durch, wenn `pose_sort: auto_vision`. Bei `manufacturer_order` wird die ursprüngliche Reihenfolge aus dem Crawl/Drive übernommen. Bei `none` bleibt die Reihenfolge zufällig (für Tech akzeptabel).

*Validierung:* Spec-Niveau, Praxis-Validierung folgt mit dem nächsten Fashion-Lieferanten-Lauf (B28).

*Verworfen:*
- *Einheits-Crop-Profil über alle Produkttypen* — würde Technik im Hochformat ungünstig zuschneiden.
- *Hersteller-Reihenfolge der Bilder universell vertrauen* — funktioniert nur, wenn Hersteller-CDN-URLs semantisch sind (z.B. `_1_front.jpg`), bei generischen IDs nicht.
- *Pose-Klassifikation per ML-Modell-Training* — Overengineering im Pilot. Coworks interne Vision-Capability reicht für die wenigen Kategorien.
- *Manuelle Sortierung als Default* — bricht Pipeline-Automation, würde pro Artikel manuelle Intervention erzwingen.

*Folgeaufgaben:* B28 (Vision-Klassifikations-Verifikation in der Praxis — wie gut funktioniert die Klassifikation für unsere Lieferanten, welche Edge-Cases tauchen auf, ab welcher Unsicherheits-Schwelle pausiert Cowork sinnvoll).

**E46 — Bilder integriert in Stammdaten-CSV, separater Bilder-Import abgeschafft.**
*Stand:* 2026-05-15. Bezug: E5, E10, E12, E29, E34, E40.
*Warum:* Der HotCakes-Arachne-Bottom-Black-Migration-Lauf 2026-05-15 hat den separaten Bilder-Import-Pfad durchgespielt — und drei Schreibversuche an strukturellen JTL-Grenzen scheitern lassen:

- **Versuch 1 — Drei-Spalten-CSV** `Artikelnummer;Bildnummer;Bild-URL`, 20 Zeilen (5 Artikel × 4 Bilder), Import-Typ „Artikelbilder pro Plattform". Ergebnis: alle 4 Bilder am Artikel angehängt, aber nur das letzte Bild (Slot 4) bekam Plattform-Aktivierung. JTL interpretiert mehrere Zeilen pro Artikel auf demselben Slot-Mapping als „zuletzt geschriebene Zeile gewinnt".
- **Versuch 2 — Workaround mit separater Verknüpfungs-CSV** `_6_BilderVerknuepfung` via Import-Typ „Artikelbild verknüpfen", Quellplattform → Zielplattform „Alle". Ergebnis: weil aus Versuch 1 nur 1 von 4 Bildern auf der Quellplattform aktiviert war, hat „Artikelbild verknüpfen" auch nur 1 Bild auf alle Plattformen verknüpft. Workaround skaliert nicht.
- **Versuch 3 — Manuelle „Alle aktivieren"-Klicks pro Bild pro Artikel** — funktioniert, aber 4 Klicks pro Artikel × 50 Artikel = 200 Klicks pro Lauf, blockiert die End-to-End-Automation.

Saubere Lösung kam aus der JTL-Doku selbst (E22-recherchiert): *„Falls die Bilder auf allen Plattformen gleich sein sollen, können Sie diese als zusätzliche Spalte im Rahmen des Artikeldaten-Imports zuweisen."* Bei polesportshop sind alle Bilder immer für alle 11 Plattformen gleich — exakt der dokumentierte Anwendungsfall.

*Operative Definition:*

- **Stammdaten-CSV bekommt 10 Bild-Spalten am Ende:** `Bild 1; Bild 2; ...; Bild 10`. Default-Anzahl 10 deckt 95%+ der Produkte ab (Fashion typisch 3-6 Bilder, Technik typisch 1-3, JTL unterstützt bis 20 — 10 ist konservativer Puffer mit Reserve nach oben).
- **Cowork-Logik:** Stammdaten-CSV pro Lauf immer mit den fixen 10 Bild-Spalten ausgeben. Leere Strings bei Artikeln mit weniger Bildern. Vorlage in JTL-Ameise wird einmalig pro Lieferant konfiguriert (`Bild 1` → `Bild Pfad/URL 1`, ..., `Bild 10` → `Bild Pfad/URL 10`) und im Reiter „Bilder/Plattformen" werden alle 11 Plattform-Häkchen gesetzt.
- **Plattform-Aktivierung automatisch:** beim Stammdaten-Import setzt JTL für jedes Bild in den Spalten die Häkchen aller in der Vorlage konfigurierten Plattformen. Kein nachgelagerter Aktivierungs-Schritt mehr nötig — B5 löst sich von alleine.
- **Pipeline-Stages-Reduktion:** Pipeline geht von 5 zurück auf 4 CSVs. Separate Bilder-CSV (`5_Bilder_…`) entfällt, Verknüpfungs-CSV (`6_BilderVerknuepfung_…`) entfällt. Übrig: Stammdaten (inkl. Bildern), Variationen, Merkmale, Attribute.
- **Bildpipeline-Output-Format ändert sich:** statt einer Bilder-CSV gibt die Bildpipeline jetzt eine Map `{artikelnummer: [bild_url_1, bild_url_2, ...]}` an die Daten-Pipeline zurück, die sie in die Stammdaten-CSV-Spalten einbettet. Die Bildpipeline bleibt als eigenständiger Sub-Process bestehen (E12 unverändert), das Übergabe-Format ändert sich.
- **Vater-Kind-Konsistenz (E34) bleibt erhalten:** jeder Artikel (Vater UND jedes Kind) bekommt eine eigene Stammdaten-Zeile mit identischen Bild-URLs in den Spalten. Die Bild-Spalten werden also pro Zeile (Vater UND alle Kinder) gefüllt, mit denselben URLs.

*Validierung:* HotCakes-Arachne-Bottom-Black-State-Run 2026-05-15: Mini-Stammdaten-CSV mit 5 Zeilen (Vater + 4 Kinder) × 5 Spalten (Artikelnummer + Bild 1-4) re-importiert, alle 4 Bilder auf allen 9 Plattform-Häkchen gesetzt ohne weiteres Klicken. Sauber funktional.

*Konsequenzen für bestehende Specs:*
- `cowork_anweisung_datenimports.md` v1.5 (2026-05-15): Pipeline auf 4 Stages reduziert, Stammdaten-Schema v3 mit 48 Spalten (38 + 10 Bilder).
- `cowork_anweisung_bildpipeline.md` v1.3 (2026-05-15): Output-Format auf Map umgestellt, Schritt 8 (Bilder-CSV generieren) entfällt.
- `WAWI-IMPORT-WISSEN.md` (2026-05-15): Abschnitt 7 vollständig neu gefasst — kein separater Bilder-Import, Bilder via Stammdaten-Import.
- `lieferanten_mapping.yaml`: Ameise-Vorlagen-Block bekommt 4 Felder statt 5 (bilder entfällt).
- BACKLOG B5 (Plattform-Aktivierung): GELÖST durch E46.

*Verworfen:*
- *Pattern A (horizontale Bilder-CSV mit eigenständigem „Artikelbilder pro Plattform"-Import)* — funktioniert technisch, aber redundant: wenn Bilder eh über die Stammdaten-CSV laufen, ist ein eigenständiger Bilder-Import nicht nötig.
- *Dynamische Spalten-Anzahl pro Lauf (nur so viele wie tatsächlich Bilder da)* — würde die Ameise-Vorlage pro Lauf brechen, da die Spalten-Anzahl in der Vorlage hartkodiert ist. 10 fixe Spalten mit Leer-Strings ist robuster.
- *Separater Bilder-Import als „Korrektur-Import" für Edge-Cases (z.B. Bild-Updates ohne Daten-Änderung)* — kann bei Bedarf später wieder eingeführt werden, ist im Pilot aber nicht nötig. Wenn ein Bild ersetzt werden muss: Mini-Stammdaten-CSV mit `Artikelnummer; Bild N` als Re-Import.

*Stolperfalle (UNVERIFIZIERT):* Re-Import-Verhalten bei leeren Bild-Spalten ist noch nicht final geklärt — wenn ein Re-Import nur die ersten 3 Bild-Spalten gefüllt hat und 4-10 leer, gibt es zwei mögliche JTL-Verhalten:
- *Verhalten A (gewünscht):* Leerer Wert = kein Update, vorhandenes Bild im Slot bleibt erhalten
- *Verhalten B (problematisch):* Leerer Wert = Slot wird aktiv geleert, vorhandenes Bild verschwindet

In der JTL-Doku nicht eindeutig dokumentiert. Verifikation pending mit einem Lauf, der weniger als 10 Bilder hat (B30).

*Folgeaufgaben:*
- *B5 (Plattform-Aktivierung):* GELÖST durch E46.
- *B22 (R2-Migration):* TEILGELÖST für Arachne Bottom Black mit E46-Mechanik; restliche HotCakes-Artikel (Hekate + Arachne Top Black) folgen sobald Bild-Beschaffung wieder läuft.
- *B30 (NEU):* Re-Import-Verhalten bei leeren Bild-Spalten verifizieren.
- *Migration POLE ADDICT:* POLE-ADDICT-Stammdaten-Vorlage muss um Bild-Spalten erweitert werden, alte Bilder-CSV-Vorlage (`POLE ADDICT Bilder Import`) wird Legacy.

**E60 — Bild-Größen-Cap < 100 KB im JPEG-Encoding mit Quality-Iteration und Floor.**
*Stand:* 2026-05-15 spät, in v1.9 vorbereitet (Implementierung in v2.0 Bildpipeline-Update). Bezug: E45 (Crop-Profile), Pilot-Erkenntnis HotCakes-Marble-Print.

*Warum:* Tjorben hat im v1.7-3-Modell-Cowork-Batch festgestellt, dass R2-Bilder mit komplexen Texturen (Marble-Print, Foto-Realismus) bei der etablierten JPEG-Quality (Q=85) durchschnittlich 150-175 KB groß sind. Sein WaWi-/Shop-Stack zeigt ab ca. 100 KB Performance-Einbußen bei Listing-Seiten (Page-Load + Mobile-Bandbreite). Aktuelle R2-Bilder der 3 Pilot-Modelle sind betroffen.

*Entscheidung — Cap-Mechanik in der Bildpipeline (Stage 4 = JPEG-Export):*
1. Initial-Quality = 85
2. Wenn Output-File > 100 KB → Quality um 5 reduzieren, neu encodieren
3. Wiederholen bis < 100 KB ODER Quality-Floor 70 erreicht
4. Bei Quality-Floor-Hit: warnen im Lauf-Bericht (Bild ist möglicherweise sichtbar matschig), nicht abbrechen
5. Resize-Strategie bleibt unverändert (Crop-Profile-Output-Dimensions wie in E45)

*Konsequenzen:*
- Bestehende R2-Bilder der 3 Pilot-Modelle (Hekate, Arachne Bottom Teal, Savanna Original Top) müssen bei v2.0-Bildpipeline-Lauf re-encodiert werden. URLs bleiben gleich (R2 überschreibt nach Key), Stammdaten-CSV muss nicht neu generiert werden.
- Cap kommt nur in Bildpipeline-Output zum Tragen — Originale auf R2 bleiben unverändert (full quality, beliebige Größe).
- Im Lauf-Bericht pro Bild: Final-Quality + Final-Filegröße ausweisen, damit Tjorben Trends erkennt.

*Status:* Im v1.9-Wissens-Update als BACKLOG-Eintrag B35 verankert. Implementierung in v2.0-Bildpipeline-Spec (parallel zum nächsten Bildpipeline-Lauf).

*Verworfen:*
- *Fester Quality-Wert von 70 für alle Bilder:* macht einfache Bilder unnötig matschig. Iterative Reduktion ist effizienter.
- *Auflösungs-Reduktion bei großen Files:* würde Crop-Profile-Konsistenz brechen — Quality-Reduktion ist die richtige Achse.
- *Quality-Floor 60 oder darunter:* Pole-Wear ist visuell anspruchsvoll (Texturen, Muster, Haut), unter 70 wird's für Marketing unbrauchbar.
- *Cap erst beim CDN ausspielen (auf-the-fly-Komprimierung via Cloudflare Image Resizing):* extra Cloudflare-Feature mit eigener Konfiguration, plus es kostet pro Request. Lokales Cap im Pipeline-Output ist einfacher und kostet nichts.

---

**E63 — Bildpipeline archiviert, manueller Bilder-Workflow im Pilot.**
*Stand:* 2026-05-16. Bezug: E12 (Bildpipeline als Sub-Process), E45 (Crop-Profile + Pose-Sortierung), E60 (Bild-Größen-Cap), B35, neue BACKLOG-Cluster „Bilder-Architektur-Refactor" und „Bildpipeline-Performance".

*Warum:* Die Bildpipeline hat im Pilot drei Probleme parallel angesammelt:
1. **Volumen/Cost-Frage** für Vision-Klassifikation (Pose-Sortierung) — Vision-API-Calls pro Bild summieren sich, Cloudflare Workers AI als Alternative ist nicht evaluiert.
2. **Modell-Qualitäts-Frage** für Pose-Klassifikation auf Pole-Wear-Bildern — Lieferantenbilder zeigen oft seitliche oder dreiviertel-Posen, die nicht sauber in Front/Rück/Seite fallen. Fallback-Rate bei `unknown`-Klassifikation war im Pilot unklar.
3. **Performance-Problem** — JPEG-Quality-Iteration (E60) kombiniert mit Vision-Calls pro Bild kann pro Lauf mehrere Minuten kosten, was Cowork's autonomen Flow blockiert.

*Entscheidung:*
- Bildpipeline-Spec `cowork_anweisung_bildpipeline.md` wird mit ARCHIVIERT-Header versehen. Inhalt bleibt erhalten als Wissens-Referenz für den späteren Refactor.
- Stage 5.6 (Bildpipeline-Aufruf) und Stage 5.7 (Bild-URL-Duplizierung) in der Daten-Pipeline werden **deaktiviert**.
- Die 10 Bild-Spalten in der Stammdaten-CSV bleiben im Schema verpflichtend, werden aber mit **leeren Strings** befüllt (Schema-Konformität für Ameise-Vorlage erhalten).
- Tjorben pflegt Bilder bis auf Weiteres **manuell** in WaWi (Drag-and-Drop pro Artikel über die WaWi-UI).
- Lieferanten-Mapping behält die Felder `crop_profile`, `pose_sort`, `category` — für die spätere Reintegration nach dem Architektur-Refactor.

*Konsequenzen:*
- Daten-Pipeline läuft End-to-End ohne Bildpipeline-Blocker.
- Cowork-Token-Budget pro Lauf frei für Daten-Stages.
- Operativer Mehraufwand für Tjorben: pro Artikel manueller Bilder-Pflege-Schritt in WaWi (Drag-and-Drop, ggf. manuelle Plattform-Aktivierung).
- Reintegration kommt nach dem Architektur-Refactor — neue Spec-Version mit klärten Antworten auf die drei Probleme oben.

*Verworfen:*
- *Bildpipeline patchen statt archivieren:* die drei Probleme oben sind systemisch, nicht punktuell. Mehrere Patches sind verschwendete Arbeit, wenn der Refactor sowieso ansteht.
- *Pose-Sortierung skippen, sonst alles behalten:* halb-funktionale Pipeline kostet auch Wartung. Sauberer Schnitt ist klarer.
- *R2-Bucket leeren / Originale archivieren:* aktuelle 3 Pilot-Modell-Bilder bleiben auf R2, URLs sind in WaWi referenziert. Nicht anfassen.

---

**E70 — Feature-Erfassung text-basiert, Vision-API-Extraktion bewusst aufgeschoben.**
*Stand:* 2026-05-16. Bezug: E63 (Bildpipeline archiviert), E45 (Bildpipeline-Funktionen vor E63), E49/E53 (Pole-Junkie als Stil-Quelle), Klärungs-Frage Tjorben am Tagesende 2026-05-16.

*Warum:* Nach E63 (Bildpipeline archiviert) stellte sich die Frage, wie Farbe, Style-Werte und andere Features in die Pipeline kommen, wenn die Bildpipeline weg ist. Antwort nach Klärung: über **Text-Quellen** — Shopify-Titel, Body_HTML, ggf. PDF/Mail-Texte. Bildanalyse wurde auch in der archivierten Bildpipeline nicht für Feature-Extraktion genutzt; sie machte nur Crop, Resize, R2-Upload und Pose-Sortierung. E63 hat an der Feature-Erfassung also de facto nichts geändert.

Im 2026-05-16-Lauf wurde das empirisch sichtbar: Farben (Beige für „Nude", Schwarz für „Dark Roast"), Style-Werte (`Open Back`, `Rundausschnitt`, `Bodysuit`) und Material kamen aus Body_HTML + Titel. An einer Stelle hat Cowork interpretiert („athletic cut at the back" → Open Back), was im Lauf-Bericht transparent als Interpretation markiert wurde. Das ist Charter-Prinzip-10-konform.

*Entscheidung (bewusste Pilot-Pragmatik):*
- Feature-Erfassung bleibt **text-basiert** für den Pilot. Keine Vision-API. Keine Bildanalyse für Merkmale.
- Im Lauf-Bericht **explizit dokumentieren**, wenn Cowork ein Style-Wert oder Feature aus dem Lieferanten-Text nicht eindeutig ableiten konnte und interpretiert hat. Das ist Pflicht, nicht optional.
- **Visueller Self-Check in WaWi** nach dem Import bleibt verpflichtend für Style-Werte. User-Konvention, kein Cowork-Schritt.
- Bei dünner Hersteller-Beschreibung darf Cowork das **Pole-Junkie-Schwestermodell als Feature-Cross-Reference** aufrufen — nicht nur als Stil-Quelle wie bisher in E49/E53. Wenn Pole Junkie das Modell führt und konkretere Feature-Texte hat, dürfen die als sekundäre Quelle dienen. NIE Copy-Paste, Eigenformulierung in polesportshop-DNA.
- `cowork_anweisung_datenimports.md` bekommt eine neue Sektion „Feature-Erfassungs-Quellen" mit diesen drei Konsequenzen verankert.

*Konsequenzen:*
- Bewusst dokumentierte Lücke: visuelle Features, die im Lieferanten-Text fehlen, werden im Pilot nicht erfasst. Mitigation: visueller Self-Check + Eigeninterpretations-Dokumentation.
- B-Cluster „Feature-Erfassung" im BACKLOG: Vision-API-Evaluation + Lieferanten-Text-Qualitäts-Indikator als Trigger-basierte Nachfolge-Aufgaben.
- Charter Prinzip 9 wird durch E70 indirekt validiert: keine Vision-Mechanik erfunden, nur das benutzt, was empirisch funktioniert.

*Verworfen:*
- *Vision-API für Feature-Extraktion jetzt einbauen:* parallel zur Daten-Pipeline-Stabilisierung wäre die nächste Baustelle. Tjorbens Disziplin: erst Kern robust, dann erweitern. Verschoben in B-Cluster „Feature-Erfassung".
- *Cowork-eigene Vision-Capability für Features nutzen:* technisch verfügbar, aber dieselbe Token-/Wallclock-Kosten-Diskussion wie bei Pose-Klassifikation (E63-Begründungen gelten analog).
- *Feature-Erfassung ganz an Tjorben auslagern:* würde die Daten-Pipeline-Idee aushöhlen, alles selbst zu machen.

---

**E93 — Bildpipeline reaktiviert (kehrt E63 um).**
*Stand:* 2026-05-18 (v1.21). *Bezug:* E63 (vorherige Archivierung 2026-05-16), E43 (R2-Upload-Mechanik), E45 (Crop-Profile + Vision-Pose-Sortierung), E46 (Bilder in Stammdaten-CSV), E60 (Bild-Größen-Cap), Trial-Lauf 2026-05-18 21:06 (HotCakes End-to-End, 21 Modelle, 25 Min Wallclock).

*Warum:* E63 archivierte die Bildpipeline 2026-05-16 mit der Begründung „Token-Budget für parallelen Vision-Call-Lauf + Architektur-Refactor-Bedarf bei Bildpipeline-Performance". Stand 2026-05-18 nach v1.20-Skalierungs-Refactor + Trial-Lauf:

1. **Daten-Pipeline ist stabil.** Live-Trial Batch 1+2 2026-05-17 und Trial-Lauf 2026-05-18 21:06 mit 16/16 Self-Check grün. Die Begründung „erst Daten-Pipeline robust" ist erfüllt.
2. **Wallclock-Bilanz rechtfertigt Bilder-Inklusion.** 25 Min für 21 Modelle + 90 Kinder (Daten) sind passabel; Bilder manuell pro Artikel in WaWi pflegen (Drag-and-Drop für 21 × bis zu 10 Bilder = bis zu 210 manuelle Bild-Uploads) ist deutlich teurer für Tjorben.
3. **R2-Architektur ist unverändert verfügbar.** E43 (boto3 + Egress-Allowlist + Drive-Credentials-File), E44 (R2 als Voll-Storage), E45 (Crop + Vision), E60 (Größen-Cap), B34 (Original-Index-HTML) — alles aus v1.6-Spec implementiert und mit Arachne-Bottom-Black 2026-05-15 validiert. Keine neue Infrastruktur nötig.
4. **Bildpipeline-Spec ist im `v1.19`-Git-Tag erhalten.** Voll-Spec v1.6 (43 KB) ist via `git show v1.19:cowork_anweisung_bildpipeline.md` rekonstruierbar — keine Wissens-Lücke.

Tjorben-Direktive 2026-05-18: „Ich frage mich, ob wir die Artikelbilder doch wieder mit reinnehmen, weil da haben wir ja alles angebunden, was die Architektur angeht und das wäre jetzt natürlich auch eine große Erleichterung, wenn die Artikelbilder mitgemacht werden würden."

*Entscheidung:* Bildpipeline reaktivieren ab v1.21. Stage 5.6 + 5.7 in `cowork_anweisung_datenimports.md` wieder aktiv. `cowork_anweisung_bildpipeline.md` von Stub (v2.0 in v1.20) auf Voll-Spec v2.1 (rekonstruiert aus v1.19-Tag, plus Wissens-Resolution-Update von Drive auf GitHub-Raw).

*Konsequenzen:*
- `cowork_anweisung_bildpipeline.md` von 3.2 KB Stub auf ~43 KB Voll-Spec. v2.0 → v2.1 (Minor, weil Wissens-Resolution-Pivot von Drive auf GitHub-Raw + Reaktivierungs-Header). ARCHIVIERT-Header durch AKTIV-Header ersetzt.
- `cowork_anweisung_datenimports.md` Stage 5.6 + 5.7 aktiv. Bild-URLs in Stammdaten-CSV-Spalten Bild 1-10. v2.0 → v2.1 (Minor).
- `run_brief_daten.md` Stage-Tabelle: Stage 5.6 + 5.7 wieder aktiv. v1.17 → v1.18 (Minor).
- B30 (Re-Import-Verhalten bei leeren Bild-Spalten) wird wieder akut — Verifikations-Test vor erstem produktivem Re-Import auf bebilderte Artikel.
- BACKLOG-Cluster „Bilder-Architektur-Refactor" (B36-B40) bleibt offen für künftige Tiefen-Optimierungen, aber der Pilot-Workflow läuft wieder.
- WaWi-Manuelle-Bilder-Pflege durch Tjorben entfällt (war seit E63 Bottleneck).

*Verworfen:*
- **„Bildpipeline-Refactor erst abschließen, dann reaktivieren":** der Refactor ist eine Tiefenoptimierung. Die v1.6-Spec ist produktionsreif (Arachne-Bottom-Black validiert), Refactor ist Optimierung nicht Voraussetzung.
- **„Hybride Variante: Cowork generiert R2-URLs, Tjorben pflegt manuell":** doppelter Aufwand statt einer Lösung.
- **„Mac-Daemon für Bildpipeline statt Cowork-Sandbox":** war eine E63-Refactor-Idee. v1.6-Cowork-Sandbox-Pattern funktioniert, kein Pivot nötig.

*Folgeaufgaben:*
- B30 (Re-Import-Verhalten bei leeren Bild-Spalten) — vor erstem Re-Import auf bebilderte Artikel verifizieren.
- B67 (NEU v1.21) — siehe BACKLOG.md.

*Stolperfallen:*
- **Egress-Allowlist:** Cowork braucht Zugriff auf `d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com` (R2-Endpoint), `pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev` (Public-URL), Lieferanten-CDN-Domain (z.B. `cdn.shopify.com` für HotCakes), `pypi.org` + `files.pythonhosted.org` (boto3). Aktueller B29-Workaround „All domains" deckt das ab.
- **R2-Credentials in Drive-File** (E33-Pfad-b): `_Credentials/r2_credentials.json` muss zugreifbar sein. Bei Drive-Down: Lauf abbrechen, kein Fallback.
- **Vision-Token-Verbrauch** pro Artikel: ~10 Thumbnail-Vision-Calls × 21 Artikel = ~210 Vision-Calls pro Lauf. Stage 0.5 Scope-Analyse muss das in Token-Schätzung einbeziehen.
- **Wallclock-Erwartung v1.21:** Vermutlich 35-50 Min für 21 Artikel inkl. Bilder (statt 25 Min nur Daten). Erste Validierung beim v1.21-Trial-Lauf.

---
