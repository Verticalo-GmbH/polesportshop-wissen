"""
Orchestrator (P10, generalisiert): Lauf für einen Lieferanten -> 5 CSVs
(+ optional 6. Lieferantenbestellung) + Bericht.

Stages: Väter-Quelle (Shopify-Crawl ODER Browser-Scrape-Builder) -> Pricing
(EK aus Rechnung, ggf. fx USD->EUR) -> A-Nummern -> EAN -> Content -> Bilder/R2
-> 5 CSVs -> Self-Check -> Lieferantenbestellung (E99, wenn menge_<x>.csv vorliegt)
-> Bericht.

Aufruf: python -m pipeline.orchestrator [--supplier hotcakes|rolling] [--images] [--referenz "..."]
"""
from __future__ import annotations

from datetime import datetime, timedelta

from . import config, constants, extract, pricing, spec, numbering, content as C, selfcheck
from .crawl import shopify_json
from .csv import stammdaten, variationen, merkmale, attribute, crossselling, bestellung
from .csv._writer import write_csv

# Lieferanten-Registry: builder=None -> Shopify-Crawl; sonst Modul mit build_vaeter()
SUPPLIERS = {
    "hotcakes": {"key": "HOTCAKES_POLEWEAR", "ek": "ek_hotcakes_00034.csv",
                 "content": "hotcakes_content.json", "builder": None,
                 "scope": "Rechnung #00034"},
    "rolling":  {"key": "ROLLING_CLOTHING", "ek": "ek_rolling_april26.csv",
                 "content": "rolling_content.json", "builder": "rolling",
                 "menge": "menge_rolling.csv",
                 "scope": "Rechnung APRIL26 (4 Ceci)"},
    "lunalae":  {"key": "LUNALAE", "ek": "ek_lunalae_3124.csv",
                 "content": "lunalae_content.json", "builder": "lunalae",
                 "ean": "ean_lunalae.csv", "menge": "menge_lunalae.csv",
                 "scope": "Rechnung #3124 (Diamante May Release)"},
    "lunalae-odessa": {"key": "LUNALAE", "ek": "ek_lunalae_odessa.csv",
                 "content": "lunalae_odessa_content.json", "builder": "lunalae_odessa",
                 "ean": "ean_lunalae.csv", "menge": "menge_lunalae.csv",
                 "scope": "Rechnung #D413 (Odessa)"},
}


def run(supplier: str = "hotcakes", stamp: str | None = None,
        with_images: bool = False, start_artnr: int | None = None,
        persist_counter: bool = False, bestell_referenz: str = "") -> dict:
    cfg = SUPPLIERS[supplier]
    stamp = stamp or datetime.now().strftime("%Y-%m-%d_%H%M")
    run_date = datetime.now().strftime("%d.%m.%Y")
    sup = config.get_supplier(cfg["key"])
    spec.set_artnr_prefix(sup.get("artnr_prefix", "HC"))
    fx = float(sup.get("fx_to_eur", 1.0) or 1.0)

    # Väter-Quelle
    if cfg["builder"] is None:                       # Shopify-Crawl (HotCakes etc.)
        ds = extract.build_dataset(shopify_json.fetch_all_products(sup["shop_url"]))
        keep, review, exclude = ds["keep"], ds["review"], ds["exclude"]
    else:                                            # Browser-Scrape-Builder (Rolling)
        from importlib import import_module
        keep = import_module(f".suppliers.{cfg['builder']}", __package__).build_vaeter()
        review, exclude = [], []

    # Pricing (EK aus Rechnung; fx falls Nicht-EUR). Interim-Margen-Schutz (E98)
    # nach Herkunft: Nicht-EU -> +5 EUR auf VK; EU/EUR -> +1 EUR auf EK (via ×2 in VK).
    is_eur = (sup.get("waehrung", "EUR") == "EUR")
    ek_auf = constants.EK_AUFSCHLAG_EU_EUR if is_eur else 0.0
    vk_auf = 0.0 if is_eur else constants.VK_AUFSCHLAG_AUSLAND_EUR
    ek_map = pricing.load_ek_csv(config.EK_INPUT_DIR / cfg["ek"])
    priced, missing = pricing.apply_pricing(keep, ek_map, fx, ek_aufschlag=ek_auf, vk_aufschlag=vk_auf)

    # Weg B (E94): A-Nummern aus dem WaWi-Nummernkreis vorab vergeben.
    artnr_next = numbering.assign(priced, start=start_artnr, persist=persist_counter)

    # E95: EAN/GTIN-Barcodes pro Größe anreichern (falls Lieferant Referenz hat).
    if cfg.get("ean"):
        from . import barcodes
        _, ean_fehlt = barcodes.attach(priced, config.PIPELINE_DIR / "content" / cfg["ean"])
        if ean_fehlt:
            print(f"[{supplier}] WARN EAN fehlt für {len(ean_fehlt)} Kinder: {ean_fehlt[:5]}")

    if with_images:
        _run_images(priced, sup)

    # Content laden + validieren
    content = C.load_content(config.PIPELINE_DIR / "content" / cfg["content"])
    vnrs = [spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw) for v in priced]
    content_missing = C.validate(content, vnrs)
    if content_missing:
        raise RuntimeError(f"Content unvollständig (STOPP): {content_missing[:5]}")

    # 5 CSV-Row-Sets
    sd = stammdaten.build_rows(priced, sup, run_date)
    va = variationen.build_rows(priced, sup, run_date)
    mk = merkmale.build_rows(priced, sup, content)
    at = attribute.build_rows(priced, sup, content)
    cs = crossselling.build_rows(priced)

    checks = selfcheck.run(sd, va, mk, at, cs, priced, ek_aufschlag=ek_auf, vk_aufschlag=vk_auf)

    # Schreiben (AP12: leere CSVs nicht ausgeben)
    kz = sup["kuerzel"]
    out = config.OUTPUTS_DIR / f"{kz}_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    written = {}
    for nr, typ, cols, rows, qa in [
        (1, "Stammdaten", stammdaten.COLUMNS, sd, False),
        (2, "Variationen", variationen.COLUMNS, va, False),
        (3, "Merkmale", merkmale.COLUMNS, mk, False),
        (4, "Attribute", attribute.COLUMNS, at, True),
        (5, "CrossSelling", crossselling.COLUMNS, cs, False),
    ]:
        if not rows:
            continue
        p = out / f"{nr}_{typ}_{kz}_{stamp}.csv"
        write_csv(p, cols, rows, quote_all=qa)
        written[typ] = (p, len(rows))

    # E99: Lieferantenbestellung als 6. Output, wenn Bestell-Mengen vorliegen.
    menge_file = cfg.get("menge")
    if menge_file and (config.EK_INPUT_DIR / menge_file).exists():
        lz = int(sup.get("lieferzeit_tage", 0) or 0)
        lieferdatum = (datetime.now() + timedelta(days=lz)).strftime("%d.%m.%Y")
        be = bestellung.build_rows(
            bestellung.load_menge(config.EK_INPUT_DIR / menge_file),
            bestellung.artnr_map(priced), lieferdatum,
            referenz=bestell_referenz, lieferant=sup["anzeigename"])
        if be:
            p = out / f"6_Lieferantenbestellung_{kz}_{stamp}.csv"
            write_csv(p, bestellung.COLUMNS, be, quote_all=False)
            written["Lieferantenbestellung"] = (p, len(be))

    artnr_range = (priced[0].artikelnummer, priced[-1].artikelnummer, artnr_next) if priced else None
    report = _report(sup, cfg, priced, missing, review, exclude, checks, written, stamp,
                     with_images, artnr_range)
    (out / f"run_{stamp}_{kz}.md").write_text(report, encoding="utf-8")
    config.copy_to_downloads(out)   # WaWi-Imports immer auch nach ~/Downloads

    return {"out": out, "priced": priced, "missing": missing, "checks": checks,
            "written": written, "review": review, "exclude": exclude}


def _run_images(priced, sup) -> None:
    """Stage 5.6/5.7: pro Vater Bilder verarbeiten + R2-Upload, URLs setzen."""
    from .images import process, r2
    client = r2.make_client()
    prefix = sup["r2_prefix"]
    profile = sup["crop_profile"]
    for v in priced:
        artnr = spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw)
        imgs = process.process_vater(v.image_urls[:10], profile)
        v.r2_bild_urls = r2.upload_vater(client, prefix, artnr, imgs)
    name_map = {spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw):
                spec.vater_artikelname(sup["marke_kurz"], v.garment_type,
                                       v.modell_basis, v.farbe_raw, "de")
                for v in priced}
    r2.build_originals_index(client, prefix, name_map,
                             titel=f"{sup['anzeigename']} Originalbilder")
    r2.build_master_index(client)


def _report(sup, cfg, priced, missing, review, exclude, checks, written, stamp,
            with_images, artnr_range=None) -> str:
    n_ok = sum(1 for c in checks if c[2])
    kz = sup["kuerzel"]
    L = [f"# Lauf-Bericht {sup['anzeigename']} {stamp}", "",
         f"**Lieferant:** {sup['anzeigename']} ({kz}) | **Pipeline:** lokal (Claude Code)",
         f"**Scope:** {len(priced)} Väter ({cfg['scope']}), {sum(len(v.kinder) for v in priced)} Kinder",
         f"**Währung:** EK {sup.get('waehrung','EUR')}, fx_to_eur {sup.get('fx_to_eur', 1.0)}", ""]
    if artnr_range:
        L += [f"**Nummernkreis (Weg B, E94):** Väter {artnr_range[0]}–{artnr_range[1]} "
              f"(+ Kinder -001…). WaWi-Zähler 'Laufende Nummer' nach Import auf "
              f"**{artnr_range[2]}** setzen.", ""]
    L += ["## Self-Check (16 Punkte)", ""]
    for n, name, passed, detail in checks:
        L.append(f"[#{n}] {'✓' if passed else '✗'} {name}{(' — ' + detail) if detail else ''}")
    L += ["", f"**Self-Check: {n_ok}/16 {'GRÜN' if n_ok == 16 else 'ROT'}**", "", "## Outputs", ""]
    for typ, (p, n) in written.items():
        L.append(f"- {p.name}: {n} Zeilen")
    L += ["", "## Out of Scope", "",
          f"- {len(missing)} Väter ohne EK", f"- {len(review)} Review-Items",
          f"- {len(exclude)} ausgeschlossen", "", "## Bilder", "",
          ("- Bilder verarbeitet + R2-Upload + URLs in Stammdaten" if with_images
           else "- Bild-Spalten leer (Lauf ohne --images)")]
    return "\n".join(L)


if __name__ == "__main__":
    import sys
    supplier = "hotcakes"
    if "--supplier" in sys.argv:
        supplier = sys.argv[sys.argv.index("--supplier") + 1]
    with_images = "--images" in sys.argv
    referenz = sys.argv[sys.argv.index("--referenz") + 1] if "--referenz" in sys.argv else ""
    r = run(supplier=supplier, with_images=with_images, bestell_referenz=referenz)
    n_ok = sum(1 for c in r["checks"] if c[2])
    print(f"[{supplier}] Self-Check: {n_ok}/16")
    for typ, (p, n) in r["written"].items():
        print(f"  {typ}: {n} Zeilen -> {p.name}")
    print(f"Outputs: {r['out']}")
