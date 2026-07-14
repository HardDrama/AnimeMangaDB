# AnimeMangaDB Project

## Development Methodology

AnimeMangaDB is developed through Scopes, implemented through Versions, completed through Feature Checkpoints, and certified through matching Platform Checkpoints.

Before advancing to the next Scope, the current Scope must be fully integrated, validated, and benchmarked using One Piece.

---

## Scope

A Scope defines what AnimeMangaDB knows.

### Scope v1

Anime:
- Episode Number

Manga:
- Chapter Number

### Scope v2

Anime:
- Episode Number
- Episode Title
- Arc

Manga:
- Chapter Number

### Scope v3

Anime:
- Episode Number
- Episode Title
- Arc

Manga:
- Chapter Number
- Chapter Title
- Arc

---

## Feature Checkpoint

A feature is not complete until every layer supports it:

- Scraper
- Database
- Comparison
- Repair
- Reports
- API
- Frontend
- Documentation
- Tests

---

## Platform Checkpoint

A Platform Checkpoint certifies that the entire project supports a Scope end-to-end.

Examples:

- Platform Checkpoint v1 = Scope v1 complete end-to-end
- Platform Checkpoint v2 = Scope v2 complete end-to-end
- Platform Checkpoint v3 = Scope v3 complete end-to-end

---

## Benchmark Dataset

One Piece is the benchmark dataset.

Before a Platform Checkpoint is declared complete, One Piece must be fully updated, validated, and repairable for that Scope.

v0.57  ✅ One Piece Scope v3 Dataset
v0.58  ✅ Naruto Scope v3 Dataset
Next   Platform Checkpoint v3 planning

## Current

### Platform Checkpoint v3 Planning

Status:

Planned

Certified Scope v3 datasets:

- One Piece
- Naruto

Next phase:

- Define Platform Checkpoint v3
- Add chapter metadata API exposure
- Integrate chapter metadata into the frontend
- Validate multi-series Scope v3 behavior
- Certify the Scope v3 platform

### Naruto Scope v3 Dataset

Status:

Certified

Certified range:

- Chapters 1–700
- 700 chapter metadata records

Included:

- Part I
- Part II
- Original Naruto manga

Excluded:

- Naruto Gaiden
- Boruto
- Sasuke Retsuden
- Other spin-off manga

Certified metadata:

- Chapter number
- English chapter title
- Manga arc or verified non-applicable classification
- Canonical source URL
- Last-updated timestamp

Verified exception:

- Chapter 700
- Standalone epilogue
- Manga arc not applicable
- Stored value remains null

Evidence:

- Metadata audit: PASS
- Coverage audit: PASS
- Dataset audit: PASS
- Manual source validation: PASS
- Final validation: PASS
- Certification failures: 0