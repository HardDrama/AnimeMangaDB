# 🗺 AnimeMangaDB Roadmap

## ✅ Completed

### Core Scraper
✔ Playwright browser client
✔ Provider architecture
✔ HTML parsing
✔ Selector engine
✔ Episode extraction
✔ Chapter parsing

### Database
✔ SQLite integration
✔ SQLAlchemy models
✔ Repository layer
✔ Metadata storage

### Metadata
✔ Live metadata retrieval
✔ Metadata comparison
✔ Arc extraction
✔ Canonical title extraction

### Developer Tools
✔ HTML download tool
✔ Metadata comparison tools
✔ Selector discovery tool
✔ Series comparison tool

### Automated Metadata Repair
✔ Comparison service
✔ Repair planning
✔ Repair preview
✔ Safe apply mode
✔ Rollback support
✔ Database commits
✔ Targeted episode repair
✔ Repair verification workflow

---

# 🔄 Next Major Milestone (v0.48.0)

## Batch Metadata Repair

### Planned
⬜ Repair entire database automatically
⬜ Batch progress reporting
⬜ Success/failure statistics
⬜ Repair summaries
⬜ Improved logging
⬜ Recovery from interrupted runs

Example:

python -m tools.preview_metadata_repairs --apply --yes

or

python -m tools.preview_metadata_repairs --all --apply --yes

---

## Future Improvements

### Metadata
⬜ Air date extraction
⬜ Season/Voyage extraction
⬜ Episode thumbnail support
⬜ Japanese titles
⬜ Crunchyroll titles
⬜ Staff information

### Providers
⬜ Additional Fandom support
⬜ Multiple provider support
⬜ Provider fallback system

### Database
⬜ Metadata history
⬜ Audit log
⬜ Repair timestamps
⬜ Change history

### Developer Experience
⬜ Rich CLI output
⬜ JSON repair reports
⬜ CSV export
⬜ HTML reports

### Website/API
⬜ REST API
⬜ Episode lookup
⬜ Manga chapter lookup
⬜ Search functionality
⬜ Public website

---

# 🌟 Long-Term Vision

AnimeMangaDB is evolving from a web scraper into a complete metadata management platform capable of:

• Collecting metadata
• Validating metadata
• Detecting outdated information
• Repairing databases automatically
• Supporting multiple anime providers
• Powering a public lookup website and API