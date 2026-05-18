# ENTSCHEIDUNGS-LOG-CRAWLING-DATEN

**Cluster:** Crawling, Quellen, CSV-Schema, Datenmodell, Mappings

**Stand:** v1.18, 2026-05-18 (neue Einträge E89 Category-Pattern + Sara-Workflow, E90 F-Fixes Sammeleintrag v1.19)

**Bezug:** Dieser Cluster ist Teil des Splits der ursprünglichen `ENTSCHEIDUNGS-LOG.md` (v1.16, 165 KB → 6 Themen-Cluster ≤ 40 KB). Historische / abgelöste Einträge liegen weiterhin in `ENTSCHEIDUNGS-LOG-ARCHIV.md`. Cross-Cluster-Referenzen über E-Nummer; der Master-Index mit allen E-Nummern → Cluster-File-Zuordnung liegt in `SPEC_KONSTANTEN.md` unter `ENTSCHEIDUNGSLOG_E_NUMMER_INDEX`.

---

## Index

- **E5** — Mehrere separate CSVs statt einer (initial vier, ab 2026-05-14 fünf, ab 2026-05-15 wieder vier — siehe E35 und E46)
- **E6** — Artikelnummer = Lieferantenartikelnummer (A-Nummer-Strategie aufgeschoben)
- **E7** — Vater-Kind-Struktur über `Identifizierungsspalte Vaterartikel`
- **E8** — Kombinierte Größen (XS/S) = ein Kind-Artikel + Merkmal-Expansion (zwei Filter-Werte XS und S)
- **E9** — Mehrsprachigkeit: Attribute via Spalten-Suffix, Merkmale nur Deutsch
- **E13** — Crawling von Pole Junkie (Wettbewerber) erlaubt, mit Auflagen
- **E19** — Merkmal-Logik bei Variantenartikeln: Farbe+Style auf Vater UND Kind, Größe nur auf Kind
- **E21** — Cloud-Storage-Links brauchen separates Handling
- **E48** — Crawl-Modus B: Code-Execution + Browser-UA gegen Shopify-Storefront-JSON
- **E49** — Pole Junkie Crawl-Freigabe: Owner-Direktive mit Verantwortungs-Übernahme
- **E50** — WaWi-Merkmalwerte: statische deutsche Liste mit zweistufiger Farb-Logik
- **E51** — Kategoriebaum-Mapping: „Pole Dance Kleidung" als Ebene 1 + passende Unterkategorie
- **E52** — A6-Pivot: CSVs nur lokal im Cowork-Workspace, kein Drive-Upload
- **E54** — Stammdaten-CSV-Schema-Layout: 38 alte Spalten + 10 Bilder am Ende (Reverse-Engineering für Vorlagen-Kontinuität)
- **E57** — Multi-Kategorie-Zuweisung via mehrfache CSV-Zeilen mit gleicher Artikelnummer + Ameise-Setting „Kategorieverknüpfungen des Artikels aktualisieren = Neue Kategorien beim jeweiligen Artikel hinzuimportieren"
- **E69** — E52-Implementation in Cowork-CI und Datenimports-Spec verankern, A6 formell archivieren
- **E89** — Category-Pattern + Sara-Review-Workflow (NEU v1.18, präzisiert E57)
- **E90** — F2-F6-Implementierung in v1.19 (Sammeleintrag, NEU v1.18)

---

**E5 — Mehrere separate CSVs statt einer (initial vier, ab 2026-05-14 fünf, ab 2026-05-15 wieder vier — siehe E35 und E46).**
*Warum:* Ameise hat eigene Import-Vorlagen pro Domain (Stammdaten, Merkmale, Attribute, Bilder), Validierung pro Domain möglich, Fehler isolierbar.
*Evolution:*
- *Ursprünglich (v1.0-v1.1):* vier CSVs — Stammdaten, Merkmale, Attribute, Bilder
- *Mit E35 (2026-05-14):* fünf CSVs — Hinzunahme der Variationen-CSV als separater Import-Schritt (Lieferantendaten-CSV wurde gleichzeitig in Stammdaten integriert)
- *Mit E46 (2026-05-15):* vier CSVs — Bilder werden als Spalten in die Stammdaten-CSV integriert, kein separater Bilder-Import mehr (siehe E46 für Begründung). Die Variationen-CSV bleibt als eigenständiger Import erhalten, weil sie Sprach-Varianten von Größen-Werten pflegt (anderes Datenmodell als Bilder).
*Verworfen:* Mega-CSV mit kreativem Mapping (würde Ameise gegen den Strich bürsten).

**E6 — Artikelnummer = Lieferantenartikelnummer (A-Nummer-Strategie aufgeschoben).**
*Warum:* Lieferanten-SKU ist eindeutig vorhanden, keine eigene Sequenz nötig, Pilot-Geschwindigkeit. Spätere Umstellung trifft nur die `Artikelnummer`-Spalte.
*Verworfen:* Eigene A-Nummer-Sequenz (zu früh, ohne klaren Vorteil). HAN als Identifier (echte Barcodes oft nicht vorhanden bei Boutique-Lieferanten).

**E7 — Vater-Kind-Struktur über `Identifizierungsspalte Vaterartikel`.**
*Warum:* Native JTL-Struktur, Ameise erkennt Beziehung direkt beim Import.
*Verworfen:* Eltern-IDs nachträglich auflösen (fehleranfällig).

**E8 — Kombinierte Größen (XS/S) = ein Kind-Artikel + Merkmal-Expansion (zwei Filter-Werte XS und S).**
*Warum:* Bestellbarkeit (ein SKU mit Lagerbestand) bleibt korrekt, aber Filter-Suche nach "S" findet das Produkt trotzdem.
*Verworfen:* Zwei Kind-Artikel pro Kombi-Größe (Lagerbestand wäre falsch). Nur ein Filter "XS/S" (Kunde sucht nach "S").

**E9 — Mehrsprachigkeit: Attribute via Spalten-Suffix, Merkmale nur Deutsch.**
*Warum:* Attribute = Rich Text pro Sprache anders. Merkmale = strukturiert, werden in WaWi-Stammdaten zentral übersetzt.
*Verworfen:* Alles in CSV-Spalten duplizieren (würde WaWi-Übersetzungs-Mechanik ignorieren).

**E13 — Crawling von Pole Junkie (Wettbewerber) erlaubt, mit Auflagen.**
*Warum:* Pole Junkie hat das HotCakes-Sortiment vollständig online, Hersteller hat keine eigenen Bilder, Bilder kommen ohnehin vom Hersteller (identische Quelle).
*Auflagen:* Beschreibungstexte werden im eigenen Shop-Stil neu geschrieben (Urheberrecht, Wettbewerb, Markenführung). Bilder direkt vom Pole-Junkie-CDN sind OK weil Hersteller-Bilder.
*Verworfen:* Discovery-only (würde Bilder-Quelle wegnehmen ohne Nutzen). Full-Copy inkl. Texte (rechtlich und marken-strategisch problematisch).
*Vorbehalt:* Diese Entscheidung steht unter dem Vorbehalt der rechtlichen Klärung in B3 (Pole-Junkie-Crawling). E13 ist operative Arbeitsentscheidung für den Test-Lauf; B3 bleibt strategisch offen.

**E19 — Merkmal-Logik bei Variantenartikeln: Farbe+Style auf Vater UND Kind, Größe nur auf Kind.**
*Warum:* Validierung durch JTL-Export *Artikelmerkmale* vom 13.05.2026 mit 80 echten Vater-Kind-Stämmen (1709 Zeilen, 478 Artikel). Standard-Beispiel A1009118 *Paradise Chick Top Gigi Active Schwarz*: Vater mit Farbe="Schwarz" und Style Tops="Open Back"+"Rundausschnitt", fünf Kinder (-001 bis -005) mit Größen XS-XL, jeweils gespiegelte Farbe+Style. Style ist multi-value möglich (mehrere Zeilen pro Artikel mit demselben Merkmalsnamen). JTL erbt Merkmale nicht implizit zu den Kindern; sie müssen explizit gepflegt sein, sonst fehlen sie in Filtern und Such-Indizes für die Kinder.
*Verworfen:* Annahme in v1.1, dass Farbe+Style ausschließlich auf Vater liegen. Falsche Vereinfachung — wurde im HotCakes-Test-Lauf nicht erkannt, weil die generierte CSV noch nicht in Ameise importiert war.
*Implementierung:* cowork_anweisung_datenimports.md v1.2.
*Erweiterung 2026-05-14:* Siehe E34 — gleiche Logik gilt auch für Attribute und Bilder (JTL erbt generell nichts implizit, nicht nur bei Merkmalen).

**E21 — Cloud-Storage-Links brauchen separates Handling.**
*Warum:* Dropbox blockt Bot-Fetches via robots.txt. Andere Cloud-Hoster (WeTransfer, Google Drive, OneDrive) mit ähnlichen Mustern.
*Verworfen:* Mit User-Agent-Spoofing umgehen — fragil, ToS-Verletzung, mittelfristig brüchig.
*Folgeaufgabe:* B16 (Connector-Strategie).

**E48 — Crawl-Modus B: Code-Execution + Browser-UA gegen Shopify-Storefront-JSON.**
*Stand:* 2026-05-15 (validiert im ersten End-to-End-Run für HotCakes Arachne Black Top). Bezug: E14, E41, B22, B25, B29.

*Warum:* Die v1.6-Spec hatte den Crawl-Modus geparkt unter der defensiven Annahme „ohne Firecrawl kein Crawl-Pfad". Mit „All Domains"-Egress-Allowlist (B29-Workaround, 2026-05-15 aktiviert) und Code-Execution + Network-Egress existiert ein zweiter, voll funktionaler Crawl-Pfad — speziell für Shopify-gehostete Lieferanten-Sites. Erster Praxis-Test 2026-05-15 mit hotcakespolewear.com: HTTP 200 ohne Anti-Bot-Treffer, 124 Produkte in einer Response (~575 KB), saubere strukturierte Daten (Titel, body_html, options, variants, 4 Bilder pro Produkt).

*Mechanik:*

1. **Code-Execution-Sandbox** mit `requests`, realistischem Browser-UA (z.B. Chrome aktueller Version), `Accept`/`Accept-Language`/`Sec-Fetch-*`-Header analog zu einem echten Browser. Das ist **kein** User-Agent-Spoofing-Hack im E21-Sinn (E21 verbietet ToS-verletzende Tricks) — ein Browser-UA-String ist Norm-Konvention für HTTP-Clients, das macht jeder `curl`-Aufruf auch.
2. **Primärer Pfad — Shopify-Storefront-JSON-Endpoints** (öffentlich, dokumentiert, ToS-konform für die meisten Shopify-Stores):
   - `/products.json?limit=250&page=N` für Katalog-Listing (max 250 pro Page, Pagination-Ende = leeres `products`-Array)
   - `/products/<handle>.json` für Detail mit `body_html`, `options`, `variants`, `images`
3. **`Accept-Encoding: gzip, deflate`** ohne `br` — das Brotli-Modul ist in der Cowork-Sandbox nicht standardmäßig installiert (operative Beobachtung aus dem ersten Lauf, A2-Pattern).
4. **Magic-Byte-Extension** beim Bild-Download zwingend — Shopify-CDN respektiert die in der URL angegebene Endung nicht zuverlässig (zwei von vier HotCakes-Bildern kamen mit `.jpg`-URL als webp zurück, weil Accept-Header webp tolerierte). Echte Extension via File-Header bestimmen.

*Trigger-Detektion (Shopify-Erkennung):* Set-Cookies `_shopify_*` im Homepage-Response sind eindeutiger Shopify-Fingerprint. Im Lieferanten-Mapping ergänzen: optionales Feld `crawl_mechanik` mit Werten `shopify_json` (für Shopify-erkannte Sites), `firecrawl` (für künftige Re-Aktivierung sobald Connector verfügbar) oder `manual_only` (kein Crawl, Drive-Upload pflicht).

*Scope nach Lieferant:*
- *HotCakes Polewear* (Shopify): validiert, `crawl_mechanik: shopify_json` aktiv.
- *POLE ADDICT*: zu prüfen — sieht nach Shopify aus, Detektion beim ersten Lauf.
- *Pole Junkie*: Crawl explizit freigegeben durch Owner-Direktive E49 — falls technisch Shopify, gilt E48-Pfad.
- *Lunalae + weitere*: pro Lieferant Shopify-Probe vor erstem Lauf.

*Konsequenz für Spec:* `cowork_anweisung_datenimports.md` v1.7 — Abschnitt 2.2 Tabelle erweitert um Zeile `shopify_json` (Status aktiv), Abschnitt 2.4 mit Detektions-Logik, Abschnitt 9 Fehler-Handling differenziert nach Crawl-Mechanik (Shopify-erkennbar durchläuft, non-Shopify ohne Firecrawl bricht ab).

*Verworfen:*
- *Reines HTML-Scraping:* fragiler als JSON, plus Brotli-Komplikationen. Storefront-JSON ist die saubere Wahl wo verfügbar.
- *Cloudflare-Workers-Code-Mode-MCP (B26):* nicht in Cowork-Registry und Setup-Aufwand für Pilot zu hoch.
- *Firecrawl als alleiniger Crawl-Pfad (E41/B25):* bleibt strategische Wahl für Non-Shopify-Sites, ist aber aktuell nicht verfügbar. E48 ist komplementär, nicht ersetzend.

*Stolperfallen:*
- **Storefront-JSON-Verfügbarkeit:** nicht alle Shopify-Stores haben `/products.json` öffentlich. Manche blockieren via `robots.txt` oder Theme-Konfiguration. Vor Lieferanten-Onboarding mit `curl` prüfen.
- **CDN-Format-Drift:** Magic-Byte-Detection ist Pflicht, nicht optional. Dokumentiert als Anomalie A2 im BACKLOG.
- **ToS-Kollision bei Non-First-Party-Daten:** wenn ein Shopify-Store ausdrücklich Scraping verbietet (selten, aber möglich), gilt der Verbot trotz technischer Verfügbarkeit. Pole Junkie ist hier Sonderfall (E49 Owner-Direktive).

*Folgeaufgaben:*
- POLE ADDICT Shopify-Probe beim Migration-Lauf
- Lessons-Learned aus 3-Modell-Batch validieren (Pose-Konsistenz, Bild-Reihenfolgen-Stabilität)

**E49 — Pole Junkie Crawl-Freigabe: Owner-Direktive mit Verantwortungs-Übernahme.**
*Stand:* 2026-05-15. Bezug: B3, E48, Charter Prinzip 9.

*Owner-Direktive:* Tjorben Becker (Geschäftsführung Verticalo GmbH) erteilt mit Datum 2026-05-15 ausdrücklich und unverhandelbar die Freigabe für das Crawling der Pole-Junkie-Domain im Rahmen der Artikelanlage-Pipeline. Volle rechtliche und operative Verantwortung wird von Verticalo GmbH übernommen.

*Hintergrund:* B3 dokumentierte den potenziellen ToS-Konflikt bei Pole Junkie als „rechtliche Grauzone". Cowork hat in seinem Übergabe-Bericht 2026-05-15 die Frage als Open Question explizit gestellt: technisch wäre E48 dort funktional, aber die ToS-Bedenken sollten vor jedem Lauf geklärt werden. Tjorben hat diese Klärung in derselben Session vorgenommen und die Freigabe ohne Vorbehalt erteilt.

*Operative Konsequenz:*
- Cowork führt Crawl-Versuche auf der Pole-Junkie-Domain ohne Vorbehalt durch, sobald entsprechende Lieferanten-Trigger ausgelöst werden.
- Wenn Pole Junkie technisch Shopify ist, gilt E48-Mechanik (Storefront-JSON + Code-Execution).
- Wenn Pole Junkie nicht-Shopify ist, gilt der jeweils verfügbare Crawl-Pfad (Firecrawl sobald in Registry, sonst manuell).
- `lieferanten_mapping.yaml` enthält Pole-Junkie-Eintrag mit `crawl_mechanik`-Feld passend zur Detektion.

*Verworfen (mit voller Transparenz festgehalten):*
- *Vorab-ToS-Konsultation und juristische Vorab-Klärung:* Tjorben hat ausdrücklich darauf verzichtet und die Verantwortung übernommen. Diese Entscheidung wird hier in ihrer ganzen Tiefe dokumentiert, damit kein zukünftiger Operator oder Nachfolger denkt, das wäre triviale Konvention oder versehentliche Lockerung der E33-Anti-Pattern-Disziplin. Die rechtlichen Bedenken aus B3 bleiben als Hintergrund-Risiko bestehen — die Geschäftsführung trägt das Risiko bewusst.
- *Halt-und-Nachfrage bei jedem Pole-Junkie-Trigger:* aufgehoben durch diese Direktive. Cowork muss nicht mehr eskalieren — die Freigabe gilt session-übergreifend bis zur expliziten Rücknahme durch Tjorben.

*Stolperfallen / Beobachtungs-Pflichten:*
- **Wenn Pole Junkie Anti-Bot-Maßnahmen einsetzt** (technische, nicht rechtliche Blockade), gilt das normale Halt-und-Recherche-Pattern aus E48-Stolperfallen. Owner-Direktive überschreibt rechtliche Bedenken, nicht technische Realitäten.
- **Bei expliziten Cease-and-Desist-Forderungen** durch Pole-Junkie-Rechtsabteilung oder ähnlichem Anlass: sofort an Tjorben eskalieren, Crawl pausieren bis zur Klärung. Diese Pause überschreibt die Owner-Direktive nicht — sie ist Reaktion auf neuen Umstand.
- **Im Lauf-Bericht** explizit erwähnen, dass der Lauf auf Pole-Junkie-Daten unter E49-Direktive operiert hat. Audit-Spur für die Geschäftsführungs-Entscheidung.

*Folgeaufgaben:*
- B3 in BACKLOG entsprechend umformulieren — von „rechtliche Grauzone, Klärung nötig" zu „Owner-Direktive E49 aktiv, Beobachtungs-Pflichten dokumentiert".
- Pole-Junkie-Eintrag im `lieferanten_mapping.yaml` anlegen oder aktualisieren mit `crawl_mechanik`-Feld.

---

**E50 — WaWi-Merkmalwerte: statische deutsche Liste mit zweistufiger Farb-Logik.**
*Stand:* 2026-05-15 Abend. Bezug: E19, E34, B19.

*Warum:* Cowork hat im 3-Modell-Batch teils gut gemappte Merkmalwerte produziert (z.B. „Cheeky/Riemchenshorts/Mid Waist" korrekt aus der WaWi-Style-Shorts-Liste), aber teils Werte erfunden oder Sonderfälle wie „Teal" als Farbe verwendet, die nicht in der WaWi-Liste existieren. Das führt zu Import-Reibung und macht den Shop-Filter inkonsistent. Plus: bei dezenten Farbtönen (Türkis, Burgund, Nude) war unklar wie sie zu mappen sind.

*Entscheidung:*

1. **Statische Merkmalwert-Listen pro Kleidungstyp** in `WAWI-IMPORT-WISSEN.md` und `cowork_anweisung_datenimports.md` Sektion 5.3 verankert:
   - **Farbe Kleidung (15):** Bunt, Gold, Schwarz, Weiß, Braun, Beige, Grau, Blau, Grün, Gelb, Orange, Rot, Pink, Lila, Silber
   - **Style Tops (11):** Crop Top, Open Back, Rundausschnitt, Bodysuit, High Neck, Langärmlig, One Shoulder, Riemchentop, Samt, T-Shirt, Triangle Ausschnitt
   - **Style Shorts (11):** Cheeky, High Leg, High Waist, Low Waist, Mid Waist, Classic Hot Pants, Riemchenshorts, Samt, Leggings, Bike Shorts, Strumpfhose

2. **Nur deutsche Werte in der CSV** — keine Mehrsprachigkeit. Die WaWi hat die Übersetzungen statisch pro Merkmalwert hinterlegt, Cowork muss nur DE-Werte schreiben. Spart Pipeline-Komplexität und bricht keine Konvention.

3. **Zweistufige Farb-Logik (zentral):**
   - **Im Artikelnamen** steht der spezifische Farbname wie er in der Marketingsprache verwendet wird (z.B. „Türkis", „Burgund", „Petrol")
   - **Im Merkmalwert Farbe** steht der **nächstpassende WaWi-Wert** aus der statischen 15er-Liste (z.B. „Blau" für Türkis, „Rot" für Burgund, „Blau" für Petrol)
   - Bei Konflikt zwischen Hersteller-Wording und WaWi-Liste **gewinnt die WaWi-Liste** beim Merkmal. Der Artikelname kann die Hersteller-Wording behalten — er ist das Customer-Facing-Element.

4. **Pilot-Beispiel (Korrektur Lauf 2026-05-15):**
   - Cowork hat „HotCakes Shorts Arachne Blau" geschrieben (sowohl im Artikelnamen als auch im Merkmal)
   - Korrekt wäre: Artikelname „HotCakes Shorts Arachne Türkis", Merkmal „Blau"

*Konsequenzen für Specs:*
- `cowork_anweisung_datenimports.md` v1.8 Sektion 5.3 erweitert um die statischen Listen plus die zweistufige Farb-Logik mit Beispielen
- `WAWI-IMPORT-WISSEN.md` als Single-Source-of-Truth für die Merkmalwert-Listen
- Pro Lieferant kann das Mapping spezifiziert werden falls Cowork systematisch falsch klassifiziert (z.B. wenn HotCakes-„Nude" konsistent zu „Beige" gemappt werden soll)

*Verworfen:*
- *Mehrsprachige Merkmal-Werte in der CSV erzeugen:* unnötig, WaWi pflegt die Übersetzungen intern.
- *„Teal" oder „Print" als zusätzliche Merkmalwerte vorschlagen (Vorschlag aus 3-Modell-Bericht Sektion 7):* fällt weg — die zweistufige Logik löst das eleganter. Spezifischer Name lebt im Artikelnamen, generischer Wert im Merkmal.

---

**E51 — Kategoriebaum-Mapping: „Pole Dance Kleidung" als Ebene 1 + passende Unterkategorie.**
*Stand:* 2026-05-15 Abend. Bezug: E2, JTL-Ameise-Konvention recherchiert 2026-05-15.

*Warum:* Cowork hat im 3-Modell-Batch „Damen" als Kategorie Ebene 1 geschrieben. Das ist nicht im polesportshop-Kategoriebaum. Plus: die JTL-Notation für Kategorien in CSV-Imports war unklar (mit Pfad-Notation `->` oder ohne).

*Recherche-Ergebnis (JTL-Forum + Guide):*
- JTL-Ameise erwartet `Kategorie Ebene 1`, `Kategorie Ebene 2`, ... als separate CSV-Spalten mit den **Einzel-Kategorienamen** pro Ebene
- Bis zu 10 Levels möglich
- Pfad-Notation mit `->` ist nur die WaWi-UI-Darstellung der Hierarchie, nicht das CSV-Format
- Jeder Artikel muss in mindestens einer Kategorie sein, sonst wird er nicht importiert

*Entscheidung:*

**Kategorie-Mapping-Tabelle pro Kleidungstyp** (in `cowork_anweisung_datenimports.md` v1.8 Sektion 5.4 verankert):

| Kleidungstyp | Kategorie Ebene 1 | Kategorie Ebene 2 |
|---|---|---|
| Top | Pole Dance Kleidung | Pole Dance Tops |
| Bottom / Shorts | Pole Dance Kleidung | Pole Dance Shorts |
| Bodysuit | Pole Dance Kleidung | Bodysuits |
| Leggings | Pole Dance Kleidung | Leggings |
| Legwarmer | Pole Dance Kleidung | Legwarmer |
| Shirt | Pole Dance Kleidung | Shirts |

*„Limited Editions"* wird **aus dem Mapping ausgeschlossen** — die Kategorie wird in WaWi demnächst gelöscht (Tjorben-Direktive 2026-05-15). Bestehende Limited-Editions-Artikel werden bei Bedarf manuell auf die passende Unterkategorie umgehängt.

*Akut-Fix für aktuellen 3-Modell-Lauf:*
- Hekate Bodysuit → Ebene 1 „Pole Dance Kleidung", Ebene 2 „Bodysuits" (nicht „Damen"/„Bodysuits")
- Arachne Bottom Teal → Ebene 1 „Pole Dance Kleidung", Ebene 2 „Pole Dance Shorts"
- Savanna Original Top → Ebene 1 „Pole Dance Kleidung", Ebene 2 „Pole Dance Tops"

*Verworfen:*
- *Pfad-Notation mit `->` in der CSV:* widerspricht JTL-Ameise-Konvention.
- *„Damen" als Ebene 1:* nicht im Kategoriebaum, Cowork-Fehler im 2026-05-15er Lauf.

---

**E52 — A6-Pivot: CSVs nur lokal im Cowork-Workspace, kein Drive-Upload.**
*Stand:* 2026-05-15 Abend. Bezug: A6, B33.

*Warum:* Im 3-Modell-Batch hat der Drive-Upload **55,9 % der Wallclock-Zeit** verbraucht (1268 s von 2269 s). Plus: das Tool-Output-Limit von ~50 K Zeichen führte beim Upload großer Attribut-CSVs (107 KB) zu partial-Uploads (A6-Symptom). Tjorben hat im Klärungs-Chat 2026-05-15 deutlich gemacht: **er braucht die CSVs zum direkten Download im Chat, nicht in Drive**. Drive-Archiv ist überdimensioniert für seinen tatsächlichen Workflow.

*Entscheidung — Output-Pfad-Pivot:*

```
ALT (v1.7, vor A6):
- 4 CSVs → /home/claude/outputs/ → Drive _PIPELINE/_Logs/<datum>_<lieferant>/
- Bericht → Drive _PIPELINE/_Logs/<datum>_<lieferant>/

NEU (v1.8, mit A6-Pivot):
- 4 CSVs → /home/claude/outputs/ (Tjorben downloadet direkt im Chat via present_files-Pattern)
- Bericht → Drive _PIPELINE/_Logs/<datum>_<lieferant>/ (klein, kein A6-Risiko, Audit-Trail)
- Mapping-Cheatsheet → Drive _PIPELINE/_Logs/... (klein)
```

*Konsequenzen:*
- A6 ist damit komplett gelöst (kein Drive-Upload-Pfad für große CSVs mehr)
- Wallclock-Ersparnis bei 3-Modell-Batch: ~55 % (laut Bericht-Profil)
- Audit-Trail bleibt über den Lauf-Bericht erhalten — Bericht enthält Output-Filenamen und MD5-Hashes, kann später jederzeit re-validiert werden gegen die heruntergeladenen CSVs
- `_PIPELINE/_Logs/`-Konzept reduziert auf „Berichte + Mapping-Cheatsheets", keine CSVs mehr darin

*Verworfen:*
- *Hybrid `Read`-Tool + textContent für große CSVs (Cowork-Empfehlung A6-Fix):* obsolet durch den Pivot. Kein Drive-Upload heißt kein Tool-Output-Limit-Problem.
- *2-File-Aufteilung der Attribute-CSV als Notbremse:* obsolet aus gleichem Grund.
- *Best-Effort-Hybrid (lokal + parallel Drive-Upload):* unnötiger Komplexitäts-Gewinn, würde A6 nicht vollständig lösen.

---

**E54 — Stammdaten-CSV-Schema-Layout: 38 alte Spalten + 10 Bilder am Ende (Reverse-Engineering für Vorlagen-Kontinuität).**
*Stand:* 2026-05-15 Abend. Bezug: E36, E46, B22.

*Warum:* Tjorben hat im 3-Modell-Batch-Mapping festgestellt, dass die Cowork-CSV der v3-Spec zwar mit 48 Spalten konform war, aber die **Spalten-Reihenfolge** in der CSV nicht mehr der ALT-Reihenfolge der `HotCakes Polewear_1_Stammdaten`-Vorlage entsprach. Konkret: in der ALT-Vorlage waren `Ist Standardlieferant` (Position 37) und `Lieferzeit in Tagen (Lieferant)` (Position 38) am ENDE der 38 Spalten. Cowork hatte sie im v3-Schema auf Position 16-17 verschoben — das hat das Mapping der Vorlage zerschossen.

Tjorben-Direktive: „Reverse engineering — die ALT-Reihenfolge der 38 Spalten beibehalten, die 10 Bild-Spalten einfach am Ende anhängen. Damit muss ich nur die letzten 10 Spalten neu mappen."

*Entscheidung — Schema-Layout v3.1 (rekonstruiert nach v2-Stand der HotCakes-Vorlage):*

```
Position 1-12:   Identifikation + Hauptdaten + Variation + Kategorie
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

Position 13-14:  Preise (Hauptpreise)
   13. EK Netto (für GLD)
   14. Brutto-VK

Position 15-17:  Lager & Status
   15. Bestandsführung aktiv
   16. Neu im Sortiment
   17. Neu im Sortiment seit

Position 18-21:  Gewicht & Versand
   18. Artikelgewicht
   19. Versandgewicht
   20. Versandklasse
   21. Herkunftsland

Position 22-25:  Sprach-Artikelnamen
   22. Global-Englisch: Artikelname
   23. Global-Französisch: Artikelname
   24. Global-Italienisch: Artikelname
   25. Global-Spanisch: Artikelname

Position 26-27:  Meta-Daten DE (nur Vater)
   26. Titel-Tag (SEO)
   27. Meta-Description (SEO)

Position 28-35:  Sprach-SEO-Daten (8 Spalten)
   28. Global-Englisch: Titel-Tag
   29. Global-Englisch: Meta-Description
   30. Global-Französisch: Titel-Tag
   31. Global-Französisch: Meta-Description
   32. Global-Italienisch: Titel-Tag
   33. Global-Italienisch: Meta-Description
   34. Global-Spanisch: Titel-Tag
   35. Global-Spanisch: Meta-Description

Position 36-38:  Lieferantenblock (am ENDE der 38 alten Spalten)
   36. Netto-EK
   37. Ist Standardlieferant
   38. Lieferzeit in Tagen (Lieferant)

Position 39-48:  Bild-URLs (E46 angehängt)
   39. Bild 1
   40. Bild 2
   ...
   48. Bild 10
```

*Konsequenzen für Tjorbens Vorlage:*
- Vorlagen-Positionen 1-38 bleiben **unverändert** kompatibel zur ALT-Vorlage (vor E46)
- Nur die **10 Bild-Spalten (39-48)** müssen einmalig neu gemappt werden
- Vorlagen-Speicher-Aufwand: ~5-10 Min statt 20-30 Min komplettes Re-Mapping

*Konsequenzen für Cowork:*
- `cowork_anweisung_datenimports.md` v1.8 Sektion 5.1 vollständig überschrieben mit dem neuen Schema-Layout
- Cowork generiert die CSV ab v1.8 in dieser Reihenfolge
- Schema-Version bleibt v3.1 (nicht v4, weil die SPALTEN sich nicht ändern, nur die REIHENFOLGE)

*Spec-Migration-Pflicht:* Bei jedem ZUKÜNFTIGEN Schema-Bump (z.B. v4 mit zusätzlichen Feldern) muss diese Reverse-Engineering-Diskussion explizit geführt werden, damit existierende Vorlagen mit minimalem Aufwand kompatibel bleiben. Konvention: **neue Spalten werden grundsätzlich am Ende angehängt, NICHT in bestehende Bereiche eingefügt.**

*Verworfen:*
- *Volle Spalten-Reorganisation nach „logischer Reihenfolge" (Cowork-Vorschlag bei E46):* zwingt User zu komplettem Re-Mapping pro Schema-Bump. Pragmatisch ist „append-only" für Spalten.
- *Komplette Schema-Versionierung mit semantischen Migrationen:* überdimensioniert für die Pilot-Phase. Konvention reicht.

**E57 — Multi-Kategorie-Zuweisung via mehrfache CSV-Zeilen mit gleicher Artikelnummer + Ameise-Setting „Kategorieverknüpfungen des Artikels aktualisieren = Neue Kategorien beim jeweiligen Artikel hinzuimportieren".**
*Stand:* 2026-05-15 spät. Bezug: E51 (Kategoriebaum), JTL-Ameise-Doku.

*Warum:* Tjorben will pro Artikel **beide** Kategorien (Oberkategorie „Pole Dance Kleidung" UND passende Unterkategorie wie „Bodysuits") sichtbar im Shop haben. Erste v3.1-CSV-Generierung hatte nur eine Zeile pro Artikel mit Ebene 1 = `Pole Dance Kleidung`, Ebene 2 = `Bodysuits` — das wies dem Artikel nur die Unterkategorie zu, nicht beide. JTL-Ameise bietet **keine zusätzlichen Kategorie-Spalten** in der Stammdaten-CSV — der Multi-Kategorie-Mechanismus geht ausschließlich über doppelte Zeilen.

*Recherche-Belege (5 Forum-Threads übereinstimmend, zuletzt April 2025):*
- Forum-Zitat: „Pro Kategoriezuordnung benötigt der Artikel eine eigene Zeile in der CSV."
- Forum-Zitat: „Die Einstellung für die Kategorien steht standardmäßig auf 'Nicht aktualisieren'. Die muss umgestellt werden."
- Forum-Zitat: „Deine Einstellung 'Neue Kategorien beim jeweiligen Artikel hinzuimportieren' ist vollkommen richtig. Du musst in deiner csv-datei aber 2 Zeilen haben mit der gleichen Artikelnummer."

*Entscheidung — Multi-Kategorie-Mechanik:*

CSV: **pro Artikel zwei Zeilen** (gleiche Artikelnummer) — eine pro Kategorie-Zuweisung:
```
Zeile A: Artikelnummer; ...; Kategorie Ebene 1 = "Pole Dance Kleidung";  Kategorie Ebene 2 = ""               ; ... (Oberkategorie)
Zeile B: Artikelnummer; ...; Kategorie Ebene 1 = "Pole Dance Kleidung";  Kategorie Ebene 2 = "Bodysuits"       ; ... (Unterkategorie)
```

Gilt **sowohl für Vater als auch für jedes Kind** (Kategorien werden in JTL pro Artikel gepflegt, nicht implizit vererbt). Resultierende CSV-Größe pro Modell: 1 Vater × 2 Zeilen + N Kinder × 2 Zeilen = 2 × (1 + N) Zeilen.

Ameise-Vorlagen-Setting (einmalig pro Lieferanten-Vorlage zu setzen, dann in der Vorlage gespeichert): **„Kategorieverknüpfungen des Artikels aktualisieren"** → Wert **„Neue Kategorien beim jeweiligen Artikel hinzuimportieren"**. Default-Wert „Nicht aktualisieren" macht die Doppelzeilen funktionslos.

*Wichtig — Setting-Name in der Tjorben-Ameise-Version (1.10.15.0):* Die Forum-Doku spricht von „Aktualisierung von Kategorien eines Artikels". In Tjorbens Ameise heißt die Einstellung **„Kategorieverknüpfungen des Artikels aktualisieren"**. Funktional identisch.

*Konsequenzen:*
- Stammdaten-CSV wird ungefähr doppelt so groß wie vorher (eine Vater-Zeile + N Kind-Zeilen → 2 × (1 + N) Zeilen pro Modell).
- Beim Pre-22-Modell-Test mit 5 Modellen × ~5 Größen ≈ 30 Datenzeilen × 2 = ~60 Zeilen statt vorher ~30.
- Beim 22-Modell-Vollauf entsprechend ~22 × 6 × 2 ≈ 264 Datenzeilen.
- Die Tjorben-Vorlage `HotCakes Polewear_1_Stammdaten` muss die Setting-Anpassung einmal gespeichert haben — gilt dann lieferanten-übergreifend, wenn die Vorlage geklont wird.

*Verworfen:*
- *Multi-Kategorie über zusätzliche Kategorie-Spalten („Kategorie Ebene 1 (1)", „Kategorie Ebene 1 (2)"):* von JTL-Ameise nicht unterstützt; mehrere Forum-Threads bestätigen das negativ.
- *Pfad-Notation in einer einzelnen Zelle (`Pole Dance Kleidung -> Bodysuits`):* würde nur die Unterkategorie setzen, nicht zwei separate Zuweisungen erzeugen.
- *Eigener Import-Typ „Artikelkategorien" zusätzlich zum Stammdaten-Import:* könnte funktionieren (Forum-Thread 9 erwähnt es), aber dann brauchen wir zwei separate CSVs und zwei Imports pro Lauf. Mehrere CSV-Zeilen im Stammdaten-Import sind die einfachst-mögliche Variante und im Forum mehrfach bestätigt.

---

**E69 — E52-Implementation in Cowork-CI und Datenimports-Spec verankern, A6 formell archivieren.**
*Stand:* 2026-05-16. Bezug: E52 (2026-05-15, CSVs lokal + present_files), A6 (Drive-Upload-Tool-Output-Limit), Lauf-Erfahrung 2026-05-16.

*Warum:* E52 hatte am 2026-05-15 schon entschieden: CSVs werden nicht mehr nach Drive hochgeladen, sondern bleiben im Cowork-Workspace und werden via `present_files`-Pattern an Tjorben ausgegeben. Die A6-Workaround-Mechanik (gzip + base64 + Chunking für `create_file`) ist damit obsolet. Aber: weder `cowork_custom_instructions.md` noch `cowork_anweisung_datenimports.md` haben das Drive-Upload-Verhalten entfernt — beide Files führen weiterhin „CSVs ablegen in `_PIPELINE > _Logs > .../`" auf. Im End-to-End-Lauf 2026-05-16 hat Cowork dementsprechend in Stage 4 einen Drive-Upload-Versuch gestartet, ist in das A6-Limit gelaufen und hat ~150 K Tokens auf b64-Chunking verbrannt, bevor der User per Override auf das E52-Pattern umgeleitet hat. Klassischer Drift zwischen Architektur-Entscheidung und Implementation in den Specs.

*Entscheidung:*
- `cowork_custom_instructions.md` Sektion „Output-Konventionen": CSVs gehen **in den Cowork-Workspace** (`/home/claude/outputs/`) und werden via `present_files` an Tjorben ausgegeben. Lauf-Bericht ebenfalls lokal, daneben. Drive-Upload für CSVs entfällt komplett.
- `cowork_anweisung_datenimports.md` Stage 7: gleiche Konvention.
- `run_brief_daten.md` Sektion 13 (Output-Konvention): auf E52-Pattern angepasst.
- `BACKLOG.md` A6: von „ARCHIVIERT 2026-05-15 durch E52-Pivot" auf „**FINAL GELÖST mit E69 (2026-05-16)** — Drive-Upload-Pfad in Specs entfernt, Drift behoben".

*Konsequenzen:*
- Stage 4 läuft jetzt in ~5 s statt potenziell 90+ s mit Sackgassen-Risiko.
- Kein b64-Chunking mehr. Keine A6-relevanten Token-Verbrauchsspitzen.
- Lieferanten-Ordner-Struktur in Drive (`_PIPELINE > _Logs > .../`) wird für Daten-Läufe nicht mehr beschrieben. Bei späterem manuellen Archivieren kann Tjorben die CSVs händisch hochladen, wenn er sie dauerhaft in Drive will.

*Verworfen:*
- *A6-Workaround stabilisieren statt entfernen:* widerspricht E52, würde die Token-Kosten nur reduzieren, nicht eliminieren.
- *Beide Pfade parallel anbieten (Drive + lokal):* schafft Wahl-Logik in Cowork, die wieder verbrennt. Eine Architektur, klar entschieden.

---

**E89 — Category-Pattern + Sara-Review-Workflow.**
*Stand:* 2026-05-18 (v1.19). *Bezug:* E51 (Kategoriebaum-Mapping), E57 (Multi-Kategorie via mehrfache CSV-Zeilen, präzisiert hier), B55 (Klärung mit Tjorben 2026-05-18), HotCakes-Run-Report 2026-05-18 (Note N2, Screenshot 1).

*Warum:* Im HotCakes-Run 2026-05-18 wurde sichtbar, dass das v1.15-Doppelzeilen-Pattern aus E57 (eine Zeile mit Oberkategorie `Pole Dance Kleidung`, eine Zeile mit Unterkategorie `Pole Dance Tops`) in WaWi nicht als Hierarchie-Pfad gelesen wird, sondern als zwei parallele Tag-Zuweisungen auf gleicher Ebene. Screenshot zeigte Artikel mit beiden Tags flach nebeneinander statt als Baum-Pfad. Plus: bei der Tjorben-Klärung kam ein neuer Use-Case dazu — Social-Media-Managerin Sara braucht eine WaWi-interne Kategorie `Intern > Neue Artikel für Sara` (Key 546) als Review-Inbox für jeden neuen Artikel.

*Entscheidung:*
- **Pro Artikel-Kategorie-Zuweisung in der Stammdaten-CSV nur die spezifischste Unterkategorie** (z.B. `Pole Dance Tops`, nicht parallel `Pole Dance Kleidung`). WaWi resolved den Pfad über die in WaWi gepflegte Kategorie-Hierarchie selbst. Keine parallele Oberkategorie-Zeile mehr.
- **Pflicht-Zuweisung für jeden neuen Artikel** in `Intern > Neue Artikel für Sara` (WaWi-Kategorie-Key `546`) — eine zweite CSV-Zeile mit gleicher `Artikelnummer` und dieser Kategorie. Sara prüft den Artikel im WaWi-Backend und entfernt die `546`-Zuweisung manuell nach Approval. Damit entsteht ein einfacher Review-Workflow ohne zusätzliche WaWi-Felder oder externes Tooling.
- Mindest-Set pro Artikel: **2 Kategorie-Zeilen** (Shop-Subkategorie + Sara-546). Weitere Marketing-Tag-Zuweisungen erlaubt → mehr Zeilen.
- Vorlagen-Setting unverändert: „Kategorieverknüpfungen des Artikels aktualisieren" = „Neue Kategorien beim jeweiligen Artikel hinzuimportieren" (E57). E75-Anti-Confusion (Doppelzeilen-Bug-Report-Lehre) weiter gültig: bei „doppelte Größen"-Bug-Reports erst Vorlagen-Setting prüfen, nicht Spec-Fix.

*Konsequenzen:*
- `run_brief_daten.md` Sektion 10 (Stammdaten-Spezifika): explizite Anweisung für Multi-Kategorie mit nur Subkategorie + Sara-546-Zeile.
- `SPEC_KONSTANTEN.md` Self-Check Punkt 4 umformuliert auf neues Pattern (mindestens 2 Zeilen, spezifischste Subkategorie + Sara-546).
- E57 bleibt gültig im Sinne von „mehrere CSV-Zeilen pro Artikel mit gleicher Artikelnummer", aber die Inhalts-Semantik pro Zeile ändert sich: jede Zeile ist eine spezifische Kategorie, nicht mehr Oberkategorie + Unterkategorie als zwei parallele Tags.
- Sara hat einen klaren Review-Indikator in WaWi (Filter auf Kategorie 546 listet alle noch nicht abgenommenen neuen Artikel).
- Self-Check-Spalte „Multi-Kategorie 2× Pflicht" bleibt erhalten, aber die zwei Zeilen sind jetzt (a) Shop-Subkategorie + (b) Sara-546, nicht mehr Ober + Unter.

*Verworfen:*
- *Pfad-Notation in einer Zelle (`Pole Dance Kleidung > Pole Dance Tops`):* nicht von Ameise unterstützt (bereits in E57 verworfen).
- *Eigener Sara-Workflow über separates WaWi-Attribut (z.B. `review_pending: true`):* würde WaWi-Konvention sprengen, keine native Filter-Möglichkeit. Kategorie ist bestehende Mechanik.
- *Sara-Zuweisung dem Anti-Pattern „Cowork pflegt WaWi-Status-Felder" zuschlagen:* Charter Prinzip 3 sagt „Cowork schreibt nichts in WaWi" — aber das bezieht sich auf API-Schreib-Calls, nicht auf CSV-Zellen-Werte. Eine Kategorie-Zuweisung via Ameise-CSV ist normale Pipeline-Mechanik. Sara entfernt manuell, das ist der menschliche Loop.
- *Auf Sara-Email als Workflow-Trigger statt WaWi-Kategorie:* fragmentiert die Tools. Sara arbeitet eh in WaWi für Social-Media-Vorbereitung, die Inbox-Liste ist genau dort sichtbar wo sie sie braucht.

*Stolperfallen:*
- **Sara muss die 546-Zuweisung wirklich manuell entfernen** — sonst akkumuliert die Kategorie und der Review-Loop wird unbrauchbar. Tjorben-Konvention: jede Sara-Approval = Zuweisung weg. Audit pro Quartal über WaWi-Filter empfohlen.
- **Wenn WaWi-Hierarchie sich ändert (z.B. neue Unterkategorie eingeführt):** Pipeline muss die neue Kategorie kennen. SPEC_KONSTANTEN Sektion 3 oder lieferanten_mapping.yaml gegebenenfalls erweitern.

---

**E90 — F2-F6-Implementierung in v1.19 (Sammeleintrag).**
*Stand:* 2026-05-18 (v1.19). *Bezug:* HotCakes-Run-Report 2026-05-18 (Notes N1-N6, Screenshots), BACKLOG B55-B59 (Tjorben-Klärungen 2026-05-18 durch).

*Warum:* HotCakes-Run-Report 2026-05-18 hatte sieben offene Findings F1-F7. Tjorben hat in der Klärungs-Session am 2026-05-18 für F2-F6 konkrete Antworten gegeben. v1.19 setzt diese als Architektur-Entscheidungen / Spec-Updates um. F1 (SPEC_KONSTANTEN Performance-Split) und F7 (Drive-Karteileichen-Cleanup) sind in v1.19 deferred bzw. als manuelle Aktion gelistet.

*Entscheidung (zusammengefasst):*
- **F2 → E89** (siehe oben): Category-Pattern + Sara-Workflow als eigenständige Architektur-Entscheidung formalisiert.
- **F3 (B56) → lieferanten_mapping.yaml:** neues Feld `article_weight_kg: 0.05` pro Lieferant. Stammdaten-CSV-Spalten `Artikelgewicht` und `Versandgewicht` mit DE-Locale-Komma `0,05` befüllen.
- **F4 (B57) → run_brief_daten.md Sektion 9.3:** HTML-Entity-Regression behoben. Latin-1-Umlaute (ß, ä, ö, ü, é, à etc.) bleiben Unicode im UTF-8-Output. HTML-Entities NUR für Zeichen außerhalb Latin-1 (z.B. ✓ = `&#10004;`, ➔ = `&#10148;`). SPEC_KONSTANTEN Sektion 5 + AP7 sind bereits kanonisch korrekt; der Bug saß in `run_brief_daten.md` Zeile 319 (alte Regel „deutsche Umlaute als `&uuml;` etc." — falsch, korrigiert).
- **F5 (B58) → run_brief_daten.md Sektion 7 + SPEC_KONSTANTEN Sektion 11:** „Unser Model trägt..." raus aus `size_and_fit`. Statt dessen Modelname aus Crawl-Body ziehen (z.B. Yifan, Vika, Elena bei HotCakes). Bei mehreren Models pro Artikel: erstes Model im Crawl-Body. Bei null Modelname: „Das Model trägt..." oder Phrase weglassen.
- **F6 (B59) → lieferanten_mapping.yaml:** neues Feld `taric_code: '62114390'` pro Lieferant (TARIC für Pole-Bekleidung). Stammdaten-CSV-Spalte `TARIC` (Sonstiges-Reiter in WaWi).

*Konsequenzen:*
- `lieferanten_mapping.yaml` wächst pro Lieferant um 2 Felder (`article_weight_kg`, `taric_code`). Schema-Doku am Ende der YAML erweitert.
- `run_brief_daten.md` Header v1.15 → v1.16, neuer „Was v1.16 ändert"-Block.
- `SPEC_KONSTANTEN.md` Header-Spec-Bezug auf v1.19-Snapshot aktualisiert (Sektion 11 size_and_fit-Modelname + Self-Check #4 Multi-Kategorie + E87/E89/E90 in Sektion 14).
- BACKLOG B55 → erledigt v1.19 (→ E89), B56-B59 → erledigt v1.19, B60 → erledigt v1.19 (manuelle Tjorben-Aktion in Drive, 3 IDs in Manifest gelistet).

*Verworfen:*
- *F-Fixes verstreut über mehrere E-Einträge schreiben:* würde den Cluster aufblähen. Ein Sammeleintrag verweist auf BACKLOG-IDs, die die konkrete Klärung halten.
- *F1 (Performance-Split SPEC_KONSTANTEN) im v1.19-Build mitnehmen:* in der neuen Git-Welt ist >50 KB kein Upload-Killer mehr (siehe E87), nur noch ein Lesbarkeits-Hinweis. Split-Aufwand ohne aktuellen Mehrwert; deferred auf v1.20+, Re-Evaluation wenn Cowork-Resolver auf GitHub umgestellt ist (B63).
- *F7 (Drive-Karteileichen) automatisch lösen:* Drive-MCP fehlt `delete_file` (B33). Manuelle Aktion durch Tjorben bleibt; v1.19-Manifest listet die 3 Drive-IDs.

*Folgeaufgaben:*
- B61, B62, B63 (alle NEU v1.19) — siehe BACKLOG.md.

---

