"""
Stage-6 Self-Check (SPEC §9, pragmatische Umsetzung der Kern-Invarianten).
Arbeitet auf den generierten Row-Sets. Gibt [(nr, name, ok, detail)] zurück.
"""
from __future__ import annotations

from . import spec, constants as C


def run(stammdaten, variationen, merkmale, attribute, crossselling, vaeter) -> list[tuple]:
    res = []
    def chk(n, name, ok, detail=""):
        res.append((n, name, bool(ok), detail))

    vnrs = {spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw) for v in vaeter}

    chk(1, "Stammdaten 48 Spalten", len(spec.STAMMDATEN_COLUMNS) == 48)

    # Multi-Kategorie: pro Vater 3 Zeilen, pro Kind 2
    from collections import Counter
    artnr_rows = Counter(r["Artikelnummer"] for r in stammdaten)
    vater_ok = all(artnr_rows[nr] == 3 for nr in vnrs)
    kind_nrs = [r["Artikelnummer"] for r in stammdaten if r["Identifizierungsspalte Vaterartikel"]]
    kind_ok = all(c == 2 for c in Counter(kind_nrs).values())
    chk(2, "Multi-Kategorie Vater=3 / Kind=2 Zeilen", vater_ok and kind_ok)

    # Sara-Zeile pro Vater genau 1
    sara = Counter(r["Artikelnummer"] for r in stammdaten if r["Kategorie Ebene 2"] == spec.SARA_EBENE2)
    chk(3, "Sara-546-Zeile je Vater", all(sara[nr] == 1 for nr in vnrs))

    # SEO nur auf Vater (Kinder leer)
    seo_on_kind = [r for r in stammdaten if r["Identifizierungsspalte Vaterartikel"] and r.get("Titel-Tag (SEO)")]
    chk(4, "SEO nur auf Vater-Zeilen", not seo_on_kind)

    # Bottom -> Shorts im DE-Namen
    bad_bottom = [r["Artikelname"] for r in stammdaten
                  if r["Artikelnummer"].split("_")[0].count("-Bottom") and " Bottom " in f" {r['Artikelname']} "]
    chk(5, "Bottom->Shorts im DE-Namen (E76)", not bad_bottom, str(bad_bottom[:2]))

    # Farb-Lokalisierung teal->Türkis
    teal_de_ok = all("Teal" not in r["Artikelname"] for r in stammdaten)
    chk(6, "Farb-Lokalisierung DE (kein 'Teal' im DE-Namen)", teal_de_ok)

    # Variationen: 1 Zeile pro Kind
    n_kinder = sum(len(v.kinder) for v in vaeter)
    chk(7, "Variationen 1 Zeile/Kind", len(variationen) == n_kinder, f"{len(variationen)}/{n_kinder}")

    # Merkmale: Farbe gültig, Größe gültig, Style gültig
    farbe_ok = all(r["Merkmalwertname 1"] in spec.MERKMAL_FARBE_ERLAUBT
                   for r in merkmale if r["Merkmalname"] == "Farbe Kleidung")
    groesse_ok = all(r["Merkmalwertname 1"] in spec.MERKMAL_GROESSE_ERLAUBT
                     for r in merkmale if r["Merkmalname"] == "Größe Kleidung")
    style_ok = all(r["Merkmalwertname 1"] in (spec.STYLE_TOPS_ERLAUBT | spec.STYLE_SHORTS_ERLAUBT)
                   for r in merkmale if r["Merkmalname"].startswith("Style"))
    chk(8, "Merkmal Farbe Kleidung gültig", farbe_ok)
    chk(9, "Merkmal Größe Kleidung gültig", groesse_ok)
    chk(10, "Merkmal Style gültig", style_ok)

    # Farbe Kleidung auf Vater UND Kind
    farbe_arts = {r["Artikelnummer (Lieferant)"] for r in merkmale if r["Merkmalname"] == "Farbe Kleidung"}
    all_arts = {r["Artikelnummer"] for r in stammdaten}
    chk(11, "Farbe Kleidung auf Vater+Kind dupliziert", all_arts <= farbe_arts)

    # Attribute: 4 je Artikel, 5 Sprachen non-empty
    from collections import Counter as Ctr
    attr_per_art = Ctr(r["Artikelnummer (Lieferant)"] for r in attribute)
    chk(12, "Attribute 4 je Artikel", all(c == 4 for c in attr_per_art.values()))
    langcols = ["Attributwert", "Englisch: Attributwert", "Französisch: Attributwert",
                "Italienisch: Attributwert", "Spanisch: Attributwert"]
    full = all(all(r[c] for c in langcols) for r in attribute)
    chk(13, "Attribute alle 5 Sprachen befüllt", full)

    # Cross-Selling: rechte Spalte nur Väter, linke enthält Kinder
    right_ok = all(r["Artikelnummer Cross-Seller"] in vnrs for r in crossselling)
    left_has_kids = any("_" in r["Artikelnummer"] for r in crossselling)
    chk(14, "Cross-Selling rechts nur Väter", right_ok)
    chk(15, "Cross-Selling Kinder-Replikation links", left_has_kids or not crossselling)

    # Preise: VK = EK*2 -> ,90 (Komma-Dezimal)
    from .pricing import round_vk_90
    vk_calc_ok = all(round(v.vk_brutto, 2) == round_vk_90(v.ek_netto * C.AUFSCHLAGSFAKTOR) for v in vaeter)
    fmt_ok = all(r["Brutto-VK"].endswith(",90") for r in stammdaten)
    chk(16, "Preise VK = EK×2 kaufm. ,90 + Komma-Dezimal", vk_calc_ok and fmt_ok)
    return res
