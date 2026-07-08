# AnimeMangaDB Tools

Developer utilities for inspecting, validating, repairing, and maintaining the AnimeMangaDB database.

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