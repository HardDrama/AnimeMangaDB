# v0.64.15.2 — Shared Manga Repository Preparation

## Purpose

Prepare the repository and chapter metadata ingestion runtime for shared
manga ownership without replacing the current production repositories.

## Branch

```text
feature/multi-series-foundation-mitigation
```

## New Staged Files

```text
scraper/repositories/episode_repository_shared_manga.py
scraper/repositories/manga_repository_shared_manga.py
scraper/services/chapter_metadata_ingestion_service_shared_manga.py
tests/repositories/test_shared_manga_repositories.py
```

## Runtime Separation

### EpisodeRepository

Owns:

- Anime records
- Episode records
- Episode-to-chapter mappings
- Episode search
- Anime search
- Episode arc summaries

### MangaRepository

Owns:

- Manga records
- Canonical manga title mapping
- Anime-to-manga resolution
- Chapter metadata persistence
- Shared chapter listing and counts
- Manga arc summaries
- Chapter metadata search

## Canonical Mapping

```text
Naruto          ─┐
                 ├── Naruto manga
Naruto Shippuden ┘

One Piece ───────── One Piece manga
```

## Safety Policy

The production files remain unchanged during this preparation batch:

```text
scraper/repositories/episode_repository.py
scraper/services/chapter_metadata_ingestion_service.py
scraper/database/models.py
scraper/database/migrations/registry.py
```

The staged repositories import:

```text
scraper/database/models_shared_manga.py
```

This keeps the existing runtime compatible until the atomic activation in
v0.64.15.4.

## Validation

Run focused repository tests:

```powershell
python -m pytest tests/repositories/test_shared_manga_repositories.py
```

Expected:

```text
6 passed
```

Run all shared-manga preparation tests:

```powershell
python -m pytest   tests/database/test_shared_manga_models.py   tests/repositories/test_shared_manga_repositories.py
```

Expected:

```text
12 passed
```

Run the complete backend suite:

```powershell
python -m pytest
```

Expected baseline:

```text
769 passed
6 skipped
```

Run database initialization:

```powershell
python init_database.py
```

Expected:

```text
Database initialized successfully!
Database migrations applied: 0
Database migrations skipped: 0
```

Do not activate the migration and do not commit the final feature yet.

## Next

v0.64.15.3 prepares the API routes and response schemas against the staged
shared-manga runtime.

## Final Commit

The feature remains uncommitted until v0.64.15.4:

```text
v0.64.15 - Integrate shared manga runtime
```
