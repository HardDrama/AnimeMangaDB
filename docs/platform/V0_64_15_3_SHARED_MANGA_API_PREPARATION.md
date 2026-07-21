# v0.64.15.3 — Shared Manga API Preparation

## Purpose

Prepare an application service that preserves the existing anime-centric
REST API while resolving chapter metadata through shared manga ownership.

## Branch

```text
feature/multi-series-foundation-mitigation
```

## New Files

```text
scraper/services/shared_manga_api_service.py
tests/services/test_shared_manga_api_service.py
docs/platform/V0_64_15_3_SHARED_MANGA_API_PREPARATION.md
```

## Architecture

```text
FastAPI routes
      ↓
SharedMangaApiService
      ├── EpisodeRepository
      └── MangaRepository
```

The service owns response construction and coordinates data from both
repositories. FastAPI routes remain thin and retain their existing URLs.

## Preserved Routes

```text
/anime
/anime/{anime_id}
/anime/{anime_id}/arcs
/anime/{anime_id}/episodes
/anime/{anime_id}/chapters
/anime/{anime_id}/chapters/{chapter_number}
/anime/{anime_id}/chapters/{chapter_number}/episodes
/chapters/{chapter_number}/episodes
/search
```

## Shared Manga Behavior

Both Naruto anime records resolve chapter metadata through the same manga:

```text
Naruto ────────────┐
                    ├── Naruto manga chapters
Naruto Shippuden ──┘
```

Episode mappings remain anime-specific. A shared chapter can therefore be
visible from both anime chapter routes while only returning episodes owned
by the selected anime.

## Search Compatibility

A shared chapter metadata match is expanded into one anime-facing response
for every anime associated with the manga. This preserves the existing
`anime_id` and `anime_title` search response contract.

## Safety Policy

The production API files remain unchanged:

```text
scraper/api/routes/anime.py
scraper/api/routes/chapters.py
scraper/api/routes/search.py
scraper/api/schemas.py
```

The new service uses staged shared-manga repositories and models. Production
activation remains deferred until v0.64.15.4.

## Validation

Run focused service tests:

```powershell
python -m pytest tests/services/test_shared_manga_api_service.py
```

Expected:

```text
6 passed
```

Run all staged shared-manga tests:

```powershell
python -m pytest tests/database/test_shared_manga_models.py tests/repositories/test_shared_manga_repositories.py tests/services/test_shared_manga_api_service.py
```

Expected:

```text
18 passed
```

Run the complete backend suite:

```powershell
python -m pytest
```

Expected baseline:

```text
775 passed
6 skipped
```

Confirm production database initialization remains unchanged:

```powershell
python init_database.py
```

Expected:

```text
Database initialized successfully!
Database migrations applied: 0
Database migrations skipped: 0
```

Do not activate the migration or create the final feature commit yet.

## Next

v0.64.15.4 performs the atomic production switch:

1. Replace production ORM models.
2. Replace production repositories and ingestion service.
3. Replace API routes as thin service consumers.
4. Activate the v0.64.14 migration.
5. Remove staged implementation files.
6. Run complete backend and frontend certification.
7. Commit the complete feature.

## Final Commit

```text
v0.64.15 - Integrate shared manga runtime
```
