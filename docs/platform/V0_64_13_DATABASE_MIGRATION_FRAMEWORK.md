# v0.64.13 — Database Migration Framework

## Feature Checkpoint

**Purpose:** Establish a durable, ordered database migration framework before introducing the shared manga schema.

## Scope

### Included

- Ordered migration contract
- Migration registry
- Persistent migration history
- Transactional migration execution
- Duplicate-version validation
- Repeat-run safety
- Automated migration-runner tests
- Integration with database initialization

### Excluded

- `Manga` model
- `Anime.manga_id`
- `ChapterMetadata.manga_id`
- Existing data transformation
- Repository, API, or frontend changes

The shared manga schema belongs to v0.64.14.

## Architecture

New package:

```text
scraper/database/migrations/
├── __init__.py
├── migration_base.py
├── registry.py
└── runner.py
```

Migration history is stored in:

```text
schema_migrations
```

Columns:

```text
version
name
applied_at
```

Each migration:

- has one positive integer version
- has one non-empty name
- implements `upgrade(connection)`
- runs inside its own transaction
- is recorded only after successful completion
- is skipped on later runs

## Version Convention

Use the project version converted to an integer:

```text
v0.64.14 → 6414
v0.65.1  → 6501
```

Migration versions must be unique.

## Database Initialization

`init_database.py` continues to call `Base.metadata.create_all()` for fresh tables and then calls the migration runner for existing-schema transformations.

This preserves current initialization behavior while adding explicit migration support.

## Validation

Run focused tests:

```powershell
python -m pytest tests/database/test_migration_runner.py
```

Expected:

```text
3 passed
```

Run database initialization:

```powershell
python init_database.py
```

Expected output includes:

```text
Database initialized successfully!
Database migrations applied: 0
Database migrations skipped: 0
```

On later runs, registered migrations will be applied once and then skipped.

Run the complete backend suite:

```powershell
python -m pytest
```

Expected baseline:

```text
753 passed
6 skipped
```

A higher passing count is acceptable if other valid tests were added.

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

v0.64.13 is certified when:

- `schema_migrations` is created
- pending migrations run in version order
- applied migrations are recorded
- repeated runs do not apply migrations twice
- duplicate migration versions are rejected
- failed migrations are not recorded
- existing application tables and data remain unchanged
- complete backend and frontend validation pass

## Commit

```text
v0.64.13 - Add database migration framework
```

Suggested branch:

```text
feature/v0.64.13-database-migration-framework
```

## Discord Changelog

```text
v0.64.13 — Database Migration Framework

Added the platform's first durable database migration framework.

Certified:
• Ordered migration execution
• Persistent migration history
• Transactional migration application
• Repeat-run safety
• Duplicate-version validation
• Database initialization integration
• Automated migration-runner coverage

No shared manga schema changes were introduced in this checkpoint.

Next:
v0.64.14 — Shared Manga Database Foundation
```

## Roadmap

### Completed

- v0.64.12 — Shared Manga Architecture Validation
- v0.64.13 — Database Migration Framework

### Next

- v0.64.14 — Shared Manga Database Foundation
- v0.64.15 — Shared Manga Repository and API Integration
- v0.64.16 — Frontend Integration and Metadata Cleanup
- v0.64.17 — Full Naruto Shippuden Certification

### After v0.64

- Platform Checkpoint v3
- Next production series
