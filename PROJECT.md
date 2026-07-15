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

---

## Current

### v0.60 — Scope v3 Frontend Integration

Status:

Series Chapter List Complete

Completed:

- Scope v3 frontend contract
- Frontend chapter API client
- Series chapter metadata list
- Local chapter filtering
- Chapter loading, error, and empty states
- Nullable manga-arc presentation

Validated datasets:

- One Piece Chapters 1–1188
- Naruto Chapters 1–700

Current phase:

Chapter detail experience

Next:

- Add chapter detail route
- Add chapter detail page
- Add breadcrumbs and back navigation
- Display source URL and last-updated timestamp

---

## ROADMAP

v0.57  ✅ One Piece Scope v3 Dataset
v0.58  ✅ Naruto Scope v3 Dataset
v0.59  ✅ Scope v3 API Integration
v0.60  🚧 Scope v3 Frontend Integration
Future Platform Checkpoint v3 Certification

---

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

### Scope v3 API Integration

Status:

Certified

API version:

0.59.0

Certified endpoints:

- `GET /anime/{anime_id}/chapters`
- `GET /anime/{anime_id}/chapters/{chapter_number}`
- Scope v3 chapter metadata search

Certified datasets:

- One Piece Chapters 1–1188
- Naruto Chapters 1–700

Compatibility:

- Scope v2 API behavior preserved

Evidence:

- Response-model validation: PASS
- One Piece API validation: PASS
- Naruto API validation: PASS
- Final API validation: PASS
- OpenAPI validation: PASS
- API metadata alignment: PASS