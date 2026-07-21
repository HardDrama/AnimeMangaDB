import pytest
from sqlalchemy import create_engine, inspect, text

from scraper.database.migrations.runner import run_pending_migrations
from scraper.database.migrations.v06414_shared_manga import (
    SharedMangaMigration,
)


def create_legacy_engine():
    engine = create_engine("sqlite:///:memory:")

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE anime (
                    id INTEGER NOT NULL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL UNIQUE,
                    provider VARCHAR(100) NOT NULL,
                    base_url VARCHAR(500) NOT NULL
                )
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE TABLE chapter_metadata (
                    id INTEGER NOT NULL PRIMARY KEY,
                    anime_id INTEGER NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    chapter_title VARCHAR(300),
                    manga_arc VARCHAR(200),
                    source_url VARCHAR(500),
                    last_updated DATETIME,
                    CONSTRAINT uq_chapter_metadata_number
                        UNIQUE(anime_id, chapter_number),
                    FOREIGN KEY(anime_id)
                        REFERENCES anime(id)
                )
                """
            )
        )

    return engine


def seed_populated_legacy_data(engine):
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO anime (
                    id,
                    title,
                    provider,
                    base_url
                )
                VALUES
                    (
                        1,
                        'One Piece',
                        'fandom',
                        'https://onepiece.fandom.com'
                    ),
                    (
                        2,
                        'Naruto',
                        'fandom',
                        'https://naruto.fandom.com'
                    ),
                    (
                        3,
                        'Naruto Shippuden',
                        'fandom',
                        'https://naruto.fandom.com'
                    )
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO chapter_metadata (
                    id,
                    anime_id,
                    chapter_number,
                    chapter_title,
                    manga_arc,
                    source_url,
                    last_updated
                )
                VALUES
                    (
                        10,
                        1,
                        1,
                        'Romance Dawn',
                        'East Blue',
                        'https://example.test/one-piece/1',
                        '2026-01-01 00:00:00'
                    ),
                    (
                        20,
                        2,
                        245,
                        'Naruto Returns',
                        'Kazekage Rescue',
                        'https://example.test/naruto/245',
                        '2026-01-02 00:00:00'
                    )
                """
            )
        )


def test_empty_legacy_schema_migrates_successfully():
    engine = create_legacy_engine()

    result = run_pending_migrations(
        engine,
        migrations=(SharedMangaMigration(),),
    )

    assert result.applied_versions == (6414,)

    inspector = inspect(engine)

    assert "manga" in inspector.get_table_names()
    assert {
        column["name"]
        for column in inspector.get_columns("anime")
    } >= {"id", "title", "provider", "base_url", "manga_id"}
    assert {
        column["name"]
        for column in inspector.get_columns("chapter_metadata")
    } == {
        "id",
        "manga_id",
        "chapter_number",
        "chapter_title",
        "manga_arc",
        "source_url",
        "last_updated",
    }

    with engine.connect() as connection:
        assert connection.execute(
            text("SELECT COUNT(*) FROM manga")
        ).scalar_one() == 0
        assert connection.execute(
            text("SELECT COUNT(*) FROM chapter_metadata")
        ).scalar_one() == 0


def test_populated_migration_preserves_primary_keys_and_metadata():
    engine = create_legacy_engine()
    seed_populated_legacy_data(engine)

    with engine.connect() as connection:
        before = connection.execute(
            text(
                """
                SELECT
                    id,
                    chapter_number,
                    chapter_title,
                    manga_arc,
                    source_url,
                    last_updated
                FROM chapter_metadata
                ORDER BY id
                """
            )
        ).all()

    run_pending_migrations(
        engine,
        migrations=(SharedMangaMigration(),),
    )

    with engine.connect() as connection:
        after = connection.execute(
            text(
                """
                SELECT
                    id,
                    chapter_number,
                    chapter_title,
                    manga_arc,
                    source_url,
                    last_updated
                FROM chapter_metadata
                ORDER BY id
                """
            )
        ).all()

    assert after == before


def test_migrated_schema_passes_direct_repeat_validation():
    engine = create_legacy_engine()
    seed_populated_legacy_data(engine)
    migration = SharedMangaMigration()

    run_pending_migrations(
        engine,
        migrations=(migration,),
    )

    with engine.begin() as connection:
        migration.upgrade(connection)

    with engine.connect() as connection:
        assert connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM anime
                WHERE manga_id IS NULL
                """
            )
        ).scalar_one() == 0
        assert connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM chapter_metadata
                WHERE manga_id IS NULL
                """
            )
        ).scalar_one() == 0


def test_migration_preserves_shared_naruto_assignment():
    engine = create_legacy_engine()
    seed_populated_legacy_data(engine)

    run_pending_migrations(
        engine,
        migrations=(SharedMangaMigration(),),
    )

    with engine.connect() as connection:
        rows = connection.execute(
            text(
                """
                SELECT
                    anime.title AS anime_title,
                    manga.title AS manga_title
                FROM anime
                JOIN manga
                    ON manga.id = anime.manga_id
                WHERE anime.title IN (
                    'Naruto',
                    'Naruto Shippuden'
                )
                ORDER BY anime.title
                """
            )
        ).all()

    assert rows == [
        ("Naruto", "Naruto"),
        ("Naruto Shippuden", "Naruto"),
    ]


def test_invalid_partial_schema_is_rejected_without_history_record():
    engine = create_legacy_engine()

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                ALTER TABLE chapter_metadata
                RENAME TO chapter_metadata_legacy
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE TABLE chapter_metadata (
                    id INTEGER NOT NULL PRIMARY KEY,
                    chapter_number INTEGER NOT NULL
                )
                """
            )
        )

    with pytest.raises(
        RuntimeError,
        match="neither the legacy 'anime_id' column nor the migrated",
    ):
        run_pending_migrations(
            engine,
            migrations=(SharedMangaMigration(),),
        )

    with engine.connect() as connection:
        history_count = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM schema_migrations
                WHERE version = 6414
                """
            )
        ).scalar_one()

    assert history_count == 0
