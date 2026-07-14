from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scraper.database.base import Base
from scraper.database.models import (
    Anime,
    ChapterMetadata,
)
from scraper.repositories.episode_repository import (
    EpisodeRepository,
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(
        bind=engine,
    )

    with Session(engine) as database_session:
        yield database_session


def create_anime(
    session: Session,
    title: str,
) -> Anime:
    anime = Anime(
        title=title,
        provider="test",
        base_url="https://example.com",
    )

    session.add(anime)
    session.commit()
    session.refresh(anime)

    return anime


def create_chapter(
    session: Session,
    anime: Anime,
    chapter_number: int,
    chapter_title: str,
    manga_arc: str | None,
) -> ChapterMetadata:
    chapter = ChapterMetadata(
        anime_id=anime.id,
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        manga_arc=manga_arc,
        source_url=(
            "https://example.com/wiki/"
            f"Chapter_{chapter_number}"
        ),
        last_updated=datetime.now(),
    )

    session.add(chapter)
    session.commit()
    session.refresh(chapter)

    return chapter


def test_searches_chapter_metadata_by_title(
    session: Session,
):
    anime = create_anime(
        session,
        "One Piece",
    )

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=1,
        chapter_title="Romance Dawn",
        manga_arc="Romance Dawn Arc",
    )

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=2,
        chapter_title="They Call Him Straw Hat Luffy",
        manga_arc="Romance Dawn Arc",
    )

    repository = EpisodeRepository(
        session
    )

    results = (
        repository.search_chapter_metadata(
            "Straw Hat"
        )
    )

    assert [
        chapter.chapter_number
        for chapter in results
    ] == [2]


def test_searches_chapter_metadata_by_arc(
    session: Session,
):
    anime = create_anime(
        session,
        "Naruto",
    )

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=1,
        chapter_title="Naruto Uzumaki!!",
        manga_arc=(
            "Prologue — Land of Waves"
        ),
    )

    repository = EpisodeRepository(
        session
    )

    results = (
        repository.search_chapter_metadata(
            "Land of Waves"
        )
    )

    assert len(results) == 1
    assert results[0].chapter_number == 1


def test_searches_chapter_metadata_by_exact_number(
    session: Session,
):
    one_piece = create_anime(
        session,
        "One Piece",
    )

    naruto = create_anime(
        session,
        "Naruto",
    )

    create_chapter(
        session=session,
        anime=one_piece,
        chapter_number=50,
        chapter_title="A Parting of Ways",
        manga_arc="Baratie Arc",
    )

    create_chapter(
        session=session,
        anime=naruto,
        chapter_number=50,
        chapter_title="The Second Exam",
        manga_arc="Chūnin Exams",
    )

    repository = EpisodeRepository(
        session
    )

    results = (
        repository.search_chapter_metadata(
            "50"
        )
    )

    assert len(results) == 2

    assert {
        chapter.anime_id
        for chapter in results
    } == {
        one_piece.id,
        naruto.id,
    }


def test_search_preserves_null_manga_arc(
    session: Session,
):
    anime = create_anime(
        session,
        "Naruto",
    )

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=700,
        chapter_title="Naruto Uzumaki!!",
        manga_arc=None,
    )

    repository = EpisodeRepository(
        session
    )

    results = (
        repository.search_chapter_metadata(
            "700"
        )
    )

    assert len(results) == 1
    assert results[0].manga_arc is None


def test_chapter_metadata_search_returns_empty_list(
    session: Session,
):
    anime = create_anime(
        session,
        "One Piece",
    )

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=1,
        chapter_title="Romance Dawn",
        manga_arc="Romance Dawn Arc",
    )

    repository = EpisodeRepository(
        session
    )

    results = (
        repository.search_chapter_metadata(
            "No Matching Chapter"
        )
    )

    assert results == []