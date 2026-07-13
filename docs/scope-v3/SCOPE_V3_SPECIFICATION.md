# Scope v3 Specification

## Goal

Expand AnimeMangaDB with manga chapter metadata while preserving all certified Scope v2 capabilities.

Scope v3 adds:

- Manga Chapter Title
- Manga Arc

---

## Existing Scope v2

### Anime

- Episode Number
- Episode Title
- Anime Arc

### Manga

- Chapter Number

---

## Scope v3

### Anime

- Episode Number
- Episode Title
- Anime Arc

### Manga

- Chapter Number
- Chapter Title
- Manga Arc

---

## Data Model

Scope v3 should represent chapter metadata independently from episode mappings.

```text
Anime
  ↓
Episode
  ↓
EpisodeChapter
  ↓
ChapterMetadata

---

## Scope v3 Foundation Progress

- [x] Scope v3 specification
- [x] Chapter metadata database model
- [x] Chapter metadata repository
- [x] Chapter metadata domain model
- [x] Chapter metadata provider framework
- [x] Chapter URL discovery
- [x] Chapter metadata extractor
- [x] Chapter metadata ingestion
- [x] Controlled batch chapter ingestion
- [ ] Scraper support
- [ ] Comparison support
- [ ] Repair support
- [ ] Reporting support
- [ ] API support
- [ ] Frontend support

## Controlled Batch Validation

Controlled ingestion was validated across:

- One Piece Chapters 1–5
- Naruto Chapters 1–5

Validation uncovered and resolved:

- Partial chapter-number matching
- Cross-work Naruto chapter ambiguity
- Naruto Tankōbon section scoping
- Noncanonical One Piece title extraction

The final workflow stores official One Piece Viz titles and main-series Naruto chapter metadata without duplicates.

---

## Scope v3 Foundation Certification

The foundational chapter metadata pipeline has been completed and validated across One Piece and Naruto.

Certified foundation:

- Database model
- Domain model
- Repository
- Provider framework
- URL discovery
- Metadata extraction
- Single ingestion
- Controlled batch ingestion

The foundation does not certify complete Scope v3 datasets.

Status:

✅ Certified

## One Piece Scope v3 Benchmark

Target dataset:

- Complete chapter coverage
- Official Viz English titles
- Manga arcs
- Canonical source URLs

Validation will require:

- Automated audit
- Manual verification
- Regression testing

Status:

In Progress