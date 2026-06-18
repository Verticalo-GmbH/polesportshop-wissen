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

    # Weg B (E94): Artikelnummer = vorab vergebene A-Nummer (nicht leer).
    vater_artnrs = {v.artikelnummer for v in vaeter}
    art_set = all(r["Artikelnummer"] for r in stammdaten)
    chk(1, "Stammdaten 49 Spalten + Artikelnummer gesetzt (Weg B)",
        len(spec.STAMMDATEN_COLUMNS) == 49 and art_set)

    # Multi-Kategorie: pro Vater 3 Zeilen, pro Kind 2 — gruppiert über A-Nummer
    from collections import Counter
    artnr_rows = Counter(r["Artikelnummer"] for r in stammdaten)
    vater_ok = all(artnr_rows[nr] == 3 for nr in vater_artnrs)
    kind_nrs = [r["Artikelnummer"] for r in stammdaten if r["Identifizierungsspalte Vaterartikel"]]
    kind_ok = all(c == 2 for c in Counter(kind_nrs).values())
    chk(2, "Multi-Kategorie Vater=3 / Kind=2 Zeilen", vater_ok and kind_ok)

    # Sara-Zeile pro Vater genau 1
    sara = Counter(r["Artikelnummer"] for r in stammdaten if r["Kategorie Ebene 2"] == spec.SARA_EBENE2)
    chk(3, "Sara-546-Zeile je Vater", all(sara[nr] == 1 for nr in vater_artnrs))

    # SEO nur auf Vater (Kinder leer)
    seo_on_kind = [r for r in stammdaten if r["Identifizierungsspalte Vaterartikel"] and r.get("Titel-Tag (SEO)")]
    chk(4, "SEO nur auf Vater-Zeilen", not seo_on_kind)

    # Bottom -> Shorts im DE-Namen
    bad_bottom = [r["Artikelname"] for r in stammdaten
                  if r["Artikelnummer (Lieferant)"].split("_")[0].count("-Bottom") and " Bottom " in f" {r['Artikelname']} "]
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
    all_arts = {r["Artikelnummer (Lieferant)"] for r in stammdaten}
    chk(11, "Farbe Kleidung auf Vater+Kind dupliziert", all_arts <= farbe_arts)

    # Attribute: 4 je Artikel, 5 Sprachen non-empty
    from collections import Counter as Ctr
    attr_per_art = Ctr(r["Artikelnummer (Lieferant)"] for r in attribute)
    chk(12, "Attribute 4 je Artikel", all(c == 4 for c in attr_per_art.values()))
    langcols = ["Attributwert", "Englisch: Attributwert", "Französisch: Attributwert",
                "Italienisch: Attributwert", "Spanisch: Attributwert"]
    full = all(all(r[c] for c in langcols) for r in attribute)
    chk(13, "Attribute alle 5 Sprachen befüllt", full)

    # Cross-Selling (Weg B: über A-Nummer): rechts nur Väter, links inkl. Kinder
    right_ok = all(r["Artikelnummer Cross-Seller"] in vater_artnrs for r in crossselling)
    left_has_kids = any(r["Artikelnummer"] not in vater_artnrs for r in crossselling)
    chk(14, "Cross-Selling rechts nur Väter (A-Nummer)", right_ok)
    chk(15, "Cross-Selling Kinder-Replikation links", left_has_kids or not crossselling)

    # Preise: VK = EK*2 -> ,90 (Komma-Dezimal)
    from .pricing import round_vk_90
    vk_calc_ok = all(round(v.vk_brutto, 2) == round(round_vk_90(v.ek_netto * C.AUFSCHLAGSFAKTOR)
                                                    + C.VK_AUFSCHLAG_EUR, 2) for v in vaeter)
    fmt_ok = all(r["Brutto-VK"].endswith(",90") for r in stammdaten)
    chk(16, f"Preise VK = EK×2 +{C.VK_AUFSCHLAG_EUR:.0f}€ kaufm. ,90 + Komma-Dezimal", vk_calc_ok and fmt_ok)
    return res
