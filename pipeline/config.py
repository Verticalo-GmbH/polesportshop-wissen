"""
Konfiguration & Pfade. Lädt lieferanten_mapping.yaml aus dem Repo-Root.

Secrets (R2-Keys, Anthropic-Key) kommen AUSSCHLIESSLICH aus Umgebungsvariablen
oder einer lokalen, nicht-getrackten Credentials-Datei — niemals aus dem Repo,
Chat oder Log (E33). Die Accessoren hier werfen erst, wenn ein Secret real
gebraucht wird (P9 R2, P5 Anthropic), nicht beim Import.
"""
from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache

import yaml

# --- Pfade ---------------------------------------------------------------
PIPELINE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PIPELINE_DIR.parent
MAPPING_PATH = REPO_ROOT / "lieferanten_mapping.yaml"
SPEC_KONSTANTEN_PATH = REPO_ROOT / "SPEC_KONSTANTEN.md"

OUTPUTS_DIR = PIPELINE_DIR / "outputs"
EK_INPUT_DIR = PIPELINE_DIR / "EK_input"


def ensure_dirs() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    EK_INPUT_DIR.mkdir(parents=True, exist_ok=True)


# --- Lieferanten-Mapping -------------------------------------------------
@lru_cache(maxsize=1)
def load_mapping() -> dict:
    """Vollständiges lieferanten_mapping.yaml als dict."""
    with MAPPING_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_supplier(key: str) -> dict:
    """Mapping-Block eines Lieferanten, z.B. 'HOTCAKES_POLEWEAR'."""
    suppliers = load_mapping().get("lieferanten", {})
    if key not in suppliers:
        raise KeyError(
            f"Lieferant {key!r} nicht im Mapping. Verfügbar: {sorted(suppliers)}"
        )
    return suppliers[key]


# --- R2 (nicht-geheime Config aus Spec E43; Secrets aus env) -------------
# Endpoint/Bucket/Public-Base sind keine Geheimnisse — sie stehen so in der
# Spec (cowork_anweisung_bildpipeline.md / E43). Nur Key+Secret sind geheim.
R2_ENDPOINT = "https://d0393bbf896236cd9033d769383756f0.r2.cloudflarestorage.com"
R2_BUCKET = "polesportshop-images"
R2_PUBLIC_BASE = "https://pub-94a3cf669ee343b2857aa4d656f9b5d6.r2.dev"
R2_REGION = "auto"


def r2_credentials() -> dict:
    """
    R2 Access-Key + Secret aus env (R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY).
    Wird erst in P9 (Upload) aufgerufen. Wirft mit klarer Anleitung, wenn nicht
    gesetzt. Gibt die Werte NIE ins Log/Chat zurück gespiegelt.
    """
    akid = os.environ.get("R2_ACCESS_KEY_ID")
    secret = os.environ.get("R2_SECRET_ACCESS_KEY")
    if not akid or not secret:
        raise RuntimeError(
            "R2-Credentials fehlen. Setze sie lokal (nie im Chat/Repo):\n"
            "  export R2_ACCESS_KEY_ID=...\n"
            "  export R2_SECRET_ACCESS_KEY=...\n"
            "Quelle: Cloudflare R2 API-Token (S3-kompatibel)."
        )
    return {
        "aws_access_key_id": akid,
        "aws_secret_access_key": secret,
        "endpoint_url": R2_ENDPOINT,
        "region_name": R2_REGION,
    }


def anthropic_api_key() -> str:
    """Anthropic-Key aus env (ANTHROPIC_API_KEY). Erst in P5 relevant."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY fehlt. Nur nötig, wenn die Text-Generierung "
            "als Standalone-Code laufen soll (P5). Alternative: Hybrid-Modus."
        )
    return key
