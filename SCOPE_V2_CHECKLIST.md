# Scope v2 Validation Checklist

## Goal

Bring the entire AnimeMangaDB platform to Platform Checkpoint v2.

---

# Scraper

- [ :white_check_mark: ] Episode Number
- [ :white_check_mark: ] Episode Title
- [ :white_check_mark: ] Arc

---

# Database

- [ :white_check_mark: ] One Piece Episode Numbers validated
- [ ] One Piece Episode Titles validated
- [ ] One Piece Arcs validated
- [ :white_check_mark: ] Missing metadata identified

---

# Comparison

- [ ] Episode Number comparison
- [ ] Episode Title comparison
- [ ] Arc comparison

---

# Repair

- [ ] Episode Title repair
- [ ] Arc repair

---

# Reports

- [ ] JSON report supports Scope v2
- [ ] CSV report supports Scope v2

---

# API

- [ :white_check_mark: ] Scope v2 endpoints
- [ :white_check_mark: ] Scope v2 response model
- [ :white_check_mark: ] Episode number returned
- [ :white_check_mark: ] Episode title returned
- [ :white_check_mark: ] Anime arc returned
- [ :white_check_mark: ] Manga chapter number returned
- [ :white_check_mark: ] API tests

---

# Frontend

- [ :white_check_mark: ] Episode lookup
- [ ] Episode title
- [ ] Arc display

---

# Documentation

- [ ] PROJECT.md
- [ ] README.md
- [ ] Tool documentation

---

# Tests

- [ ] Scraper
- [ ] Database
- [ ] Comparison
- [ ] Repair
- [ ] Reports
- [ ] API
- [ ] Frontend

---

# Platform Checkpoint v2

Platform Checkpoint v2 is achieved only when every checklist item is complete and One Piece has been fully validated against Scope v2.

---

# Latest Audit Results

_Last Updated: 2026-07-10_

## One Piece

Episodes Checked:
- 1168

Title Completion:
- 99.83%

Arc Completion:
- 99.23%

Audit Status:
- NEARLY COMPLETE

Outstanding Work:

### Titles
- Empty titles: 0
- Placeholder titles: 2

### Arcs
- Missing arcs: 9

Notes:

- Episodes 1167 and 1168 currently have no arc because the Fandom pages have not yet been updated.

## Missing Arc Review

Current known source-data limitations:

- Episode 1167: Arc missing from live Fandom source.
- Episode 1168: Arc missing from live Fandom source.

These are not currently considered scraper or repair failures. They should be rechecked after the source pages are updated.

---

# Scope v2 Validation Workflow

Every validation cycle follows these steps:

1. Run the Scope v2 audit.
2. Review missing titles and arcs.
3. Apply metadata repairs.
4. Re-run the audit.
5. Update this checklist.
6. Repeat until Platform Checkpoint v2 is achieved.

Commands:

```bash
python -m tools.audit_scope_v2

python -m tools.repair_metadata --all --apply --yes

python -m tools.audit_scope_v2 --json-report scope_v2_audit.json
```