"""
Interne Datenmodelle der Pipeline (Lieferanten-unabhängig).

Begriffe (JTL-Welt):
- Vater  = ein konkretes Produkt-Modell in EINER Farbe (z.B. "Arachne Top - tan").
           Bei Shopify entspricht das einem `product`. Farbe ist Teil der Identität.
- Kind   = eine Größen-Variante des Vaters (z.B. "XS"). Bei Shopify ein `variant`.
- Familie = alle Väter mit gleichem Modell-Stamm (z.B. "Arachne Top" in allen Farben)
            bzw. Outfit-Paare (Top+Bottom gleicher Farbe) — relevant für Cross-Selling (E80/E84).

Befüllung: crawl/extract (P2) füllt alles außer ek/vk; pricing (P3) ergänzt diese.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Kind:
    """Größen-Variante (JTL-Kind)."""
    groesse: str                 # normalisiert nach groessen_konvention, z.B. "XS"
    groesse_raw: str             # wie vom Lieferanten, z.B. "XS/S"
    position: int                # Reihenfolge im Quell-Datensatz
    artikelnummer: Optional[str] = None   # Vater-ArtNr + Suffix (-001 ...), in P4 vergeben
    ean: Optional[str] = None             # GTIN/UTC-Barcode pro Größe (E95), aus Lieferanten-Referenz
    sku: Optional[str] = None
    grams: Optional[int] = None
    price_retail: Optional[float] = None  # Shop-VK des Lieferanten (NICHT unser EK)
    available: bool = True


@dataclass
class Vater:
    """Produkt-Modell in einer Farbe (JTL-Vater)."""
    # Identität / Herkunft
    handle: str
    product_id: int
    title_raw: str               # voller Lieferanten-Titel, z.B. "Arachne Top - tan"
    vendor: str
    product_type: Optional[str] = None
    tags: list[str] = field(default_factory=list)

    # Abgeleitete Identität (P2)
    modell_basis: str = ""       # Modell OHNE Typ und OHNE Farbe, z.B. "Arachne"
    garment_type: str = ""       # normalisiert: Top|Bottom|Bodysuit|Leggings|Shorts
    farbe_raw: str = ""          # z.B. "tan" (Roh aus Titel); "" = keine Farb-Variante im Titel
    farbe_de: str = ""           # lokalisiert für DE-Artikelname (E92), in P4 gefüllt

    # Inhalt
    body_html: str = ""          # Quelle für Modelname/Material/Features (E77-Originalität)
    image_urls: list[str] = field(default_factory=list)

    # Varianten
    kinder: list[Kind] = field(default_factory=list)

    # Identifikatoren (P4 vergeben)
    artikelnummer: Optional[str] = None

    # Preise (P3)
    ek_netto: Optional[float] = None        # EUR (nach fx) — für GLD / VK-Kalkulation
    ek_original: Optional[float] = None      # EK in Lieferanten-Währung (z.B. AUD) — Lieferanten-Netto-EK
    vk_brutto: Optional[float] = None

    # Bild-URLs nach R2 (P9)
    r2_bild_urls: list[str] = field(default_factory=list)
