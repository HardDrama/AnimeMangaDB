# v0.64.14 — Shared Manga Migration Implementation

## Feature Checkpoint

**Purpose:** Implement and certify the database transformation required for shared manga ownership without activating it against the current production runtime.

## Scope

### Included

- Shared manga migration implementation
- `manga` table creation
- `anime.manga_id` creation and assignment
- Naruto and Naruto Shippuden mapping to one Naruto manga row
- One Piece mapping to one One Piece manga row
- `chapter_metadata` ownership migration from `anime_id` to `manga_id`
- Chapter row-count and metadata preservation
- Duplicate shared-chapter collision detection
- Transaction rollback validation
- Repeat-run safety through the migration framework
- Isolated legacy-schema migration tests

### Excluded

- Production migration registry activation
- ORM model replacement
- Repository changes
- Service changes
- API changes
- Search response changes
- Frontend changes
- Production database transformation

Those changes must switch together in v0.64.15.

## New Files

```text
scraper/database/migrations/v06414_shared_manga.py
tests/database/test_shared_manga_migration.py
docs/platform/V0_64_14_SHARED_MANGA_MIGRATION_IMPLEMENTATION.md
```

## Activation Policy

The migration is intentionally **not** added to:

```text
scraper/database/migrations/registry.py
```

during v0.64.14.

The current runtime still expects:

```text
ChapterMetadata.anime_id
```

Registering the migration before the ORM, repositories, services, and API are updated would make the current application incompatible with its database.

v0.64.14 therefore certifies the migration against isolated temporary SQLite databases.

v0.64.15 will:

1. replace the ORM schema
2. update repository and service ownership
3. update API resolution
4. register `SharedMangaMigration`
5. apply the migration to the production database
6. validate runtime compatibility

## Target Schema

```text
Manga
├── id
├── title
├── provider
└── base_url

Anime
├── id
├── title
├── provider
├── base_url
└── manga_id

ChapterMetadata
├── id
├── manga_id
├── chapter_number
├── chapter_title
├── manga_arc
├── source_url
└── last_updated
```

## Canonical Mapping

```text
One Piece anime
└── One Piece manga

Naruto anime
└── Naruto manga

Naruto Shippuden anime
└── Naruto manga
```

## Data Safety

The migration:

- runs inside the migration runner transaction
- preserves chapter metadata IDs
- preserves chapter numbers
- preserves titles, arcs, source URLs, and timestamps
- verifies the chapter row count before replacing the legacy table
- rejects duplicate chapter numbers that would collide after shared ownership
- is not recorded in `schema_migrations` when it fails

No collision is silently merged or discarded.

## Transitional `anime.manga_id`

SQLite cannot add a populated `NOT NULL` foreign-key column to an existing table using a simple `ALTER TABLE`.

The migration adds `anime.manga_id` as a nullable database column, populates every existing row, and validates that no migrated anime row remains unassigned.

Runtime creation rules and the final ORM contract will be updated in v0.64.15.

## Validation

Run focused migration tests:

```powershell
python -m pytest tests/database/test_shared_manga_migration.py
```

Expected:

```text
4 passed
```

Run all migration tests:

```powershell
python -m pytest tests/database
```

Expected minimum:

```text
7 passed
```

Run the complete backend suite:

```powershell
python -m pytest
```

Expected baseline:

```text
757 passed
6 skipped
```

Run the current database initializer:

```powershell
python init_database.py
```

Expected:

```text
Database initialized successfully!
Database migrations applied: 0
Database migrations skipped: 0
```

The migration count remains zero because v0.64.14 is not registered for production activation.

Run frontend validation:

```powershell
npm run lint
npm run build
```

Expected:

```text
0 lint errors
Build successful
```

## Certification Criteria

v0.64.14 is certified when:

- the migration creates the shared manga schema in an isolated legacy database
- Naruto and Naruto Shippuden resolve to one Naruto manga row
- One Piece resolves to one One Piece manga row
- chapter metadata ownership changes to `manga_id`
- chapter metadata content and row counts are preserved
- duplicate shared ownership is rejected
- failed migration state is rolled back
- the migration is not registered in production
- the existing runtime remains fully operational
- complete backend and frontend validation pass

## Commit

```text
v0.64.14 - Implement shared manga database migration
```

Existing branch:

```text
feature/multi-series-foundation
```

## Discord Changelog

```text
v0.64.14 — Shared Manga Migration Implementation

Implemented and certified the database transformation for normalized shared manga ownership.

Added:
• Manga catalog creation
• Anime-to-manga assignment
• Shared Naruto manga mapping
• Chapter metadata ownership migration
• Metadata and row-count preservation checks
• Duplicate chapter collision protection
• Transaction rollback coverage
• Isolated legacy-schema migration tests

The migration is intentionally not active in production yet.

Next:
v0.64.15 — Shared Manga Runtime Integration
```

## Roadmap

### Completed

- v0.64.12 — Shared Manga Architecture Validation
- v0.64.13 — Database Migration Framework
- v0.64.14 — Shared Manga Migration Implementation

### Next

- v0.64.15 — Shared Manga Runtime Integration
- v0.64.16 — Frontend Integration and Metadata Cleanup
- v0.64.17 — Full Naruto Shippuden Certification

### After v0.64

- Platform Checkpoint v3
