from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scraper.database.base import Base
from scraper.database.models import Anime
from scraper.repositories.episode_repository import (
    EpisodeRepository,
)
from scraper.models.chapter_metadata import (
    ChapterMetadata as ChapterMetadataData,
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as database_session:
        yield database_session


def create_anime(
    session: Session,
) -> Anime:
    anime = Anime(
        title="Test Anime",
        provider="test",
        base_url="https://example.com",
    )

    session.add(anime)
    session.commit()
    session.refresh(anime)

    return anime


def test_create_chapter_metadata(
    session: Session,
):
    anime = create_anime(session)
    repository = EpisodeRepository(session)

    chapter = (
        repository.create_or_update_chapter_metadata(
            anime=anime,
            chapter_number=1,
            chapter_title="Chapter One",
            manga_arc="Test Arc",
            source_url="https://example.com/chapter/1",
            last_updated=datetime.now(),
        )
    )

    assert chapter.id is not None
    assert chapter.anime_id == anime.id
    assert chapter.chapter_number == 1
    assert chapter.chapter_title == "Chapter One"
    assert chapter.manga_arc == "Test Arc"


def test_get_chapter_metadata(
    session: Session,
):
    anime = create_anime(session)
    repository = EpisodeRepository(session)

    repository.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=10,
        chapter_title="Chapter Ten",
    )

    chapter = repository.get_chapter_metadata(
        anime_id=anime.id,
        chapter_number=10,
    )

    assert chapter is not None
    assert chapter.chapter_title == "Chapter Ten"


def test_update_chapter_metadata(
    session: Session,
):
    anime = create_anime(session)
    repository = EpisodeRepository(session)

    repository.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=20,
        chapter_title="Old Title",
    )

    updated = (
        repository.create_or_update_chapter_metadata(
            anime=anime,
            chapter_number=20,
            chapter_title="New Title",
            manga_arc="Updated Arc",
        )
    )

    assert updated.chapter_title == "New Title"
    assert updated.manga_arc == "Updated Arc"


def test_list_chapter_metadata(
    session: Session,
):
    anime = create_anime(session)
    repository = EpisodeRepository(session)

    repository.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=2,
    )
    repository.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=1,
    )

    chapters = repository.list_chapter_metadata(
        anime_id=anime.id
    )

    assert [
        chapter.chapter_number
        for chapter in chapters
    ] == [1, 2]

def test_count_chapters_for_anime(
    session: Session,
):
    anime = create_anime(session)
    repository = EpisodeRepository(session)

    repository.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=1,
        chapter_title="Chapter One",
        manga_arc="Test Arc",
        source_url=(
            "https://example.com/chapter/1"
        ),
        last_updated=datetime.now(),
    )

    repository.create_or_update_chapter_metadata(
        anime=anime,
        chapter_number=2,
        chapter_title="Chapter Two",
        manga_arc="Test Arc",
        source_url=(
            "https://example.com/chapter/2"
        ),
        last_updated=datetime.now(),
    )

    assert (
        repository.count_chapters_for_anime(
            anime.id
        )
        == 2
    )

def test_save_chapter_metadata_domain_model(
    session: Session,
):
    anime = create_anime(session)
    repository = EpisodeRepository(session)

    metadata = ChapterMetadataData(
        chapter_number=30,
        chapter_title="Domain Model Chapter",
        manga_arc="Domain Model Arc",
        source_url="https://example.com/chapter/30",
        last_updated=datetime.now(),
    )

    chapter = repository.save_chapter_metadata(
        anime=anime,
        metadata=metadata,
    )

    assert chapter.chapter_number == 30
    assert chapter.chapter_title == "Domain Model Chapter"
    assert chapter.manga_arc == "Domain Model Arc"

def test_get_anime_by_title(
    session: Session,
):
    anime = create_anime(session)
    repository = EpisodeRepository(session)

    result = repository.get_anime_by_title(
        "Test Anime"
    )

    assert result is not None
    assert result.id == anime.id
    assert result.title == "Test Anime"


def test_get_missing_anime_by_title(
    session: Session,
):
    repository = EpisodeRepository(session)

    result = repository.get_anime_by_title(
        "Does Not Exist"
    )

    assert result is None