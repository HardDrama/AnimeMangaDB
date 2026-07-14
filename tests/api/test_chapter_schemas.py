from datetime import datetime

import pytest
from pydantic import ValidationError

from scraper.api.schemas import (
    ChapterMetadataResponse,
)
from scraper.database.models import (
    ChapterMetadata,
)


def test_chapter_response_with_complete_metadata():
    timestamp = datetime(
        2026,
        7,
        14,
        12,
        30,
        0,
    )

    response = ChapterMetadataResponse(
        chapter_number=1,
        chapter_title="Romance Dawn",
        manga_arc="Romance Dawn Arc",
        source_url=(
            "https://onepiece.fandom.com/wiki/"
            "Chapter_1"
        ),
        last_updated=timestamp,
    )

    assert response.chapter_number == 1
    assert response.chapter_title == "Romance Dawn"
    assert response.manga_arc == "Romance Dawn Arc"
    assert (
        response.source_url
        == (
            "https://onepiece.fandom.com/wiki/"
            "Chapter_1"
        )
    )
    assert response.last_updated == timestamp


def test_chapter_response_allows_null_manga_arc():
    response = ChapterMetadataResponse(
        chapter_number=700,
        chapter_title="Naruto Uzumaki!!",
        manga_arc=None,
        source_url=(
            "https://naruto.fandom.com/wiki/"
            "Naruto_Uzumaki!!_(chapter_700)"
        ),
        last_updated=datetime.now(),
    )

    assert response.chapter_number == 700
    assert response.manga_arc is None


def test_chapter_response_serializes_from_orm_model():
    timestamp = datetime(
        2026,
        7,
        14,
        13,
        0,
        0,
    )

    chapter = ChapterMetadata(
        id=10,
        anime_id=2,
        chapter_number=700,
        chapter_title="Naruto Uzumaki!!",
        manga_arc=None,
        source_url=(
            "https://naruto.fandom.com/wiki/"
            "Naruto_Uzumaki!!_(chapter_700)"
        ),
        last_updated=timestamp,
    )

    response = (
        ChapterMetadataResponse
        .model_validate(
            chapter
        )
    )

    assert response.chapter_number == 700
    assert response.chapter_title == "Naruto Uzumaki!!"
    assert response.manga_arc is None
    assert response.last_updated == timestamp


def test_chapter_response_serializes_datetime_to_json():
    response = ChapterMetadataResponse(
        chapter_number=1,
        chapter_title="Romance Dawn",
        manga_arc="Romance Dawn Arc",
        source_url=(
            "https://onepiece.fandom.com/wiki/"
            "Chapter_1"
        ),
        last_updated=datetime(
            2026,
            7,
            14,
            14,
            15,
            30,
        ),
    )

    payload = response.model_dump(
        mode="json"
    )

    assert (
        payload["last_updated"]
        == "2026-07-14T14:15:30"
    )


def test_chapter_response_requires_certified_fields():
    with pytest.raises(
        ValidationError,
    ):
        ChapterMetadataResponse(
            chapter_number=1,
            manga_arc="Romance Dawn Arc",
        )