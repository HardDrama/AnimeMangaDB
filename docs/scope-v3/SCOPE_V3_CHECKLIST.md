# Scope v3 Foundation Checklist

## Scope v3 Metadata

### Anime

- [x] Episode Number
- [x] Episode Title
- [x] Anime Arc

### Manga

- [x] Chapter Number
- [x] Chapter Title
- [x] Manga Arc

---

## Data Foundation

- [x] Chapter metadata ORM model
- [x] Unique chapter identity by series and chapter number
- [x] Chapter metadata domain model
- [x] Chapter metadata repository methods
- [x] Idempotent create-or-update behavior
- [x] Existing Scope v2 tables preserved

---

## Provider Foundation

- [x] Chapter metadata provider interface
- [x] Fandom chapter metadata provider
- [x] Multi-series provider factory
- [x] Typed chapter metadata configuration
- [x] Series-specific discovery strategies
- [x] Series-specific extraction strategies

---

## URL Discovery

### One Piece

- [x] Numbered chapter URL generation
- [x] Canonical chapter page URLs

### Naruto

- [x] Volume-index discovery
- [x] Exact chapter-number matching
- [x] Tankōbon section scoping
- [x] Part I and Part II support
- [x] Spin-off manga exclusion
- [x] Index-page caching

---

## Metadata Extraction

### One Piece

- [x] Official Viz chapter title extraction
- [x] Manga arc extraction
- [x] Descriptive prose excluded as canonical title source

### Naruto

- [x] Chapter page-title extraction
- [x] Chapter-number suffix normalization
- [x] Manga arc factbox extraction
- [x] Missing values remain null

---

## Ingestion

- [x] Chapter metadata ingestion service
- [x] Thin command-line interface
- [x] Single-chapter ingestion
- [x] Controlled range ingestion
- [x] Per-chapter failure isolation
- [x] Existing records updated without duplication
- [x] Series data remains isolated

---

## Controlled Validation

### One Piece

- [x] Chapters 1–5 ingested
- [x] Chapter titles validated
- [x] Manga arcs validated
- [x] Source URLs validated

### Naruto

- [x] Chapters 1–5 ingested
- [x] Chapter titles validated
- [x] Manga arcs validated
- [x] Source URLs validated
- [x] Sasuke Retsuden contamination removed

### Integrity

- [x] Ten expected controlled records
- [x] Zero duplicate chapter records
- [x] Episode data unchanged
- [x] Episode-chapter mappings unchanged

---

## Automated Validation

- [x] Backend test suite passes with 140 tests
- [x] Frontend production build passes
- [x] Frontend lint passes with zero errors

---

## Scope Limitation

The Scope v3 foundation is certified.

Full One Piece and Naruto chapter-metadata population, repair, reporting, API exposure, frontend integration, and dataset certification remain future work.

---

## Status

✅ Scope v3 Foundation Certified

## Audit Foundation

- [x] Scope v3 chapter metadata audit tool
- [x] Controlled Chapters 1–5 baseline recorded
- [ ] Complete dataset audit passes