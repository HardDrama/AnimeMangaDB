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


def seed_standard_legacy_data(engine):
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO anime (id, title, provider, base_url)
                VALUES
                    (1, 'One Piece', 'fandom', 'https://onepiece.fandom.com'),
                    (2, 'Naruto', 'fandom', 'https://naruto.fandom.com'),
                    (3, 'Naruto Shippuden', 'fandom', 'https://naruto.fandom.com')
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
                        1,
                        1,
                        1,
                        'Romance Dawn',
                        'East Blue',
                        'https://example.test/one-piece/1',
                        '2026-01-01 00:00:00'
                    ),
                    (
                        2,
                        2,
                        245,
                        'Naruto Returns',
                        'Kazekage Rescue',
                        'https://example.test/naruto/245',
                        '2026-01-02 00:00:00'
                    ),
                    (
                        3,
                        2,
                        249,
                        'The Kazekage Stands Tall',
                        'Kazekage Rescue',
                        'https://example.test/naruto/249',
                        '2026-01-03 00:00:00'
                    )
                """
            )
        )


def test_shared_manga_migration_normalizes_naruto_catalog():
    engine = create_legacy_engine()
    seed_standard_legacy_data(engine)

    result = run_pending_migrations(
        engine,
        migrations=(SharedMangaMigration(),),
    )

    assert result.applied_versions == (6414,)
    assert result.skipped_versions == ()

    inspector = inspect(engine)
    assert "manga" in inspector.get_table_names()

    anime_columns = {
        column["name"]
        for column in inspector.get_columns("anime")
    }
    chapter_columns = {
        column["name"]
        for column in inspector.get_columns("chapter_metadata")
    }

    assert "manga_id" in anime_columns
    assert "manga_id" in chapter_columns
    assert "anime_id" not in chapter_columns

    with engine.connect() as connection:
        manga_rows = connection.execute(
            text("SELECT id, title FROM manga ORDER BY title")
        ).mappings().all()
        anime_rows = connection.execute(
            text(
                """
                SELECT
                    anime.title AS anime_title,
                    manga.title AS manga_title
                FROM anime
                JOIN manga ON manga.id = anime.manga_id
                ORDER BY anime.id
                """
            )
        ).mappings().all()
        chapter_rows = connection.execute(
            text(
                """
                SELECT
                    chapter_metadata.chapter_number,
                    manga.title AS manga_title
                FROM chapter_metadata
                JOIN manga ON manga.id = chapter_metadata.manga_id
                ORDER BY chapter_metadata.id
                """
            )
        ).mappings().all()

    assert [row["title"] for row in manga_rows] == [
        "Naruto",
        "One Piece",
    ]
    assert [
        (row["anime_title"], row["manga_title"])
        for row in anime_rows
    ] == [
        ("One Piece", "One Piece"),
        ("Naruto", "Naruto"),
        ("Naruto Shippuden", "Naruto"),
    ]
    assert [
        (row["chapter_number"], row["manga_title"])
        for row in chapter_rows
    ] == [
        (1, "One Piece"),
        (245, "Naruto"),
        (249, "Naruto"),
    ]


def test_shared_manga_migration_preserves_metadata_rows():
    engine = create_legacy_engine()
    seed_standard_legacy_data(engine)

    with engine.connect() as connection:
        before_rows = connection.execute(
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
        after_rows = connection.execute(
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

    assert after_rows == before_rows


def test_shared_manga_migration_is_applied_only_once():
    engine = create_legacy_engine()
    seed_standard_legacy_data(engine)
    migrations = (SharedMangaMigration(),)

    first_result = run_pending_migrations(engine, migrations=migrations)
    second_result = run_pending_migrations(engine, migrations=migrations)

    assert first_result.applied_versions == (6414,)
    assert second_result.applied_versions == ()
    assert second_result.skipped_versions == (6414,)


def test_shared_manga_migration_rejects_chapter_collisions():
    engine = create_legacy_engine()

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO anime (id, title, provider, base_url)
                VALUES
                    (1, 'Naruto', 'fandom', 'https://naruto.fandom.com'),
                    (
                        2,
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
                    chapter_title
                )
                VALUES
                    (1, 1, 249, 'Naruto ownership'),
                    (2, 2, 249, 'Shippuden ownership')
                """
            )
        )

    with pytest.raises(RuntimeError, match="duplicate chapter ownership"):
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
        chapter_columns = {
            column["name"]
            for column in inspect(connection).get_columns("chapter_metadata")
        }

    assert history_count == 0
    assert "anime_id" in chapter_columns
