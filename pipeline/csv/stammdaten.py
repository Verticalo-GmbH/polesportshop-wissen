"""
CSV 1: Stammdaten (48 Spalten, SPEC §1/§4).

Multi-Kategorie: Vater = 3 Zeilen (Oberkat / Subkat / Sara-546), Kind = 2 Zeilen
(Oberkat / Subkat), alle mit gleicher Artikelnummer. SEO nur auf Vater-Zeilen.
Bild 1-10 leer (werden in P9 nach R2-Upload befüllt).
"""
from __future__ import annotations

from .. import spec, constants as C
from ..model import Vater
from ._writer import fmt_decimal


def _base_row(supplier: dict, run_date: str) -> dict:
    d = dict(spec.DEFAULTS)
    d["Hersteller"] = supplier["hersteller"]
    d["Steuerklasse"] = supplier.get("steuerklasse") or spec.DEFAULTS["Steuerklasse"]
    d["TARIC-Code"] = str(supplier.get("taric_code") or spec.DEFAULTS["TARIC-Code"])
    d["Herkunftsland"] = supplier.get("herkunftsland", "")
    d["Neu im Sortiment seit"] = run_date
    return d


def _kategorie_rows(is_vater: bool, garment_type: str) -> list[tuple[str, str]]:
    sub = spec.KATEGORIE_SUB[garment_type]
    rows = [
        (spec.OBERKATEGORIE, ""),            # A Oberkategorie (Ebene 2 leer)
        (spec.OBERKATEGORIE, sub),           # B Unterkategorie
    ]
    if is_vater:
        rows.append((spec.SARA_EBENE1, spec.SARA_EBENE2))  # C Sara-546 (nur Vater)
    return rows


def _bild_fields(v: Vater) -> dict:
    """Bild 1..10 aus v.r2_bild_urls (P9). Leer wenn noch keine Bilder."""
    out = {}
    for i in range(1, C.MAX_BILD_SPALTEN + 1):
        out[f"Bild {i}"] = v.r2_bild_urls[i - 1] if i - 1 < len(v.r2_bild_urls) else ""
    return out


def _names(marke: str, gtype: str, modell: str, farbe: str) -> dict[str, str]:
    return {lang: spec.vater_artikelname(marke, gtype, modell, farbe, lang)
            for lang in C.LANGUAGES}


def _seo_fields(names: dict[str, str]) -> dict:
    out = {}
    out["Titel-Tag (SEO)"] = spec.SEO_TITEL["de"].format(name=names["de"])
    out["Meta-Description (SEO)"] = spec.SEO_META["de"].format(name=names["de"])
    langmap = {"en": "Global-Englisch", "fr": "Global-Französisch",
               "it": "Global-Italienisch", "es": "Global-Spanisch"}
    for lang, pfx in langmap.items():
        out[f"{pfx}: Titel-Tag"] = spec.SEO_TITEL[lang].format(name=names[lang])
        out[f"{pfx}: Meta-Description"] = spec.SEO_META[lang].format(name=names[lang])
    return out


def build_rows(vaeter: list[Vater], supplier: dict, run_date: str) -> list[dict]:
    marke = supplier["marke_kurz"]
    rows: list[dict] = []
    # Weg B (E94): Artikelnummer = vorab vergebene A-Nummer aus dem WaWi-Nummernkreis
    # (numbering.assign). Verknüpfung Vater<->Kind + Cross-Selling über die A-Nummer;
    # der sprechende Schlüssel bleibt in 'Artikelnummer (Lieferant)' für Merkmale/Attribute.
    for v in vaeter:
        vnr = spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)
        vnames = _names(marke, v.garment_type, v.modell_basis, v.farbe_raw)
        seo = _seo_fields(vnames)

        # --- Vater: 3 Kategorie-Zeilen ---
        for ebene1, ebene2 in _kategorie_rows(True, v.garment_type):
            r = _base_row(supplier, run_date)
            r.update({
                "Artikelnummer": v.artikelnummer, "Artikelnummer (Lieferant)": vnr,
                "Identifizierungsspalte Vaterartikel": "",
                "Artikelname": vnames["de"],
                "Variationsname 1": "Größe", "Variationswert 1": "",
                "Kategorie Ebene 1": ebene1, "Kategorie Ebene 2": ebene2,
                "EK Netto (für GLD)": fmt_decimal(v.ek_netto),
                "Brutto-VK": fmt_decimal(v.vk_brutto),
                "Netto-EK": fmt_decimal(v.ek_netto),
                "Global-Englisch: Artikelname": vnames["en"],
                "Global-Französisch: Artikelname": vnames["fr"],
                "Global-Italienisch: Artikelname": vnames["it"],
                "Global-Spanisch: Artikelname": vnames["es"],
                **seo, **_bild_fields(v),
            })
            rows.append(r)

        # --- Kinder: 2 Kategorie-Zeilen je Kind, SEO leer ---
        for k in v.kinder:
            knr = spec.kind_artnr(vnr, k.groesse)
            knames = {lang: f"{vnames[lang]} {k.groesse}" for lang in C.LANGUAGES}
            for ebene1, ebene2 in _kategorie_rows(False, v.garment_type):
                r = _base_row(supplier, run_date)
                r.update({
                    "Artikelnummer": k.artikelnummer, "Artikelnummer (Lieferant)": knr,
                    "EAN": k.ean or "",   # GTIN/UTC pro Größe (E95), nur Kind
                    "Identifizierungsspalte Vaterartikel": v.artikelnummer,
                    "Artikelname": knames["de"],
                    "Variationsname 1": "Größe", "Variationswert 1": k.groesse,
                    "Kategorie Ebene 1": ebene1, "Kategorie Ebene 2": ebene2,
                    "EK Netto (für GLD)": fmt_decimal(v.ek_netto),
                    "Brutto-VK": fmt_decimal(v.vk_brutto),
                    "Netto-EK": fmt_decimal(v.ek_netto),
                    "Global-Englisch: Artikelname": knames["en"],
                    "Global-Französisch: Artikelname": knames["fr"],
                    "Global-Italienisch: Artikelname": knames["it"],
                    "Global-Spanisch: Artikelname": knames["es"],
                    **_bild_fields(v),
                })
                rows.append(r)
    return rows


COLUMNS = spec.STAMMDATEN_COLUMNS
