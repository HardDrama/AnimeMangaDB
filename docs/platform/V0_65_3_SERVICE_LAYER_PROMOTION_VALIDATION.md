# v0.65.3 — Service Layer Preparation Validation

## Purpose

v0.65.3 introduces a dormant shared-manga service composition path
without changing production runtime behavior.

## Included

- Keep the production-candidate `MangaRepository`.
- Keep the staged `SharedMangaApiService`.
- Add an explicit staged service provider.
- Add a focused composition test.
- Preserve legacy production routes and runtime wiring.

## Excluded

These remain unchanged:

- Production `EpisodeRepository`
- Production API routes
- Chapter metadata ingestion
- Runtime repository provider and factory
- Production database activation
- Production test fixtures

## Architecture state

Production:

```text
API routes
    ↓
Legacy EpisodeRepository
```

Dormant path:

```text
build_staged_api_service()
    ↓
SharedMangaApiService
    ├── staged EpisodeRepository
    └── staged MangaRepository
```

Nothing in production invokes `build_staged_api_service()`.

## Files

### Retained

- `scraper/repositories/manga_repository.py`
- `scraper/services/shared_manga_api_service.py`

### Replaced

- `scraper/api/service_provider.py`

### Added

- `tests/api/test_staged_service_provider.py`

## Validation

Focused test:

```powershell
python -m pytest tests/api/test_staged_service_provider.py -q
```

Expected:

```text
1 passed
```

Runtime regression:

```powershell
python -m pytest tests/runtime -q
```

API/service regression:

```powershell
python -m pytest tests/api tests/services -q
```

Full suite:

```powershell
python -m pytest -q
```

Expected for all regression commands:

- No failures
- No errors
- Legacy production wiring remains unchanged

## Validation record

- Focused staged composition: 1 passed
- Runtime regression: 14 passed
- API/service regression: 132 passed
- Full suite: 799 passed 6 skipped

## Certification

Status: Certified
