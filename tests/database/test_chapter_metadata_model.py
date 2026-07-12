from datetime import datetime

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from scraper.database.base import Base
from scraper.database.models import (
    Anime,
    ChapterMetadata,
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

    chapter = ChapterMetadata(
        anime_id=anime.id,
        chapter_number=1,
        chapter_title="Test Chapter",
        manga_arc="Test Arc",
        source_url="https://example.com/chapter/1",
        last_updated=datetime.now(),
    )

    session.add(chapter)
    session.commit()
    session.refresh(chapter)

    assert chapter.id is not None
    assert chapter.anime_id == anime.id
    assert chapter.chapter_number == 1
    assert chapter.chapter_title == "Test Chapter"
    assert chapter.manga_arc == "Test Arc"


def test_lookup_chapter_metadata(
    session: Session,
):
    anime = create_anime(session)

    chapter = ChapterMetadata(
        anime_id=anime.id,
        chapter_number=10,
    )

    session.add(chapter)
    session.commit()

    result = session.execute(
        select(ChapterMetadata)
        .where(
            ChapterMetadata.anime_id == anime.id,
            ChapterMetadata.chapter_number == 10,
        )
    ).scalar_one()

    assert result.chapter_number == 10
    assert result.anime.title == "Test Anime"


def test_update_chapter_metadata(
    session: Session,
):
    anime = create_anime(session)

    chapter = ChapterMetadata(
        anime_id=anime.id,
        chapter_number=20,
    )

    session.add(chapter)
    session.commit()

    chapter.chapter_title = "Updated Chapter"
    chapter.manga_arc = "Updated Arc"

    session.commit()
    session.refresh(chapter)

    assert chapter.chapter_title == "Updated Chapter"
    assert chapter.manga_arc == "Updated Arc"


def test_chapter_number_is_unique_per_anime(
    session: Session,
):
    anime = create_anime(session)

    session.add_all(
        [
            ChapterMetadata(
                anime_id=anime.id,
                chapter_number=30,
            ),
            ChapterMetadata(
                anime_id=anime.id,
                chapter_number=30,
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_same_chapter_number_allowed_for_different_anime(
    session: Session,
):
    first_anime = create_anime(session)

    second_anime = Anime(
        title="Second Test Anime",
        provider="test",
        base_url="https://example.org",
    )

    session.add(second_anime)
    session.commit()
    session.refresh(second_anime)

    session.add_all(
        [
            ChapterMetadata(
                anime_id=first_anime.id,
                chapter_number=1,
            ),
            ChapterMetadata(
                anime_id=second_anime.id,
                chapter_number=1,
            ),
        ]
    )

    session.commit()

    chapters = session.execute(
        select(ChapterMetadata)
        .where(
            ChapterMetadata.chapter_number == 1
        )
    ).scalars().all()

    assert len(chapters) == 2