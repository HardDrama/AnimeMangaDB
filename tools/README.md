# AnimeMangaDB Tools

Developer utilities for inspecting, validating, repairing, and maintaining the AnimeMangaDB database.

---

# API Tools

The AnimeMangaDB API is served by FastAPI.

Run the API locally:

```bash
uvicorn scraper.api.app:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Current Scope v2 API endpoints:

- `GET /health`
- `GET /scope`
- `GET /version`
- `GET /series`
- `GET /episodes`
- `GET /episodes/count`
- `GET /episodes/id/{episode_id}`
- `GET /episodes/{episode_number}`

Scope v2 episode responses include:

- Anime title
- Episode number
- Episode title
- Anime arc
- Source URL

---

# Inspection Tools

These tools help inspect pages, selectors, and downloaded HTML during development.

## inspect_fandom_page.py

Inspect a Fandom page and print useful information including headings, infobox fields, tables, and links.

Example:

```bash
python -m tools.inspect_fandom_page
```

---

## find_selector_text.py

Locate text inside downloaded HTML and display the surrounding element hierarchy.

Useful for discovering CSS selectors.

Example:

```bash
python -m tools.find_selector_text episode_1130.html "Egghead Arc"
```

---

## download_episode_html.py

Download the rendered HTML for a specific episode.

Examples:

```bash
python -m tools.download_episode_html --episode 1

python -m tools.download_episode_html --episode 1130
```

---

# Database Inspection

These tools inspect the current database for missing or incorrect metadata.

## inspect_database_quality.py

Generate an overall database quality report.

---

## find_generic_titles.py

List episodes that still use placeholder titles.

Example output:

```
Episode 1
Episode 349
Episode 1130
```

---

## find_missing_arcs.py

List episodes missing arc information.

---

## find_missing_chapters.py

List episodes missing manga chapter mappings.

---

## Scope v2 Audit

### audit_scope_v2.py

Audits whether the database is ready for Scope v2.

Scope v2 includes:

- Anime Episode Number
- Anime Episode Title
- Anime Arc
- Manga Chapter Number

Example:

```bash
python -m tools.audit_scope_v2
```

Generate a JSON audit report:

```bash
python -m tools.audit_scope_v2 --json-report scope_v2_audit.json
```

Audit One Piece:

```bash
python -m tools.audit_scope_v2
```

Audit Naruto:

```bash
python -m tools.audit_scope_v2
    --anime "Naruto"
    --json-report naruto_scope_v2_audit.json
```

The audit reports:

- Episodes checked
- Missing titles
- Empty titles
- Placeholder titles
- Missing arcs
- Title completion percentage
- Arc completion percentage
- Audit status
- Missing episode lists

---

## Scope v3 Chapter Metadata Audit

Audit the stored chapter metadata for a series:

```bash
python -m tools.audit_scope_v3 --anime "One Piece"
```

Write a JSON report:

```bash
python -m tools.audit_scope_v3 \
    --anime "One Piece" \
    --json-report one_piece_scope_v3_audit.json
```

The audit evaluates:

- Chapter-title completion
- Manga-arc completion
- Source-URL completion
- Last-updated completion
- Duplicate chapter numbers

### Audit Status

`PASS` means every currently stored chapter record contains the required Scope v3 metadata and no duplicate chapter numbers were detected.

`IN PROGRESS` means one or more stored records contain unresolved metadata gaps, or the selected series has no chapter metadata records.

### Dataset Status

The metadata audit status does not, by itself, certify complete chapter coverage.

During the One Piece Scope v3 import phase, the report continues to show:

```text
Dataset Status: IN PROGRESS
```

until the complete intended chapter range has been imported, audited, validated, and certified.

### Full-Range Coverage Audit

Validate both metadata quality and expected chapter coverage:

```bash
python -m tools.audit_scope_v3 \
    --anime "One Piece" \
    --expected-start 1 \
    --expected-end 1188 \
    --json-report reports/one_piece_scope_v3_audit.json
```

The full-range audit evaluates:

- Required metadata on stored records
- Expected chapter count
- Missing chapter numbers
- Duplicate chapter numbers
- Coverage completion

A dataset receives `PASS` only when:

- Metadata audit status is `PASS`
- Coverage audit status is `PASS`

---

# Metadata Comparison

These tools compare stored database metadata against live Fandom metadata.

## compare_episode_metadata.py

Compare one episode.

Examples:

```bash
python -m tools.compare_episode_metadata

python -m tools.compare_episode_metadata --episode 1130
```

---

## compare_series_metadata.py

Compare multiple episodes.

Examples:

```bash
python -m tools.compare_series_metadata

python -m tools.compare_series_metadata --limit 25
```

---

# Metadata Repair

These tools preview and apply metadata repairs.

## repair_metadata.py

Repair metadata using live Fandom information.

### Preview

```bash
python -m tools.repair_metadata --episode 1130
```

### Apply

```bash
python -m tools.repair_metadata --episode 1130 --apply --yes
```

### Preview First Five Episodes

```bash
python -m tools.repair_metadata --limit 5
```

### Preview Entire Database

```bash
python -m tools.repair_metadata --all
```

> **Note**
>
> `--apply` requires `--yes` before any database updates are performed.

---

# Metadata Repair Workflow

Recommended workflow for repairing a specific episode.

### Step 1 — Compare

```bash
python -m tools.compare_episode_metadata --episode 1130
```

---

### Step 2 — Preview

```bash
python -m tools.repair_metadata --episode 1130
```

---

### Step 3 — Apply

```bash
python -m tools.repair_metadata --episode 1130 --apply --yes
```

---

### Step 4 — Verify

```bash
python -m tools.compare_episode_metadata --episode 1130
```

Expected result:

```
Differences
-----------
All 3 metadata fields match.
```

---

### JSON Report

```bash
python -m tools.repair_metadata --limit 5 --json-report repair_report.json
```

The JSON report includes:

- Run metadata
- Command arguments
- Episode totals
- Repair totals
- Failure details
- Per-episode repair results
- Status totals
- Field totals

---

# Safety Recommendations

- Always preview repairs before applying them.
- Use `--episode` whenever possible during development.
- Keep a backup of `animemanga.db` before large repair batches.
- Test with `--limit` before using `--all`.
- Verify repaired episodes using `compare_episode_metadata.py`.

---

# Current Tool Categories

| Category | Purpose |
|----------|---------|
| Inspection | Inspect downloaded HTML and discover selectors |
| Database Inspection | Find missing or placeholder metadata |
| Comparison | Compare stored metadata with live metadata |
| Repair | Preview and apply metadata repairs |

---

Last Updated: v0.48.0

### CSV Report

```bash
python -m tools.repair_metadata --limit 5 --csv-report repair_report.csv
```

The CSV report includes:

- Episode ID
- Episode number
- Status
- Proposed repair count
- Applied repair count
- Skipped repair count
- Repair fields
- Repair value details
- Summary rows
```

### Combined Reports

```bash
python -m tools.repair_metadata --limit 5 --json-report repair_report.json --csv-report repair_report.csv

Validate:

```bash
pytest

### Report Format Guidance

Use JSON reports for automation, auditing, and future API or dashboard integrations.

Use CSV reports for spreadsheet review, quick filtering, and manual data-quality inspection.

# Product Scope Notes

AnimeMangaDB is focused on anime episode to manga chapter mapping.

Pre-v1.0 priorities:

- Anime episode number
- Anime episode title
- Anime arc
- Manga chapter number
- Manga chapter title
- Manga arc
- One Piece support
- Naruto support
- Repair/report tooling
- API and basic lookup website

Additional anime metadata such as air dates, staff, thumbnails, and streaming metadata are considered post-v1.0 enhancements.

### Ingestion Preflight

Preview a chapter range without fetching chapter pages or writing to the database:

```bash
python -m tools.ingest_chapter_metadata \
    --anime "One Piece" \
    --start-chapter 1 \
    --end-chapter 100 \
    --dry-run
```

Dry-run mode reports:

- Chapters selected
- Existing records
- Records that would be inserted
- Records that would be updated
- Planned source URLs
- Unresolved chapter URLs

Dry-run mode does not:

- Fetch individual chapter pages
- Extract live chapter metadata
- Create or update database records

---

## Scope v3 Manual Validation Manifest

Export selected records for representative manual source review:

```bash
python -m tools.export_scope_v3_samples \
    --anime "One Piece" \
    --chapters "1,50,100,500,1000,1188" \
    --json-report reports/one_piece_scope_v3_manual_validation.json
```

The manifest includes:

- Stored chapter number
- Stored chapter title
- Stored manga arc
- Source URL
- Last-updated timestamp
- Manual validation fields

The exporter does not fetch remote pages or modify database records.

---

## Scope v3 Dataset Certification Audit

Evaluate whether a Scope v3 dataset has sufficient evidence for certification:

```bash
python -m tools.certify_scope_v3_dataset \
    --anime "One Piece" \
    --expected-start 1 \
    --expected-end 1188 \
    --audit-report reports/one_piece_scope_v3_audit.json \
    --manual-report reports/one_piece_scope_v3_manual_validation.json \
    --json-report reports/one_piece_scope_v3_certification.json
```

Certification eligibility requires:

- Metadata audit status: `PASS`
- Coverage audit status: `PASS`
- Dataset audit status: `PASS`
- Manual validation status: `PASS`
- Every sampled title validated
- Every sampled manga arc validated
- Every sampled source URL validated
- Zero unresolved certification failures

`ELIGIBLE` means the evidence supports certification. It does not itself modify project documentation or certify the dataset.

---

## One Piece Scope v3 Evidence

Dataset documentation:

```text
docs/scope-v3/ONE_PIECE_SCOPE_V3_DATASET.md
```

Validation log:

```text
docs/scope-v3/ONE_PIECE_SCOPE_V3_VALIDATION_LOG.md
```

Manual review:

```text
docs/scope-v3/ONE_PIECE_SCOPE_V3_MANUAL_REVIEW.md
```

Machine-readable reports:

```text
reports/
```

Current certification target:

```text
One Piece Chapters 1–1188
```

---

## Chapter Index Inspection

Inspect the configured main-series section of a volume index:

```bash
python -m tools.inspect_chapter_index \
    --config configs/fandom/naruto.json \
    --html-file tests/fixtures/naruto_list_of_volumes.html \
    --json-report reports/naruto_scope_v3_source_inspection.json
```

Inspect the live source:

```bash
python -m tools.inspect_chapter_index \
    --config configs/fandom/naruto.json \
    --json-report reports/naruto_scope_v3_live_source_inspection.json
```

The inspection reports:

- Entry count
- Unique chapter count
- Minimum and maximum chapter
- Missing chapter numbers
- Duplicate chapter numbers

The tool inspects source structure only. It does not fetch individual chapter pages or modify the database.

### Index-Based Dry Runs

Some series require an index page to discover canonical chapter URLs.

For Naruto:

```bash
python -m tools.ingest_chapter_metadata \
    --anime "Naruto" \
    --start-chapter 1 \
    --end-chapter 700 \
    --dry-run \
    --json-report reports/naruto_scope_v3_preflight.json
```

During an index-based dry run:

- The shared chapter index may be fetched.
- Index HTML is cached for the execution.
- Individual chapter pages are not fetched.
- Providers and extractors are not executed.
- Database records are not created or updated.

### Naruto Scope v3 Manual Validation

Export the representative Naruto review sample:

```bash
python -m tools.export_scope_v3_samples \
    --anime "Naruto" \
    --chapters "1,2,5,10,25,50,75,100,125,150,175,200,225,244,245,275,300,325,350,375,400,425,450,500,550,600,650,675,699,700" \
    --json-report reports/naruto_scope_v3_manual_validation.json
```