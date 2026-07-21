from sqlalchemy import (
    create_engine,
    inspect,
    text,
)
from sqlalchemy.engine import Connection

from scraper.database.migrations.migration_base import (
    BaseMigration,
)
from scraper.database.migrations.runner import (
    run_pending_migrations,
)


class CreateExampleTableMigration(
    BaseMigration
):
    version = 1
    name = "Create example table"

    def upgrade(
        self,
        connection: Connection,
    ) -> None:
        connection.execute(
            text(
                """
                CREATE TABLE example (
                    id INTEGER PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
        )


class InsertExampleRowMigration(
    BaseMigration
):
    version = 2
    name = "Insert example row"

    def upgrade(
        self,
        connection: Connection,
    ) -> None:
        connection.execute(
            text(
                """
                INSERT INTO example (value)
                VALUES ('created by migration')
                """
            )
        )


def create_test_engine():
    return create_engine(
        "sqlite:///:memory:"
    )


def test_runner_creates_history_table_and_applies_migrations():
    engine = create_test_engine()

    result = run_pending_migrations(
        engine,
        migrations=(
            InsertExampleRowMigration(),
            CreateExampleTableMigration(),
        ),
    )

    inspector = inspect(engine)

    assert "schema_migrations" in inspector.get_table_names()
    assert "example" in inspector.get_table_names()

    assert result.applied_versions == (1, 2)
    assert result.skipped_versions == ()

    with engine.connect() as connection:
        value = connection.execute(
            text(
                "SELECT value FROM example"
            )
        ).scalar_one()

    assert value == "created by migration"


def test_runner_skips_already_applied_migrations():
    engine = create_test_engine()

    migrations = (
        CreateExampleTableMigration(),
        InsertExampleRowMigration(),
    )

    first_result = run_pending_migrations(
        engine,
        migrations=migrations,
    )

    second_result = run_pending_migrations(
        engine,
        migrations=migrations,
    )

    assert first_result.applied_versions == (1, 2)

    assert second_result.applied_versions == ()
    assert second_result.skipped_versions == (1, 2)

    with engine.connect() as connection:
        row_count = connection.execute(
            text(
                "SELECT COUNT(*) FROM example"
            )
        ).scalar_one()

    assert row_count == 1


def test_runner_rejects_duplicate_versions():
    engine = create_test_engine()

    class DuplicateVersionMigration(
        BaseMigration
    ):
        version = 1
        name = "Duplicate version"

        def upgrade(
            self,
            connection: Connection,
        ) -> None:
            del connection

    try:
        run_pending_migrations(
            engine,
            migrations=(
                CreateExampleTableMigration(),
                DuplicateVersionMigration(),
            ),
        )

    except ValueError as error:
        assert (
            str(error)
            == "Database migration versions must be unique."
        )

    else:
        raise AssertionError(
            "Expected duplicate migration versions to fail."
        )