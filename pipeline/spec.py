"""
Verbatim-Port der harten Schema-Konstanten aus SPEC_KONSTANTEN.md (Snapshot v1.21).
Sektionen 1-7. Bei Konflikt gewinnt SPEC_KONSTANTEN.md (Charter-Prinzip 11).

Quelle-Anker:
  §1 Stammdaten-Schema (48 Spalten, v3.1/E54)
  §2 Standardwerte Kleidung-Pilot
  §3 Kategorie-Mapping (E51)
  §4 Vater-Kind-Konventionen (Multi-Kategorie 3-Zeilen, E57+E89+E92)
  §5 SEO-Templates (E55)
  §6 Sprach-Lokalisierung (E58) + Farb-Lookup
  §7 Merkmalwerte (E50)
"""
from __future__ import annotations

# --- §1 Stammdaten-Schema: 48 Spalten in EXAKTER Reihenfolge -------------
STAMMDATEN_COLUMNS = [
    "Artikelnummer", "Artikelnummer (Lieferant)", "HAN",
    "Identifizierungsspalte Vaterartikel", "Artikelname", "Hersteller",
    "Steuerklasse", "TARIC-Code", "Variationsname 1", "Variationswert 1",
    "Kategorie Ebene 1", "Kategorie Ebene 2",
    "EK Netto (für GLD)", "Brutto-VK",
    "Bestandsführung aktiv", "Neu im Sortiment", "Neu im Sortiment seit",
    "Artikelgewicht", "Versandgewicht", "Versandklasse", "Herkunftsland",
    "Global-Englisch: Artikelname", "Global-Französisch: Artikelname",
    "Global-Italienisch: Artikelname", "Global-Spanisch: Artikelname",
    "Titel-Tag (SEO)", "Meta-Description (SEO)",
    "Global-Englisch: Titel-Tag", "Global-Englisch: Meta-Description",
    "Global-Französisch: Titel-Tag", "Global-Französisch: Meta-Description",
    "Global-Italienisch: Titel-Tag", "Global-Italienisch: Meta-Description",
    "Global-Spanisch: Titel-Tag", "Global-Spanisch: Meta-Description",
    "Netto-EK", "Ist Standardlieferant", "Lieferzeit in Tagen (Lieferant)",
    "Bild 1", "Bild 2", "Bild 3", "Bild 4", "Bild 5",
    "Bild 6", "Bild 7", "Bild 8", "Bild 9", "Bild 10",
]
assert len(STAMMDATEN_COLUMNS) == 48

# --- §2 Standardwerte ----------------------------------------------------
DEFAULTS = {
    "Steuerklasse": "OSS2-undefiniert - Standard alle Länder",
    "TARIC-Code": "62114390",
    "Artikelgewicht": "0,05",
    "Versandgewicht": "0,05",
    "Versandklasse": "standard",
    "Bestandsführung aktiv": "Y",
    "Neu im Sortiment": "Y",
    "Ist Standardlieferant": "Y",
    "Lieferzeit in Tagen (Lieferant)": "0",
}

# --- §3 Kategorie-Mapping (Ebene1, Ebene2) pro Garment-Typ ---------------
OBERKATEGORIE = "Pole Dance Kleidung"
KATEGORIE_SUB = {
    "Top": "Pole Dance Tops",
    "Bottom": "Pole Dance Shorts",
    "Shorts": "Pole Dance Shorts",
    "Bodysuit": "Bodysuits",
    "Leggings": "Leggings",
}
# §4 Sara-Pflicht-Zeile (Key 546)
SARA_EBENE1 = "Intern"
SARA_EBENE2 = "Neue Artikel für Sara"

# --- §6 Produkt-Substantiv pro Sprache (Bottom -> Shorts, E76) -----------
# garment_type -> {lang: Substantiv}
PRODUKTTYP = {
    "Top":      {"de": "Top",      "en": "Top",      "fr": "Haut",    "it": "Top",   "es": "Top"},
    "Bottom":   {"de": "Shorts",   "en": "Shorts",   "fr": "Short",   "it": "Shorts","es": "Pantalones Cortos"},
    "Shorts":   {"de": "Shorts",   "en": "Shorts",   "fr": "Short",   "it": "Shorts","es": "Pantalones Cortos"},
    "Bodysuit": {"de": "Bodysuit", "en": "Bodysuit", "fr": "Body",    "it": "Body",  "es": "Body"},
    "Leggings": {"de": "Leggings", "en": "Leggings", "fr": "Legging", "it": "Leggings","es": "Leggings"},
}

# --- §6 Farb-Lookup: token(lower) -> {lang: Name, 'merkmal': WaWi-Wert} --
# 'merkmal' = nächstpassender Wert aus der 15er-Liste (§7 zweistufige Logik).
COLOR_LOOKUP = {
    "black":    {"de": "Schwarz", "en": "Black", "fr": "Noir", "it": "Nero", "es": "Negro", "merkmal": "Schwarz"},
    "white":    {"de": "Weiß", "en": "White", "fr": "Blanc", "it": "Bianco", "es": "Blanco", "merkmal": "Weiß"},
    "teal":     {"de": "Türkis", "en": "Teal", "fr": "Turquoise", "it": "Turchese", "es": "Turquesa", "merkmal": "Blau"},
    "sky":      {"de": "Himmelblau", "en": "Sky", "fr": "Bleu Ciel", "it": "Azzurro Cielo", "es": "Azul Cielo", "merkmal": "Blau"},
    "emerald":  {"de": "Smaragdgrün", "en": "Emerald", "fr": "Émeraude", "it": "Smeraldo", "es": "Esmeralda", "merkmal": "Grün"},
    "lime":     {"de": "Limettengrün", "en": "Lime", "fr": "Vert Citron", "it": "Verde Lime", "es": "Verde Lima", "merkmal": "Grün"},
    "cherry":   {"de": "Kirschrot", "en": "Cherry", "fr": "Cerise", "it": "Ciliegia", "es": "Cereza", "merkmal": "Rot"},
    "pink":     {"de": "Pink", "en": "Pink", "fr": "Rose", "it": "Rosa", "es": "Rosa", "merkmal": "Pink"},
    "burgundy": {"de": "Burgundrot", "en": "Burgundy", "fr": "Bordeaux", "it": "Borgogna", "es": "Burdeos", "merkmal": "Rot"},
    "beige":    {"de": "Beige", "en": "Beige", "fr": "Beige", "it": "Beige", "es": "Beige", "merkmal": "Beige"},
    "grey":     {"de": "Grau", "en": "Grey", "fr": "Gris", "it": "Grigio", "es": "Gris", "merkmal": "Grau"},
    "brown":    {"de": "Braun", "en": "Brown", "fr": "Marron", "it": "Marrone", "es": "Marrón", "merkmal": "Braun"},
    "red":      {"de": "Rot", "en": "Red", "fr": "Rouge", "it": "Rosso", "es": "Rojo", "merkmal": "Rot"},
    "blue":     {"de": "Blau", "en": "Blue", "fr": "Bleu", "it": "Blu", "es": "Azul", "merkmal": "Blau"},
    "yellow":   {"de": "Gelb", "en": "Yellow", "fr": "Jaune", "it": "Giallo", "es": "Amarillo", "merkmal": "Gelb"},
    "green":    {"de": "Grün", "en": "Green", "fr": "Vert", "it": "Verde", "es": "Verde", "merkmal": "Grün"},
    # Niemals lokalisieren (§6) — identisch in allen Sprachen:
    "nude":  {"de": "Nude", "en": "Nude", "fr": "Nude", "it": "Nude", "es": "Nude", "merkmal": "Beige"},
    "mauve": {"de": "Mauve", "en": "Mauve", "fr": "Mauve", "it": "Mauve", "es": "Mauve", "merkmal": "Lila"},
    "tan":   {"de": "Tan", "en": "Tan", "fr": "Tan", "it": "Tan", "es": "Tan", "merkmal": "Beige"},
    "skin":  {"de": "Skin", "en": "Skin", "fr": "Skin", "it": "Skin", "es": "Skin", "merkmal": "Beige"},
    "taupe": {"de": "Taupe", "en": "Taupe", "fr": "Taupe", "it": "Taupe", "es": "Taupe", "merkmal": "Beige"},
    "lilac": {"de": "Flieder", "en": "Lilac", "fr": "Lilas", "it": "Lilla", "es": "Lila", "merkmal": "Lila"},
    # Print-Familien (§6/§7): identisch; Merkmal-Farbe = Bunt (Default Multi-Print)
    "original": {"de": "Original", "en": "Original", "fr": "Original", "it": "Original", "es": "Original", "merkmal": "Bunt"},
    "heat":     {"de": "Heat", "en": "Heat", "fr": "Heat", "it": "Heat", "es": "Heat", "merkmal": "Bunt"},
}

# --- §5 SEO-Templates (deterministisch) ----------------------------------
SEO_TITEL = {
    "de": "{name} | polesportshop.de",
    "en": "{name} | polesportshop.de",
    "fr": "{name} | polesports.fr",
    "it": "{name} | polesports.it",
    "es": "{name} | polesports.es",
}
SEO_META = {
    "de": "{name} &#10004; große Auswahl &#10004; TOP Preise &#10004; Schneller Versand &#10148; jetzt hier online bestellen!",
    "en": "{name} &#10004; Five star customer support &#10004; Top quality and price &#10004; Instant shipping &#10148; order now!",
    "fr": "{name} &#10004; Support client cinq étoiles &#10004; Qualité et prix au top &#10004; Expédition instantanée &#10148; commandez maintenant !",
    "it": "{name} &#10004; Assistenza clienti a cinque stelle &#10004; Qualità e prezzo al top &#10004; Spedizione immediata &#10148; ordina ora!",
    "es": "{name} &#10004; Soporte al cliente de cinco estrellas &#10004; Calidad y precio superiores &#10004; Envío instantáneo &#10148; ¡Ordénalo ahora!",
}

# --- §7 Merkmalwerte (statische WaWi-Listen) -----------------------------
MERKMAL_FARBE_ERLAUBT = {"Bunt", "Gold", "Schwarz", "Weiß", "Braun", "Beige",
                         "Grau", "Blau", "Grün", "Gelb", "Orange", "Rot", "Pink",
                         "Lila", "Silber"}
MERKMAL_GROESSE_ERLAUBT = {"XS", "S", "M", "L", "XL", "2XL"}
STYLE_TOPS_ERLAUBT = {"Crop Top", "Open Back", "Rundausschnitt", "Bodysuit",
                      "High Neck", "Langärmlig", "One Shoulder", "Riemchentop",
                      "Samt", "T-Shirt", "Triangle Ausschnitt"}
STYLE_SHORTS_ERLAUBT = {"Cheeky", "High Leg", "High Waist", "Low Waist",
                        "Mid Waist", "Classic Hot Pants", "Riemchenshorts",
                        "Samt", "Leggings", "Bike Shorts", "Strumpfhose"}


# --- Helfer: Artikelname (§4 E26/E56) ------------------------------------
def color_localized(farbe_raw: str, lang: str) -> str:
    """Lokalisierter Farbname; '' wenn keine Farbe. Unbekannt -> STOPP-Signal None."""
    if not farbe_raw:
        return ""
    key = farbe_raw.strip().lower()
    entry = COLOR_LOOKUP.get(key)
    if entry is None:
        raise KeyError(f"Farbe {farbe_raw!r} nicht im COLOR_LOOKUP (§6) — STOPP, nicht raten (AP8)")
    return entry[lang]


def vater_artikelname(marke_kurz: str, garment_type: str, modell: str,
                      farbe_raw: str, lang: str) -> str:
    """'{Marke} {Typ} {Modell} {Farbe}' (Farbe optional). E26/E58."""
    typ = PRODUKTTYP[garment_type][lang]
    farbe = color_localized(farbe_raw, lang)
    parts = [marke_kurz, typ, modell] + ([farbe] if farbe else [])
    return " ".join(p for p in parts if p).strip()


# --- Artikelnummer-Konvention (run_brief Cross-Selling-Beispiel v1.21) ----
# Vater:  HC-{Modell}-{Typ}-{Farbe}   z.B. HC-Peonies-Top-Nude, HC-Hekate-Bodysuit
# Kind:   {Vater}_{Größe}             z.B. HC-Peonies-Top-Nude_XS
# Typ im ARTNR = roher garment_type (Top/Bottom/Bodysuit), NICHT lokalisiert.
# Farbe im ARTNR = roher Farbtoken, Title-Case, ohne Leerzeichen.
ARTNR_PREFIX = "HC"


def set_artnr_prefix(prefix: str) -> None:
    """Pro Lieferant gesetzt (z.B. 'RO' für Rolling). Orchestrator ruft das am Lauf-Start."""
    global ARTNR_PREFIX
    ARTNR_PREFIX = prefix


def _slug(s: str) -> str:
    return "".join(w.capitalize() for w in s.replace("-", " ").split())


def vater_artnr(garment_type: str, modell: str, farbe_raw: str) -> str:
    parts = [ARTNR_PREFIX, _slug(modell), garment_type]
    if farbe_raw:
        parts.append(_slug(farbe_raw))
    return "-".join(parts)


def kind_artnr(vater_nr: str, groesse: str) -> str:
    return f"{vater_nr}_{groesse}"
