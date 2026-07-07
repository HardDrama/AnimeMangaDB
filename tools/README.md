# AnimeMangaDB Tools

Developer utilities for inspecting, validating, and debugging AnimeMangaDB data.

## Inspection Tools

### inspect_fandom_page.py
Inspects a Fandom page and prints page structure details such as headings, infobox fields, tables, and links.

### inspect_database_quality.py
Generates an overall database quality report.

### find_generic_titles.py
Lists episodes using placeholder titles such as `Episode 1130`.

### find_missing_arcs.py
Lists episodes missing arc metadata.

### find_missing_chapters.py
Lists episodes missing manga chapter mappings.

## Metadata Repair Workflow

Use this workflow when repairing metadata for a specific episode.

### 1. Preview the repair

```bash
python -m tools.preview_metadata_repairs --episode 3