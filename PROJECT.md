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

## Roadmap

v0.57  ✅ One Piece Scope v3 Dataset
v0.58  🚧 Naruto Scope v3 Dataset
Future  Platform Checkpoint v3

## Current

### v0.58 — Naruto Scope v3 Dataset

Status:

Verified Exception Identified

Dataset:

- Chapters 1–700
- 700 records present
- Coverage audit: PASS
- Missing titles: 0
- Raw missing manga arcs: 1
- Verified non-applicable manga arcs: 1
- Unresolved manga-arc gaps: 0
- Missing source URLs: 0
- Duplicate records: 0

Verified exception:

- Naruto Chapter 700
- Standalone epilogue
- Manga arc not applicable
- Database value remains null

Current phase:

Add Scope v3 chapter-metadata exception support

Next:

- Add exception configuration
- Make the audit exception-aware
- Re-run full metadata and coverage audits