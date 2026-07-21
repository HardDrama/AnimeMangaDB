# v0.64.17 — Repository Runtime Selection

## Purpose

Introduce one explicit repository factory that can construct either the
certified production repository runtime or the staged shared-manga repository
runtime.

This checkpoint does not activate the shared-manga database schema.

## Branch

```text
feature/multi-series-foundation-mitigation
```

## Files

Replace:

```text
scraper/runtime/repository_provider.py
```

Create:

```text
scraper/runtime/repository_factory.py
tests/runtime/test_repository_factory.py
docs/platform/V0_64_17_REPOSITORY_RUNTIME_SELECTION.md
```

## Production Safety

The factory defaults to:

```text
RuntimeRepositoryMode.PRODUCTION
```

The shared-manga repository set can only be selected explicitly.

Do not change:

```text
scraper/database/models.py
scraper/database/migrations/registry.py
scraper/repositories/episode_repository.py
scraper/services/chapter_metadata_ingestion_service.py
scraper/api/routes/
```

No production caller is switched during this checkpoint.

## Ownership Compatibility

Legacy runtime:

```text
RuntimeRepositorySet.episode
RuntimeRepositorySet.chapter
```

both reference the same production `EpisodeRepository`.

Shared-manga runtime:

```text
RuntimeRepositorySet.episode -> staged EpisodeRepository
RuntimeRepositorySet.chapter -> staged MangaRepository
```

## Validation

Focused:

```powershell
python -m pytest tests/runtime/test_repository_factory.py
```

Expected:

```text
6 passed
```

Staged architecture:

```powershell
python -m pytest tests/database/test_shared_manga_models.py tests/repositories/test_shared_manga_repositories.py tests/services/test_shared_manga_api_service.py tests/runtime/test_repository_factory.py
```

Expected:

```text
24 passed
```

Complete backend:

```powershell
python -m pytest
```

Expected:

```text
781 passed
6 skipped
```

Database:

```powershell
python init_database.py
```

Expected:

```text
Database initialized successfully
```

The shared-manga migration must remain inactive.

## Commit

```text
v0.64.17 - Add repository runtime selection
```

## Next

v0.64.18 will introduce API/service composition through the runtime factory
without activating the shared-manga ORM or database migration.
