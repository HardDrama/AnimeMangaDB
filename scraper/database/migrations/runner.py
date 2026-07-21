from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    insert,
    select,
)
from sqlalchemy.engine import Engine

from scraper.database.migrations.migration_base import (
    BaseMigration,
)
from scraper.database.migrations.registry import (
    MIGRATIONS,
)


migration_metadata = MetaData()

schema_migrations = Table(
    "schema_migrations",
    migration_metadata,
    Column(
        "version",
        Integer,
        primary_key=True,
    ),
    Column(
        "name",
        String(255),
        nullable=False,
    ),
    Column(
        "applied_at",
        DateTime(timezone=True),
        nullable=False,
    ),
)


@dataclass(frozen=True)
class MigrationRunResult:
    applied_versions: tuple[int, ...]
    skipped_versions: tuple[int, ...]

    @property
    def applied_count(self) -> int:
        return len(self.applied_versions)

    @property
    def skipped_count(self) -> int:
        return len(self.skipped_versions)


def _validate_migrations(
    migrations: Iterable[BaseMigration],
) -> list[BaseMigration]:
    ordered = sorted(
        migrations,
        key=lambda migration: migration.version,
    )

    versions = [
        migration.version
        for migration in ordered
    ]

    if len(versions) != len(set(versions)):
        raise ValueError(
            "Database migration versions must be unique."
        )

    for migration in ordered:
        if migration.version <= 0:
            raise ValueError(
                "Database migration versions must be positive integers."
            )

        if not migration.name.strip():
            raise ValueError(
                "Database migrations must have a non-empty name."
            )

    return ordered


def run_pending_migrations(
    engine: Engine,
    migrations: Iterable[BaseMigration] = MIGRATIONS,
) -> MigrationRunResult:
    """
    Create the migration history table and apply all pending migrations.

    Every migration runs in its own transaction. A failed migration is rolled
    back and is not recorded as applied.
    """
    ordered = _validate_migrations(
        migrations
    )

    migration_metadata.create_all(
        bind=engine,
        tables=[schema_migrations],
    )

    applied_versions: list[int] = []
    skipped_versions: list[int] = []

    with engine.connect() as connection:
        existing_versions = set(
            connection.execute(
                select(schema_migrations.c.version)
            ).scalars()
        )

    for migration in ordered:
        if migration.version in existing_versions:
            skipped_versions.append(
                migration.version
            )
            continue

        with engine.begin() as connection:
            migration.upgrade(connection)

            connection.execute(
                insert(schema_migrations).values(
                    version=migration.version,
                    name=migration.name,
                    applied_at=datetime.now(
                        timezone.utc
                    ),
                )
            )

        applied_versions.append(
            migration.version
        )
        existing_versions.add(
            migration.version
        )

    return MigrationRunResult(
        applied_versions=tuple(
            applied_versions
        ),
        skipped_versions=tuple(
            skipped_versions
        ),
    )
