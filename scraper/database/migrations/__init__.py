"""Database migration framework."""

from scraper.database.migrations.runner import (
    MigrationRunResult,
    run_pending_migrations,
)

__all__ = [
    "MigrationRunResult",
    "run_pending_migrations",
]
