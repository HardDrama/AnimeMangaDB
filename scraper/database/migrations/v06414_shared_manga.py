from collections.abc import Mapping

from sqlalchemy import inspect, text
from sqlalchemy.engine import Connection

from scraper.database.migrations.migration_base import BaseMigration


class SharedMangaMigration(BaseMigration):
    """
    Convert anime-owned chapter metadata into shared manga-owned metadata.

    This migration is implemented and tested in v0.64.14, but it is not added
    to the production migration registry until the runtime ORM, repositories,
    services, and API are updated together in v0.64.15.
    """

    version = 6414
    name = "Create shared manga database foundation"

    _CANONICAL_MANGA_TITLES = {
        "Naruto Shippuden": "Naruto",
    }

    def upgrade(self, connection: Connection) -> None:
        if connection.dialect.name != "sqlite":
            raise RuntimeError(
                "The v0.64.14 shared manga migration currently supports "
                "SQLite only."
            )

        inspector = inspect(connection)
        table_names = set(inspector.get_table_names())

        if "anime" not in table_names:
            raise RuntimeError(
                "Cannot migrate shared manga architecture because the "
                "'anime' table does not exist."
            )

        if "chapter_metadata" not in table_names:
            raise RuntimeError(
                "Cannot migrate shared manga architecture because the "
                "'chapter_metadata' table does not exist."
            )

        chapter_columns = {
            column["name"]
            for column in inspector.get_columns("chapter_metadata")
        }

        if "manga_id" in chapter_columns and "anime_id" not in chapter_columns:
            self._validate_migrated_schema(connection)
            return

        if "anime_id" not in chapter_columns:
            raise RuntimeError(
                "The chapter_metadata table has neither the legacy "
                "'anime_id' column nor the migrated 'manga_id' column."
            )

        self._create_manga_table(connection)
        self._add_anime_manga_id_column(connection)
        self._populate_manga_catalog(connection)
        self._assign_anime_manga_ids(connection)
        self._validate_no_shared_chapter_collisions(connection)
        self._rebuild_chapter_metadata(connection)
        self._validate_migrated_schema(connection)

    def _canonical_manga_title(self, anime_title: str) -> str:
        return self._CANONICAL_MANGA_TITLES.get(anime_title, anime_title)

    def _create_manga_table(self, connection: Connection) -> None:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS manga (
                    id INTEGER NOT NULL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    provider VARCHAR(100) NOT NULL,
                    base_url VARCHAR(500) NOT NULL,
                    CONSTRAINT uq_manga_title UNIQUE (title)
                )
                """
            )
        )

    def _add_anime_manga_id_column(self, connection: Connection) -> None:
        anime_columns = {
            column["name"]
            for column in inspect(connection).get_columns("anime")
        }

        if "manga_id" not in anime_columns:
            connection.execute(
                text(
                    """
                    ALTER TABLE anime
                    ADD COLUMN manga_id INTEGER
                    REFERENCES manga(id)
                    """
                )
            )

        connection.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS ix_anime_manga_id
                ON anime (manga_id)
                """
            )
        )

    def _populate_manga_catalog(self, connection: Connection) -> None:
        anime_rows = connection.execute(
            text(
                """
                SELECT id, title, provider, base_url
                FROM anime
                ORDER BY id
                """
            )
        ).mappings().all()

        canonical_sources: dict[str, Mapping[str, object]] = {}

        for row in anime_rows:
            anime_title = str(row["title"])
            manga_title = self._canonical_manga_title(anime_title)
            existing = canonical_sources.get(manga_title)

            if existing is None or anime_title == manga_title:
                canonical_sources[manga_title] = row

        for manga_title, source in canonical_sources.items():
            connection.execute(
                text(
                    """
                    INSERT INTO manga (
                        title,
                        provider,
                        base_url
                    )
                    VALUES (
                        :title,
                        :provider,
                        :base_url
                    )
                    ON CONFLICT(title) DO UPDATE SET
                        provider = excluded.provider,
                        base_url = excluded.base_url
                    """
                ),
                {
                    "title": manga_title,
                    "provider": source["provider"],
                    "base_url": source["base_url"],
                },
            )

    def _assign_anime_manga_ids(self, connection: Connection) -> None:
        anime_rows = connection.execute(
            text(
                """
                SELECT id, title
                FROM anime
                ORDER BY id
                """
            )
        ).mappings().all()

        for row in anime_rows:
            manga_title = self._canonical_manga_title(str(row["title"]))
            manga_id = connection.execute(
                text(
                    """
                    SELECT id
                    FROM manga
                    WHERE title = :title
                    """
                ),
                {"title": manga_title},
            ).scalar_one()

            connection.execute(
                text(
                    """
                    UPDATE anime
                    SET manga_id = :manga_id
                    WHERE id = :anime_id
                    """
                ),
                {
                    "manga_id": manga_id,
                    "anime_id": row["id"],
                },
            )

    def _validate_no_shared_chapter_collisions(
        self,
        connection: Connection,
    ) -> None:
        collisions = connection.execute(
            text(
                """
                SELECT
                    anime.manga_id AS manga_id,
                    chapter_metadata.chapter_number AS chapter_number,
                    COUNT(*) AS row_count
                FROM chapter_metadata
                JOIN anime
                    ON anime.id = chapter_metadata.anime_id
                GROUP BY
                    anime.manga_id,
                    chapter_metadata.chapter_number
                HAVING COUNT(*) > 1
                ORDER BY
                    anime.manga_id,
                    chapter_metadata.chapter_number
                """
            )
        ).mappings().all()

        if collisions:
            formatted = ", ".join(
                (
                    f"manga_id={row['manga_id']}, "
                    f"chapter={row['chapter_number']}, "
                    f"rows={row['row_count']}"
                )
                for row in collisions
            )

            raise RuntimeError(
                "Shared manga migration detected duplicate chapter "
                f"ownership that requires manual resolution: {formatted}"
            )

    def _rebuild_chapter_metadata(self, connection: Connection) -> None:
        legacy_count = connection.execute(
            text("SELECT COUNT(*) FROM chapter_metadata")
        ).scalar_one()

        connection.execute(text("DROP TABLE IF EXISTS chapter_metadata_new"))

        connection.execute(
            text(
                """
                CREATE TABLE chapter_metadata_new (
                    id INTEGER NOT NULL PRIMARY KEY,
                    manga_id INTEGER NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    chapter_title VARCHAR(300),
                    manga_arc VARCHAR(200),
                    source_url VARCHAR(500),
                    last_updated DATETIME,
                    CONSTRAINT fk_chapter_metadata_manga
                        FOREIGN KEY(manga_id)
                        REFERENCES manga(id),
                    CONSTRAINT uq_chapter_metadata_number
                        UNIQUE(manga_id, chapter_number)
                )
                """
            )
        )

        connection.execute(
            text(
                """
                INSERT INTO chapter_metadata_new (
                    id,
                    manga_id,
                    chapter_number,
                    chapter_title,
                    manga_arc,
                    source_url,
                    last_updated
                )
                SELECT
                    chapter_metadata.id,
                    anime.manga_id,
                    chapter_metadata.chapter_number,
                    chapter_metadata.chapter_title,
                    chapter_metadata.manga_arc,
                    chapter_metadata.source_url,
                    chapter_metadata.last_updated
                FROM chapter_metadata
                JOIN anime
                    ON anime.id = chapter_metadata.anime_id
                ORDER BY chapter_metadata.id
                """
            )
        )

        migrated_count = connection.execute(
            text("SELECT COUNT(*) FROM chapter_metadata_new")
        ).scalar_one()

        if migrated_count != legacy_count:
            raise RuntimeError(
                "Shared manga migration did not preserve the chapter "
                f"metadata row count: before={legacy_count}, "
                f"after={migrated_count}."
            )

        connection.execute(text("DROP TABLE chapter_metadata"))
        connection.execute(
            text(
                """
                ALTER TABLE chapter_metadata_new
                RENAME TO chapter_metadata
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS ix_chapter_metadata_manga_id
                ON chapter_metadata (manga_id)
                """
            )
        )

    def _validate_migrated_schema(self, connection: Connection) -> None:
        inspector = inspect(connection)
        table_names = set(inspector.get_table_names())

        if "manga" not in table_names:
            raise RuntimeError(
                "Shared manga migration validation failed: "
                "'manga' table is missing."
            )

        anime_columns = {
            column["name"]
            for column in inspector.get_columns("anime")
        }
        if "manga_id" not in anime_columns:
            raise RuntimeError(
                "Shared manga migration validation failed: "
                "'anime.manga_id' is missing."
            )

        chapter_columns = {
            column["name"]
            for column in inspector.get_columns("chapter_metadata")
        }
        if "manga_id" not in chapter_columns:
            raise RuntimeError(
                "Shared manga migration validation failed: "
                "'chapter_metadata.manga_id' is missing."
            )
        if "anime_id" in chapter_columns:
            raise RuntimeError(
                "Shared manga migration validation failed: legacy "
                "'chapter_metadata.anime_id' still exists."
            )

        unassigned_anime = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM anime
                WHERE manga_id IS NULL
                """
            )
        ).scalar_one()
        if unassigned_anime != 0:
            raise RuntimeError(
                "Shared manga migration validation failed: "
                f"{unassigned_anime} anime rows have no manga assignment."
            )

        orphaned_chapters = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM chapter_metadata
                LEFT JOIN manga
                    ON manga.id = chapter_metadata.manga_id
                WHERE manga.id IS NULL
                """
            )
        ).scalar_one()
        if orphaned_chapters != 0:
            raise RuntimeError(
                "Shared manga migration validation failed: "
                f"{orphaned_chapters} chapter rows are orphaned."
            )
