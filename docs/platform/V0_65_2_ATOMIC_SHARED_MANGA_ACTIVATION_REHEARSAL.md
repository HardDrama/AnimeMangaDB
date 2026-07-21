# v0.65.2 — Atomic Shared Manga Activation Rehearsal

## Objective

Prove that the certified shared manga migration and certified shared runtime
work together against the same database before either becomes the production
default.

## Evidence-Driven Roadmap Correction

The production initializer creates tables from the current production ORM and
then runs registered migrations. The current production ORM expects
`chapter_metadata.anime_id`, while the shared manga migration replaces that
ownership column with `chapter_metadata.manga_id`.

Registering the migration while leaving the legacy runtime active would create
a database the production ORM can no longer use. Migration registration and
shared runtime activation therefore must occur in the same production
checkpoint.

v0.65.2 is an isolated atomic activation rehearsal. The production registry
remains unchanged.

## Files

Create:

```text
tests/database/test_shared_manga_atomic_activation.py
docs/platform/V0_65_2_ATOMIC_SHARED_MANGA_ACTIVATION_REHEARSAL.md
```

Do not modify:

```text
scraper/database/migrations/registry.py
scraper/database/models.py
scraper/runtime/* default modes
scraper/api/routes/*
```

## Rehearsal Coverage

The tests certify:

1. the production registry remains inactive before the atomic switch
2. a populated legacy database migrates successfully
3. the migrated database is readable through the shared manga ORM
4. the shared runtime bootstrap composes against the migrated database
5. repeated migration execution remains safe

## Validation

Focused rehearsal:

```powershell
python -m pytest tests/database/test_shared_manga_atomic_activation.py
```

Expected:

```text
4 passed
```

All migration and activation tests:

```powershell
python -m pytest tests/database/test_shared_manga_migration.py tests/database/test_shared_manga_migration_readiness.py tests/database/test_shared_manga_atomic_activation.py
```

Expected:

```text
13 passed
```

Runtime composition:

```powershell
python -m pytest tests/runtime
```

Expected:

```text
14 passed
```

Complete suite:

```powershell
python -m pytest
```

Expected:

```text
798 passed
6 skipped
```

Current production initializer:

```powershell
python init_database.py
```

Expected:

```text
Database initialized successfully
```

No shared manga migration should be applied by the production registry.

## Certification Gate

v0.65.2 is certified when:

- the shared ORM reads the migrated database successfully
- the shared runtime composes against the migrated database
- migration execution remains repeat-safe
- the complete suite passes
- the production registry remains inactive
- production initialization remains unchanged

## Commit

```text
v0.65.2 - Certify atomic shared manga activation
```

## Next

v0.65.3 performs the atomic production switch:

1. promote the shared manga ORM
2. register the shared manga migration
3. switch runtime defaults to shared manga
4. update production composition points together
5. run complete API and database certification

These changes must be applied in one checkpoint because the legacy ORM is not
compatible with the migrated chapter metadata schema.
