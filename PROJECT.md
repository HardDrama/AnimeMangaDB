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

Canonical Source Verified

Verified target:

- Chapters 1–700
- Expected records: 700

Included:

- Part I
- Part II

Excluded:

- Naruto Gaiden
- Boruto
- Spin-off manga

Current phase:

Full-range ingestion preflight

Next:

- Validate existing controlled records
- Run Chapters 1–700 dry-run
- Import full Naruto chapter metadata