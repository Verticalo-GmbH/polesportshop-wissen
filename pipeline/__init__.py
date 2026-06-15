"""
polesportshop Artikel-Pipeline (lokale Standalone-Portierung von Cowork).

Erzeugt aus Lieferanten-Daten die 5 JTL-Ameise-CSVs + Bildpipeline (R2).
Spec-Quelle: run_brief_daten.md, SPEC_KONSTANTEN.md, lieferanten_mapping.yaml
(im Repo-Root, Snapshot-Stand v1.21).

Architektur-Pivot: bisher lief die Ausführung in Cowork (Browser-Engine).
Diese Codebasis verlagert sie nach Claude Code lokal. Cowork bleibt Fallback.
Siehe Plan + (künftig) Entscheidungs-Log E-Nummer (P11).
"""

__version__ = "0.1.0-P1"
