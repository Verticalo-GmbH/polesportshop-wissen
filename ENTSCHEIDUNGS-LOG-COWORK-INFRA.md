# ENTSCHEIDUNGS-LOG-COWORK-INFRA

**Cluster:** Cowork-Architektur, R2-Mechanik, Wissens-Architektur, Resilience

**Stand:** v1.19, 2026-05-18 (neuer Eintrag E87: Migration Drive → Git als Wissens-Backbone)

**Bezug:** Dieser Cluster ist Teil des Splits der ursprünglichen `ENTSCHEIDUNGS-LOG.md` (v1.16, 165 KB → 6 Themen-Cluster ≤ 40 KB). Historische / abgelöste Einträge liegen weiterhin in `ENTSCHEIDUNGS-LOG-ARCHIV.md`. Cross-Cluster-Referenzen über E-Nummer; der Master-Index mit allen E-Nummern → Cluster-File-Zuordnung liegt in `SPEC_KONSTANTEN.md` unter `ENTSCHEIDUNGSLOG_E_NUMMER_INDEX`.

---

## Index

- **E1** — Cowork als Produktions-Engine, Claude.ai als Planungs-Engine
- **E2** — Lineare Pipeline ohne User-Review-Gate vor CSV-Output
- **E3** — Manueller Tages-Trigger durch Einkäufer
- **E4** — Multi-Input-Trigger (6 Modi: firecrawl, Drive-Link, Excel/CSV, PDF, Mail, Hybrid)
- **E15** — service@polesportshop.de für alle Pipeline-Services (R2, firecrawl)
- **E17** — Plattform-Aktivierung als bewusstes Backlog-Item, nicht jetzt lösen
- **E24** — Konfigurationsdaten als separate Files, getrennt von Anweisungs-Specs
- **E32** — Cowork-Setup, Drive `Wichtig: Claude Backup/` als Brücke
- **E33** — Credential-Mechanismen für externe Services in Cowork
- **E41** — Crawl-Tool-Marktcheck 2026-05: Firecrawl bleibt strategische Wahl, Pilot ohne Crawl-Tool
- **E43** — R2-Upload-Mechanik: Code-Execution + boto3 + Egress-Allowlist + Drive-File-Credentials
- **E47** — Wissens-Architektur: Immutable Snapshots in Drive
- **E61** — Konstanten-Auslagerung in `SPEC_KONSTANTEN.md` (Charter-Prinzip 11 NEU)
- **E62** — Spec-Caching-Konvention (Stage-0-Pflicht, `cowork_anweisung_datenimports.md` Sektion 3.1 NEU)
- **E64** — Lokaler Workflow als Default für Wissens-Updates
- **E65** — Stückelung in Prompt-Cycles als Default für mehrstufige Wissens-Updates
- **E66** — Build-Strategie: `create_file` vs. `str_replace` nach Änderungs-Volumen
- **E67** — Tag-Neustart-Disziplin als Context-Window-Resilienz
- **E68** — Selective Spec-Loading in Stage 0 + Pre-Compiled Run-Brief
- **E85** — Wissens-Update-Build-Pattern als Standard-Playbook (Cowork-Spec für Wissens-Builds)
- **E86** — File-Header-Versionierungs-Konvention (SemVer für Snapshot-Disziplin)
- **E87** — Migration Drive → Git als Wissens-Backbone (NEU v1.19, Pattern-Pivot)

---

**E1 — Cowork als Produktions-Engine, Claude.ai als Planungs-Engine.**
*Warum:* Cowork hat Tool-Zugriff (Drive, Code-Execution, MCP), Claude.ai ist besser im Reasoning-Dialog. Trennung ermöglicht versionierte Anweisungen und iterativen Quality-Loop.
*Verworfen:* Alles in Claude.ai (keine echte Automation). Alles in Cowork (Planungs-Dialog wäre frustrierend).

**E2 — Lineare Pipeline ohne User-Review-Gate vor CSV-Output.**
*Warum:* Review aus Vermutungen vs. Review aus Shop-Realität — letzteres ist ehrlicher. Bottleneck vermeiden.
*Verworfen:* Approval-Step nach Daten-Extraktion (Bottleneck, Pre-Specification statt Realitäts-Feedback).

**E3 — Manueller Tages-Trigger durch Einkäufer.**
*Warum:* Klare Verantwortung, keine "es ist plötzlich was passiert"-Effekte, einfacheres Debugging.
*Verworfen:* Auto-Polling auf Drive (zu magisch). Mail-getriggert (Mails unstrukturiert, falsche Auslöser). Cron-täglich (vermutet Aktivität ohne Notwendigkeit).

**E4 — Multi-Input-Trigger (6 Modi: firecrawl, Drive-Link, Excel/CSV, PDF, Mail, Hybrid).**
*Warum:* Lieferanten-Heterogenität ist Realität. Einkäufer-Aufwand minimieren statt Lieferanten-Format erzwingen.
*Verworfen:* firecrawl-only (ignoriert ~20% der Lieferanten ohne Online-Shop). Single-Format-Pflicht (würde Arbeit erhöhen statt reduzieren).
*Update 2026-05-15:* Firecrawl-Modus aktuell im Pilot geparkt (E41/B25), die anderen 5 Modi tragen die Pipeline.

**E15 — service@polesportshop.de für alle Pipeline-Services (R2, firecrawl).**
*Warum:* Zentrale Mailbox, Service-Account vs. Persönlich, unabhängig von Mitarbeiter-Wechsel.
*Verworfen:* Tjorben-persönlich (Schlüssel-am-Mitarbeiter-Risiko).

**E17 — Plattform-Aktivierung als bewusstes Backlog-Item, nicht jetzt lösen.**
*Stand:* 2026-05-13. *Status-Update 2026-05-15:* gelöst durch E46 (Bilder integriert in Stammdaten-Import aktivieren JTL alle Plattformen automatisch).
*Warum (ursprünglich):* Manueller "Alle aktivieren"-Klick reicht für Pilot. Auto-Aktivierung kann später ergänzt werden, ohne Pipeline-Flow zu blockieren.
*Auflösung:* Mit E46 löst sich das B5-Thema von alleine — beim Stammdaten-Import via Reiter "Bilder/Plattformen" mit allen 11 Plattform-Häkchen werden die Bilder direkt allplattform-aktiv geschrieben.
*Verworfen:* Sofort-Lösung mit zusätzlichen CSV-Spalten (war damals Komplexität ohne kritischen Nutzen; nicht mehr nötig wegen E46-Auflösung).

**E24 — Konfigurationsdaten als separate Files, getrennt von Anweisungs-Specs.**
*Stand:* 2026-05-14
*Warum:* Lieferanten-Metadaten waren in v1.1 als YAML-Block in beiden Cowork-Anweisungen inline gepflegt — identisches Schema, getrennte Wartung. Diskrepanz-Risiko stieg mit jeder Lieferanten-Aufnahme. Saubere Trennung: Anweisungen beschreiben *Verhalten*, Konfiguration ist *Daten*.

*Regel:* Daten, die mehr als einmal referenziert werden oder häufiger aktualisiert werden als die zugehörigen Specs, leben in eigenen Files unter `Wichtig: Claude Backup/`. Anweisungen referenzieren diese Files namentlich.

*Aktuell ausgelagert:*
- `lieferanten_mapping.yaml` — Single Source of Truth für Lieferanten-Metadaten. Beide Cowork-Anweisungen lesen daraus. Schema in der Datei selbst dokumentiert. Löst B2.

*Antizipierte weitere Auslagerungen (folgen demselben Pattern):*
- `lieferanten_zoll_versand.csv` (E23, B17/B18) — pro Lieferant Zoll- und Versandkosten-Aggregat
- `warengruppen_aufschlag.csv` (E23, B18) — pro Warengruppe Aufschlagsfaktor

*Verworfen:* YAML-Block inline in den Anweisungen lassen (kein Single Source of Truth, Diskrepanz-Risiko, schlechte Skalierbarkeit auf 50 Lieferanten).

*Folgeaufgabe:* Bei Skalierung auf >20 Lieferanten Format-Frage (YAML vs. CSV/Google Sheet) neu bewerten — derzeit als YAML pragmatisch ausreichend.

**E32 — Cowork-Setup, Drive `Wichtig: Claude Backup/` als Brücke.**
*Stand:* 2026-05-14, präzisiert 2026-05-15.
*Warum (ursprünglich 2026-05-14):* Claude.ai-Projekt (hier) und Cowork sind zwei technisch unabhängige Anthropic-Konstrukte ohne direkte Verbindung. Bislang war die Architektur in den Custom Instructions als „Cowork = autonome Ausführung" verkürzt, ohne zu konkretisieren wie Cowork organisiert ist. Bildpipeline-Versuch 2026-05-14 hat gezeigt: jede Cowork-Session ohne Projekt-Kontext startet bei null — keine akkumulierten Connectoren, kein Working-folder-Kontext, kein automatischer Zugriff auf Drive-Specs.
*Präzisierung 2026-05-15 (nach Cowork-Setup-Session):* Cowork hat **keine projekt-spezifischen Custom Instructions**, sondern Global Instructions in Settings → Cowork, die session-übergreifend gelten. Das ursprünglich angenommene „Cowork-Projekt" als Anthropic-isoliertes Konstrukt entspricht nicht der Realität — Cowork ist eher eine Settings-Ebene innerhalb der Claude-Desktop-Umgebung. Funktional ändert das nichts: Drive bleibt einzige Brücke, Connectors werden in der Cowork-UI verbunden, Credentials laufen über Connector-Setup oder über dediziertes Drive-File (E33-Erweiterung 2026-05-15).
*Architektur ab 2026-05-15:*
- **Claude.ai-Projekt** = Planung, Anweisungs-Tuning, Wissens-Pflege. Memory + Past-Chats halten Tagesstand. Drive-Files werden hier orchestriert.
- **Cowork** = autonome Ausführung mit:
  - Global Instructions in Settings → Cowork als Pointer auf die Drive-Specs (statt Spec-Inhalt zu duplizieren — Cowork liest sie pro Lauf aus Drive)
  - Cloud-Connectoren aus Anthropic-Registry: Google Drive (Wissens-Files lesen, Credentials-File für R2 lesen), Cloudflare Developer Platform (R2-Bucket-Lifecycle, Pre-Checks)
  - Cowork-eigene System-Tools: Bash-Sandbox, Code-Execution mit Network-Egress (für R2-Upload via boto3, siehe E43), interne Vision-Capability (für Pose-Klassifikation in Bildpipeline, siehe E45)
- **Drive `Wichtig: Claude Backup/`** = einzige Brücke. Beide Engines lesen daraus. Updates werden im Claude.ai-Projekt orchestriert und in Drive ausgetauscht; Cowork zieht beim nächsten Lauf den aktualisierten Stand.
*Verworfen:*
- Cowork ohne Setup-Persistenz (verschwendet Setup-Arbeit pro Session, kein akkumulierter Kontext).
- Eine einzige Anwendung statt Trennung (würde Tool-Sets vermischen und Reasoning-Dialog mit Ausführung kollidieren lassen).
- Direkte Verbindung Claude.ai ↔ Cowork (technisch nicht vorgesehen; auch nicht nötig solange Drive als Brücke funktioniert).
- *Verworfen 2026-05-15:* Cowork als isoliertes Projekt mit projekt-spezifischen Custom Instructions (existiert nicht in der Cowork-UI; nur Global Instructions auf Settings-Ebene).
*Folgeaufgabe:* B23 (MCP-Connector-Inventur) — wurde 2026-05-15 weitgehend erledigt (cloudflare_inventur.md + local_mcp_probe_result.md unter `_PIPELINE/_Logs/2026-05-15_crawl-tool-evaluation/`).

**E33 — Credential-Mechanismen für externe Services in Cowork.**
*Stand:* 2026-05-15.
*Warum:* Frühere Spec-Versionen 2026-05-14 bezogen sich auf einen „Cowork Secret Store"-Vault, der in der Cowork-Umgebung nicht existiert. Plus: Local MCP via Desktop-Config wurde als potentielle dritte Option getestet, ist aber für Cowork-Sessions nicht sichtbar (E42). Beide Annahmen waren Spec-Hoffnung statt verifizierter Stand. Mit dem R2-Upload-Pfad (Code-Execution + boto3, E43) und der Tatsache, dass der Cloudflare-Connector keine Object-Operations abdeckt, brauchen wir eine klare Regel mit den real existierenden Mechanismen.

*Zwei (und nur zwei) zulässige Credential-Mechanismen:*

1. **Connector-Setup in der Cowork-UI** — API-Key wird beim Hinzufügen eines MCP-Connectors direkt in der Cowork-Settings-UI eingegeben (aus Dashlane geholt). Cowork ruft den externen Service danach über den Connector, ohne dass die Credentials je im Chat oder in Specs auftauchen. Gilt für: Google Drive, Cloudflare Developer Platform, künftige Firecrawl-Aufnahme (B25).

2. **Drive-Credentials-File mit eingeschränktem Zugriff** — für Services ohne nativen Connector (Pilot-Stand: R2-Object-Upload). Datei liegt in einem dedizierten Drive-Sub-Ordner `_Credentials` unter dem Pipeline-Hauptordner mit Permissions nur für Tjorben. Cowork liest die Datei pro Lauf via Drive-Connector, extrahiert die Werte als ENV-Vars für die Code-Execution-Sandbox. Niemals in Logs, Berichten, CSVs oder Chat spiegeln.

*Was bleibt strikt verboten:*
- API-Keys über den Chat-Input weitergeben oder als ad-hoc-Parameter setzen lassen — auch nicht in Test-/Probe-Sessions. Cowork hat in mehreren Setup-Versuchen 2026-05-15 solche Chat-Key-Versuche selbst als E33-Anti-Pattern geflaggt. Diese Eskalation ist die gewünschte Behaviour.
- Erfundene Mechanismen in Specs verankern, die nicht durch Probe-Test verifiziert sind (Charter Prinzip 9).

*Verifikations-Pattern (generalisierbar):* Bevor ein neuer Credential- oder Tool-Mechanismus in einer Spec verankert wird, mit Probe-Test verifizieren: kleinen, harmlosen Test-Server/-File registrieren → Cowork explizit fragen, ob es ihn sieht → bestätigen oder widerlegen. Beispiele: filesystem-MCP-Probe für Local-MCP-Bridge (E42), Cloudflare-Connector-Tool-Inventur für R2-Object-Support.

*Konsequenz:* Specs sagen „Credentials kommen über den installierten MCP-Connector ODER über das Drive-Credentials-File mit eingeschränktem Zugriff" — abhängig davon, ob ein nativer Connector den Service abdeckt.

*Verworfen:* „Cowork Secret Store" (existiert nicht). Credentials im Chat oder in Specs hinterlegen (verboten). Local MCP via Desktop-Config als Credential-Brücke (Bridge tot, E42). Cloudflare-Worker-Proxy für den Pilot (Aufwand ohne aktuellen Mehrwert; Reserve in B27 für Skalierung).

**E41 — Crawl-Tool-Marktcheck 2026-05: Firecrawl bleibt strategische Wahl, Pilot ohne Crawl-Tool.**
*Stand:* 2026-05-15. Bezug: E14, B25.
*Warum:* Im Cowork-Setup 2026-05-15 stellte sich heraus: Firecrawl ist nicht als nativer Connector in der Anthropic-Registry verfügbar. Frage war, ob wir ad-hoc auf Tavily oder Brightdata wechseln sollten. Marktcheck (Stand Mai 2026): Firecrawl bleibt mit >85k GitHub-Stars, 13 MCP-Tools und führender Anti-Bot-Performance der Marktführer beim Web-Crawling; Tavily hat schwächere Extract-Strukturierung und niedrigere Success-Rate; Brightdata ist potenziell stark, aber kein direkter Vergleich zur Firecrawl-Tiefe verfügbar. Konsequenz: Wechsel wäre Down-Grade.

*Lenkungs-Entscheidung:* Crawl-Tool-Diskussion parken, Pilot ohne autonomen Crawl-Modus betreiben. Die 5 anderen Input-Modi aus E4 (Drive-Upload, Excel/CSV, PDF, Mail, Hybrid) reichen für die nächsten 1-2 Lieferanten. Anthropic-Registry beobachten (B25). Falls ein konkreter Lieferant nur über Crawl erreichbar wird, bevor Firecrawl in der Registry erscheint, dann neu evaluieren.

*Charter-Prinzip 9 in Aktion:* „klein nach groß" — Crawl ist nicht der aktuelle Engpass (R2 ist es, siehe E43). Wegwerf-Arbeit vermieden, weil Firecrawl-Registry-Aufnahme realistisch in Wochen kommt (Anthropic kuratiert die Registry aktiv, Marktführer landen meist nativ).

*Verworfen:* Tavily- oder Brightdata-Connector ad-hoc in Specs verankern (technischer Down-Grade, würde bei späterer Firecrawl-Aufnahme zu Migrations-Aufwand führen). API-Keys via Chat-Input für Firecrawl-Code-Execution durchreichen (E33-Anti-Pattern, von Cowork selbst geflaggt 2026-05-15). Crawl-Modus für den Pilot komplett aus E4 streichen (zu früh — sobald Firecrawl-Connector da ist, ist die Reaktivierung trivial).

**E43 — R2-Upload-Mechanik: Code-Execution + boto3 + Egress-Allowlist + Drive-File-Credentials.**
*Stand:* 2026-05-15. Bezug: E10, E33, E40, E42, B22.
*Warum:* B22 (R2-Migration) musste zwischen zwei Pfaden entscheiden, nachdem feststand, dass der Cloudflare-Connector nur Bucket-Lifecycle abdeckt (kein `put_object`, kein `execute()`-Code-Mode):
- *Pfad (a) S3-MCP via Local-MCP-Bridge* — Probe-Test mit filesystem-MCP gescheitert (E42). Bridge tot für Cowork.
- *Pfad (b) Code-Execution + boto3* — funktioniert mit Cowork-Standard-Capabilities, sauber unter E33 zu lösen.
Pfad (b) ist die einfachst-mögliche Variante, die funktioniert (Charter Prinzip 9).

*Operative Definition (für `cowork_anweisung_bildpipeline.md` v1.3):*

- **Mechanik:** Python in Cowork-Code-Execution-Sandbox, `boto3` via PyPI installiert, S3-API-kompatibler Aufruf gegen R2-Endpoint.
- **Endpoint:** `https://d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com`
- **Region:** `auto` (R2-Standardwert)
- **Bucket:** `polesportshop-images`
- **Public Base URL:** `https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev`
- **Network-Egress-Allowlist** in Cowork-Settings → Capabilities → „Additional allowed domains":
  - Idealer Stand: granulare Liste mit `d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com`, `pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev` und Hersteller-CDN-Domains pro Lieferant.
  - Aktueller Pilot-Stand (2026-05-15): Allowlist-Modus „All domains" wegen Anthropic-Bug (Issues #38984, #51400) — die granulare Liste wird im Modus „Package managers only" silent ignoriert. Reversibel zur granularen Liste sobald Bug-Fix vorliegt (B29).
- **Credentials:** In Drive-File `r2_credentials.json` unter Sub-Ordner `_Credentials` (Permissions: nur Tjorben als Owner, nicht geteilt). Cowork liest die Datei pro Lauf via Drive-Connector und nutzt die Werte als ENV-Vars (`R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`). Niemals in Logs, Berichten, CSVs oder Chat spiegeln (E33-Erweiterung).
- **Cloudflare-Connector ergänzend:** Wird beibehalten für Pre-Checks (`r2_bucket_get(name='polesportshop-images')` vor Pipeline-Lauf, prüft ob Bucket erreichbar) — nicht für Upload.

*Verworfen:*
- Pfad (a) S3-MCP via Local-MCP-Bridge (Bridge tot, E42).
- Pfad (c) Cloudflare-Worker als Upload-Proxy für den Pilot (architektonisch eleganter, aber Worker-Setup-Aufwand ohne aktuellen Mehrwert; als Reserve in B27 für Skalierung).
- Pfad (d) Out-of-band manueller Upload (bricht die End-to-End-Pipeline-Automation).
- API-Keys via Chat-Trigger durchreichen (E33-Anti-Pattern, von Cowork selbst geflaggt).
- Cowork-Secrets-Feature nutzen (existiert nicht in der Cowork-UI).

*Folgeaufgaben:* B22 (R2-Migration der HotCakes-CSV mit erstem End-to-End-Smoke — für Arachne Bottom Black 2026-05-15 erledigt, Hekate und Arachne Top noch offen), B26 (Cloudflare-Code-Mode-MCP beobachten als zukünftigen Bypass-Kandidaten), B27 (Worker-Proxy-Migration bei Skalierung), B29 (Anthropic-Allowlist-Bug-Tracker).

**E47 — Wissens-Architektur: Immutable Snapshots in Drive.**
*Stand:* 2026-05-15. Bezug: E32, E35, E36, E46, plus die vorhergehenden Wissens-Update-Iterationen vom 2026-05-14 (ZIP-Workflow) und 2026-05-15 vormittags (Pre-Flight-Checkliste).
*Warum:* Während der Wissens-Update-Session 2026-05-15 nachmittags hat sich gezeigt, dass der ZIP-Upload-/Download-Workflow drei Schwachstellen hat:

- **Stream-Abbruch im Chat während eines Wissens-Updates** macht ein Re-Run mit unklarem Zustand nötig — was wurde schon geschrieben, was nicht?
- **Manueller Re-Upload nach Drive** ist 8 atomare Schritte pro Update, jeder mit Fehlerpotenzial (falsche Datei, vergessene Datei, Überschreib-Bestätigung übersehen).
- **Keine Versions-Historie** — nach jedem Update sind die vorherigen Stände verloren (außer im Chat-Verlauf), keine Audit-Trail.

Parallel haben mehrere Iterations-Vorschläge (Pre-Flight-Checkliste, Stage-Pattern mit `_Stage/`-Ordner und manueller Promote-Move) immer einen manuellen Schritt für Tjorben übrig gelassen — was bei einem Core-Feature der Firma nicht zumutbar ist. Tjorbens Aussage 2026-05-15: „Das ist ein absolutes Core-Feature unserer gesamten Firma, woran diese Firma hängt — deswegen muss das wirklich professionell langfristig robust laufen."

Tjorben hat dann das Pattern selbst entwickelt: bei jedem Update wird ein neuer Versions-Sub-Ordner direkt im Live-Ordner erstellt. Es wird nichts verschoben, kopiert oder gelöscht — nur erstellt. Aktueller Stand ist per Definition der jüngste vollständige Sub-Ordner.

*Operative Definition:*

- **Drive-Pfad-Konvention:** `Geteilte Ablagen / Artikelanlage Bilder Pipeline / Wichtig: Claude Backup / Version_YYYY-MM-DD_HHMMSS / {Files}`. Der historische Drift-String `_PIPELINE/_Wissen/` ist endgültig abgelöst.
- **Sub-Ordner-Namen** sekundengenau im Format `Version_2026-05-15_171539`. Alphabetische Sortierung entspricht chronologischer Sortierung. Sekundengenauigkeit verhindert Namens-Kollisionen bei mehreren Updates am selben Tag.
- **Inhalt pro Snapshot:** die 8 Wissens-Files (PROJEKT-CHARTER.md, ENTSCHEIDUNGS-LOG.md, BACKLOG.md, cowork_anweisung_datenimports.md, cowork_anweisung_bildpipeline.md, lieferanten_mapping.yaml, WAWI-IMPORT-WISSEN.md, Projekt-Anweisungen.md) plus `_MANIFEST.md` mit Stand-Datum, SHA256-Hashes aller 8 Files und kurzer Change-Summary. **Komplett-Marker:** der Resolver prüft beim Lesen, ob Manifest UND alle 8 namentlich erwarteten Wissens-Files im Sub-Ordner liegen. Damit ist die Upload-Reihenfolge egal — abgebrochene Uploads zeigen sich durch fehlende Files und der Sub-Ordner wird übersprungen.
- **Resolution-Strategie (für Claude in Klärungs-Chats UND für Cowork):** liste die Sub-Ordner in `Wichtig: Claude Backup/` (parent-ID `12wDy0Z0cmB0p-OAs10Y7XqBWhmtQEip5`), filtere auf `title contains 'Version_'`, sortiere nach `title` absteigend, iteriere durch die Liste und nimm den ersten Sub-Ordner mit Manifest **und** allen 8 Wissens-Files vorhanden. Unvollständige Sub-Ordner (fehlende Files) überspringen.
- **Workflow-Pattern (heute final geklärt, Token-effizient):** Claude generiert die 9 Files im Workspace, validiert lokal (Datei-Existenz, Hash-Konsistenz, Byte-Counts), legt einen neuen Sub-Ordner via Drive-MCP an, gibt alle 9 Files via `present_files` aus. Tjorben lädt sie per Drag-and-Drop in einem Rutsch in den Sub-Ordner — Reihenfolge egal. Diese Aufteilung spart ggü. einer direkten Drive-MCP-Schreib-Operation Tokens im Größen-Bereich (Faktor 15-20), weil der Dateiinhalt nicht durch den Antwort-Stream geschoben wird.
- **Vertrauenskette:** Claude validiert bis zur Ausgabe (Workspace-Files, Hashes, Vollständigkeit). Ab `present_files` liegt die Verifikation bei Tjorben — er zählt die Files beim Hochladen und bestätigt Vollständigkeit. Kein nachgelagerter Post-Check via Drive-MCP von Claude — wäre Pseudo-Theater und kostet wieder Tokens.
- **Tjorbens Rolle:** einmal pro Update „Wissens-Update fahren" sagen, Schritt-1-Revue bestätigen, am Ende die 9 Files in einem Rutsch in den Sub-Ordner hochladen. Sonst nichts. Keine Move-, Copy-, Delete-Operationen.

*Validierung:* Bootstrap-Snapshot am 2026-05-15 nachmittags gegenüber dem Pattern durchgeführt — alle 9 Files per `present_files` ausgegeben, von Tjorben in `Version_2026-05-15_175144` hochgeladen, Resolution-Strategie greifbar.

*Konsequenzen für bestehende Specs:*
- `Projekt-Anweisungen.md` (2026-05-15): Routine-Output-Schritt 2 definiert das Workflow-Pattern (Claude generiert + `present_files`, Tjorben lädt hoch).
- `cowork_anweisung_datenimports.md` v1.6 (2026-05-15): Resolution-Strategie für den aktuellen Snapshot eingebaut, prüft Manifest + alle 8 Wissens-Files für Komplett-Marker.
- `cowork_anweisung_bildpipeline.md` v1.4 (2026-05-15): gleiche Resolution-Strategie.
- `BACKLOG.md`: B22 (R2-Migration) und B5 (Plattform-Aktivierung) sind unbeeinflusst, weil sie auf Pipeline-Operationen abzielen, nicht auf Wissens-Architektur. Neue Einträge B31 (Praxis-Validierung des Snapshot-Patterns) und B32 (Legacy-Files aufräumen).

*Verworfen:*

- *ZIP-Upload mit Pre-Flight-Checkliste (Mittags-Vorschlag 2026-05-15):* Pre-Flight verbessert die Lese-Seite (8 Files verifiziert), aber löst nicht die manuelle Drive-Tausch-Seite und nicht den Stream-Abbruch. Nur halbe Lösung.
- *Stage-Pattern mit `_Stage/`- und `_Archiv/`-Sub-Ordnern:* eleganter als ZIP, aber ein finaler Move-Schritt von Tjorben bleibt nötig (Live → Archiv, Stage → Live). Für „Core-Feature der Firma" zu interaktiv.
- *Claude schreibt autonom via Drive-MCP `create_file` mit Manifest zuletzt:* funktional richtig, aber token-teuer (Dateiinhalt zweimal durch den Antwort-Stream: einmal beim Lesen via cat, einmal als Tool-Argument). Bei 8-9 Files = 150-200k Tokens. Plus die Disziplin „Manifest zuletzt" wurde durch den Komplett-Marker-Check (Manifest + 8 named Files) im Resolver obsolet. Tjorben-uploaded Pattern ist 15-20× billiger und atomar gleich robust.
- *Drive-MCP-direkter Schreib-Workflow im Live-Ordner mit gleichen Datei-Namen:* würde Duplikate erzeugen (Drive-MCP `create_file` mit gleichem Titel im gleichen Parent erzeugt einen zweiten File, kein Update).
- *Google Apps Script für atomaren Promote als 1-Klick-Action:* möglich, aber Setup-Aufwand und Wartungs-Abhängigkeit. Mit Snapshot-Pattern unnötig.
- *GitHub-Repo statt Drive für Versionierung:* atomare Commits sind elegant, aber Setup-Aufwand (Git, GitHub Desktop, SSH-Keys) ist für einen Nicht-Entwickler zu viel Reibung. Drive-basierte Snapshots geben dieselbe Versions-Garantie mit Null Setup.

*Stolperfallen:*

- **Drive füllt sich mit alten Snapshots:** bei 1 Update pro Woche entstehen ~50 Sub-Ordner pro Jahr × 9 Files = ~450 Files × ~30 KB = 13 MB jährlich. Vernachlässigbar für Drive-Quota. Falls die Ordner-Liste in Drive Web unhandlich wird, kann Tjorben quartalsweise alte Snapshots in einen tieferen Archiv-Sub-Ordner verschieben (z.B. `Wichtig: Claude Backup/_Q1_2026_Archiv/`). Die Resolution-Strategie wirkt nur auf die Top-Level-Snapshots, also stören tiefer geschachtelte alte Snapshots die Auto-Resolution nicht.
- **Race-Conditions bei parallelen Wissens-Updates:** Sekundengenauigkeit ist Schutz bei zwei Updates am selben Tag, aber zwei Updates in derselben Sekunde wäre theoretisch möglich. In der Praxis ein einzelner Operator (Tjorben), daher unrealistisch.
- **Cowork und Wissens-Update mitten im Pipeline-Lauf:** Wenn Cowork einen Pipeline-Job laufen hat während Tjorben ein Wissens-Update fährt, sollte Cowork den laufenden Job mit dem Snapshot zu Ende führen, der beim Job-Start aktuell war. Den neuen Snapshot zieht Cowork erst beim nächsten Job. Eindeutige Resolution bei Job-Start ist Pflicht.

*Folgeaufgaben:*

- *B31:* Snapshot-Pattern im Praxis-Betrieb validieren — bei den ersten 3-5 echten Wissens-Updates beobachten, ob die Architektur hält oder ob Edge-Cases auftauchen.
- *B32:* Alt-Files in `Wichtig: Claude Backup/` direkt im Live-Ordner (8 Files vom 2026-05-14 plus die `Untitled`-Karteileiche, plus der unvollständige Sub-Ordner `Version_2026-05-15_171539` mit nur PROJEKT-CHARTER.md drin) sind durch das neue Pattern nicht mehr referenziert. Können bei Gelegenheit manuell entfernt werden. Stören die Resolution nicht.

**E61 — Konstanten-Auslagerung in `SPEC_KONSTANTEN.md` (Charter-Prinzip 11 NEU).**
*Stand:* 2026-05-16. Bezug: E47 (Snapshot-Architektur), E59 (WaWi-Mapping als Fels), Pilot-Beobachtung End-to-End-Cowork-Läufe 2026-05-15/16.

*Warum:* In mehreren End-to-End-Versuchen mit dem v1.8-Workflow verbrannte Cowork **~50K Tokens** beim wiederholten Extrahieren derselben Konstanten (48-Spalten-Schema, SEO-Templates, Sprach-Lookup-Tabellen, Merkmalwerte, Self-Check 12-Punkte, AP1-AP8) aus `cowork_anweisung_datenimports.md` und `WAWI-IMPORT-WISSEN.md`. Stage 0 (Wissens-Resolution) wurde nie überschritten. Symptom war systemisch: die operativen Specs vermischten *Was/Warum* mit *Genau-Wie* und zwangen Cowork, dieselben Strings stage-übergreifend wieder und wieder zu parsen.

*Entscheidung:*
- Neue Datei `SPEC_KONSTANTEN.md` als **kanonische Single Source** für alle harten Konstanten der Daten-Pipeline.
- Operative Specs (`cowork_anweisung_datenimports.md`, `WAWI-IMPORT-WISSEN.md`) verweisen ab v1.10 nur noch auf SPEC_KONSTANTEN.md, statt die Konstanten selbst zu enthalten.
- Konflikt-Auflösung: bei Widerspruch zwischen SPEC_KONSTANTEN und WAWI-IMPORT-WISSEN → STOPP + User-Frage, niemals autonom entscheiden.
- Snapshot wächst von 8 auf 10 Wissens-Files (plus Manifest).
- Charter-Prinzip 11 NEU: „Konstanten leben in einer einzigen Datei, werden 1:1 als Quelle gelesen, ändern sich nur dort."

*Konsequenzen:*
- Cowork-Stage-0-Lade-Pflicht (siehe E62, Spec-Caching) liest SPEC_KONSTANTEN.md einmalig und cacht lokal.
- WAWI-IMPORT-WISSEN.md Sektion 10.5 (AP1-AP8) ist nach SPEC_KONSTANTEN.md Sektion 10 gewandert — bleibt mit Verweis als Stub erhalten für Backwärts-Kompatibilität.
- Datenimports.md Sektionen 5.1, 5.1.1, 5.1.2, 5.3, Stage-6-Self-Check verweisen statt zu definieren.

*Verworfen:*
- *Konstanten im Header der jeweiligen Stage-Sektion belassen:* gibt das Token-Problem nicht her, Cowork muss trotzdem die ganze Datei lesen.
- *Pro Konstante eine eigene Datei:* zu fragmentiert, Snapshot bläht sich auf, Resolution wird komplex.
- *Konstanten in YAML statt Markdown:* Tabellen und Lookup-Strukturen sind in Markdown lesbarer für menschliche Pflege, YAML wäre rein maschinell. Mixed Mode (YAML in Markdown-Codeblocks) bleibt für Lookups erlaubt.

---

**E62 — Spec-Caching-Konvention (Stage-0-Pflicht, `cowork_anweisung_datenimports.md` Sektion 3.1 NEU).**
*Stand:* 2026-05-16. Bezug: E47, E61, Pilot-Beobachtung Cowork-Token-Verbrauch 2026-05-15/16.

*Warum:* Selbst nach E61 (Konstanten-Auslagerung) blieb das Risiko, dass Cowork pro Stage erneut `download_file_content` auf SPEC_KONSTANTEN.md, lieferanten_mapping.yaml, WAWI-IMPORT-WISSEN.md und die Anweisung selbst aufruft. Drive-MCP-Reads sind zwar günstiger als String-Extraktion, aber 5-7 Wiederholungen pro Lauf summieren sich messbar.

*Entscheidung:*
1. Cowork lädt alle benötigten Wissens-Files **einmalig zu Lauf-Beginn** (Stage 0) via Snapshot-Resolution.
2. Files werden lokal im Workspace gecacht (`/home/claude/wissens_cache/`).
3. Alle weiteren Stages lesen ausschließlich aus dem lokalen Cache — kein Mid-Run-Reload.
4. Bei Lauf-Ende: Cache wird verworfen (Workspace-Reset zwischen Läufen normal).
5. Bei Drift-Verdacht („der Snapshot wurde gerade aktualisiert"): Lauf abbrechen, neu starten — kein Mid-Run-Reload.

*Konsequenzen:*
- Wallclock-Reduktion pro Lauf (geschätzt 20-30% Token-Ersparnis bei mittlerem Lauf-Volumen, nicht gemessen).
- Stage-übergreifende Konsistenz garantiert (alle Stages lesen denselben Konstanten-Stand).
- Anti-Pattern explizit verboten: pro-Stage-Drive-Read, pro-Artikel-Lookup-Reload.

*Verworfen:*
- *Memory-Cache mit TTL:* unnötig komplex für Pilot, Workspace-Reset zwischen Läufen ist sauberer.
- *Inline-Definitionen in der Cowork-Anweisung (alles in eine Datei):* widerspricht E61 (Konstanten-Trennung) und macht die Spec unwartbar.

---

**E64 — Lokaler Workflow als Default für Wissens-Updates.**
*Stand:* 2026-05-16. Bezug: E47 (Snapshot-Architektur), E52 (Workflow-Refinement), Pilot-Erfahrung 2026-05-16.

*Warum:* Drei aufeinanderfolgende Drive-basierte Wissens-Updates am 2026-05-16 scheiterten an Drive-Connector-Instabilität — Timeouts und Fail-Loops bei `create_file` für die Sub-Ordner-Anlage und nachfolgenden File-Uploads. Symptom war reproduzierbar im Sinne von „passiert wieder", aber nicht im Sinne von greifbarem API-Fehler-Detail (Tool-Responses ohne diagnostische Tiefe). Der lokale Workflow mit Uploads + `present_files` war im selben Zeitfenster zuverlässig.

*Entscheidung:*
- Default-Workflow für Wissens-Updates: **lokal**. Tjorben gibt die v1.X-Files (jüngster Snapshot) als Uploads in den Chat, Claude baut im Workspace `/home/claude/wissens_out/`, gibt die fertigen Files per `present_files` aus, Tjorben legt den neuen Sub-Ordner in Drive an und macht Drag-and-Drop.
- Drive-direkt via Drive-MCP (`create_file` für Folder + serielles Hochladen der Files) wird zum **Fallback** degradiert — nur, wenn der lokale Pfad ausnahmsweise nicht praktikabel ist (z.B. Tjorben unterwegs ohne lokalen File-Zugriff).
- Custom Instructions in `Projekt-Anweisungen.md` werden im Snapshot-Anlage-Workflow neu sortiert: lokal = Schritt 1, Drive-direkt = expliziter Fallback.

*Konsequenzen:*
- Cowork-Pfad bleibt unverändert: Cowork **liest** weiter aus Drive über den Snapshot-Resolver. Der Drive-Connector hat sich für Read-Operationen als zuverlässig erwiesen, nur Folder-/Upload-Schreiboperationen sind aktuell wackelig.
- Verantwortungs-Verschiebung: ab `present_files` liegt die Verifikation der Vollständigkeit bei Tjorben (er zählt die Files beim Drag-and-Drop, sieht in der Drive-UI direkt, ob alle 11 angekommen sind). Kein nachgelagerter Post-Check via Drive-MCP von Claude — würde wieder Tokens kosten und Drive-Connector-Risiko reaktivieren.
- Memory-Edit zur „Tjorben legt keine Folder selbst an"-Regel ist obsolet und wird beim nächsten passenden Anlass aktualisiert.

*Verworfen:*
- *Drive-direkt-Bug isolieren und fixen:* nicht reproduzierbar genug ohne API-Fehler-Detail; Symptom-Mitigation via lokal-Workflow ist günstiger als Connector-Debugging.
- *Drei Retry-Mechanismen pro Drive-Call:* erhöht nur die Latenz, ohne das systemische Problem zu lösen.
- *Auf Drive-Connector-Fix von Anthropic warten:* Wissens-Updates sind alltagskritisch, Warten blockiert den Pilot.

---

**E65 — Stückelung in Prompt-Cycles als Default für mehrstufige Wissens-Updates.**
*Stand:* 2026-05-16. Bezug: E47, E64, beobachtetes Tool-Use-Limit pro Assistant-Turn 2026-05-16.

*Warum:* Beim Versuch, einen vollen 10-File-Snapshot-Build in einem einzigen Assistant-Turn durchzuziehen, schlug das Tool-Use-Limit pro Turn zu. Die Bauarbeiten an mehreren Files mit Hash-Verifikation, str_replace-Ketten und Validierung summieren sich auf 30+ Tool-Calls — über dem Limit. Das Budget resetst aber bei jedem neuen Assistant-Turn (neue User-Message dazwischen).

*Entscheidung:*
- Default-Stückelung für Wissens-Updates: **3-5 Cycles pro Update**, je etwa 3-4 Files pro Cycle.
- **Cycle 0** = Pre-Flight-Briefing: Workspace-Anlage, Hash-Check der Upload-Files gegen das vorherige Manifest (Drift-Detektion), konkreter Stückelungs-Vorschlag mit Mechanik-Spalte (siehe E66) pro Cycle. Tjorben bestätigt die Stückelung, dann startet Cycle 1.
- **Cycle 1..N** = je ein Bauabschnitt mit Status-Bericht am Ende, sodass Tjorben pro Cycle Sichtbarkeit hat und ggf. eingreifen kann.
- **Letzter Cycle** = Manifest-Erstellung, lokale Validierung (Hashes, Byte-Counts, UTF-8-Sanity), `present_files` für alle Snapshot-Files.

*Konsequenzen:*
- Wissens-Update-Workflow ist explizit mehrstufig in `Projekt-Anweisungen.md` dokumentiert.
- Pre-Flight-Briefing ist neuer fester Bestandteil des Workflows, nicht optional.
- Inter-Cycle-User-Bestätigung ist Default — gibt Tjorben Eingriffs-Punkte, kostet kaum spürbare Reibung.

*Verworfen:*
- *Alles in einem Assistant-Turn:* scheitert am Tool-Use-Limit bei umbau-schweren Updates.
- *Pro File ein eigener Cycle (10+ Cycles):* zu viele User-Bestätigungs-Punkte, Tjorben wird zum Bottleneck.
- *Tool-Calls parallelisieren:* viele Build-Schritte haben Reihenfolge-Abhängigkeiten (Manifest braucht alle anderen Hashes zuerst).

---

**E66 — Build-Strategie: `create_file` vs. `str_replace` nach Änderungs-Volumen.**
*Stand:* 2026-05-16. Bezug: E65, Tool-Call-Verteilung im v1.10-Build (mehrere Files mit 3-7 str_replace-Calls).

*Warum:* Bei umbau-schweren Files (z.B. `Projekt-Anweisungen.md` im v1.10-Build) summierten sich `str_replace`-Calls auf 5-7 pro File und verbrannten unverhältnismäßig viel Tool-Call-Budget pro Cycle. Ein einziger `create_file` mit Vollinhalt ist genau 1 Tool-Call, kostet aber mehr Output-Tokens. Bei kleinen Patches ist umgekehrt `create_file` Token-Verschwendung.

*Entscheidung:*
- **>50% einer Datei geändert oder strukturell umgebaut → `create_file`** (1 Tool-Call, mehr Output-Tokens, vertretbar).
- **<30% geändert → `str_replace`** (mehrere Tool-Calls möglich, aber Output-Token-effizient).
- **30-50%-Zone → nach Komplexität:** wenn die Änderungen lokal und gut isolierbar sind, str_replace; wenn sie verflochten sind, create_file.
- **0% geändert → `cp` via bash**, kein Tool-Call für Inhalt nötig (siehe Cycle-1-Mechanik).
- Pre-Flight-Briefing (Cycle 0) nennt die Build-Strategie pro Datei explizit in der Mechanik-Spalte, sodass Tjorben den Plan vor dem Build sieht.

*Konsequenzen:*
- Build-Plan pro Cycle dokumentiert die Mechanik. Spielt rein in die Cycle-0-Tabelle.
- Mentale Disziplin: vor jedem File-Build kurz das geschätzte Änderungs-Volumen abgleichen.

*Verworfen:*
- *Immer create_file:* Output-Token-Verschwendung bei Update-Snapshots, in denen oft 60-80% der Files unverändert oder minimal geändert sind.
- *Immer str_replace:* Tool-Call-Budget wird bei großen Umbauten gesprengt, Cycle scheitert.
- *Automatische diff-basierte Strategie-Wahl:* Diff-Tool-Call würde wieder Budget kosten; mentale Schätzung reicht.

---

**E67 — Tag-Neustart-Disziplin als Context-Window-Resilienz.**
*Stand:* 2026-05-16. Bezug: E47, E65, Context-Window-Limit als hartes Anthropic-Limit; Beobachtung: Chats über mehrere Arbeitstage akkumulieren Token-Volumen, das Compaction-Failure-Risiko überproportional erhöht.

*Warum:* Wenn ein Chat das Context-Limit erreicht und Compaction fehlschlägt, geht **alles** zwischen dem letzten Wissens-Update-Anker und dem aktuellen Moment verloren. Das Risiko skaliert mit Chat-Länge. Drei Optionen wurden diskutiert: technische Living-Notes-Lösung (Files schreiben pro Substanz-Punkt), Chat-Splits nach Token-Counter (fragil), oder Disziplin.

*Entscheidung (Tjorbens):* **Pro Arbeitstag ein neuer Chat.** Am Tagesende generiert die aktive Claude-Instanz einen **Übergabeprompt** mit dem Tages-Stand (verworfene Optionen, neue E-Einträge, neue Backlog-Punkte, neue Anomalien, ggf. neue Spec-Versions-Auftrag). Tjorben startet den nächsten Arbeitstag mit einem neuen Chat: Übergabeprompt + Uploads des jüngsten Snapshots als Ausgangs-Material.

*Konsequenzen:*
- Maximale Chat-Länge ist hart auf einen Arbeitstag begrenzt.
- Übergabeprompt-Generierung ist neue Pflicht am Tagesende, nicht laufend gepflegt.
- Erste Operation in jedem neuen Chat: Pre-Flight gemäß E65/E66 — Hash-Check der Uploads gegen das im Übergabeprompt referenzierte Manifest.
- Wenn Tagesarbeit ohne substantielle Wissens-Änderungen endet (z.B. reine Klärungs- oder Recherche-Sessions): kein Übergabeprompt nötig, Chat kann am nächsten Tag weiterlaufen — solange das Context-Volumen unter Schmerzgrenze bleibt.

*Verworfen:*
- *Technische Living-Notes-Lösung* (laufendes File-Schreiben jeder Substanz-Entscheidung): zu hoher Engineering-Overhead für den Pilot, klagloser Tagesbruch reicht.
- *Chat-Splits nach Token-Counter:* fragil — Counter ist nicht sichtbar für Claude, Splits würden mitten in Stages passieren.
- *Mehrere parallele Chats für unterschiedliche Themen:* fragmentiert das Wissens-Update zu sehr, Tjorben verliert den Faden.

---

**E68 — Selective Spec-Loading in Stage 0 + Pre-Compiled Run-Brief.**
*Stand:* 2026-05-16. Bezug: E47 (Snapshot-Architektur), E61 (SPEC_KONSTANTEN als kanonische Quelle), E62 (Spec-Caching), A8 (Sub-Agent-Extraction-Schwelle).

*Warum:* Erster End-to-End-Daten-Lauf-Versuch am 2026-05-16 brach nach >30 Min ab. Diagnose: Cowork lud in Stage 0 alle 10 Wissens-Files. Bei zwei Files über ~50 KB (`WAWI-IMPORT-WISSEN.md` 56 KB, `cowork_anweisung_datenimports.md` 52 KB) triggerte Cowork eine interne **Sub-Agent-Extraction-Stufe** (siehe A8) — parallele LLM-Calls, um „relevante Sektionen" zu extrahieren. Das frisst pro betroffenes File mehrere Minuten. Für einen reinen Daten-Lauf werden viele dieser Files gar nicht gebraucht (Bildpipeline archiviert, LOG/Charter/Backlog nur bei Klärung relevant). Volle Stage-0-Load war 85 % Overkill.

*Entscheidung:*
- Für einen Daten-Lauf lädt Cowork in Stage 0 **genau 3 Files**: `run_brief_daten.md` (Pipeline-Hauptordner bzw. ab v1.12 Snapshot), `SPEC_KONSTANTEN.md` (Snapshot), `lieferanten_mapping.yaml` (Snapshot).
- `run_brief_daten.md` ist eine **kompakte operative Spec** (~15 KB), die die operative Essenz aus `WAWI-IMPORT-WISSEN.md` und `cowork_anweisung_datenimports.md` ersetzt. Pflichtteil: Stage-Sequenz, CSV-Format-Regeln, Variationen/Merkmale/Attribute-Schemas, Pricing-Logik, Stil-Briefing für `artikeldetails`, Ameise-Mapping-Stolperfallen, Fehler-Handling, Konventionen DARF/NICHT DARF.
- **NICHT in Stage 0 laden**: `WAWI-IMPORT-WISSEN.md`, `cowork_anweisung_datenimports.md`, `PROJEKT-CHARTER.md`, `ENTSCHEIDUNGS-LOG.md`, `BACKLOG.md`, `cowork_anweisung_bildpipeline.md`, `Projekt-Anweisungen.md`, `cowork_custom_instructions.md`.
- **Lazy-Load erlaubt** bei legitimer Architektur-Klärung (Charter-Prinzip-10-STOPP, Mapping-Lücke, unklare Begründung) — dann darf Charter/LOG/Backlog nachgeladen werden. Im Lauf-Bericht zu dokumentieren. Das ist kein E62-Verstoß.
- Ab v1.12 ist `run_brief_daten.md` offizieller Teil des Snapshots → 11 Wissens-Files statt 10. Komplett-Marker, Resolution-Strategie und Snapshot-Liste in `cowork_custom_instructions.md` und `Projekt-Anweisungen.md` entsprechend angepasst.

*Konsequenzen:*
- Stage 0 fiel von >10 Min auf 63 s (gemessen im zweiten End-to-End-Lauf 2026-05-16, `run_2026-05-16_1827_hotcakes.md`).
- Keine Sub-Agent-Extraction mehr getriggert (verifiziert).
- Snapshot wächst von 10 auf 11 Wissens-Files.
- Bei Änderung an WAWI-IMPORT-WISSEN.md oder cowork_anweisung_datenimports.md muss der Run-Brief ggf. mitgepflegt werden — neuer Drift-Pfad, der über Cycle 4 jedes Wissens-Updates abgefangen werden muss.

*Verworfen:*
- *Run-Brief direkt in den Cowork-Trigger einbetten:* möglich, aber Trigger wird ~15 KB länger und drift-frei nur, wenn jedem Lauf der ganze Brief mitgegeben wird. Snapshot-Pfad ist sauberer.
- *Großen Files auf Stub kürzen:* würde die Wissens-Substanz für künftige Klärungen verlieren. Originale bleiben im Snapshot, sind nur nicht mehr in Stage 0.
- *Cowork-internes Extraction-Verhalten deaktivieren:* aus dem Klärungs-Chat nicht abschaltbar (A8, Cowork-Internals).

---

**E85 — Wissens-Update-Build-Pattern als Standard-Playbook.**
*Stand:* 2026-05-18. *Bezug:* E47 (Snapshot-Architektur), E64 (Lokaler Workflow), E65 (Stückelung), E66 (Build-Strategie), E67 (Tag-Neustart), v1.17-Build-Run.
*Warum:* Der v1.17-Build (165-KB-Monolith in 6 Themen-Cluster, 79/79 byte-identisch) lief mehrere Stunden Cowork autonom durch. Der Erfolgsfaktor war ein detaillierter Vorab-Plan mit 12 linearen Stages, harten Rules und klaren Anti-Patterns. Damit künftige Wissens-Builds nicht jedes Mal den Plan neu erfinden, wird das Pattern als operative Spec gefroren.
*Entscheidung:* Neues File `WISSENS-UPDATE-PLAYBOOK.md` (entstanden in v1.18 als Bootstrap). Cowork lädt es bei Trigger „Verarbeite Wissens-Update für ..." analog zu `run_brief_daten.md` für Daten-Läufe. Inhalt: 12-Stage-Pattern, Tool-Patterns (Sandbox-Pfad-Trick, Subagent für große Files, base64Content-Default), Anti-Patterns (Karteileiche, Trailing-Newline, Header-Bump-Vergessen), Versionierungs-Policy (siehe E86), Self-Check-Liste WSC-1 bis WSC-17, Manifest-Spec.
*Konsequenzen:* Snapshot wächst um ein File (von 17 auf 18 Wissens-Files). SPEC_KONSTANTEN Sektion 13 aktualisiert. `cowork_custom_instructions.md` bekommt neue Trigger-Erkennung. Ab v1.19 sind Cowork-Trigger viel kürzer (Scope-Definition statt voller Build-Plan).
*Verworfen:* Pattern als Teil von `cowork_anweisung_datenimports.md` belassen (würde Daten-Pipeline-Spec aufblähen, falsche Domäne). Pattern nur als E-Eintrag dokumentieren (zu wenig konkret für autonome Ausführung). Pattern in `Projekt-Anweisungen.md` belassen (das ist Claude.ai-Projekt-Spec, nicht Cowork-Spec).

---

**E86 — File-Header-Versionierungs-Konvention.**
*Stand:* 2026-05-18. *Bezug:* Charter-Prinzip 12, E47 (Snapshot-Architektur), Beobachtung v1.17-Build (4 Files modifiziert ohne Header-Bump).
*Warum:* Im v1.17-Build wurden vier Files (SPEC_KONSTANTEN.md, cowork_anweisung_datenimports.md, Projekt-Anweisungen.md, cowork_custom_instructions.md) durch Referenz-Updates modifiziert, aber die File-internen Versions-Header wurden nicht mit-gebumpt. Konsequenz: gleicher Versions-String im File-Header, unterschiedlicher Inhalt zwischen Snapshots — forensisch verwirrend bei Rollback-Analyse oder Cross-Snapshot-Diff.
*Entscheidung:* SemVer-style Bump-Konvention.
- **Patch** (v1.15 → v1.15.1): reine Referenz-/Cross-Verweis-Updates ohne Inhalts-Änderung.
- **Minor** (v1.15 → v1.16): Inhalts-Updates, neue Sektionen, neue Regeln.
- **Major** (v1.15 → v2.0): strukturelle Umbauten, Architektur-Pivots.
- **Edge-Case:** wenn ein File nur „mit-mitgenommen" (ohne Modifikation kopiert) wird, kein Bump.
Snapshot-Version (Folder-Name) und File-Header sind entkoppelt — der Snapshot ist der Stand des Sets, der Header ist der Stand des einzelnen Files.
*Konsequenzen:* WSC-17 in Self-Check des Playbooks. Charter-Prinzip 12 verankert die Disziplin. v1.18-Build holt die 4 ausstehenden v1.17-Header-Bumps nach (Patch-Bumps).
*Verworfen:* Patch-Bumps weglassen und nur Inhalts-Updates bumpen (würde das Original-Problem nicht lösen — forensische Lücke bleibt). Snapshot-Version 1:1 in File-Header spiegeln (würde Modifikations-Stand verschleiern).

---

**E87 — Migration Drive → Git als Wissens-Backbone.**
*Stand:* 2026-05-18 (v1.19, Pattern-Pivot). *Bezug:* E47 (Drive-Snapshot-Architektur, abgelöst), E64 (Lokaler Workflow, präzedent), E85 (Build-Pattern als Standard), E86 (Versionierungs-Disziplin), A9/A10/A11 (Drive-MCP-Tool-Limits aus v1.18-Build).

*Warum:* Drei voneinander unabhängige Schmerzpunkte hatten sich im v1.17- und v1.18-Build zur kritischen Engstelle akkumuliert:

1. **Drive-MCP-Tool-Limits (A9/A10/A11):** Files >50 KB markdown (≈ >67 KB base64 ≈ >17k Output-Tokens) sind über `create_file` mit `base64Content`-Parameter weder im Main-Agent noch im Subagent zuverlässig uploadbar. Sonnet-Subagent leidet zusätzlich an UTF-8-Drift (~1 char/10KB) bei längeren base64-Strings. Im v1.18-Build mussten 2 von 18 Files (BACKLOG 71 KB, datenimports 73 KB) per `present_files` an Tjorben ausgegeben und manuell per Drag-and-Drop hochgeladen werden — bricht die End-to-End-Automation.

2. **Karteileichen ohne `delete_file` (B33):** Drive-MCP hat keine Delete-Operation. Fehlgeschlagene Uploads bleiben als Karteileichen im Snapshot-Folder, müssen manuell in der Drive-Web-UI bereinigt werden. v1.18 hatte 6 neue Karteileichen + 3 Altlasten aus v1.17. Akkumulation latent, weil pro Build neue dazu kommen.

3. **Manueller Tjorben-Upload als End-to-End-Bruch:** Selbst wenn die ersten beiden Probleme nicht zuschlagen, war Tjorbens Drag-and-Drop in den Drive-Sub-Folder ein expliziter manueller Schritt — bricht die „Mensch initiiert, Maschine arbeitet"-Disziplin (Charter Prinzip 1) genau in der falschen Richtung, weil hier die Maschine etwas tun könnte, das sie ans Werkzeug zurückgibt.

Tjorben hat parallel auf Claude Code als lokale CLI umgestellt. Damit ist ein lokales Git-Repo + GitHub-Remote technisch trivial pflegbar — und löst alle drei Schmerzpunkte gleichzeitig.

*Entscheidung:*
- **Wissens-Backbone:** lokales Git-Repo `~/Documents/polesportshop-wissen/`, Remote `https://github.com/verticalogmbh/polesportshop-wissen` (Branch `main`).
- **Snapshots:** Git-Tags `v1.19`, `v1.20`, ... — kein Sub-Folder-Pattern mehr, kein sekundengenaues Timestamp-Naming. Tag entspricht dem Stand des gesamten Sets, atomar referenzierbar.
- **Build-Engine:** Claude Code (lokal, Opus 4.7 oder Sonnet) öffnet das Repo, modifiziert Files via Edit/Write-Tools direkt auf Disk, committet, taggt, pusht.
- **Resolution-Pfad:** Lokales Repo für Claude-Code-Sessions und Klärungs-Chats sofort verfügbar. Cowork-Resolution auf GitHub-Raw (`https://raw.githubusercontent.com/verticalogmbh/polesportshop-wissen/<tag>/<file>`) wird in v1.20 nachgezogen (B63). Bis dahin läuft Cowork weiter mit dem Drive-Snapshot `Version_2026-05-18_141930` — der bleibt als Read-Only-Archiv erhalten.
- **Playbook-Pivot:** `WISSENS-UPDATE-PLAYBOOK.md` v1.0 → v2.0 als Major-Bump. Drive-Pattern wandert in den Legacy-Anhang (Sektion 11). 7-Stage-Build-Pattern statt 12-Stage. WSC-1 bis WSC-17 Git-adaptiert (Drive-spezifische Checks ersetzt durch `git status`, Tag-Existenz, Push-Verifikation).

*Konsequenzen:*
- v1.19 ist der erste Build, der nach dem Git-Pattern entsteht.
- Drive-Folder `Wichtig: Claude Backup/` bleibt als Read-Only-Archiv erhalten; keine neuen Sub-Folder ab v1.19.
- B61 (WAWI-IMPORT-WISSEN.md Split) und B62 (cowork_anweisung_datenimports.md Split) deferred — in der Git-Welt ist >50 KB kein Upload-Killer mehr, nur noch ein Lesbarkeits-Hinweis. Re-Evaluation bei konkreter Performance-Notlage.
- B33 (Drive-MCP fehlt `delete_file`) wird bedeutungslos für Wissens-Updates (Git-`rm` ersetzt es).
- A9/A10/A11 sind im Git-Pfad keine Limits mehr (Edit/Write-Tools haben keinen vergleichbaren Token-Output-Cap für File-Inhalt).
- Charter-Prinzip 9 („Klein nach groß, modular wachsen") greift: ein Werkzeug-Wechsel löst drei latente Probleme strukturell, statt jedes einzeln zu patchen.

*Verworfen:*
- *Drive-MCP-Erweiterung um `update_file` + `delete_file` anfordern:* würde A9/A10/A11 nicht lösen (Output-Token-Cap bleibt unabhängig von Tool-Repertoire). Plus: Wartezeit auf Anthropic-Feature-Release unkalkulierbar.
- *Eigenen Workspace-Worker für Drive-API bauen:* zu viel Engineering-Aufwand für ein Symptom-Fix (Charter Prinzip 9). Git/GitHub ist seit Jahrzehnten gelöstes Problem.
- *Drive-Pattern aufrechterhalten und Files unter 50 KB zwingen (Cluster-Split bei jedem >50 KB-File):* würde 3 große Files gleichzeitig splitten erzwingen (WAWI-IMPORT-WISSEN, cowork_anweisung_datenimports, BACKLOG). Aus Cowork-Token-Optik wünschenswert, aber als Mitigation gegen Drive-MCP-Limit überdimensioniert — der Limit verschwindet mit Git komplett.
- *Hybrid-Pattern (Git für Build, Drive für Cowork-Resolution dauerhaft):* würde zwei Truth-Quellen erzeugen. Akzeptiert nur als Übergangsmodus für v1.19, mit klarem Migrations-Pfad (B63) zu Git als Single Truth.

*Folgeaufgaben:*
- B63 (NEU v1.19): Cowork-Resolution auf GitHub-Raw-URL umstellen, `cowork_custom_instructions.md` + `Projekt-Anweisungen.md` entsprechend anpassen. v1.20-Scope.
- B61/B62 (NEU v1.19, deferred): Cluster-Splits in Git-Welt nicht zwingend, neu evaluieren wenn konkreter Pain auftritt.

*Stolperfallen:*
- **Cowork läuft bis v1.20 noch mit Drive-Snapshot.** Falls Tjorben in v1.19 einen Cowork-Pipeline-Lauf startet, zieht Cowork den letzten gültigen Drive-Snapshot (`Version_2026-05-18_141930` = v1.18-Stand). Die v1.19-Änderungen (E89, E90, F2-F6-Fixes) wirken sich erst aus, wenn (a) Cowork explizit auf Git umstellt (B63) oder (b) Tjorben die v1.19-Files manuell in einen neuen Drive-Sub-Folder kopiert. Übergangs-Workaround dokumentiert in Lauf-Brief-Trigger.
- **Tag-Disziplin:** `git tag` muss nach `commit`, vor `push --tags`. Bei vergessenem `--tags` ist der Tag lokal nur, GitHub-Release-Page fehlt. WSC-16 prüft Remote-Tag-Existenz.
