# v0.65.1 — Shared Manga Migration Readiness Certification

## Objective

Re-certify the existing shared manga migration against the final runtime
composition architecture before production registry activation.

The migration remains disabled in the production registry during this
checkpoint.

## Evidence Review

The existing migration already provides the required structural transformation:

- creates the `manga` table
- adds and assigns `anime.manga_id`
- maps Naruto and Naruto Shippuden to one Naruto manga
- rebuilds `chapter_metadata` with `manga_id`
- preserves chapter metadata rows and identifiers
- rejects shared chapter collisions
- validates the migrated schema
- supports safe repeat execution through migration history

No migration implementation replacement is required for v0.65.1.

## Files

Create:

```text
tests/database/test_shared_manga_migration_readiness.py
docs/platform/V0_65_1_SHARED_MANGA_MIGRATION_READINESS.md
```

Do not modify:

```text
scraper/database/migrations/v06414_shared_manga.py
scraper/database/migrations/registry.py
scraper/database/models.py
```

## Added Certification Coverage

The readiness tests certify:

1. empty legacy schema migration
2. populated legacy database preservation
3. direct validation of an already-migrated schema
4. shared Naruto manga assignment
5. rejection and rollback of an invalid partial schema

## Validation

Focused readiness tests:

```powershell
python -m pytest tests/database/test_shared_manga_migration_readiness.py
```

Expected:

```text
5 passed
```

All shared manga migration tests:

```powershell
python -m pytest tests/database/test_shared_manga_migration.py tests/database/test_shared_manga_migration_readiness.py
```

Expected:

```text
9 passed
```

Runtime composition tests:

```powershell
python -m pytest tests/runtime
```

Expected:

```text
14 passed
```

Complete backend suite:

```powershell
python -m pytest
```

Expected:

```text
794 passed
6 skipped
```

Current production database initialization:

```powershell
python init_database.py
```

Expected:

```text
Database initialized successfully
```

The shared manga migration must remain unregistered and unapplied by the
production initializer.

## Certification Gate

v0.65.1 is certified when:

- all five readiness scenarios pass
- all original migration tests remain passing
- the full regression suite remains passing
- production database initialization remains unchanged
- `registry.py` remains unchanged
- no production database is migrated

## Commit

```text
v0.65.1 - Certify shared manga migration readiness
```

## Next

v0.65.2 will activate the migration registry in a controlled checkpoint.
Runtime defaults will remain unchanged until the migrated database and shared
ORM are activated together safely.
