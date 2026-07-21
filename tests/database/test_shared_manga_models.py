from datetime import datetime

import pytest
from sqlalchemy import (
    create_engine,
    inspect,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from scraper.database.models_shared_manga import (
    Anime,
    ChapterMetadata,
    Episode,
    EpisodeChapter,
    Manga,
    SharedMangaBase,
)


def create_test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    SharedMangaBase.metadata.create_all(
        bind=engine,
    )

    return engine


def test_shared_manga_models_create_expected_schema():
    engine = create_test_engine()
    inspector = inspect(engine)

    assert set(
        inspector.get_table_names()
    ) == {
        "anime",
        "chapter_metadata",
        "episode_chapters",
        "episodes",
        "manga",
    }

    anime_columns = {
        column["name"]
        for column in inspector.get_columns(
            "anime"
        )
    }

    chapter_columns = {
        column["name"]
        for column in inspector.get_columns(
            "chapter_metadata"
        )
    }

    assert "manga_id" in anime_columns
    assert "manga_id" in chapter_columns
    assert "anime_id" not in chapter_columns


def test_naruto_anime_share_one_manga():
    engine = create_test_engine()

    with Session(engine) as session:
        manga = Manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        naruto = Anime(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga=manga,
        )

        shippuden = Anime(
            title="Naruto Shippuden",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga=manga,
        )

        session.add_all(
            [
                naruto,
                shippuden,
            ]
        )
        session.commit()

        session.refresh(manga)

        assert manga.title == "Naruto"

        assert {
            anime.title
            for anime in manga.anime
        } == {
            "Naruto",
            "Naruto Shippuden",
        }

        assert naruto.manga_id == shippuden.manga_id


def test_chapter_metadata_belongs_to_manga():
    engine = create_test_engine()

    with Session(engine) as session:
        manga = Manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        chapter = ChapterMetadata(
            manga=manga,
            chapter_number=245,
            chapter_title="Homecoming",
            manga_arc="Kazekage Rescue Mission",
            source_url=(
                "https://naruto.fandom.com/wiki/"
                "Chapter_245"
            ),
            last_updated=datetime(
                2026,
                7,
                20,
            ),
        )

        session.add(chapter)
        session.commit()

        stored = session.execute(
            select(ChapterMetadata)
            .where(
                ChapterMetadata.chapter_number
                == 245
            )
        ).scalar_one()

        assert stored.manga.title == "Naruto"
        assert stored.manga_id == manga.id
        assert stored.chapter_title == "Homecoming"


def test_chapter_number_is_unique_per_manga():
    engine = create_test_engine()

    with Session(engine) as session:
        manga = Manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        session.add_all(
            [
                ChapterMetadata(
                    manga=manga,
                    chapter_number=245,
                ),
                ChapterMetadata(
                    manga=manga,
                    chapter_number=245,
                ),
            ]
        )

        with pytest.raises(
            IntegrityError,
        ):
            session.commit()


def test_same_chapter_number_can_exist_in_different_manga():
    engine = create_test_engine()

    with Session(engine) as session:
        naruto = Manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        one_piece = Manga(
            title="One Piece",
            provider="fandom",
            base_url="https://onepiece.fandom.com",
        )

        session.add_all(
            [
                ChapterMetadata(
                    manga=naruto,
                    chapter_number=1,
                ),
                ChapterMetadata(
                    manga=one_piece,
                    chapter_number=1,
                ),
            ]
        )

        session.commit()

        chapters = session.execute(
            select(ChapterMetadata)
            .where(
                ChapterMetadata.chapter_number
                == 1
            )
        ).scalars().all()

        assert len(chapters) == 2

        assert {
            chapter.manga.title
            for chapter in chapters
        } == {
            "Naruto",
            "One Piece",
        }


def test_episode_mappings_remain_anime_owned():
    engine = create_test_engine()

    with Session(engine) as session:
        manga = Manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        anime = Anime(
            title="Naruto Shippuden",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga=manga,
        )

        episode = Episode(
            anime=anime,
            episode_number=1,
            episode_title="Homecoming",
            arc="Kazekage Rescue Mission",
            source_url=(
                "https://naruto.fandom.com/wiki/"
                "Naruto:_Shipp%C5%ABden_Episode_1"
            ),
            last_updated=datetime(
                2026,
                7,
                20,
            ),
        )

        mapping = EpisodeChapter(
            episode=episode,
            chapter_number=245,
        )

        session.add(mapping)
        session.commit()

        assert episode.anime.title == (
            "Naruto Shippuden"
        )

        assert mapping.episode_id == episode.id
        assert mapping.chapter_number == 245