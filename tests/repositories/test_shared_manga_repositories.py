from datetime import datetime

from sqlalchemy import (
    create_engine,
    select,
)
from sqlalchemy.orm import Session

from scraper.database.models_shared_manga import (
    Anime,
    ChapterMetadata,
    Manga,
    SharedMangaBase,
)
from scraper.models.chapter_metadata import (
    ChapterMetadata as ChapterMetadataData,
)
from scraper.repositories.episode_repository_shared_manga import (
    EpisodeRepository,
)
from scraper.repositories.manga_repository_shared_manga import (
    MangaRepository,
)


def create_test_session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
    )

    SharedMangaBase.metadata.create_all(
        bind=engine,
    )

    return Session(engine)


def test_get_or_create_manga_normalizes_shippuden():
    with create_test_session() as session:
        repository = MangaRepository(session)

        naruto = repository.get_or_create_manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        shippuden = repository.get_or_create_manga(
            title="Naruto Shippuden",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        assert naruto.id == shippuden.id
        assert naruto.title == "Naruto"

        manga_count = session.query(Manga).count()

        assert manga_count == 1


def test_episode_repository_assigns_anime_to_manga():
    with create_test_session() as session:
        manga_repository = MangaRepository(session)
        episode_repository = EpisodeRepository(session)

        manga = manga_repository.get_or_create_manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        naruto = episode_repository.get_or_create_anime(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga_id=manga.id,
        )

        shippuden = episode_repository.get_or_create_anime(
            title="Naruto Shippuden",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga_id=manga.id,
        )

        assert naruto.manga_id == manga.id
        assert shippuden.manga_id == manga.id


def test_save_chapter_metadata_for_anime_uses_shared_manga():
    with create_test_session() as session:
        manga_repository = MangaRepository(session)
        episode_repository = EpisodeRepository(session)

        manga = manga_repository.get_or_create_manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        naruto = episode_repository.get_or_create_anime(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga_id=manga.id,
        )

        shippuden = episode_repository.get_or_create_anime(
            title="Naruto Shippuden",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga_id=manga.id,
        )

        metadata = ChapterMetadataData(
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

        first = (
            manga_repository
            .save_chapter_metadata_for_anime(
                anime=naruto,
                metadata=metadata,
            )
        )

        second = (
            manga_repository
            .save_chapter_metadata_for_anime(
                anime=shippuden,
                metadata=metadata,
            )
        )

        assert first.id == second.id
        assert first.manga_id == manga.id
        assert session.query(
            ChapterMetadata
        ).count() == 1


def test_list_and_count_chapters_are_shared_by_anime():
    with create_test_session() as session:
        manga_repository = MangaRepository(session)
        episode_repository = EpisodeRepository(session)

        manga = manga_repository.get_or_create_manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        naruto = episode_repository.get_or_create_anime(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga_id=manga.id,
        )

        shippuden = episode_repository.get_or_create_anime(
            title="Naruto Shippuden",
            provider="fandom",
            base_url="https://naruto.fandom.com",
            manga_id=manga.id,
        )

        for chapter_number in (1, 245, 700):
            manga_repository.create_or_update_chapter_metadata(
                manga=manga,
                chapter_number=chapter_number,
            )

        naruto_chapters = (
            manga_repository
            .list_chapter_metadata_for_anime(
                naruto
            )
        )

        shippuden_chapters = (
            manga_repository
            .list_chapter_metadata_for_anime(
                shippuden
            )
        )

        assert [
            chapter.chapter_number
            for chapter in naruto_chapters
        ] == [1, 245, 700]

        assert [
            chapter.chapter_number
            for chapter in shippuden_chapters
        ] == [1, 245, 700]

        assert (
            manga_repository
            .count_chapters_for_anime(naruto)
            == 3
        )

        assert (
            manga_repository
            .count_chapters_for_anime(shippuden)
            == 3
        )


def test_search_chapter_metadata_orders_by_manga():
    with create_test_session() as session:
        repository = MangaRepository(session)

        naruto = repository.get_or_create_manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        one_piece = repository.get_or_create_manga(
            title="One Piece",
            provider="fandom",
            base_url="https://onepiece.fandom.com",
        )

        repository.create_or_update_chapter_metadata(
            manga=naruto,
            chapter_number=1,
            chapter_title="Naruto",
        )

        repository.create_or_update_chapter_metadata(
            manga=one_piece,
            chapter_number=1,
            chapter_title="Romance Dawn",
        )

        results = repository.search_chapter_metadata(
            "1"
        )

        assert len(results) == 2
        assert {
            result.manga.title
            for result in results
        } == {
            "Naruto",
            "One Piece",
        }


def test_chapter_metadata_has_no_anime_ownership():
    with create_test_session() as session:
        manga = Manga(
            title="Naruto",
            provider="fandom",
            base_url="https://naruto.fandom.com",
        )

        session.add(manga)
        session.commit()

        chapter = ChapterMetadata(
            manga_id=manga.id,
            chapter_number=245,
        )

        session.add(chapter)
        session.commit()

        stored = session.execute(
            select(ChapterMetadata)
        ).scalar_one()

        assert stored.manga_id == manga.id
        assert not hasattr(stored, "anime_id")
