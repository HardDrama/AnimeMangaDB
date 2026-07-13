import json
import sys
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scraper.database.base import Base
from scraper.database.models import (
    Anime,
    ChapterMetadata,
)
from tools import export_scope_v3_samples


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
    title: str = "Test Anime",
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
) -> ChapterMetadata:
    chapter = ChapterMetadata(
        anime_id=anime.id,
        chapter_number=chapter_number,
        chapter_title=(
            f"Chapter {chapter_number} Title"
        ),
        manga_arc="Test Arc",
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


def test_parses_chapter_numbers():
    result = (
        export_scope_v3_samples
        .parse_chapter_numbers(
            "50, 1, 50, 100"
        )
    )

    assert result == [
        1,
        50,
        100,
    ]


def test_rejects_invalid_chapter_number():
    with pytest.raises(
        ValueError,
        match="Invalid chapter number",
    ):
        export_scope_v3_samples.parse_chapter_numbers(
            "1,invalid,50"
        )


def test_builds_sample_report(
    session: Session,
):
    anime = create_anime(session)

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=1,
    )

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=50,
    )

    report = (
        export_scope_v3_samples
        .build_sample_report(
            session=session,
            anime_title="Test Anime",
            chapter_numbers=[
                1,
                25,
                50,
            ],
        )
    )

    assert report["chapters_requested"] == 3
    assert report["records_found"] == 2
    assert report["missing_records"] == 1
    assert (
        report["missing_chapter_numbers"]
        == [25]
    )

    assert (
        report["results"][0][
            "chapter_title"
        ]
        == "Chapter 1 Title"
    )

    assert (
        report["results"][1][
            "record_found"
        ]
        is False
    )


def test_cli_writes_json_manifest(
    monkeypatch,
    tmp_path,
    session: Session,
):
    anime = create_anime(
        session,
        title="One Piece",
    )

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=1,
    )

    report_path = (
        tmp_path
        / "manual_validation.json"
    )

    monkeypatch.setattr(
        export_scope_v3_samples,
        "SessionLocal",
        lambda: session,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "export_scope_v3_samples",
            "--anime",
            "One Piece",
            "--chapters",
            "1",
            "--json-report",
            str(report_path),
        ],
    )

    export_scope_v3_samples.main()

    assert report_path.exists()

    report = json.loads(
        report_path.read_text(
            encoding="utf-8"
        )
    )

    assert report["anime"] == "One Piece"
    assert report["chapters_requested"] == 1
    assert report["records_found"] == 1
    assert (
        report["validation_status"]
        == "PENDING MANUAL REVIEW"
    )