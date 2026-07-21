from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from scraper.database.migrations.registry import MIGRATIONS
from scraper.database.migrations.runner import run_pending_migrations
from scraper.database.migrations.v06414_shared_manga import SharedMangaMigration
from scraper.database.models_shared_manga import Anime, ChapterMetadata, Manga
from scraper.runtime.api_service_factory import RuntimeApiMode
from scraper.runtime.runtime_bootstrap import build_runtime


def create_populated_legacy_engine():
    engine = create_engine("sqlite:///:memory:")

    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE anime (
                id INTEGER NOT NULL PRIMARY KEY,
                title VARCHAR(200) NOT NULL UNIQUE,
                provider VARCHAR(100) NOT NULL,
                base_url VARCHAR(500) NOT NULL
            )
        """))
        connection.execute(text("""
            CREATE TABLE episodes (
                id INTEGER NOT NULL PRIMARY KEY,
                anime_id INTEGER NOT NULL,
                episode_number INTEGER NOT NULL,
                episode_title VARCHAR(300),
                arc VARCHAR(200),
                source_url VARCHAR(500),
                last_updated DATETIME,
                FOREIGN KEY(anime_id) REFERENCES anime(id)
            )
        """))
        connection.execute(text("""
            CREATE TABLE episode_chapters (
                id INTEGER NOT NULL PRIMARY KEY,
                episode_id INTEGER NOT NULL,
                chapter_number INTEGER NOT NULL,
                FOREIGN KEY(episode_id) REFERENCES episodes(id)
            )
        """))
        connection.execute(text("""
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
                FOREIGN KEY(anime_id) REFERENCES anime(id)
            )
        """))
        connection.execute(text("""
            INSERT INTO anime (id, title, provider, base_url)
            VALUES
                (1, 'One Piece', 'fandom', 'https://onepiece.fandom.com'),
                (2, 'Naruto', 'fandom', 'https://naruto.fandom.com'),
                (3, 'Naruto Shippuden', 'fandom', 'https://naruto.fandom.com')
        """))
        connection.execute(text("""
            INSERT INTO chapter_metadata (
                id, anime_id, chapter_number, chapter_title,
                manga_arc, source_url, last_updated
            )
            VALUES
                (
                    1, 1, 1, 'Romance Dawn', 'East Blue',
                    'https://example.test/one-piece/1',
                    '2026-01-01 00:00:00'
                ),
                (
                    2, 2, 245, 'Naruto Returns', 'Kazekage Rescue',
                    'https://example.test/naruto/245',
                    '2026-01-02 00:00:00'
                )
        """))

    return engine


def test_production_registry_remains_inactive_before_atomic_switch():
    assert MIGRATIONS == ()


def test_migrated_database_is_readable_by_shared_manga_orm():
    engine = create_populated_legacy_engine()

    result = run_pending_migrations(
        engine,
        migrations=(SharedMangaMigration(),),
    )

    assert result.applied_versions == (6414,)

    with Session(engine) as session:
        manga_titles = session.scalars(
            select(Manga.title).order_by(Manga.title)
        ).all()
        anime_rows = session.execute(
            select(Anime.title, Manga.title)
            .join(Manga, Anime.manga_id == Manga.id)
            .order_by(Anime.id)
        ).all()
        chapter_rows = session.execute(
            select(ChapterMetadata.chapter_number, Manga.title)
            .join(Manga, ChapterMetadata.manga_id == Manga.id)
            .order_by(ChapterMetadata.id)
        ).all()

    assert manga_titles == ["Naruto", "One Piece"]
    assert anime_rows == [
        ("One Piece", "One Piece"),
        ("Naruto", "Naruto"),
        ("Naruto Shippuden", "Naruto"),
    ]
    assert chapter_rows == [
        (1, "One Piece"),
        (245, "Naruto"),
    ]


def test_shared_runtime_bootstrap_composes_against_migrated_database():
    engine = create_populated_legacy_engine()

    run_pending_migrations(
        engine,
        migrations=(SharedMangaMigration(),),
    )

    with Session(engine) as session:
        runtime = build_runtime(
            session,
            RuntimeApiMode.SHARED_MANGA,
        )

        assert runtime.mode is RuntimeApiMode.SHARED_MANGA
        assert runtime.models.Anime is Anime
        assert runtime.models.Manga is Manga
        assert runtime.models.ChapterMetadata is ChapterMetadata


def test_atomic_rehearsal_remains_repeat_safe():
    engine = create_populated_legacy_engine()
    migrations = (SharedMangaMigration(),)

    first = run_pending_migrations(engine, migrations=migrations)
    second = run_pending_migrations(engine, migrations=migrations)

    assert first.applied_versions == (6414,)
    assert second.applied_versions == ()
    assert second.skipped_versions == (6414,)

    with Session(engine) as session:
        assert session.scalar(
            select(Manga).where(Manga.title == "Naruto")
        ) is not None
