"""
One-off-Build: POLE ADDICT „The Goddess Top" (1 Vater, 5 Cup-Größen).

Besonderheiten (Tjorben 2026-06-21):
- Cup-System als EINE Variationsdimension „Größe" mit kombinierten, **selbst-
  erklärenden** Werten (z.B. „XS/S Fairy (kleinere Oberweite)") in allen 5 Sprachen
  -> Kunde sieht sofort am Auswahlpunkt, was Fairy/Goddess bedeutet (Retouren-Schutz).
  KEINE zweite Variationsdimension, KEINE Sonder-Vorlage.
- Darstellung SELECTBOX (Dropdown), damit der erklärende Text voll sichtbar ist
  (Swatch würde ihn abschneiden).
- „Größe Kleidung"-Merkmal (Shop-Filter) auf Standardgrößen gemappt (XS/S -> XS+S …).
- Vorab existierender Cross-Selling-Artikel A1009207 (passende Shorts).
- PrestaShop-Quelle (shop.poleaddict.eu) -> Daten hand-assembliert, kein Crawl.

Lauf:  python -m pipeline.build_poleaddict_goddess
"""
from __future__ import annotations

import csv
from datetime import datetime, timedelta

from . import config, constants as C, pricing, numbering, spec, content as Cont, selfcheck
from .csv import stammdaten, variationen, attribute, merkmale, bestellung
from .csv._writer import write_csv
from .model import Vater, Kind

SUPPLIER_KEY = "POLE_ADDICT_WORKOUT_WEAR"
VATER_ARTNR_START = 1009303          # bestätigt Tjorben: nächste freie WaWi-Nummer
CROSS_SELL_PARTNER = "A1009207"      # bestehende passende Shorts (Outfit-Partner)
CROSS_SELL_PARTNER_KINDER = 5        # A1009207-001..-005 (XS/S/M/L/XL, aus WaWi bestätigt)
BESTELL_REFERENZ = "Bestellung POL-2026-01 | Rechnung WDT/10 | Pole Addict Goddess Top"
PRODUCT_URL = "https://shop.poleaddict.eu/en_GB/p/The-Goddess-Top-for-pole-dance/2392"
WITH_IMAGES = True
# Reviewte Hero-Reihenfolge (Front-Studio zuerst, dann Seite/Rücken/Detail, dann Lifestyle/Set).
IMAGE_ORDER = ["top_goddesss_1", "top_goddesss_3", "top_goddesss_2", "top_goddesss_4",
               "NEW3600", "NEW3612", "Set_top"]

VARNAME = {"de": "Größe", "en": "Size", "fr": "Taille", "it": "Taglia", "es": "Talla"}

# Reihenfolge = Dropdown-Anzeige + Kind-Suffix (-001..-005): Größenband aufsteigend, Fairy vor Goddess.
# kurzcode (= groesse_raw, für Mengen-Match) | Anzeige je Sprache | Standardgrößen für Filter-Merkmal
KINDER_SPEC = [
    ("XS/S Fairy", {
        "de": "XS/S Fairy (kleinere Oberweite)", "en": "XS/S Fairy (smaller bust)",
        "fr": "XS/S Fairy (poitrine plus petite)", "it": "XS/S Fairy (seno più piccolo)",
        "es": "XS/S Fairy (pecho más pequeño)"}, ["XS", "S"]),
    ("XS/S Goddess", {
        "de": "XS/S Goddess (vollere Oberweite)", "en": "XS/S Goddess (fuller bust)",
        "fr": "XS/S Goddess (poitrine plus généreuse)", "it": "XS/S Goddess (seno più abbondante)",
        "es": "XS/S Goddess (pecho más voluminoso)"}, ["XS", "S"]),
    ("M/L Fairy", {
        "de": "M/L Fairy (kleinere Oberweite)", "en": "M/L Fairy (smaller bust)",
        "fr": "M/L Fairy (poitrine plus petite)", "it": "M/L Fairy (seno più piccolo)",
        "es": "M/L Fairy (pecho más pequeño)"}, ["M", "L"]),
    ("M/L Goddess", {
        "de": "M/L Goddess (vollere Oberweite)", "en": "M/L Goddess (fuller bust)",
        "fr": "M/L Goddess (poitrine plus généreuse)", "it": "M/L Goddess (seno più abbondante)",
        "es": "M/L Goddess (pecho más voluminoso)"}, ["M", "L"]),
    ("XL Goddess", {
        "de": "XL Goddess (vollere Oberweite)", "en": "XL Goddess (fuller bust)",
        "fr": "XL Goddess (poitrine plus généreuse)", "it": "XL Goddess (seno più abbondante)",
        "es": "XL Goddess (pecho más voluminoso)"}, ["XL"]),
]
DISP = {kc: d for kc, d, _ in KINDER_SPEC}
SIZE_MERKMAL = {kc: stds for kc, _, stds in KINDER_SPEC}


def build_vater() -> Vater:
    # k.groesse = DE-Anzeigewert (= Stammdaten „Variationswert 1" + Variationen-DE, müssen matchen);
    # k.groesse_raw = Kurzcode (Mengen-Match). kind_artnr strippt den Klammer-Zusatz -> saubere ID.
    kinder = [Kind(groesse=d["de"], groesse_raw=kc, position=i)
              for i, (kc, d, _) in enumerate(KINDER_SPEC)]
    return Vater(
        handle="the-goddess-top-for-pole-dance", product_id=2392,
        title_raw="The Goddess Top for Pole Dance black", vendor="POLE ADDICT",
        modell_basis="Goddess", garment_type="Top", farbe_raw="black",
        body_html="", image_urls=[], kinder=kinder,
    )


def build_variationen(v: Vater) -> list[dict]:
    """Lokalisierte, selbst-erklärende Variationswerte; Darstellung Dropdown (SELECTBOX)."""
    rows = []
    for i, k in enumerate(v.kinder, start=1):
        d = DISP[k.groesse_raw]
        rows.append({
            "Artikelnummer": v.artikelnummer,
            "Variationsname": VARNAME["de"], "Darstellungsform": "SELECTBOX",
            "Variationswertname": d["de"],
            "Global-Englisch: Variationsname": VARNAME["en"], "Global-Englisch: Variationswertname": d["en"],
            "Global-Französisch: Variationsname": VARNAME["fr"], "Global-Französisch: Variationswertname": d["fr"],
            "Global-Italienisch: Variationsname": VARNAME["it"], "Global-Italienisch: Variationswertname": d["it"],
            "Global-Spanisch: Variationsname": VARNAME["es"], "Global-Spanisch: Variationswertname": d["es"],
            "Sortiernummer Variation": "1", "Sortiernummer Variationswert": str(i),
        })
    return rows


def build_merkmale(v: Vater, sup: dict, content: dict) -> list[dict]:
    """Wie csv.merkmale, aber Größe-Merkmal aus kombiniertem Wert auf Standardgrößen gemappt."""
    lieferant = sup["anzeigename"]
    vnr = spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)
    c = content[vnr]
    farben = c["merkmal_farbe"]
    farben = [farben] if isinstance(farben, str) else farben
    rows: list[dict] = []

    def add(artnr, name, wert):
        rows.append({"Lieferant": lieferant, "Artikelnummer (Lieferant)": artnr,
                     "Merkmalname": name, "Merkmalwertname 1": wert})

    for f in farben:
        add(vnr, "Farbe Kleidung", f)
    for w in c["style_werte"]:
        add(vnr, "Style Tops", w)
    for k in v.kinder:
        knr = spec.kind_artnr(vnr, k.groesse)
        for f in farben:
            add(knr, "Farbe Kleidung", f)
        for std in SIZE_MERKMAL[k.groesse_raw]:
            add(knr, "Größe Kleidung", std)
        for w in c["style_werte"]:
            add(knr, "Style Tops", w)
    return rows


def _ordered_image_urls(gallery: list[dict]) -> list[str]:
    def rank(it):
        fn = it["filename"].lower()
        for i, p in enumerate(IMAGE_ORDER):
            if fn.startswith(p.lower()):
                return i
        return len(IMAGE_ORDER)
    return [it["url"] for it in sorted(gallery, key=rank)]


def build_crossselling(v: Vater) -> list[dict]:
    """Beidseitig verknüpft (Tjorben): Goddess <-> Shorts A1009207."""
    g = "Vervollständige Dein Outfit"
    rows = []
    # Vorwärts: Goddess (Vater + alle Kinder) -> Shorts
    for l in [v.artikelnummer] + [k.artikelnummer for k in v.kinder]:
        rows.append({"Artikelnummer": l, "Artikelnummer Cross-Seller": CROSS_SELL_PARTNER,
                     "Cross-Selling-Gruppe": g})
    # Rückwärts: Shorts (Vater + alle Kinder) -> Goddess (Vater). Rechte Spalte strikt Vater (E80).
    shorts = [CROSS_SELL_PARTNER] + [f"{CROSS_SELL_PARTNER}-{i:03d}" for i in range(1, CROSS_SELL_PARTNER_KINDER + 1)]
    for l in shorts:
        rows.append({"Artikelnummer": l, "Artikelnummer Cross-Seller": v.artikelnummer,
                     "Cross-Selling-Gruppe": g})
    return rows


def main() -> None:
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    run_date = datetime.now().strftime("%d.%m.%Y")
    sup = config.get_supplier(SUPPLIER_KEY)
    spec.set_artnr_prefix(sup["artnr_prefix"])

    v = build_vater()
    ek_map = pricing.load_ek_csv(config.EK_INPUT_DIR / "ek_poleaddict.csv")
    priced, missing = pricing.apply_pricing([v], ek_map, 1.0,
                                            ek_aufschlag=C.EK_AUFSCHLAG_EU_EUR, vk_aufschlag=0.0)
    if missing or not priced:
        raise SystemExit(f"EK fehlt: {missing}")

    artnr_next = numbering.assign(priced, start=VATER_ARTNR_START, persist=True)
    vnr = spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)

    # Bilder (Standard-Hersteller-Weg PrestaShop): Galerie-Originale ziehen, in reviewter
    # Reihenfolge croppen (fashion 2:3 1000x1500) + nach R2 laden -> Bild 1..10 in Stammdaten.
    if WITH_IMAGES:
        from .images import process, r2
        from .crawl import prestashop_images
        v.image_urls = _ordered_image_urls(prestashop_images.gallery_originals(PRODUCT_URL))
        client = r2.make_client()
        imgs = process.process_vater(v.image_urls[:10], sup["crop_profile"])
        v.r2_bild_urls = r2.upload_vater(client, sup["r2_prefix"], vnr, imgs)
        r2.update_artikel_index(client, sup["r2_prefix"], {vnr: v.artikelnummer})
        name_de = spec.vater_artikelname(sup["marke_kurz"], v.garment_type, v.modell_basis, v.farbe_raw, "de")
        r2.build_originals_index(client, sup["r2_prefix"], {vnr: name_de},
                                 titel=f"{sup['anzeigename']} Originalbilder")
        r2.build_master_index(client)
        print(f"Bilder: {len(v.r2_bild_urls)} verarbeitet + R2-Upload ({sup['r2_prefix']})")

    content = Cont.load_content(config.PIPELINE_DIR / "content" / "poleaddict_goddess_content.json")
    miss_c = Cont.validate(content, [vnr])
    if miss_c:
        raise SystemExit(f"Content unvollständig: {miss_c}")

    sd = stammdaten.build_rows(priced, sup, run_date)
    va = build_variationen(v)
    mk = build_merkmale(v, sup, content)
    at = attribute.build_rows(priced, sup, content)
    cs = build_crossselling(v)
    checks = selfcheck.run(sd, va, mk, at, cs, priced,
                           ek_aufschlag=C.EK_AUFSCHLAG_EU_EUR, vk_aufschlag=0.0)

    # Lieferantenbestellung (6. Output): Lieferdatum = Importdatum + lieferzeit_tage (E97/E99).
    menge = {}
    with open(config.EK_INPUT_DIR / "menge_poleaddict_goddess.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            menge[r["groesse"]] = int(r["menge"])
    lz = int(sup.get("lieferzeit_tage", 0) or 0)
    lieferdatum = (datetime.now() + timedelta(days=lz)).strftime("%d.%m.%Y")
    be = [{"Artikelnummer": k.artikelnummer, "Menge": str(menge[k.groesse_raw]),
           "Lieferdatum": lieferdatum, "Zugehörige Auftragsnummer": BESTELL_REFERENZ,
           "Lieferant": sup["anzeigename"], "Warenlager": bestellung.WARENLAGER_DEFAULT,
           "Firma": bestellung.FIRMA_DEFAULT, "Benutzer": bestellung.BENUTZER_DEFAULT}
          for k in v.kinder]

    kz = sup["kuerzel"]
    out = config.OUTPUTS_DIR / f"{kz}_GODDESS_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    written = {}
    for nr, typ, cols, rows, qa in [
        (1, "Stammdaten", stammdaten.COLUMNS, sd, False),
        (2, "Variationen", variationen.COLUMNS, va, False),
        (3, "Merkmale", merkmale.COLUMNS, mk, False),
        (4, "Attribute", attribute.COLUMNS, at, True),
        (5, "CrossSelling", ["Artikelnummer", "Artikelnummer Cross-Seller", "Cross-Selling-Gruppe"], cs, False),
        (6, "Lieferantenbestellung", bestellung.COLUMNS, be, False),
    ]:
        if not rows:
            continue
        p = out / f"{nr}_{typ}_{kz}_GODDESS_{stamp}.csv"
        write_csv(p, cols, rows, quote_all=qa)
        written[typ] = (p, len(rows))

    n_ok = sum(1 for c in checks if c[2])
    L = [f"# Lauf-Bericht POLE ADDICT Goddess Top {stamp}", "",
         f"**Vater:** {priced[0].artikelnummer} ({vnr}) | 5 Kinder -001..-005",
         f"**EK:** {priced[0].ek_original} EUR | **GLD:** {priced[0].gld} | **VK brutto:** {priced[0].vk_brutto}",
         f"**BE-Lieferdatum:** {lieferdatum} (heute + {lz} Tage Lieferzeit)",
         f"**Nummernkreis:** Vater {priced[0].artikelnummer}; WaWi-Zähler nach Import auf **{artnr_next}** setzen.",
         "", "## Self-Check", ""]
    for n, name, passed, detail in checks:
        mark = "✓" if passed else "✗"
        if n == 14 and not passed:
            mark, detail = "✓*", f"extern: Cross-Seller {CROSS_SELL_PARTNER} (bestehender Artikel, bewusst)"
        L.append(f"[#{n}] {mark} {name}{(' — ' + detail) if detail else ''}")
    L += ["", f"**Self-Check: {n_ok}/16 (#14 = bewusster externer Cross-Sell)**", "", "## Outputs", ""]
    for typ, (p, n) in written.items():
        L.append(f"- {p.name}: {n} Zeilen")
    (out / f"run_{stamp}_GODDESS.md").write_text("\n".join(L), encoding="utf-8")
    dl = config.copy_to_downloads(out)   # WaWi-Imports immer auch nach ~/Downloads

    print(f"Self-Check: {n_ok}/16 (#14 extern bewusst) | Lieferdatum {lieferdatum}")
    for typ, (p, n) in written.items():
        print(f"  {typ}: {n} -> {p.name}")
    print(f"Outputs: {out}")
    if dl:
        print(f"Downloads: {dl}")


if __name__ == "__main__":
    main()
