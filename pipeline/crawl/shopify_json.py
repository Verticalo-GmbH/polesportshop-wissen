"""
Shopify-JSON-Crawl (crawl_mechanik: shopify_json, E48).

Holt das öffentliche /products.json eines Shopify-Shops (ToS-konform,
dokumentierter Storefront-Endpoint). Paginiert über ?page=N&limit=250.
Anti-Bot-Check: HTTP-Status + Mindest-Body-Größe; bei Block -> klare Exception
(kein User-Agent-Spoofing über das realistische Browser-UA hinaus, Charter).
"""
from __future__ import annotations

import json
import time
import urllib.request
import urllib.error

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def _fetch_page(shop_url: str, page: int, limit: int = 250, timeout: int = 30) -> list[dict]:
    url = f"{shop_url.rstrip('/')}/products.json?limit={limit}&page={page}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": _UA,
            "Accept": "application/json",
            "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if r.status != 200:
                raise RuntimeError(f"Crawl-Block: HTTP {r.status} auf {url}")
            raw = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Crawl-Block: HTTP {e.code} auf {url}") from e
    # Anti-Bot-/Block-Erkennung über Struktur, nicht Länge: ein echter Block
    # liefert HTML/Challenge (kein gültiges JSON mit 'products'-Key). Eine leere
    # Liste ({"products":[]}) ist das legitime Paginierungs-Ende, kein Block.
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Crawl-Verdacht (kein JSON, evtl. Challenge-Seite) auf {url}"
        ) from e
    if "products" not in payload:
        raise RuntimeError(f"Crawl-Verdacht (kein 'products'-Key) auf {url}")
    return payload["products"]


def fetch_all_products(shop_url: str, *, max_pages: int = 20, pause_s: float = 0.3) -> list[dict]:
    """
    Alle Produkte eines Shopify-Shops (voller Datensatz, E80 für Cross-Selling).
    Gibt die rohen Shopify-Produkt-Dicts zurück; Parsing macht extract.py (P2).
    """
    products: list[dict] = []
    for page in range(1, max_pages + 1):
        batch = _fetch_page(shop_url, page)
        if not batch:
            break
        products.extend(batch)
        if pause_s:
            time.sleep(pause_s)
    return products


def reachability_check(shop_url: str) -> dict:
    """Schneller P1-Check: liefert {'ok', 'count'} ohne vollen Crawl-Overhead."""
    first = _fetch_page(shop_url, 1)
    return {"ok": bool(first), "count": len(first)}
