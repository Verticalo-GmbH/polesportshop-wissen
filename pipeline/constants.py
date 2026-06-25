"""
Aus SPEC_KONSTANTEN.md abgeleitete harte Konstanten (Snapshot v1.21).

P1: nur die gesicherten Konstanten (Pricing-Faktor, Farb-Lokalisierung E92,
Sprachen, CSV-Format, Multi-Kategorie-Anker). Die großen Lookup-Tabellen
(E58 Sprach-Lookup, E50 Merkmalwerte, E55 SEO-Templates, E51 Kategorien)
werden in P4 verbatim aus SPEC_KONSTANTEN portiert — bis dahin TODO-markiert,
damit nichts geraten wird (Charter-Prinzip 10).
"""
from __future__ import annotations

# --- Pricing (Marge-Modell E104) -----------------------------------------
# Brutto-VK wird so gesetzt, dass die JTL-Spalte „Gewinn %" (= Marge: Netto-VK gegen
# Ø-Netto-EK/GLD) einen Zielwert trifft. MARGE_ZIEL = 0,40 = 40 % (Haus-Standard, an dem
# auch das Bestandssortiment liegt). Rechenweg: Netto-VK = GLD / (1 - MARGE_ZIEL);
# Brutto-VK = Netto-VK * MWST_FAKTOR -> kaufm. auf ,90 -> Charm. Da der VK aus der GLD
# folgt, treibt jede GLD-Änderung direkt den VK. (Löst E102-Fix ab: „EK×2" gab ~50 %.)
MARGE_ZIEL = 0.40
MWST_FAKTOR = 1.19  # DE-Mehrwertsteuer; Netto-VK -> Brutto-VK
AUFSCHLAGSFAKTOR = 2.0  # LEGACY (altes „EK×2"-Modell) — vom Marge-Modell abgelöst, nicht mehr im VK
# Interim-Margen-Schutz (E98/E103), bis pro Lieferant historische Werte vorliegen (B68/B70).
# Nach EU/Nicht-EU differenziert — gesteuert über den expliziten Lieferanten-Tag `eu:`
# im Mapping (NICHT mehr über die Währung; ein EUR-fakturierender Nicht-EU-Lieferant
# würde sonst falsch eingestuft). Drei Hebel:
# - VK-Aufschlag (Brutto-VK): Nicht-EU +5,00 EUR (Zoll/Versand/Bank); EU 0 (statt dessen EK-Puffer).
# - EK-Aufschlag (EU): +1,00 EUR auf den EK -> via ×2×MwSt in den VK.
# - GLD-Aufschlag (Ø-EK/GLD): EU +0,50 EUR (Bank/Handling); Nicht-EU +2,30 EUR (Zoll+Versand+Bank).
# GLD-Aufschlag = geschätzte Beschaffungs-Zusatzkosten je Stück; fließt in die GLD und
# damit (über das Marge-Modell, ×1,98 auf den VK) in den Brutto-VK. Übergangs-Pauschalen,
# bis historische Rechnungsdaten pro Lieferant vorliegen (B68):
GLD_AUFSCHLAG_EU_EUR = 1.00        # EU: innereurop. Versand/Bank -> ~+2 € VK
GLD_AUFSCHLAG_NICHTEU_EUR = 2.75   # Nicht-EU: Zoll+Versand+Bank (konservativ) -> ~+5 € VK
# LEGACY (altes „EK×2"+Puffer-Modell, vom Marge-Modell E104 abgelöst — nicht mehr im VK):
VK_AUFSCHLAG_AUSLAND_EUR = 5.00
EK_AUFSCHLAG_EU_EUR = 1.00

# --- Sprachen ------------------------------------------------------------
LANGUAGES = ["de", "en", "fr", "it", "es"]  # DE ist Master (Charter-Prinzip 6)

# --- Farb-Lokalisierung DE (E92, v1.21) ----------------------------------
# Marketing-Farben mit sinnvollem DE-Pendant werden im deutschen Artikelnamen
# lokalisiert. Volle Tabelle: SPEC_KONSTANTEN Sektion 6 — in P4 verifizieren.
FARB_LOKALISIERUNG_DE = {
    "teal": "Türkis",
    "sky": "Himmelblau",
    "cherry": "Kirschrot",
    "emerald": "Smaragdgrün",
    "lime": "Limettengrün",
}
# Marketing-Farben OHNE DE-Pendant bleiben identisch; Print-Familien (Original,
# Heat, ...) bleiben überall identisch.
FARB_NICHT_LOKALISIEREN = {"nude", "mauve", "tan", "skin"}

# --- Multi-Kategorie 3-Zeilen-Pattern (E92, korrigiert E89) --------------
KATEGORIE_OBERKATEGORIE = "Pole Dance Kleidung"  # Ebene 1; bei dieser Zeile Ebene 2 leer
SARA_KATEGORIE_PFAD = ("Intern", "Neue Artikel für Sara")  # WaWi-Key 546
SARA_KATEGORIE_KEY = 546

# --- CSV-Format (run_brief_daten.md, alle 5 CSVs) ------------------------
CSV_ENCODING = "utf-8-sig"   # UTF-8 MIT BOM
CSV_DELIMITER = ";"
CSV_LINETERMINATOR = "\r\n"  # CRLF
DECIMAL_SEPARATOR = ","      # DE-Locale: 12,50 nicht 12.50

# --- Bild-Spalten (Stammdaten) -------------------------------------------
MAX_BILD_SPALTEN = 10  # Bild 1 .. Bild 10

# --- Extraktion: Scope-Filter & Typ-Klassifikation (P2) ------------------
# Scope-Entscheidung Tjorben 2026-06-15: STRIKT POLE-KLEIDUNG.
# Behalten = diese Garment-Typen (Reihenfolge = Match-Priorität, längste zuerst):
GARMENT_TYPES_KEEP = [
    ("bodysuit", "Bodysuit"),
    ("biker shorts", "Shorts"),
    ("biker", "Shorts"),
    ("leggings", "Leggings"),
    ("shorts", "Shorts"),
    ("bottom", "Bottom"),
    ("top", "Top"),
]
# Ausschluss-Tokens (Swimwear, Outerwear, Streetwear, Accessoires): wenn ein
# Titel eines dieser Tokens enthält, fällt das Produkt RAUS (vor KEEP-Match).
EXCLUDE_TOKENS = [
    "bikini", "bandeau", "bralette", "garter", "hoodie", "bomber",
    "sweater", "romper", "tote bag",
]
# Titel ohne Garment-Token, die wirklich raus müssen:
EXCLUDE_TITLES_EXPLICIT = {"valentine's garden"}
# Kuratierte Titel-Overrides: Titel ohne sauberen Garment-Token, aber bekannte
# Pole-Kleidung. Form: lower(titel) -> (modell_basis, garment_type, farbe_raw).
TITLE_OVERRIDES = {
    "robbie- aqua": ("Robbie", "Bodysuit", "aqua"),  # Robbie Bodysuit, 4. Farbe
}
# Titel, die in den Review-Bucket gezwungen werden (Material-als-Modell / Streetwear):
FORCE_REVIEW_TITLES = {
    "voyeur leggings",                          # Streetwear-Familie (Voyeur Sweater)
    "neoprene biker shorts- pure vanilla",      # "Neoprene" ist Material, kein Modell
    "neoprene bottom- wild things",             # dito
}

# --- Extraktion: Farb-Vokabular & Print-Familien (P2) --------------------
# Farbe wird nur extrahiert (a) als Dash-Suffix nach dem Garment-Typ, oder
# (b) via Override (Farbe im Namen). Colorway-Namen wie "Black Coffee" oder
# "Dark Roast" sind KEINE Farb-Variante -> color="" (Default-Zweig).
# Bekannte Farb-Tokens (lowercase) für die Dash-Suffix-Validierung:
COLOR_VOCAB = {
    "tan", "cherry", "nude", "gold", "black", "teal", "aqua", "red", "mauve",
    "light blue", "skin", "skin tones", "emerald", "sky", "lime", "marine blue",
    "olive green", "leopard", "silver", "coral red", "peach", "blue grey",
    "dusty pink", "aquamarine", "neon orange", "light pistachio/white",
    "pure vanilla", "wild things", "japanese peonies",
}
# Print-/Muster-Familien: bleiben in JEDER Sprache identisch, werden NICHT als
# Farbe lokalisiert (E92). Teil von Savanna-Serie.
PRINT_FAMILIES = {"original", "heat"}
# Override: Modelle mit Farbe IM Namen (kein Dash-Separator). Form:
#   "savanna" -> Farbe ist das/die Token zwischen Modell-Stamm und Garment-Typ.
# Savanna-Serie: "Savanna <Farbe/Print> <Top|Bottom>". Modell-Stamm = "Savanna".
COLOR_IN_NAME_FAMILIES = {"savanna"}

# --- Größen-Normalisierung (E27) -----------------------------------------
# kombi_reduziert_auf_kleinste: "XS/S"->"XS", "S/M"->"S", "M/L"->"M", "L/XL"->"L",
# "XL/XXL"->"XL". Einzel-/Sonderfälle separat behandeln.
GROESSEN_RANG = ["XS", "S", "M", "L", "XL", "XXL"]
GROESSE_EINHEIT = {"o/s", "os", "one size", "default title"}  # keine echte Größen-Achse

# --- TODO (P4): verbatim aus SPEC_KONSTANTEN portieren -------------------
# - SPRACH_LOOKUP (E58): Größen/Variations-Begriffe DE->EN/FR/IT/ES
# - MERKMALWERTE (E50): erlaubte WaWi-Merkmalwerte (Farbe, Größe, Style)
# - SEO_TEMPLATES (E55): Titel-Tag + Meta-Description Templates
# - KATEGORIE_MAP (E51): Produkt-Typ -> Subkategorie
# - STAMMDATEN_SCHEMA: die 48 Spaltennamen in Reihenfolge (Sektion 1)
