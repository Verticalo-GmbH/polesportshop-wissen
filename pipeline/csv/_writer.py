"""
Gemeinsame CSV-Schreib-Mechanik (run_brief Format-Regeln, alle 5 CSVs):
UTF-8 mit BOM, Semikolon, CRLF, Komma-Dezimal. Attribute-CSV zusätzlich QUOTE_ALL.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path

from .. import constants as C


def fmt_decimal(value) -> str:
    """Float -> DE-Dezimal mit Komma, 2 Nachkommastellen. 41.9 -> '41,90'."""
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    return f"{value:.2f}".replace(".", ",")


def write_csv(path: Path, columns: list[str], rows: list[dict], *, quote_all: bool = False) -> int:
    """Schreibt rows (list[dict]) gegen columns. Gibt Zeilenzahl (ohne Header) zurück."""
    path.parent.mkdir(parents=True, exist_ok=True)
    quoting = csv.QUOTE_ALL if quote_all else csv.QUOTE_MINIMAL
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=C.CSV_DELIMITER, quoting=quoting,
                   lineterminator=C.CSV_LINETERMINATOR)
    w.writerow(columns)
    for r in rows:
        w.writerow([r.get(col, "") for col in columns])
    with path.open("w", encoding=C.CSV_ENCODING, newline="") as f:
        f.write(buf.getvalue())
    return len(rows)
