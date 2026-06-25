# Backlog: Strategische Entscheidungsbedarfe

**Stand:** v1.21, 2026-05-18 (Trial-Findings v1.20 → v1.21-Refactor E92+E93: B49 teilvalidiert durch Override im Trial 2026-05-18 21:06, B36-B40 deferred-Status auf gelöst-durch-Reaktivierung, B66 + B67 neu für v1.21-Validierung). · **Vorheriger Stand:** v1.20 (Skalierungs-Refactor, B63 erledigt). · Älteste Einträge B1-B53 aus v1.17 (Live-Trial).

> **Hinweis ab v1.20:** Erledigte und deferred B-Einträge stehen kompakt als Index in `BACKLOG-ARCHIV.md`. Diese Datei enthält weiter alle Details — ARCHIV gibt nur schnelle Übersicht „was ist nicht mehr aktiv".

Offene Punkte, die *Entscheidungen* brauchen — nicht Tasks. Tasks gehören in die Pipeline. Sortiert nach Priorität.

## Hoch — vor Produktiv-Schalten zu entscheiden

**B4 — A-Nummer-Strategie: wann kippen?**
Aktuell ist Artikelnummer = Lieferantenartikelnummer. Wann lohnt sich die Umstellung auf eigene A-Nummern? Mögliche Trigger: Lieferanten-Wechsel bei gleichem Artikel, Lieferant ändert sein SKU-Schema, Marken-Diskussion mit dem Lieferanten, Wachstum auf >X Artikel. Migration für bestehende Artikel braucht Plan.

**B17 — Buchhaltungs-Connector für Lieferanten-Referenztabelle.**
Stand: 2026-05-13. Bezug: E23. Vorbedingung für B18.
Offene Fragen:
- Welches Buchhaltungssystem läuft bei Verticalo? (DATEV / Lexware / sevDesk / Buchhaltungsbutler / andere?) → bestimmt den Connector-Aufwand erheblich. Anfrage an Chef läuft.
- Format der Referenztabelle: CSV in Drive vs. live-gelesenes Google Sheet vs. direkter API-Pull aus Buchhaltung?
- Update-Frequenz: pro Wareneingang automatisch, monatlich Batch, manuell auf Knopfdruck?

**B18 — Initial-Befüllung der zwei Referenztabellen.**
Stand: 2026-05-13. Bezug: E23.
Aufgaben:
- `lieferanten_zoll_versand.csv`: Erstexport für die ~5 wichtigsten Lieferanten anhand der letzten 20 Rechnungen pro Lieferant. Verantwortlich: Tjorben (Datenzugriff) + Claude (Aggregation/Format).
- `warengruppen_aufschlag.csv`: Tjorben exportiert die aktuelle Aufschlagsfaktoren-Logik aus dem System. Claude leitet daraus die Tabelle ab. *Zwischenstand 2026-05-13:* erste Version v0.1 aus JTL-Export abgeleitet, muss noch auf 2-Cluster-Logik (Kleidung + Technik) konsolidiert und mit preisabhängiger Marge-Kurve versehen werden.
- Physische Ablage der Tabellen klären (in Abstimmung mit B17).

**B68 — GLD enthält nur Waren-EK, nicht Zoll/Versand/Bankgebühren → Marge verzerrt. Interim +4€ auf VK. — NEU 2026-06-18**
Stand: 2026-06-18. Bezug: B17, B18, E23, E98.
Problem: Der GLD (Ø-EK netto, Basis für den Brutto-VK) enthält aktuell nur den Waren-EK. **Zoll, Versandkosten und Bankgebühren** (z.B. AUD-Auslandsüberweisung) fehlen → GLD zu niedrig → bei VK = EK×2 ist die Marge verzerrt, wir nehmen weniger ein als nötig.
Interim-Maßnahme (E98, aktiv seit 2026-06-18): zwei Hebel. (a) **VK-Schutz differenziert nach Herkunft** — Nicht-EU **+5,00 EUR auf den Brutto-VK**, EU/EUR **+1,00 EUR auf den EK** (via ×2 in den VK). (b) **GLD-Kosten-Aufschlag +2,30 EUR/Stück** auf den Ø-EK/GLD (gegen die verzerrte Buchhaltungs-Marge), nur GLD nicht VK. Beide bis die echten Kostenanteile vorliegen.
Zukunft (zu diskutieren): pro Lieferant **historische Mittelwerte** (Zoll/Versand/Bankgebühren aus den letzten N Rechnungen) ins `lieferanten_mapping.yaml` aufnehmen und in die GLD/VK-Kalkulation einfließen lassen — knüpft direkt an B17/B18 (`lieferanten_zoll_versand.csv`) an, erweitert um Bankgebühren. Offene Entscheidung: pauschaler Aufschlag vs. echte Kostentabelle pro Lieferant vs. Mix; und ob der Aufschlag in den GLD oder (wie jetzt) direkt in den VK fließt.

**B19 — WaWi-Merkmalswerte als Validierungs-Quelle.**
Stand: 2026-05-14. Bezug: E19, Charter-Prinzip 7.
Hintergrund: JTL-Export *Artikelmerkmale* vom 13.05.2026 zeigt die real existierenden Merkmalsnamen und deren erlaubte Werte (`Farbe Kleidung`, `Größe Kleidung`, `Style Tops`, `Style Shorts` plus UI-Extras). Cowork generiert teils Werte, die nicht im WaWi-Bestand sind — z.B. "Style Bodysuits" existiert nicht als Merkmalsname, Bodysuits werden über `Style Tops` mit Werten wie "Bodysuit" gepflegt.
Aufgabe: Datei `Wichtig: Claude Backup/wawi_merkmalswerte.yaml` aus dem Export ableiten. Schema pro Merkmalsname: Liste erlaubter Werte (aktuell belegt + UI-Extras). Cowork validiert in Stage 6 (Validierung vor Output) jeden generierten Merkmalswert gegen diese Liste. Lauf abbrechen bei Treffer außerhalb. Regenerieren bei nennenswerten WaWi-Änderungen.

**B20 — Konflikt-Auflösung zwischen WAWI-IMPORT-WISSEN und ENTSCHEIDUNGS-LOG.**
Stand: 2026-05-14.
Hintergrund: Im POLE-ADDICT-Pilot wurde in der WAWI-IMPORT-WISSEN.md aufgenommen, dass Kinder die Merkmale vom Vater erben (Abschnitt 5, Aussage "Kinder erben Merkmale vom Vater automatisch in WaWi"). Validierung durch JTL-Export 13.05.2026 zeigt aber: Merkmale stehen explizit auf Vater UND auf jedem Kind. Die alte Aussage wurde in WAWI-IMPORT-WISSEN.md korrigiert. Aber: das wirft die Frage auf, wie systematisch die Datei mit dem ENTSCHEIDUNGS-LOG abgeglichen wird.
Aufgabe: Quartalsweise Review-Pass — WAWI-IMPORT-WISSEN-Behauptungen gegen ENTSCHEIDUNGS-LOG-Eintrage prüfen. Bei Konflikt: ENTSCHEIDUNGS-LOG ist die Wahrheit (dort steht das Warum + die Validierungsquelle), WAWI-IMPORT-WISSEN ist die operative Spiegelung des Wahrheitsstands.

**B21 — Verkaufskanal-Aktivierung beim Import steuerbar machen.**
Stand: 2026-05-14. Bezug: Custom Instructions B5 (zusammenhängend), E37.
Hintergrund: Beim Stammdaten-Import gehen Artikel sofort online, weil in der Ameise-Importvorlage rechts oben im Bereich "Verkaufskanal aktiv" alle Häkchen (polesportshop.de, poledanceshop.de, Mobile Kasse) defaultmäßig gesetzt sind. Aktueller Workaround beim HotCakes-Import war: Häkchen in der Vorlage entfernen, dann manuell pro Artikel aktivieren wenn reviewt (in E37 als Konvention etabliert).
Aufgabe: Cowork erzeugt in der Stammdaten-CSV pro Verkaufskanal eine Spalte mit Default "N" — z.B. `polesportshop.de aktiv`, `poledanceshop.de aktiv`, `Mobile Kasse aktiv`. Tjorben aktiviert pro Artikel im Shop-Review oder per Massen-Update in WaWi. Vorteil: deterministisch pro Artikel, nicht abhängig von Importvorlagen-Standardwerten.
Hinweis: nicht zu verwechseln mit B5 (Plattform-Aktivierung der Bilder) — B5 ist mit E46 gelöst. B21 betrifft das Einschalten des Artikels selbst pro Verkaufskanal, nicht der Bilder.

**B22 — R2-Migration und R2-Upload in Bildpipeline als Default verankern. — TEILGELÖST 2026-05-15**
Stand: 2026-05-15. Bezug: E10, E40, E42, E43, E44, E46.
Hintergrund (bis 2026-05-15): Der HotCakes-Bildpipeline-Versuch am 2026-05-14 lief mit direkten Hersteller-CDN-URLs (E40-Übergangslösung). Cowork-Setup-Session 2026-05-15 hat zwei Lösungspfade evaluiert:
- *Pfad (a) S3-MCP via Local-MCP-Bridge gegen R2-Endpoint* — Probe 2026-05-15 mit `@modelcontextprotocol/server-filesystem`: Cowork-UI zeigt "Server disconnected"-Banner, kein Tool-Namespace sichtbar. Bridge tot für Cowork-Pipelines, siehe E42. **Verworfen.**
- *Pfad (b) Code-Execution + boto3 + Network-Egress-Allowlist + Drive-File-Credentials* — funktioniert mit Cowork-Standard-Capabilities, sauber unter E33 (Credentials in Drive-File mit eingeschränktem Zugriff, nicht im Chat). **Gewählt — siehe E43.**

Status der Sub-Items (2026-05-15):
- ✅ Egress-Allowlist user-konfigurierbar via Settings → Capabilities → „Additional allowed domains" (verifiziert in Settings-Screenshots 2026-05-15). Aktueller Pilot-Stand: Allowlist-Modus „All domains" wegen Anthropic-Bug, siehe B29.
- ✅ Drive-File-Credentials: `r2_credentials.json` in dediziertem Drive-Sub-Ordner `_Credentials` (`1r8dSh1qh72ABuFlfjsEXZ8f3W3oWtIXc`) unter `Artikelanlage Bilder Pipeline` mit Permissions nur für Tjorben.
- ✅ `cowork_anweisung_bildpipeline.md` v1.3 spezifiziert die Mechanik (R2-Upload-Sektion).
- ✅ Cleanup: `test-filesystem`-Probe-Eintrag aus `claude_desktop_config.json` entfernt.
- ✅ R2-Upload-Pfad erstmals End-to-End validiert mit Arachne-Bottom-Black: 4 verarbeitete Shop-Bilder auf R2 unter `hotcakes/HC-Arachne-Bottom-Black_NN_HOTCAKES_2026-05-15.jpg`, 4 Originale auf R2 unter `originals/hotcakes/...`.
- ✅ Migration der HotCakes-Arachne-Bottom-Black-Bilder auf R2-URLs erfolgreich (5 Artikel: Vater + 4 Kinder).
- ✅ Bilder im Shop sichtbar auf allen 9 Plattformen via Stammdaten-Re-Import (E46-Mechanik).

Offene Aufgaben (Rest):
- ~~Hekate Bodysuit + Arachne Top Black: Bild-Beschaffung steht aus — Anti-Bot beim 2026-05-14er Versuch hatte das blockiert.~~ **Korrektur 2026-05-15 Abend (E48-Lauf):** war kein Anti-Bot. Erste End-to-End-Validierung mit Arachne Top Black per Crawl-Modus B (Shopify-Storefront-JSON, E48) lief problemlos durch — HTTP 200, sauberer Download, 4 Bilder auf R2 migriert. Die wahrscheinliche Ursache des 2026-05-14er Fehlschlags: Sandbox-Egress-Limitierung in der damals noch granular konfigurierten Allowlist (vor B29-Workaround). Hekate Bodysuit + die restlichen 19 Modelle aus HotCakes-Rechnung 00034 können per E48-Pfad ohne technischen Blocker nachgezogen werden.
- Check für POLE ADDICT — ob deren Bilder im Shop schon auf R2 zeigen oder auf POLE-ADDICT-CDN. Falls letzteres: POLE-ADDICT-Stammdaten-Vorlage um Bild-Spalten erweitern und Re-Import durchführen.

**B23 — MCP-Connector-Inventur im Cowork-Projekt. — WEITGEHEND ERLEDIGT 2026-05-15**
Stand: 2026-05-15. Bezug: E33.
Hintergrund: Cowork-Setup-Session 2026-05-15 hat die Connector-Inventur tatsächlich durchgeführt — Cloudflare-Developer-Platform-Connector verbunden, vollständige Tool-Inventur abgelegt unter `_PIPELINE/_Logs/2026-05-15_crawl-tool-evaluation/cloudflare_inventur.md` (25 Tools, R2-Block deckt nur Bucket-Lifecycle ab, kein Object-PUT). Probe-Result zur Local-MCP-Bridge unter `local_mcp_probe_result.md` im selben Ordner.
Status sichtbare MCP-Server in Cowork (aus Probe-Result):
- Cloud-Connectors: Google Drive, Cloudflare Developer Platform
- System-MCPs: Cowork (Artefakte/Directories), Workspace (Bash/web_fetch), Claude-in-Chrome (deferred), MCP-Registry, Plugins, Scheduled-Tasks, Session-Info, Skills, Visualize
- Keine user-konfigurierten Local-MCP-Server sichtbar (Bridge tot, E42).
Restaufgabe: Bei jedem zukünftigen Spec-Update neue Tool-Annahme gegen Cowork-Realität abgleichen, bevor sie schriftlich verankert wird (Charter Prinzip 9 mit konkreten Probe-Mechanismen).

**B25 — Crawl-Tool-Verfügbarkeit in Anthropic-Registry beobachten. — NEU 2026-05-15**
Stand: 2026-05-15. Bezug: E14, E41.
Hintergrund: Firecrawl bleibt nach Marktcheck 2026-05 strategisch beste Wahl (Marktführer beim Web-Crawling, beste Anti-Bot-Performance, größte Tool-Vielfalt im MCP-Ökosystem). Aktuell aber nicht als nativer Cowork-Connector in der Anthropic-Registry verfügbar. Pilot läuft ohne autonomen Crawl-Modus — Drive-Upload/Excel/PDF/Mail/Hybrid (5 von 6 Input-Modi) decken die nächsten Lieferanten ab.
Aufgabe: Anthropic-Registry periodisch prüfen (alle ~4 Wochen oder bei größeren Anthropic-Announcements). Sobald Firecrawl als Connector auftaucht: in Cowork verbinden, Crawl-Modus in `cowork_anweisung_datenimports.md` reaktivieren. Alternative Crawl-Tools (Tavily, Brightdata) wurden bewusst nicht ad-hoc getestet — wäre Wegwerf-Arbeit, wenn Firecrawl in Wochen kommt (E41).
Trigger zur Re-Evaluation: Wenn ein konkreter Lieferant nur über Crawl erreichbar ist UND Firecrawl noch nicht nativ verfügbar ist, neu bewerten.

**B26 — Cloudflare-Code-Mode-MCP-Server beobachten. — NEU 2026-05-15**
Stand: 2026-05-15. Bezug: E10, E43.
Hintergrund: Cloudflare betreibt zwei MCP-Server: `bindings.mcp.cloudflare.com/mcp` (Workers-Bindings, was wir aktuell als Connector haben — deckt nur Bucket-Lifecycle ab, siehe cloudflare_inventur.md) und `mcp.cloudflare.com/mcp` (Code-Mode mit `search()` + `execute()`-Tools, der via JavaScript-Snippets die volle Cloudflare-API erreicht — inkl. R2-Object-Operationen). Der Code-Mode-Server ist aktuell nicht in der Anthropic-Cowork-Registry angeboten.
Aufgabe: Beobachten, ob Cloudflare-Code-Mode-MCP als zweiter Cloudflare-Connector in die Cowork-Registry aufgenommen wird. Wenn ja: B22 würde sich vermutlich direkt darüber lösen lassen (R2-Object-Ops via execute(), keine boto3-Sandbox-Mechanik mehr nötig). Migration in `cowork_anweisung_bildpipeline.md` wäre Rewrite der R2-Upload-Sektion.

**B27 — Migration zu Cloudflare-Worker-Proxy für R2-Credentials. — NEU 2026-05-15 (Reserve)**
Stand: 2026-05-15. Bezug: E43.
Hintergrund: Der Pilot nutzt Drive-File-Credentials (Pfad b von E43). Architektonisch ist das die einfachst-mögliche Variante, die noch funktioniert (Charter Prinzip 9). Aber: Blast-Radius im Worst-Case ist die volle R2-API (Bucket-Pollution, Object-Delete). Eine sauberere Architektur wäre ein eigener Cloudflare-Worker mit R2-Binding, der Upload-Requests von Cowork mit Bearer-Token-Auth annimmt. R2-Credentials leben dann nur im Worker-Setup; ein kompromittierter Worker-Token bricht nur Upload, nicht S3-API.
Trigger zur Re-Evaluation: Wenn (a) >5 Lieferanten produktiv laufen und R2-Volume wächst, ODER (b) ein zweiter User Cowork-Pipelines triggern soll (Multi-User-Setup mit Permission-Trennung), ODER (c) ein Drive-Sicherheitsvorfall passiert. Bis dahin nicht angehen — Worker-Code zu schreiben + zu deployen ist Aufwand ohne aktuellen Mehrwert.

**B33 — Drive-MCP fehlt update_file und delete_file. — NEU 2026-05-15, verschärft v1.15 (2026-05-17)**
Stand: 2026-05-17. Bezug: A5, AP10.
Symptom: Im 3-Modell-Batch-Lauf 2026-05-15 erneut bestätigt — Drive-MCP-Connector kennt nur `create_file`, `copy_file`, `download_file_content`, `read_file_content`, `search_files`, `list_recent_files`, `get_file_metadata`, `get_file_permissions`. Es gibt **kein** `update_file` und kein `delete_file`. Bestehende Files können nicht überschrieben oder gelöscht werden.

Konkreter Schaden im 3-Modell-Batch (A6-Vorgängerproblem):
- Cowork hat partielle 4_Attribute-CSV in Drive abgelegt
- Konnte sie weder löschen noch überschreiben — musste mit Placeholder-Datei und „FULL"-Suffix arbeiten
- Tjorben musste die korrekte Version manuell aus dem Workspace hochladen und die partiellen Files manuell löschen

**Neuer Schaden v1.15 (2026-05-17, Live-Trial Batch 1):** Cowork hat AP10-Verstoß begangen und 3 korrupte CSVs in `2026-05-17_HOTCAKES_batch1/`-Drive-Ordner geladen. Die korrupten Files können wegen fehlendem `delete_file` nicht von Cowork bereinigt werden. Tjorben muss sie manuell in Drive-UI löschen — oder den ganzen Ordner mit den korrupten Files (eventuell zusammen mit dem Erfolg-Ordner) verschieben/löschen. Workaround dokumentiert in AP10.

Aktuelle Workarounds:
- Versionierter Naming bei jedem Upload (Datum + Suffix)
- Manuelles Cleanup durch Tjorben pro Lauf
- Für CSVs gilt ab v1.8 der A6-Pivot (lokal statt Drive) → Problem entschärft
- v1.15 AP10 verschärft: KEIN Drive-Upload mehr für CSVs/Berichte (auch nicht zu Archivzwecken). Bug-Beleg vom 2026-05-17 zeigt, dass das echte Risiko ist.

Offene Aufgabe (Feature-Wunsch):
- Anthropic Drive-MCP-Connector-Erweiterung anfragen (`update_file`, `delete_file`)
- ALTERNATIV: eigenen Workspace-Worker mit direkter Drive-API-Anbindung bauen (analog zu B27 für R2)
- Priorität: niedrig — Workaround ist akzeptabel, A6-Pivot reduziert den Pain weiter

Trigger zur Re-Evaluation: wenn Drive-Berichte regelmäßig neu generiert werden müssen (z.B. bei iterativen Lauf-Verbesserungen), könnte das relevant werden.

**B34 — Originalbilder-Index für Social-Media-Bearbeitung. — NEU 2026-05-15**
Stand: 2026-05-15 Abend. Bezug: E44.
Hintergrund: Tjorbens Social-Media-Bearbeiterin braucht Zugriff auf die Original-Bilder pro Lieferant, sortiert nach Datum desc (neueste oben). Aktuell liegen die Originale auf R2 unter `originals/<lieferant>/<dateiname>_HOTCAKES_<datum>.{jpg|webp}` — flach, ohne Browser-fähiges Index.

Tjorbens Idee: einen Ordner-artigen Zugriff bauen, der die Original-Bilder pro Lieferant chronologisch listet.

Lösung in v1.8 verankert (cowork_anweisung_bildpipeline.md v1.6 Stage 6.5):
- Cowork generiert pro Lieferant nach jedem Bildpipeline-Lauf eine HTML-Index-Seite unter `originals/<lieferant>/_index.html`
- Die Seite listet alle Originale im Lieferanten-Prefix, sortiert nach Upload-Datum desc
- Pro Bild: Thumbnail-Preview + Dateiname + Upload-Datum + Direkt-Download-Link
- HTML-Datei wird bei jedem Lauf neu generiert (überschrieben) — immer up-to-date

Plus: Filename-Konvention auf **Sekundengenauigkeit** verschärft — `_HOTCAKES_2026-05-15_203045.jpg` statt `_HOTCAKES_2026-05-15.jpg`. Damit Sortierung auch bei mehreren Läufen am selben Tag funktioniert.

Aufgaben:
- Spec-Update in cowork_anweisung_bildpipeline.md v1.6 (gemacht)
- Validierung beim nächsten 3-Modell-Test-Lauf
- Bearbeiterin den Public-Link kommunizieren: `https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev/originals/<lieferant>/_index.html`

**B29 — Anthropic-Allowlist-Bug beobachten und granularen Modus reaktivieren. — NEU 2026-05-15**
Stand: 2026-05-15. Bezug: E43.
Hintergrund: Cowork-Settings → Capabilities → Network-Egress hat zwei Modi: „All domains" und „Package managers only" mit Möglichkeit, „Additional allowed domains" hinzuzufügen. Im Modus „Package managers only" wird die Additional-Liste **silent ignoriert** — d.h. eigentlich erlaubte Domains werden trotzdem geblockt. Anthropic-Bug-Issues #38984 und #51400 dokumentieren das Problem.
Pilot-Workaround (aktiv): Allowlist-Modus auf „All domains" gesetzt. Funktioniert für R2-Upload, aber unnötig breite Egress-Konfiguration.
Aufgabe: Anthropic-Bug-Tracker periodisch prüfen. Sobald Issues #38984 oder #51400 als „fixed" markiert sind: Allowlist zurück auf „Package managers only" stellen, granulare Liste hinzufügen mit:
- `d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com` (R2-Endpoint, PUT/HEAD/DELETE gegen Bucket)
- `pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev` (R2-Public-URL für Smoke-Checks)
- Hersteller-CDN-Domains pro Lieferant (z.B. `cdn.shopify.com` für HotCakes/POLE-ADDICT, je nach Bild-Quelle)
- `pypi.org` und `files.pythonhosted.org` (für boto3-Installation in der Sandbox — werden vom „Package managers only"-Modus eh erlaubt)
- Falls Firecrawl aktiviert: `api.firecrawl.dev`
Trigger zur Re-Evaluation: Anthropic-Announcement zum Fix, oder eigener Test auf Stichprobenbasis.

**B30 — Re-Import-Verhalten bei leeren Bild-Spalten verifizieren. — NEU 2026-05-15**
Stand: 2026-05-15. Bezug: E46.
Hintergrund: Mit E46 hat die Stammdaten-CSV 10 Bild-Spalten am Ende. Wenn ein Artikel weniger als 10 Bilder hat, sind die übrigen Spalten leer. Beim Re-Import eines bestehenden Artikels mit leeren Bild-Spalten ist das JTL-Verhalten nicht eindeutig dokumentiert:
- *Verhalten A (gewünscht):* Leerer Wert = kein Update, vorhandenes Bild im Slot bleibt erhalten.
- *Verhalten B (problematisch):* Leerer Wert = Slot wird aktiv geleert, vorhandenes Bild verschwindet.
Aufgabe: Mit einem späteren Lauf testen — Lieferant mit weniger als 10 Bildern pro Artikel (z.B. 3-6 Bilder typisch für Mode) durchspielen, dann Re-Import mit denselben Daten. Schauen ob Slots 4-10 leer bleiben oder bestehende Bilder gelöscht werden.
Falls Verhalten B: in der Ameise-Vorlage prüfen, ob es eine Option „leere Werte beim Update ignorieren" gibt (Standardwert pro Spalte oder Vorlage-Setting). Falls keine Option: Cowork-Logik anpassen, leere Bild-Spalten dürfen nicht in der CSV erscheinen (dann auch keine fixe 10-Spalten-Default-Konvention mehr, sondern dynamisch).
Trigger: Nächster Fashion-Lauf mit weniger als 10 Bildern pro Artikel.

**B35 — Bild-Größen-Cap < 100 KB für v2.0-Bildpipeline. — NEU 2026-05-15**
Stand: 2026-05-15 spätabends. Bezug: E60, E45.
Hintergrund: Tjorben hat im 3-Modell-Cowork-Batch (Hekate, Arachne, Savanna) festgestellt, dass R2-Bilder mit komplexen Texturen (Marble-Print, Foto-Realismus) bei der etablierten JPEG-Quality (Q=85) durchschnittlich 150-175 KB groß sind. Der polesportshop-Shop-Stack zeigt ab ~100 KB Performance-Einbußen bei Listing-Seiten (Page-Load + Mobile-Bandbreite). Die aktuellen R2-Bilder der 3 Pilot-Modelle sind betroffen.
Aufgabe (Implementierung in v2.0-Bildpipeline-Spec):
- Cap-Mechanik in Stage 4 (JPEG-Export) hinzufügen: Initial-Quality 85, iterativ -5 reduzieren bis < 100 KB ODER Quality-Floor 70 erreicht.
- Bei Quality-Floor-Hit: warnen im Lauf-Bericht (Bild möglicherweise sichtbar matschig), Lauf nicht abbrechen.
- Resize-Strategie bleibt unverändert (Crop-Profile-Output-Dimensions wie in E45).
- Im Lauf-Bericht pro Bild: Final-Quality + Final-Filegröße ausweisen.
Migration: bestehende R2-Bilder der 3 Pilot-Modelle (Hekate, Arachne Bottom Teal, Savanna Original Top) müssen bei v2.0-Bildpipeline-Lauf re-encodiert werden. URLs bleiben gleich (R2 überschreibt nach Key), Stammdaten-CSV muss nicht neu generiert werden.
Trigger: parallel zum nächsten Bildpipeline-Lauf des Pre-22-Modell-Tests.

## Mittel — innerhalb der ersten 2-3 Monate

**B6 — Mehrsprachigkeits-Qualitätssicherung.**
Italienisch, Französisch, Spanisch werden von Claude übersetzt. Ohne Native-Reviewer ist die Qualität nicht messbar. Optionen: Stichproben-Review durch externe Übersetzer, Kundenfeedback abwarten, Native-Reviewer pro Sprache fest engagieren. Risiko: peinliche Übersetzungs-Fehler bleiben unentdeckt im Shop.

**B7 — Quality-Tracking-Mechanismus.**
Wie messen wir Konvergenz des iterativen Loops? Anzahl Shop-Korrekturen pro Lauf? Fehler-Kategorien? Ohne Tracking ist "die Pipeline wird besser" Gefühl statt Faktum. Trigger für Übergang Pilot → Produktiv unklar.

**B8 — Lieferanten-Onboarding-Prozess.**
Neuer Lieferant kommt → wer pflegt den Eintrag in `lieferanten_mapping.yaml`? Wer entscheidet über Standard-Pflegehinweise, Markentext, Steuerklasse? Aktuell ad-hoc. Bei 50 Lieferanten braucht's ein Checklisten-Template — was muss vor dem ersten Lauf befüllt sein, was kann später nachgepflegt werden.
Update 2026-05-15: Mit E45 kommen drei neue Felder ins Mapping (`category`, `crop_profile`, `pose_sort`). Diese müssen Teil des Onboarding-Checklisten-Templates sein.
Update v1.15 (2026-05-17): Plus optional `max_groesse` (Default-Größen-Cap pro Lieferant). Beim Onboarding entscheiden ob Lieferant Standard-Vollsortiment hat oder ein Cap braucht.

**B9 — Stil-Definition für eigene Beschreibungstexte. (Teilweise gelöst durch E22.)**
Status: 80-20-Stilprofil ist in E22 fixiert und fließt in cowork_anweisung_datenimports.md v1.3 ein. Offen bleibt die finale CI-Schärfung (Tonalitäts-Feintuning pro Produktkategorie, Marken-spezifische Vorgaben, ggf. Sprach-Adaption — siehe auch B14).

**B10 — Backup-Strategie für R2 und Drive.**
Wenn R2 ausfällt, sind die Originale jetzt auch auf R2 (E44) — Single Point of Failure. Wenn Drive ausfällt, sind die Anweisungen weg. Wenn Cowork-Account gelöscht wird, sind die Anweisungen weg? Die Anweisungen liegen ja redundant in Drive `Wichtig: Claude Backup/` und als Custom-Instructions im Anthropic-Projekt — beide Quellen könnten theoretisch wegfallen. Versionierung der Anweisungen als Git-Repo sinnvoll?
Update 2026-05-15: Mit E44 sind Originale jetzt vollständig auf R2 (statt teilweise in Drive). Backup-Strategie für R2 selbst (bucket-zu-bucket-Replikation oder ähnliches) wird wichtiger — siehe Risiken-Sektion am Ende.

**B16 — Cloud-Storage-Connector-Strategie.**
Stand: 2026-05-13. Bezug: E21.
Offene Fragen:
- Soll Cowork einen dedizierten Dropbox-MCP-Connector pflegen?
- Welche anderen Cloud-Quellen kommen bei Lieferanten häufig vor (WeTransfer, Google Drive, OneDrive)?
- Bei welchem Volumen lohnt sich Custom-Integration vs. manueller Workaround?
Trigger zur Re-Evaluation: Wenn ≥3 Lieferanten Assets über Cloud-Storage liefern.

## Niedrig — nice-to-have, nicht blockend

**B11 — Multi-User-Pipeline-Nutzung.**
Wenn ein Praktikant oder zweiter Einkäufer die Pipeline triggern soll, braucht es Trigger-Templates und Onboarding. Aktuell nur Tjorben.

**B12 — Wochen-/Monats-Reporting.**
Cowork könnte einen periodischen Bericht generieren (X Artikel angelegt, Y Lieferanten, Z Fehler). Nice für Reflexion und Geschäftsführung, nicht blockend für Pipeline-Funktion.

**B13 — A/B-Testing eigener Texte vs. Lieferanten-Texte.**
Hypothese ist, dass eigener Stil Conversion-stärker ist. Ist nicht validiert. Wenn ja, lohnt sich der Aufwand. Wenn nein, wäre Discovery + Lieferanten-Text-Übernahme effizienter.

**B14 — Internationalisierung des Shop-Stils.**
Aktuell wird DE-Stil 1:1 in andere Sprachen übersetzt. Kann sein, dass der italienische Markt einen anderen Tonalitäts-Code hat. Stil-Adaption pro Sprache wäre möglich, ist aber deutlich mehr Aufwand. Mit E73 (v1.13) wird das wichtiger: alle 5 Sprachen voll ausformuliert pro Artikel, also wird Tonalität pro Sprache überhaupt erst sichtbar.

**B31 — Snapshot-Pattern im Praxis-Betrieb validieren.**
Stand: 2026-05-15. Bezug: E47.
Aufgabe: Bei den ersten 3-5 echten Wissens-Updates nach E47 beobachten, ob die Immutable-Snapshot-Architektur unter Real-Bedingungen hält. Beobachtungspunkte:
- Hält die Resolution-Strategie auch bei vielen Sub-Ordnern (>30) noch schnell? Drive-API-Latenz für `search_files` mit Sort?
- Was passiert bei einem echten Stream-Abbruch mitten in einem Lauf — wird der unvollständige Sub-Ordner beim nächsten Resolve sauber ignoriert?
- Funktioniert die Manifest-Hash-Verifikation als Drift-Detektion in der Praxis?
- Findet Cowork den aktuellen Snapshot ohne Spec-Nachbesserung?

Trigger zur Re-Evaluation: Nach dem dritten echten Wissens-Update — Erkenntnisse in einer kurzen Snapshot-Review-Notiz festhalten und ggf. die Architektur nachschärfen.

Update v1.15: nach v1.12, v1.13, v1.14, v1.15-Snapshots ist die Architektur stabil. Resolution-Strategie funktioniert weiter. Datenpunkt für Review-Notiz: 4 Wissens-Updates ohne Strukturprobleme.

**B32 — Legacy-Files in Wichtig: Claude Backup aufräumen.**
Stand: 2026-05-15. Bezug: E47.
Hintergrund: vor E47 lagen die 8 Wissens-Files direkt im Live-Ordner `Wichtig: Claude Backup/`. Plus es liegt eine `Untitled`-Karteileiche (Drive-ID `1HAGOII4VrcGqLtDLrRluTwcexl_pxkUb`) aus einem abgebrochenen v1.3-Draft-Versuch im Live-Ordner.

Mit E47 sind diese Files nicht mehr referenziert. Die Resolution-Strategie filtert auf Sub-Ordner mit `title contains 'Version_'`, also stören die Legacy-Files die Auto-Resolution nicht. Aber sie sind visuell verwirrend im Drive-Web-UI.

Aufgabe: Tjorben kann die 8 Legacy-Files plus die `Untitled`-Datei bei Gelegenheit manuell in einen Sub-Ordner `_Pre_E47_Legacy/` verschieben oder direkt löschen. Kein Zeitdruck — nur Kosmetik. Resolution funktioniert auch mit Karteileichen im Live-Ordner sauber.

Trigger zur Re-Evaluation: keiner — wann immer Tjorben Lust auf Aufräumen hat.

---

## Anomalien (separat von Entscheidungen)

Beobachtete Tool- oder Plattform-Eigenheiten, die kein Entscheidungsbedarf sind, aber Workarounds erfordern und dokumentiert sein müssen.

**A1 — Drive-MCP-Size-Limit für `download_file_content`.**
Stand: 2026-05-15. Bezug: E44.
Symptom: JPEG-Originale zwischen 130 und 500 KB sprengen das Token-Budget der Drive-Connector-Calls, weil die Datei base64-codiert in den Tool-Response geladen wird. Lauf scheitert mit Token-Overflow.
Workaround: Originale gehen jetzt direkt nach R2 (E44), Drive wird nur noch für kleine Files (CSVs, Markdown-Specs, YAML-Configs) genutzt. Keine großen Binärdateien mehr via Drive-MCP.

**A2 — Shopify-CDN-Content-Negotiation.**
Stand: 2026-05-15. Bezug: E44, E48. **OPERATIONAL LESSON LEARNED — Magic-Byte-Detection ist Pflicht, nicht optional.**
Symptom: Shopify-Hosted-Lieferanten-Shops (HotCakes, Pole Junkie) liefern auf `*.jpg`-URLs Bytes mit Content-Type `image/webp`, wenn Accept-Header WebP zulässt. URL-Endung ist nicht verlässlich, Content-Type-Header ist auch nicht verlässlich. **Validiert 2026-05-15 mit HotCakes-Arachne-Top-Black-Lauf:** 2 von 4 Bildern kamen als webp zurück, obwohl URL `.jpg` war. Ohne Magic-Byte-Detection wären die Originale falsch benannt im R2 gelandet.
Workaround (Pflicht, nicht optional): Magic-Byte-Detection für Original-Extension (siehe cowork_anweisung_bildpipeline.md). Plus: Accept-Header `image/jpeg, image/png, image/webp;q=0.5, */*;q=0.1` beim Download, damit Shopify in vielen Fällen ein echtes JPEG liefert. Für verarbeitete Bilder ist es egal (Pillow konvertiert intern auf JPEG), für Originale entscheidend.

**A3 — Anti-Bot-Treffer ohne klare Unterscheidung zum Sandbox-Tunnel-Block.**
Stand: 2026-05-15. Bezug: E20, E40, E48, B22.
Symptom: Bei Hersteller-Shop-Crawls/Downloads kann der Request fehlschlagen aus zwei Gründen mit ähnlichem Response-Pattern: (a) echter Anti-Bot-Block (Cloudflare-Challenge, Server-Side-Block) oder (b) Sandbox-Egress-Tunnel-Block (Cowork-Network-Config oder Anthropic-Allowlist-Bug). Bei B22 hat sich 2026-05-15 herausgestellt, dass der 2026-05-14er „Anti-Bot"-Verdacht eigentlich (b) war.
Workaround: Bei Fehler **erst** Egress-Allowlist und Sandbox-Net prüfen, **dann** erst Anti-Bot annehmen. Disambiguierung: bei (b) gibt's typischerweise einen DNS- oder Connection-Error vor dem HTTP-Handshake; bei (a) kommt ein vollständiger HTTP-Response (oft 403 oder 200 mit Challenge-Body). Fallback-Reihenfolge (Retailer → Hersteller → Halt) gilt für echten Anti-Bot, nicht für Egress-Probleme.

**A4 — JTL-Multi-Row-Import-Quirk bei Bilder-Slot-Mapping.**
Stand: 2026-05-15. Bezug: E46.
Symptom: Beim Bilder-Import-Versuch mit mehreren Zeilen pro Artikel (Pattern: `Artikelnummer;Bildnummer;Bild-URL`, 4 Zeilen pro Artikel), alle gemappt auf JTL-Feld `Bild Pfad/URL 1`, landet nur das **letzte** Bild im Slot mit Plattform-Aktivierung. Die ersten 3 Bilder sind zwar am Artikel hinterlegt, aber „verwaist" — kein Slot, keine Plattform-Aktivierung.
Workaround: nicht mehr relevant — Bilder kommen jetzt über die Stammdaten-CSV mit eigenen Spalten `Bild 1` bis `Bild 10` (E46). Pattern A (horizontal) wäre theoretische Alternative, ist aber redundant zur Stammdaten-Integration.

**A5 — Kein `update_file` im Drive-MCP-Connector, daher versionierte Berichte über `create_file`.**
Stand: 2026-05-15.
Symptom: Der Drive-MCP-Connector bietet `create_file`, `copy_file`, `download_file_content`, `read_file_content`, `search_files`, `list_recent_files`, `get_file_metadata`, `get_file_permissions` — aber **kein** `update_file` oder `delete_file`. Bestehende Files können also nicht in-place überschrieben oder gelöscht werden.
Workaround: 
- Für Berichte und Logs: bei jedem Update ein neues File mit versioniertem Namen anlegen (z.B. `run_2026-05-15_hotcakes_v2.md`). Alte Versionen bleiben als Audit-Spur erhalten.
- Für Wissens-Files: Snapshot-Pattern E47 mit Sub-Ordner-Versionierung umgeht das Limit komplett.
- Konvention: Claude legt keine neuen Wissens-File-Versionen in Drive an — Drive-Schreibvorgänge werden vom User durchgeführt nach Edit-Runde.
- Drive-MCP-Feature-Wunsch dokumentiert in B33.

**A6 — Drive-Upload-Tool-Output-Limit bei großen CSVs. — FINAL GELÖST mit E69 (2026-05-16)**
Stand: 2026-05-16. Bezug: E52, E69.
Symptom (historisch): Drive-MCP `create_file` mit `base64Content` für CSVs >~80 KB sprengt das Tool-Output-Limit von ~50 K Zeichen. Bei der 3-Modell-Batch-Attribute-CSV (107 KB) führte das zu partial-Uploads (~25 % der Daten) und Placeholder-Workarounds.
Lösung (E52 entschieden 2026-05-15, **E69 final gelöst 2026-05-16**): CSVs und Lauf-Berichte landen nur noch im Cowork-Workspace `/home/claude/outputs/`, Tjorben downloadet direkt im Chat via `present_files`-Pattern. Kein Drive-Upload mehr, daher kein Tool-Output-Limit-Problem. Drift in Cowork-CI und Datenimports-Spec mit v1.12 behoben (E69), nachdem E52-Drift im Pilot-Lauf 2026-05-16 noch zu 150K verbrannten Tokens auf b64-Chunking-Versuche geführt hat.
Status: **final gelöst, nicht mehr aktiv. Workaround-Code (gzip+base64+Chunking) wird nicht mehr ausgeführt.**

**A7 — Drive-MCP-Connector-Instabilität bei Folder-Anlage und seriellen File-Uploads.**
Stand: 2026-05-16. Bezug: E64.
Symptom: Am 2026-05-16 scheiterten drei aufeinanderfolgende Versuche, einen Snapshot-Sub-Ordner via Drive-MCP `create_file` (`mimeType='application/vnd.google-apps.folder'`) anzulegen und anschließend 9-11 Files seriell hochzuladen. Fehlerbild: Timeouts, Fail-Loops auf Folge-Operationen, kein diagnostisch verwertbares API-Fehler-Detail im Tool-Response. Read-Operationen (`download_file_content`, `search_files`, `list_recent_files`) waren im selben Zeitfenster zuverlässig.
Workaround: E64 — lokaler Wissens-Update-Workflow als Default. Tjorben legt Sub-Ordner manuell in Drive an, Drag-and-Drop für die Files. Drive-MCP-Schreiboperationen für Wissens-Updates nur noch im Fallback. Cowork-Pfad (Read-only auf Wissens-Files, Write auf CSVs/Logs in Lieferanten-Ordner) ist nicht betroffen, da Cowork keine Sub-Ordner anlegt und nur einzelne Files schreibt.

Trend-Tracking: Wenn das Symptom in den folgenden Wochen abklingt, A7 als „transient, beobachtet" markieren. Wenn es wiederkommt: B33 (Drive-MCP-Feature-Wunsch) um Reliability-Aspekt erweitern und ggf. mit Anthropic-Support melden.

Update v1.15 (2026-05-17): A7 ist nach v1.12-v1.15-Erfahrung wieder akut — Drive-MCP-Folder-Anlage hat in Live-Trial-Run-Sessions mehrfach gehakt. Drive-direkt-Schreiben (kompletter Snapshot via `create_file` mit `textContent`) funktioniert dagegen zuverlässig. Bestätigt E64-Pivot.

**A8 — Cowork-interne Sub-Agent-Extraction-Schwelle bei ~50 KB.**
Stand: 2026-05-16. Bezug: E68.
Symptom: Files über etwa 50 KB werden von Cowork in Stage 0 nicht direkt im Cache gehalten und gelesen, sondern durch eine interne **Sub-Agent-Extraction-Stufe** geleitet. Cowork startet pro betroffenes File parallele LLM-Sub-Agents, die „relevante Sektionen" extrahieren. Das frisst pro File mehrere Minuten Wallclock und nicht-trivial Token. Symptom war reproduzierbar im ersten End-to-End-Daten-Lauf 2026-05-16 mit `WAWI-IMPORT-WISSEN.md` (56 KB) und `cowork_anweisung_datenimports.md` (52 KB) — der Lauf brach nach >30 Min ab.
Workaround (Mitigation): **E68** — Selective Spec-Loading + Pre-Compiled Run-Brief. Für reine Daten-Läufe wird die operative Essenz der zwei großen Files in `run_brief_daten.md` (~15 KB, klar unter Schwelle) gehalten. Die Original-Files bleiben im Snapshot als Referenz für Lazy-Load bei tiefen Klärungs-Situationen.
Aus dem Klärungs-Chat **nicht direkt abschaltbar** — ist Cowork-internes Verhalten. Wenn künftige Cowork-Versionen das ändern (höhere Schwelle oder konfigurierbar): A8 entsprechend reklassifizieren.

Trend-Tracking: bei jedem Lauf-Bericht prüfen, ob Sub-Agent-Extraction trotz Run-Brief getriggert wurde. Wenn ja: Bug-Signal, Files sind zu groß geworden oder Schwelle hat sich gesenkt.

**A9 — Falsch-Diagnose E57-Doppelzeilen als Spec-Bug. — ARCHIVIERT mit E75 (2026-05-16)**
Stand: 2026-05-16 (gleicher Tag wie Entdeckung und Lösung). Bezug: E57, E75.
Symptom (historisch): Im Klärungs-Chat 2026-05-16 nach dem v1.12-Baseline-Lauf las Tjorben „doppelte Größen" in der importierten CSV als Bug-Symptom. Claude diagnostizierte voreilig die E57-Doppelzeilen-Architektur als Spec-Bug und bot eine korrigierte CSV mit halbierter Zeilenzahl (29 statt 58). Beim Spec-Cross-Check stellte sich heraus: E57 ist Forum-recherchiert und Re-Import-validiert. Goldstandard-CSV `1_Stammdaten_HotCakes_2026-05-16.csv` hat ebenfalls Doppelzeilen und wurde sauber importiert. Die tatsächliche Ursache lag in einem Vorlagen-Setting in WaWi (bzw. war beim Re-Test nicht reproduzierbar — Tjorbens Setting war korrekt).
Lösung: **E75 Anti-Confusion-Note** an drei Stellen (`WAWI-IMPORT-WISSEN.md`, `SPEC_KONSTANTEN.md` Self-Check Punkt 4, hier in A9). Lehre: bei vermuteten Spec-Bugs zuerst Spec-Cross-Check via grep nach dem Pattern in LOG + WAWI-IMPORT-WISSEN, bevor Fix-CSVs gebaut werden. Charter-Prinzip 10 wurde durch die Selbstkorrektur eingehalten — Diagnose-Antibody-Failure ist transparent dokumentiert.
Status: archiviert, Anti-Confusion-Note an drei Stellen aktiv. Sollte das Symptom wieder auftauchen: A9 reaktivieren und prüfen, ob das WaWi-Setting unter bestimmten Bedingungen verloren geht.

---

---

## Architektur-Refactor Themen (v1.10, 2026-05-16, ausgelöst durch E63)

### Bilder-Architektur-Refactor (Cluster)

**B36 — Pose-Sortierung: Vision-Klassifikation vs deterministisches Fallback. — NEU 2026-05-16**
Bezug: E45 (Pose-Sortierung), E63 (Pipeline archiviert).
Frage: Brauchen wir Vision-API-Calls überhaupt, oder reicht deterministisches Naming (z.B. Lieferanten-Konvention „file_001 = Front, file_002 = Rück")? Pilot-Beobachtung: viele Lieferanten haben konsistente Datei-Namens-Konventionen. Vision-Calls kosten pro Bild und sind unzuverlässig bei dreiviertel-Posen.
Optionen:
- (a) Vision-Klassifikation behalten, Fallback bei `unknown` auf manuelle Sortierung.
- (b) Vision komplett ersetzen durch Lieferanten-Konvention im `lieferanten_mapping.yaml` (Feld `pose_sort: filename_convention` mit Regex).
- (c) Hybrid: erst Filename-Pattern versuchen, dann Vision als Fallback.
Entscheidung offen, blockt Reaktivierung der Bildpipeline.

**B37 — Bilder-Storage: R2 vs WaWi-eigenes Bilder-Verzeichnis vs Hybrid. — NEU 2026-05-16**
Bezug: E44 (R2 als vollständiger Storage), E63.
Frage: Ist R2 als externe Quelle in WaWi der richtige Weg, oder wäre es operativ einfacher, Bilder direkt in WaWi's eigenes Bild-Verzeichnis hochzuladen (Drag-and-Drop in WaWi-UI)? Das ist genau das, was Tjorben aktuell manuell macht.
Trade-Offs:
- R2: stabile Public-URLs, schnelles Hosting, Vendor-Lock-in, Bild-Migration aller Artikel bei R2-Wechsel.
- WaWi-Bilder: kein externes Hosting, alles im WaWi-Stack, dafür WaWi-Backup-Größe wächst, Plattform-Aktivierung über Reiter Bilder/Plattformen wie bisher.
- Hybrid: Originale auf R2 (Social-Media-Zugriff über `_index.html`, E44), Verarbeitete in WaWi.
Entscheidung offen, hängt an B36-Klärung und B27 (Worker-Proxy-Architektur).

**B38 — Bildpipeline Ausführungs-Ort: Cowork vs Mac-Daemon vs Cloudflare-Worker. — NEU 2026-05-16**
Bezug: E12, E43 (Code-Execution + boto3), E63.
Frage: Wo läuft die Bildpipeline am sinnvollsten?
- (a) Cowork (aktueller Stand bis E63): einfach, aber Token-teuer und blockiert Cowork's Daten-Pipeline-Flow.
- (b) Mac-Daemon auf Tjorbens Rechner: Bilder kommen lokal vom Lieferanten-Download an, Daemon verarbeitet im Hintergrund, lädt nach R2. Kein Cowork-Token-Verbrauch.
- (c) Cloudflare-Worker: serverless, eigene Latenz, Workers AI für Vision-Klassifikation günstig.
- (d) Hybrid: Crop/JPEG-Encoding lokal (Daemon), Vision-Klassifikation in Worker.
Entscheidung offen, hängt an Volumen-Schätzung und Tjorbens Mac-Verfügbarkeits-Toleranz.

### Bildpipeline-Performance (Cluster)

**B39 — JPEG-Quality-Iteration vs einmalige Cap-Strategie. — NEU 2026-05-16**
Bezug: E60 (Quality-Iteration), E63.
Frage: Ist iterative Quality-Reduktion (Q=85 → 80 → 75 → 70) bei jedem Bild der richtige Weg, oder kann das durch eine smartere Erst-Wahl (z.B. Quality basierend auf Bild-Komplexität geschätzt) ersetzt werden? Iteration kann pro Bild mehrere Sekunden kosten, bei 20-30 Bildern pro Lauf summiert es sich.
Optionen:
- (a) Iteration behalten (E60-Stand), Floor weiter Q=70.
- (b) Heuristik: bei komplexen Texturen (Marble, Foto-Realismus) direkt Q=75 statt Q=85 starten.
- (c) Vision-Pre-Pass schätzt Komplexität, dann adaptive Quality.
Entscheidung offen, niedrige Priorität bis Bildpipeline-Reaktivierung.

**B40 — Vision-Klassifikations-Latenz vs Batch-Verarbeitung. — NEU 2026-05-16**
Bezug: E45, B36.
Frage: Aktuelle Vision-Calls sind sequenziell (ein Bild zur Zeit). Bei 20-30 Bildern pro Lauf kostet das mehrere Minuten. Optionen:
- (a) Batch-Vision-Calls (mehrere Bilder pro Request).
- (b) Parallele Async-Calls.
- (c) Pre-Compute: Vision läuft beim ersten Original-Upload nach R2, Ergebnis wird gespeichert. Daten-Lauf liest nur das gespeicherte Resultat.
Entscheidung offen, niedrige Priorität bis Bildpipeline-Reaktivierung.

### R2-Status (Carry-over)

**B41 — R2-Migration der HotCakes-Bestandsbilder. — Carry-over aus v1.9-Risiko-Liste**
Bezug: B22 (HotCakes Arachne-Bottom-Black migriert, Rest offen), E63.
Status: Hekate Bodysuit und Arachne Top Black noch nicht migriert. Mit E63 läuft die Bildpipeline nicht mehr automatisch — Migration läuft entweder manuell oder wartet auf Architektur-Refactor. Tjorbens manuelle Pflege via WaWi-UI ist für jetzt akzeptiert.

### WaWi-Update-Validation

**B42 — Hypothese: Doppelter Ameise-Stammdaten-Import überschreibt nur Bild-Spalten. — NEU 2026-05-16**
Bezug: E46 (Bilder integriert in Stammdaten-Import), E63 (Bildpipeline manuell).
Frage: Wenn Tjorben Bilder manuell in WaWi pflegt und später die Stammdaten-CSV (mit leeren Bild-Spalten) erneut über Ameise importiert — überschreibt der Import die manuell gepflegten Bilder oder werden leere Bild-Spalten als „keine Änderung" interpretiert?
Hypothese (UNVERIFIZIERT): Ameise interpretiert leere Bild-Spalten als „keine Aktion", manuelle Bilder bleiben erhalten. Aber: bei Stammdaten-Update könnte ein anderes Verhalten greifen, je nach Ameise-Setting „Leere Werte überschreiben vorhandene Werte".
Validierung: Test-Lauf mit einem manuell bebilderten Artikel und Re-Import der Stammdaten-CSV mit leeren Bild-Spalten. Status: Pflicht-Test vor dem ersten produktiven Re-Import nach E63. Mitigation falls Hypothese falsch: Stammdaten-Vorlage muss Bild-Spalten als „nicht aktualisieren" konfigurieren, oder Cowork muss die Bild-Spalten ganz aus der CSV weglassen (Schema-Änderung).
Verwandt: B30 (Re-Import-Verhalten bei leeren Bild-Spalten — älter, aber gleiche Familie).

---

## Bekannte Risiken (separat von Entscheidungen)

- **Cloudflare R2 Vendor-Lock-in.** Wenn R2 teurer wird oder Bedingungen ändern, ist Migration aller Bild-URLs aufwändig (alle Artikel in WaWi müssten umgehängt werden). Mit E44 (Originale auch auf R2) ist die Abhängigkeit größer geworden — Originale wären auch betroffen.
- **firecrawl-Abhängigkeit.** Wenn firecrawl die Preise hochsetzt oder die Qualität abnimmt, brauchen wir eine Fallback-Strategie (eigenes Scraping? anderes Tool?). Akut entschärft, weil Crawl im Pilot geparkt ist (B25).
- **JTL-WaWi-Versions-Wechsel.** Pipeline ist auf 1.10.15.0 ausgelegt. Major-Update könnte Ameise-Vorlagen brechen.
- **Claude-Modell-Wechsel.** Wenn das zugrundeliegende Modell sich ändert (Cowork-Updates), kann die Übersetzungs- oder Beschreibungsqualität schwanken. Regression-Tests fehlen. Zusätzliches Risiko ab 2026-05-15: Vision-Klassifikations-Qualität (E45) könnte sich bei Modell-Wechsel ändern.
- **Buchhaltungs-Anbindung als neuer Single Point of Failure.** Sobald die Pricing-Architektur (E23) live ist, hängt die Preis-Korrektheit von der Aktualität der Referenztabellen ab. Veraltete Zoll-/Versand-Werte = systematisch falsche Preise. Mitigation: Update-Zyklus und Frische-Warnung als Teil von B17 mitdenken.
- **Zentralisiertes Lieferanten-Mapping als neue Abhängigkeit.** Mit E24 hängen beide Cowork-Pipelines an `lieferanten_mapping.yaml`. Wenn diese Datei nicht erreichbar ist oder fehlerhaftes YAML enthält, hält beides an. Mitigation: YAML-Syntaxcheck vor Drive-Upload; Backup-Kopie über Drive-Versionshistorie reicht für den Fall menschlicher Editier-Fehler.
- **Hersteller-CDN-URLs in Bildpipeline-Übergang.** Mit dem Arachne-Bottom-Black-Lauf 2026-05-15 ist die Übergangslösung beendet. Die restlichen HotCakes-Artikel (Hekate Bodysuit + Arachne Top Black) sind noch nicht migriert mangels Bild-Beschaffung — solange CDN-URLs aktiv sind, Risiko, dass Hersteller URL-Struktur ändert und Shop-Bilder kaputtgehen. Akut, aber durch laufende B22-Restarbeiten adressiert.
- **R2-Credentials in Drive-File als Pilot-Trade-off.** E43-Pfad legt Credentials in einem dedizierten Drive-Sub-Ordner mit Tjorben-only Permissions ab. Kompromittierung des Google-Accounts würde Credentials freisetzen. Akzeptiert für Pilot-Scope; Migration zu Worker-Proxy in B27 als Reserve. Mitigation: Drive-Permissions regelmäßig prüfen; bei Verdacht auf Account-Kompromittierung R2-Keys sofort in Cloudflare rotieren.
- **Annahme-getriebene Spec-Drift.** Specs verankern Tool- und Connector-Annahmen, die nicht verifiziert sind. Konkrete historische Fälle: „Cowork Secret Store" (existiert nicht, E33), Local-MCP via Desktop-Config-Bridge (für Cowork tot, E42), separater Bilder-Import via „Artikelbilder pro Plattform" mit mehreren Zeilen pro Artikel (skaliert nicht, E46). Mitigation: Charter Prinzip 9 mit Verifikations-Pattern „registrieren → fragen → bestätigen" (im Probe-Stil) bei jedem Spec-Update, das einen neuen Mechanismus annimmt — gilt auch für JTL-Mechanik-Annahmen, nicht nur für Cowork-Tools.
- **R2 als Single-Storage-Backbone nach E44.** Mit E44 liegen sowohl verarbeitete Bilder als auch Originale auf R2. Bei R2-Ausfall oder Account-Kompromittierung sind beide Quellen betroffen. Mitigation für Skalierung: Worker-Proxy (B27) reduziert Blast-Radius; eigene Backup-Strategie via bucket-zu-bucket-Replikation überlegen (B10 erweitert).
- **Vision-Klassifikations-Verlässlichkeit (NEU mit E45).** Pose-Sortierung hängt an Coworks interner Vision-Capability. Falls die Klassifikation systematisch danebenliegt (z.B. Detail-Aufnahmen mit Model im Hintergrund werden als `lifestyle` klassifiziert), erscheinen falsche Bilder als Hero im Shop. Mitigation: B28-Verifikations-Pass nach erstem produktiven Fashion-Lauf, Confidence-Schwelle ggf. anpassen, Fallback auf `manufacturer_order` für betroffene Lieferanten.
- **Anthropic-Allowlist-Bug (Issues #38984, #51400).** Pilot läuft mit „All domains"-Egress als Workaround, was unnötig breite Network-Konfiguration ist. Wenn der Bug länger ungefixt bleibt, akzeptieren wir das Risiko (siehe B29). Wenn weitere Side-Effects auftauchen (z.B. unbeabsichtigte Outbound-Calls): granulare Allowlist zurückholen auch ohne Fix, einzelne Domains manuell pflegen.
- **Manueller Bilder-Pflege-Overhead nach E63 (NEU 2026-05-16).** Mit Bildpipeline-Archivierung pflegt Tjorben Bilder pro Artikel manuell in WaWi. Bei steigendem Lieferanten-Volumen wird das zur Engpass. Mitigation: Architektur-Refactor (B36-B40) priorisieren sobald die Daten-Pipeline produktiv stabil ist. Volumen-Schwelle (z.B. „ab >50 Artikel/Woche") als Re-Aktivierungs-Trigger definieren.
- **Stammdaten-Re-Import-Verhalten unverifiziert (NEU 2026-05-16, B42).** Wenn manuell gepflegte Bilder durch Re-Import mit leeren Bild-Spalten überschrieben werden, gehen sie verloren. Akut: Pflicht-Test vor erstem produktiven Re-Import nach E63. Mitigation: bis B42 verifiziert ist, **keine** Stammdaten-Re-Imports auf bereits bebilderte Artikel ohne separaten Test-Lauf. Update v1.15: Live-Trial Batch 1+2 2026-05-17 hatten keine Re-Imports auf bestehende Artikel, daher noch nicht validiert. Bleibt offen.
- **Autonomie-Drift-Risiko durch E81 (NEU v1.15, 2026-05-17).** Mit E81-Autonomie kann Cowork operativ falsche Workflow-Entscheidungen treffen ohne User-Veto-Möglichkeit (Batch-Splitting zu grob/zu fein, Stage-Reihenfolge suboptimal, Token-Budget falsch geschätzt). Mitigation: Stage 0.5 Pre-Run Scope-Analyse (E83) muss im Lauf-Bericht dokumentiert sein, damit Tjorben Post-Hoc Drift erkennt und in nachfolgenden Läufen korrigiert. Bei mehrfacher Fehl-Autonomie: STOPP-Trigger-Liste erweitern.
- **E82-Stil-Drift bei großen Batches (NEU v1.15).** Mit E82-Verschärfung (Doppelpunkt + Meta-Einleitungen verboten) wird die Stil-Generierung anspruchsvoller. Risiko bei großen Batches: Cowork „ermüdet" und fällt in den alten Stil zurück (Doppelpunkte schleichen sich ein). Mitigation: Self-Check Punkt 13 prüft das pro Artikel; bei mehrfachen Fails Batch verkleinern oder Stil-Regel ins Prompt nachjustieren.
- **Cross-Selling-Zeilen-Explosion durch v1.15-Kinder-Replikation (NEU 2026-05-17).** Mit E80-Erweiterung wächst die Cross-Selling-CSV pro Beziehung von 2 auf 10 Zeilen (Faktor 5). Bei HotCakes Live-Trial: 36 Zeilen wurden 180. Bei einem Lieferanten mit dutzenden Modellen + dutzenden Farben kann die CSV in die Zehntausenden gehen. WaWi-Performance-Grenze unbekannt. Mitigation: B47 ist verschärft, Performance-Test bei >5000 Zeilen vorgesehen.

---

## Feature-Erfassung (Cluster, NEU 2026-05-16 mit E70)

Bewusst auf später vertagt. Tjorbens Disziplin: erst Kern-End-to-End-Run robust optimieren, nicht parallel die nächste Baustelle öffnen. Trigger-Bedingungen pro B-Eintrag.

**B44 — Vision-API-Feature-Extraktion evaluieren.**
Bezug: E70, E63, B-Cluster „Bilder-Architektur-Refactor".
Kontext: aktuell kommen Farb-, Style- und Material-Features ausschließlich aus Lieferanten-Texten (Shopify-Titel, Body_HTML). Visuelle Features, die im Text fehlen, werden nicht erfasst. Bewusste Pilot-Pragmatik.
Trigger-Bedingung für Eval: wenn Shop-Review zeigt, dass Style-Werte fehlen oder falsch sind, die im Bild offensichtlich gewesen wären (z.B. Riemchen, Spitze, Lace-Up); ODER wenn der dritte/vierte Lieferant onboardet wird und der Text-Qualitäts-Vergleich zu HotCakes signifikant schlechter ist.
Eval-Inhalt: (a) Optionen-Vergleich Cloudflare Workers AI vs. Anthropic Vision vs. OpenAI Vision, (b) Kosten pro Artikel-Bild kalkulieren, (c) Pilot-Probe-Lauf auf 10 Pole-Wear-Bildern mit Ground-Truth-Vergleich (Tjorben benennt korrekte Style-Werte), (d) Empfehlung zur Integration in Stage 2 (Daten extrahieren) oder als optionaler Sub-Step in Stage 5.5.

**B45 — Lieferanten-Text-Qualitäts-Indikator im `lieferanten_mapping.yaml`.**
Bezug: E70.
Kontext: HotCakes hat ordentliche Body_HTML-Texte. Andere Lieferanten könnten dünn sein. Cowork sollte pro Lieferant wissen, wie skeptisch er eigeninterpretieren darf vs. wann er stoppen sollte.
Vorschlag: neues optionales Feld `text_quality: rich | thin | minimal` pro Lieferant. Pflege beim Onboarding eines neuen Lieferanten, nach 1-2 Probe-Läufen. Cowork-Verhalten pro Stufe:
- `rich`: Eigeninterpretation erlaubt, im Bericht markieren
- `thin`: STOPP bei kritischen Features, User-Frage
- `minimal`: STOPP fast immer, fast alle Features brauchen User-Bestätigung
Trigger-Bedingung für Implementierung: zweiter Lieferant onboardet, Text-Qualität deutlich anders als HotCakes.

**B46 — Pole-Junkie-Cross-Reference für Features systematisieren (NEU mit E70).**
Bezug: E49, E53, E70.
Kontext: Pole Junkie ist seit E49 als Stil-Inspirations-Quelle für `artikeldetails` erlaubt, seit E70 auch als Feature-Cross-Reference. Aktuell hat Cowork aber keine systematische Logik dafür, **wann** Pole Junkie konsultiert werden soll (bei dünnem Hersteller-Text? Immer bei HotCakes? Nur bei bestimmten Lieferanten?). Heute (2026-05-16) keine konkrete Lücke aufgetreten, aber konzeptionell offen.
Trigger-Bedingung: wenn B45 implementiert ist, kann Pole-Junkie-Cross-Reference automatisch bei `text_quality: thin/minimal` aktiviert werden. Oder als manueller Override pro Lieferant im Mapping (`pole_junkie_cross_ref: auto | manual | off`).

---

## Cross-Selling-Skalierung (Cluster, NEU v1.14, 2026-05-16 mit E80, verschärft v1.15)

**B47 — Cross-Selling-Beziehungen-Volumen wächst quadratisch. — VERSCHÄRFT v1.15 (2026-05-17)**
Bezug: E80, Stage 5.8, E80-Erweiterung v1.15.
Kontext: pro Modell-Stamm mit N Farben generiert die „Ähnliche Artikel"-Logik N×(N-1) Beziehungs-Zeilen (jede Farbe verweist auf jede andere, beidseitig). Plus Outfit-Pairs. **Mit v1.15-Erweiterung (E80 Kinder-Replikation) wachsen die Zeilen pro Beziehung um Faktor 5** (Vater + 4 Kinder auf der linken Spalte). Bei HotCakes Live-Trial Batch 1+2 (21 Modelle): 36 Vater-Beziehungen wurden mit Kinder-Replikation zu 180 Zeilen. Hochrechnung für volles HotCakes-Sortiment mit 124 Produkten + breiterer Farb-Variation: schätzungsweise mehrere tausend Zeilen.

Bei einem Lieferanten mit dutzenden Modellen × dutzenden Farben kann die CSV in die Zehntausende gehen. WaWi-Performance-Grenze unbekannt; Ameise-Import-Wallclock skaliert linear, sollte handhabbar bleiben.

Trigger-Bedingung für Aktion: wenn ein Cross-Selling-Lauf >5000 Zeilen produziert (Schwelle gesenkt von 5000 auf 2000 mit v1.15-Erweiterung, da Zeilen jetzt um Faktor 5 schneller wachsen), einmaligen WaWi-Import-Performance-Test machen. Falls Ameise hängt oder DB merklich langsam wird: Plan B = nur Beziehungen innerhalb der aktuellen Lieferung schreiben (Pipeline-Option `cross_selling_scope: full | delivery_only` ins Mapping).

Plan C (NEU v1.15): nur Vater-Zeilen schreiben (linke Spalte ohne Kinder-Replikation) und WaWi-Mechanik prüfen, ob Cross-Selling-Anzeige auf Kindern dann über Vererbung greift. Hypothese ungeprüft.

**B48 — Farbnamen-Matching für „Ähnliche Artikel" zwischen Modell-Stämmen mit unterschiedlichen Farbbezeichnungen.**
Bezug: E80, E58.
Kontext: der Algorithmus matcht Farben über exakten String-Vergleich des Hersteller-Farbnamens. Wenn HotCakes ein Modell „Nude" und ein anderes „Beige" hat, sind das semantisch ähnliche Farben — aber der Algorithmus sieht sie als verschieden und liefert daher KEIN „Vervollständige Dein Outfit"-Pairing zwischen Peonies-Top-Nude und einer Bottom-Variante in Beige (falls die nur in Beige existiert). Heute (2026-05-16) kein konkreter Fall im HotCakes-Sortiment, aber latent.
Trigger-Bedingung für Aktion: wenn beim ersten Trial-Run mit 19 Modellen (Rechnung #00034) sichtbar wird, dass Outfit-Pairs durch Farb-Namens-Unterschiede verloren gehen. Mitigation: SPEC_KONSTANTEN Sektion 6 Sprach-Lookup um eine optionale Farb-Äquivalenz-Tabelle erweitern (z.B. `Nude ≈ Beige`, `Sky ≈ Hellblau`). Pflege pro Lieferant, weil Farb-Konvention herstellerspezifisch ist.

Update v1.15: Im Live-Trial 2026-05-17 hat die `(modell_basis, farbe_im_namen)`-Schlüssel-Logik den Outfit-Pair-Algorithmus präzise gemacht. B48 bleibt aber für Farb-Äquivalenz-Frage offen.

**B49 — Cross-Selling-CSV-Re-Import-Verhalten unverifiziert. — TEILVALIDIERT v1.15 (Initial-Import OK, Re-Import nicht getestet)**
Bezug: E80, B42.
Kontext: wenn beim zweiten Lauf für denselben Lieferanten der Cross-Selling-Import re-läuft, ist offen, ob WaWi (a) bestehende Beziehungen überschreibt, (b) neue Beziehungen anhängt ohne Duplikate-Check, (c) Duplikate als neue Einträge anlegt. JTL-Doku unklar. Risiko: Verdopplung der Beziehungen bei jedem Re-Import.

Update v1.15 (2026-05-17): Live-Trial Batch 1+2 hat die **v1.14-Mechanik bei Initial-Import validiert**:
- Batch 1: 10 Modelle, Cross-Selling-CSV importiert, 16/16 Self-Check grün
- Batch 2: 11 Modelle (mit Schwester-Beziehungen zu Batch 1), Cross-Selling-CSV mit 180 Zeilen importiert, 16/16 Self-Check grün
- Initial-Import-Mechanik (Vater + Kinder-Replikation, bidirektional, alle WaWi-Gruppen vorhanden) funktioniert produktiv

Was NOCH NICHT validiert ist:
- **Re-Import-Verhalten** auf bestehende Cross-Selling-Beziehungen (Batch 3 oder Refresh-Lauf für Family-Refresh-Modus, E80-Erweiterung 3)
- **Cross-Selling-Family-Refresh-Modus** (späterer Re-Lauf wenn Schwester-Artikel nachgezogen werden, siehe Schwester-Artikel-Liste B52)

Trigger-Bedingung für Verifikation: vor erstem produktiven Re-Import mit Cross-Selling auf bereits importierte Beziehungen. Sicherheitsmechanismus bis dahin: vor Re-Import alle Cross-Selling-Beziehungen des betroffenen Lieferanten in WaWi manuell löschen, dann frischer Import. Sobald verifiziert, Anweisung an Cowork-Lauf-Bericht.

*Update v1.21 (2026-05-18):* **Re-Import-Verhalten weiter unverifiziert, aber durch Trial-Lauf 2026-05-18 21:06 umgangen:** Tjorben hat die 21 Live-Trial-Modelle in WaWi gelöscht vor dem v1.20-Trial-Lauf, daher war es ein Initial-Import (kein Re-Import-Test). Cowork-Stage-0.5 hat den Re-Import-Schutz (STOPP-Trigger) ausgelöst, Tjorben hat manuell deaktiviert mit „behandle es als wäre es das erste Mal". → B49 bleibt offen, wird beim v1.21-Trial-Lauf erneut umgangen weil Artikel weiterhin gelöscht sind. Echter Re-Import-Test erst, wenn auf eine bestehende Anlage später eine zweite Lieferung mit Schwester-Artikeln drauf-importiert wird (B52-Family-Refresh-Trigger).

**B50 — Bodysuit-Outfit-Cross-Selling: aktuell ohne Pendant, soll perspektivisch zu Top oder Bottom mit gleichem Print vorgeschlagen werden?**
Bezug: E80, Tjorben-Direktive.
Kontext: der aktuelle Algorithmus generiert für Bodysuits keine „Vervollständige Dein Outfit"-Beziehung, weil sie kein direktes Pendant haben. Aber: wenn HotCakes einen Hekate-Bodysuit UND ein Hekate-Top + Hekate-Bottom hätte (gleicher Print), wäre eine Cross-Selling-Empfehlung sinnvoll. Heute (2026-05-16) keine konkrete Konstellation im Bestand, aber denkbar.
Trigger-Bedingung für Eval: wenn ein Lieferant das anbietet (z.B. Hekate-Print als Bodysuit + Top + Bottom). Mitigation-Option: dritte Cross-Selling-Gruppe „Im gleichen Print" oder Erweiterung der „Ähnliche Artikel"-Logik um Print-Match statt nur Farb-Match.

**B51 — Drive-Cleanup-Workaround für 3 korrupte HotCakes-Uploads in `2026-05-17_HOTCAKES_batch1/`. — NEU v1.15 (2026-05-17)**
Bezug: AP10, B33.
Hintergrund: Cowork hat im Live-Trial Batch 1 AP10-Verstoß begangen und 3 korrupte CSVs (Datei-Naming ohne Nummer-Präfix, AP11 ebenfalls verletzt) in den Drive-Ordner `2026-05-17_HOTCAKES_batch1/` geladen. Drive-MCP fehlt `delete_file` (B33), Cowork kann nicht aufräumen.
Workaround-Optionen für Tjorben:
- (a) Manuell in Drive-UI: 3 korrupte Files einzeln auswählen und löschen.
- (b) Ganzen Ordner verschieben/löschen, dann erneut anlegen mit den korrekten Files (aus Workspace-Re-Download wenn nötig).
- (c) Ordner umbenennen mit `_KORRUPT_NICHT_NUTZEN`-Suffix als Warnung, ohne zu löschen.
Empfehlung: (a) — minimaler Aufwand, klare Trennung.
Trigger-Bedingung: nächste Drive-Aufräum-Session.

**B52 — Schwester-Artikel-Liste für späteren Cross-Selling-Family-Refresh. — NEU v1.15 (2026-05-17)**
Bezug: E80-Erweiterung 3, B47.
Hintergrund: Bei den HotCakes Live-Trial-Runs Batch 1+2 wurden 21 Modelle angelegt. Es gibt aber Schwester-Artikel im HotCakes-Sortiment, die NICHT in der Lieferung waren und später nachgezogen werden können. Sobald nachgezogen, würde Cross-Selling-Family-Refresh-Modus sinnvoll werden, um die Beziehungen auf den bestehenden 21 Modellen UND den neuen Schwester-Artikeln vollständig zu aktualisieren.

Bekannte Schwester-Artikel (Stand 2026-05-17):
- **Arachne-Familie:** Tan, Cherry (Top + Bottom je) — gleicher Modell-Stamm wie die im Trial angelegten Arachne-Modelle, andere Farben
- **Savanna-Familie:** Black, Skin, Emerald, Lime, Heat (Top + Bottom je) — die im Trial angelegten Savanna-Modelle sind nur ein Teil; weitere Farben existieren
- **Peonies-Familie Bodysuit:** skin-tone Varianten (Nude/Beige/Mauve und ähnliche) als Bodysuit-Erweiterung

Trigger-Bedingung für Family-Refresh-Lauf: wenn Tjorben einen oder mehrere dieser Schwester-Artikel anlegt. Cowork führt dann einen separaten Cross-Selling-Family-Refresh-Lauf für die betroffenen Modell-Stämme aus (Trigger: `Verarbeite Cross-Selling-Refresh für HotCakes, Modell-Stamm Y`). Output: nur die aktualisierte 5_CrossSelling-CSV (AP12 schützt vor leeren CSVs falls Modell-Stamm zu eng gewählt).

**B53 — Skalierungs-Validierung Live-Trial-Architektur (Batch 1+2 erfolgreich, größere Batches offen). — NEU v1.15 (2026-05-17)**
Bezug: E80, E81, E83, E84, Stage 0.5 Pre-Run Scope-Analyse.
Hintergrund: Live-Trial-Runs Batch 1 (10 Modelle) + Batch 2 (11 Modelle) waren erfolgreich, jeweils 16/16 Self-Check grün. Stage 0.5 hat funktional gegriffen (Cowork hat autonom Batch-Aufteilung entschieden und im Bericht dokumentiert). E84-Familien-erhaltende Split-Regel hat funktioniert (Outfit-Pair-Familien blieben pro Batch zusammen, Cross-Selling-Stage 5.8 lief im letzten Batch über alle 21 Modelle vereint).

Was NOCH NICHT validiert ist:
- Batches >15 Modelle in einem Lauf (Token-Budget-Skalierung)
- Lieferanten mit deutlich anderem Profil (z.B. POLE ADDICT mit 80+ Artikeln, eventuell andere Modell-Stamm-Struktur)
- Stage 0.5 mit komplexerer Familien-Topologie (mehrstufige Modell-Stamm-Beziehungen)

Trigger-Bedingung: nächster Lieferanten-Onboarding mit >15 Modellen in einem Lauf ODER POLE ADDICT erster Lauf mit Cross-Selling.

## v1.18 — neue Einträge B54-B60 aus HotCakes-Run-Report 2026-05-18

**B54 — Cowork-Run-Performance: Snapshot-Resolution + Stage-0-Caching optimieren. — DEFERRED v1.19**
*Update v1.19 (2026-05-18):* SPEC_KONSTANTEN-Split in Git-Welt nicht zwingend. In der Drive-Welt war >50 KB der Tool-Limit-Killer (A9/A10/A11); in der Git-Welt ist >50 KB nur ein Lesbarkeits-Hinweis. Re-Evaluation wenn Cowork-Resolver auf GitHub-Raw umgestellt ist (B63, v1.20-Scope) und konkreter Pain im neuen Pfad auftritt. Bis dahin: Stand bleiben lassen, Diagnose-Anforderung (Stage-Timing-Probe) bei nächster Datenimports-Spec-Touch mitnehmen.
*Bezug:* HotCakes-Run-Report 2026-05-18 (Sektion 8, Notes N1+N6), Tool-Limit-Anomalie Stage 0, Sub-Agent-Detour für SPEC_KONSTANTEN.md (48 KB). *Stand v1.18:* offen, Priorität HOCH. *Stand v1.19:* deferred (Begründung siehe oben).
*Problem:* Stage 0 (Snapshot-Resolution + Spec-Caching) dauerte im HotCakes-Run ~3-5 Min und überstieg damit die in Stage 0.5 geschätzte Wallclock. Treiber: SPEC_KONSTANTEN.md (48 KB) und lieferanten_mapping.yaml (23 KB) brauchen den Sandbox-Pfad-Trick (E68), weil Drive-`read_file_content` über Cowork-Token-Limit. Sub-Agent-Extraktion summiert pro File 2-5 Min Overhead. Bei End-to-End mit 21 Artikeln frisst der Pre-Run ~25 % der Gesamt-Wallclock.
*Lösungs-Pfade (zu evaluieren in v1.19):*
1. SPEC_KONSTANTEN-Split: Sektionen 13+14 in eigenes File `SPEC_KONSTANTEN_SNAPSHOT_INDEX.md` (~5-10 KB) auslagern, Hauptfile unter 30 KB halten.
2. Parallel-Loading: SPEC_KONSTANTEN und YAML parallel statt sequenziell.
3. Sub-Agent-Pattern in `run_brief_daten.md` Sektion 1 als Standard dokumentieren — kein Versuch mehr mit direktem `read_file_content`.
*Diagnose-Anforderung für künftige Runs:* in `cowork_anweisung_datenimports.md` eine Stage-Timing-Probe einbauen, die pro File-Load die Wallclock dokumentiert (Manifest oder Lauf-Bericht).

## v1.19 — neue Einträge B61-B63 aus Pattern-Pivot Drive → Git (E87)

**B61 — WAWI-IMPORT-WISSEN.md Cluster-Split. — DEFERRED v1.19**
*Bezug:* WAWI-IMPORT-WISSEN.md 75060 B (>50 KB known-exception), v1.18-Manifest Sektion 9, E87 (Drive → Git Pivot).
*Stand:* deferred — in der Drive-Welt war >50 KB der Tool-Limit-Killer (A9/A10/A11), in der Git-Welt nur ein Lesbarkeits-Hinweis. Re-Evaluation:
- wenn konkreter Lesbarkeits-/Pflege-Pain in der Praxis auftritt
- wenn Cowork-Resolution auf GitHub-Raw umgestellt ist (B63) und sich zeigt, dass GitHub-Raw-Token-Verbrauch oder Cowork-Sub-Agent-Extraction-Schwelle für so große Files dort wieder problematisch wird
*Priorität:* niedrig.

**B62 — cowork_anweisung_datenimports.md Cluster-Split. — DEFERRED v1.19**
*Bezug:* cowork_anweisung_datenimports.md 73110 B (>50 KB known-exception), v1.18-Manifest Sektion 9, E87 (Drive → Git Pivot).
*Stand:* deferred — gleiche Begründung wie B61. In der Drive-Welt war >50 KB der Tool-Limit-Killer, in der Git-Welt nur ein Lesbarkeits-Hinweis. Re-Evaluation bei konkretem Pain oder nach B63-Migration.
*Priorität:* niedrig.

## v1.20 — neue Einträge B64+ aus Skalierungs-Refactor (E91)

**B64 — Brand-Story-Skalierungs-Pfad in `lieferanten_mapping.yaml`. — NEU v1.20, deferred bis N≥5 Lieferanten**
*Bezug:* `lieferanten_mapping.yaml` aktuell 25 KB bei 4 Lieferanten (1 aktiver), Brand-Story-Felder dominieren mit ~3 KB pro Lieferant in 5 Sprachen. Bei 20 Lieferanten Hochrechnung: ~250 KB Mapping-File (Brand-Stories ~60 KB davon allein).
*Stand:* offen, Priorität NIEDRIG bis N=5 aktive Lieferanten, dann hoch.
*Problem:* YAML-Lesen + Cache durch Cowork wird ineffizient. Pro Lauf wird das ganze YAML geladen, auch wenn nur 1 Lieferant gebraucht wird.
*Lösungs-Optionen (zu evaluieren wenn Trigger greift):*
1. **Brand-Story-Split:** `brand-stories/<kuerzel>.yaml` pro Lieferant, vom Mapping-YAML per `$include` referenziert (oder Cowork lädt zusätzlich pro Lauf das jeweilige Brand-Story-File).
2. **Mapping pro Lieferant in eigene Datei:** `lieferanten/<KUERZEL>.yaml`. Vollständig dezentralisiert, Mapping-Index zeigt nur Liste. Onboarding-Spec entsprechend anpassen.
3. **Inline behalten:** wenn YAML-Read in Cowork unproblematisch bei 250 KB ist (zu validieren), dann nichts ändern. Charter-Prinzip 9 (klein nach groß).
*Trigger zur Re-Evaluation:* bei Onboarding des 5. aktiven Lieferanten, oder bei messbarem Performance-Issue in Cowork-Stage-0 (`yaml.safe_load` >5 s).
*Priorität:* niedrig aktuell, hoch sobald Trigger greift.

**B65 — Probe-Test Cowork-`web_fetch` gegen GitHub-Raw — NEU v1.20**
*Bezug:* B63-Erledigung, E91, `cowork_custom_instructions.md` v2.0.
*Stand:* offen, Priorität HOCH, soll im ersten v1.20-Cowork-Daten-Lauf validiert werden.
*Problem:* Mit B63-Migration liest Cowork ab v1.20 die Wissens-Files über GitHub-Raw-URLs. Tool-Mechanik unbestätigt: kann Cowork `web_fetch` auf `https://raw.githubusercontent.com/...` URLs? Hat das Egress-Allowlist-Implikationen?
*Lösungs-Pfad:* beim ersten produktiven Cowork-Daten-Lauf nach v1.20-Push verifizieren. Im Lauf-Bericht dokumentieren: Stage 0 Wallclock, ob Raw-URLs erreichbar, ob Egress-Allowlist angepasst werden muss.
*Falls Issue:* Fallback: Tjorben kopiert die 3 Stage-0-Files in den Drive-Folder als temporäre Brücke, B63-Migration in v1.21 nachschärfen mit Auth/Allowlist-Klärung.
*Trigger zur Re-Evaluation:* erster Cowork-Lauf nach v1.20-Push.

*Update v1.21 (2026-05-18):* Trial-Lauf 2026-05-18 21:06 `run_2026-05-18_2106_HotCakes.md` hat B65 zumindest teilvalidiert — Cowork hat alle 4 GitHub-Raw-Files in 1,25 s parallelem `curl`-Batch geladen (HTTP 200, B65-Wallclock < 5 s Toleranz, "GitHub-Raw schlägt Drive-Connector um Faktor ~5"). **Aber:** das war über den Drive-Übergang oder mit Public-Repo (im Trial wurde das Repo public für den Lauf, oder Cowork hatte Auth). Repo ist aktuell privat (404 für anonyme Reads), daher: B65 bleibt bis zur sauberen Klärung der Auth-Mechanik offen. v1.21 nutzt weiter Drive-Übergang als Fallback (siehe v1.21-Manifest Aktion 1).

## v1.21 — neue Einträge B66+ aus Trial-Findings + Bildpipeline-Reaktivierung (E92, E93)

**B66 — Trial-Lauf-Wiederholung nach v1.21-Push (Validierung E92 + E93). — NEU v1.21**
*Bezug:* E92 (Multi-Kategorie 3-Zeilen + Farb-Lokalisierung DE), E93 (Bildpipeline reaktiviert), Trial-Lauf 2026-05-18 21:06 zeigte beide Bugs sichtbar.
*Stand:* offen, Priorität HOCH, soll im nächsten Cowork-Lauf validiert werden.
*Zu validieren:*
1. **Multi-Kategorie 3-Zeilen-Pattern (E92.1):** Oberkategorie `Pole Dance Kleidung` erscheint im Shop bei allen Artikeln (war im Trial-Lauf 2026-05-18 fehlend). Subkategorie + Sara-546 wie bisher korrekt.
2. **Farb-Lokalisierung DE (E92.2):** `Teal → Türkis`, `Sky → Himmelblau`, ggf. weitere wenn relevant in der Lieferung. Artikelnamen DE prüfen.
3. **Bildpipeline-Output (E93):** Stammdaten-CSV-Spalten Bild 1-10 mit R2-URLs befüllt, im Shop alle Plattform-Häkchen aktiv, Hero-Bild Front, Mouse-Hover-Bild Rück.
4. **Wallclock-Bilanz:** Stage 5.6 + 5.7 (Bildpipeline) wie lange? Vermutung ~10-20 Min zusätzlich bei 21 Artikeln. Im Lauf-Bericht dokumentieren.
*Trigger:* nächster Cowork-Daten-Lauf nach v1.21-Push.

**B67 — Bildpipeline-Performance bei Vision-Token-Verbrauch — NEU v1.21, monitoring**
*Bezug:* E93-Reaktivierung, E45 (Thumbnail-Vision Faktor 10 Token-Reduktion), B28 (Vision-Klassifikation validiert).
*Stand:* offen, Priorität NIEDRIG (Monitoring), zu reviewen wenn Lieferanten-Volumen steigt.
*Kontext:* Bei 21 Artikeln × ~10 Bilder/Artikel = ~210 Thumbnail-Vision-Calls pro Lauf. Bei 50 Artikeln × 10 Bilder × 20 Lieferanten = ~10.000 Vision-Calls pro Monat (Hochrechnung).
*Trigger:* wenn Cowork-Credit-Verbrauch in Vision-Stage sichtbar dominiert, Re-Evaluation der `pose_sort`-Strategie pro Lieferant (`auto_vision` vs. `manufacturer_order` vs. `none`). Für HotCakes konkret: nach erstem v1.21-Trial-Lauf prüfen ob `auto_vision` weiter sinnvoll ist, oder ob B28-Verifikation mit mehr Datenpunkten zu `manufacturer_order` führt.

**B69 — Eigenes Merkmal/Filter für Röcke (Rock/Skirt). — NEU 2026-06-25**
*Bezug:* RAD „Lara skirt" (A1009311) — ein Rock, der mangels statischem Rock-Merkmal als Bottom/Shorts gefiltert wird. Der Anzeigename trägt bereits korrekt „Rock"/„Skirt" (Namens-Typ-Override `Vater.name_typ` + `PRODUKTTYP["Rock"]`), aber Merkmal/Kategorie laufen weiter als Shorts.
*Stand:* offen, Priorität NIEDRIG. Filterlogik/Merkmalsverwaltung in der WaWi ist statisch (siehe Memory feedback_statische_merkmale) — neue Merkmalwerte/Kategorien nur bewusst + abgestimmt anlegen.
*Aufgabe:* Wenn genug Röcke im Sortiment sind, ein sauberes Rock-Merkmal (Style-Wert oder eigene Kategorie) in WaWi anlegen und im Code (`spec.KATEGORIE_SUB`, `merkmale._style_merkmalname`, ggf. eigener `garment_type`) sauber abbilden, dann betroffene Artikel re-importieren.
*Trigger:* mehrere Rock-Artikel im Sortiment ODER Tjorben-Freigabe für neuen Merkmalwert.
