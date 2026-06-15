"""
Orchestrator (P10): voller HotCakes-Lauf -> 5 CSVs + Lauf-Bericht.

Stages: Crawl -> Extraktion -> Scope-Filter -> Pricing (EK aus Rechnung) ->
Content (Hybrid) -> 5 CSVs -> Self-Check -> Bericht. Bild-Spalten leer bis P9.

Aufruf: python -m pipeline.orchestrator
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from . import config, extract, pricing, spec, content as C, selfcheck
from .crawl import shopify_json
from .csv import stammdaten, variationen, merkmale, attribute, crossselling
from .csv._writer import write_csv

SUPPLIER_KEY = "HOTCAKES_POLEWEAR"
EK_FILE = "ek_hotcakes_00034.csv"
CONTENT_FILE = "hotcakes_content.json"


def run(stamp: str | None = None) -> dict:
    stamp = stamp or datetime.now().strftime("%Y-%m-%d_%H%M")
    run_date = datetime.now().strftime("%d.%m.%Y")
    hc = config.get_supplier(SUPPLIER_KEY)

    # Stage 1-3: Crawl + Extraktion + Scope
    prods = shopify_json.fetch_all_products(hc["shop_url"])
    ds = extract.build_dataset(prods)

    # Stage 4: Pricing (EK aus Rechnung; ohne EK = out of scope)
    ek_map = pricing.load_ek_csv(config.EK_INPUT_DIR / EK_FILE)
    priced, missing = pricing.apply_pricing(ds["keep"], ek_map)

    # Stage 5: Content laden + validieren
    content = C.load_content(config.PIPELINE_DIR / "content" / CONTENT_FILE)
    vnrs = [spec.vater_artnr(v.garment_type, v.modell_basis, v.farbe_raw) for v in priced]
    content_missing = C.validate(content, vnrs)
    if content_missing:
        raise RuntimeError(f"Content unvollständig (STOPP): {content_missing[:5]}")

    # Stage 6: 5 CSV-Row-Sets
    sd = stammdaten.build_rows(priced, hc, run_date)
    va = variationen.build_rows(priced, hc, run_date)
    mk = merkmale.build_rows(priced, hc, content)
    at = attribute.build_rows(priced, hc, content)
    cs = crossselling.build_rows(priced)

    # Stage 7: Self-Check
    checks = selfcheck.run(sd, va, mk, at, cs, priced)

    # Schreiben (AP12: leere CSVs nicht ausgeben)
    out = config.OUTPUTS_DIR / f"HOTCAKES_{stamp}"
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
        p = out / f"{nr}_{typ}_HOTCAKES_{stamp}.csv"
        write_csv(p, cols, rows, quote_all=qa)
        written[typ] = (p, len(rows))

    report = _report(hc, priced, missing, ds, checks, written, stamp)
    (out / f"run_{stamp}_HOTCAKES.md").write_text(report, encoding="utf-8")

    return {"out": out, "priced": priced, "missing": missing, "checks": checks,
            "written": written, "review": ds["review"], "exclude": ds["exclude"]}


def _report(hc, priced, missing, ds, checks, written, stamp) -> str:
    n_ok = sum(1 for c in checks if c[2])
    L = [f"# Lauf-Bericht HotCakes {stamp}", "",
         f"**Lieferant:** {hc['anzeigename']} | **Snapshot:** v1.21 (lokal, Claude Code)",
         f"**Scope:** {len(priced)} Väter (Rechnung #00034), {sum(len(v.kinder) for v in priced)} Kinder", "",
         "## Self-Check (16 Punkte)", ""]
    for n, name, passed, detail in checks:
        L.append(f"[#{n}] {'✓' if passed else '✗'} {name}{(' — ' + detail) if detail else ''}")
    L += ["", f"**Self-Check: {n_ok}/16 {'GRÜN' if n_ok == 16 else 'ROT'}**", "",
          "## Outputs", ""]
    for typ, (p, n) in written.items():
        L.append(f"- {p.name}: {n} Zeilen")
    L += ["", "## Out of Scope", "",
          f"- {len(missing)} Väter ohne EK (nicht in Rechnung #00034)",
          f"- {len(ds['review'])} Review-Items raus (strikt Pole)",
          f"- {len(ds['exclude'])} ausgeschlossen (Swim/Outerwear/Accessoire)",
          "", "## Offen", "", "- Bild-Spalten leer (P8/P9 Bildpipeline + R2 ausstehend)"]
    return "\n".join(L)


if __name__ == "__main__":
    r = run()
    n_ok = sum(1 for c in r["checks"] if c[2])
    print(f"Self-Check: {n_ok}/16")
    for typ, (p, n) in r["written"].items():
        print(f"  {typ}: {n} Zeilen -> {p.name}")
    print(f"Outputs: {r['out']}")
