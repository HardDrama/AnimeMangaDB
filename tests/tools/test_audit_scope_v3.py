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
from tools import audit_scope_v3


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
    chapter_title: str | None = "Test Chapter",
    manga_arc: str | None = "Test Arc",
    source_url: str | None = (
        "https://example.com/chapter"
    ),
    last_updated: datetime | None = None,
) -> ChapterMetadata:
    chapter = ChapterMetadata(
        anime_id=anime.id,
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        manga_arc=manga_arc,
        source_url=source_url,
        last_updated=(
            last_updated
            if last_updated is not None
            else datetime.now()
        ),
    )

    session.add(chapter)
    session.commit()
    session.refresh(chapter)

    return chapter


def test_complete_dataset_passes(
    session: Session,
):
    anime = create_anime(session)

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=1,
    )

    report = audit_scope_v3.build_scope_v3_report(
        session=session,
        anime_title="Test Anime",
    )

    assert report["chapter_records"] == 1
    assert report["title_completion"] == 100.0
    assert report["arc_completion"] == 100.0
    assert (
        report["source_url_completion"]
        == 100.0
    )
    assert (
        report["last_updated_completion"]
        == 100.0
    )
    assert report["duplicate_chapters"] == 0
    assert report["metadata_audit_status"] == "PASS"
    assert report["coverage_audit_status"] == "NOT EVALUATED"
    assert report["dataset_status"] == "IN PROGRESS"


def test_empty_dataset_is_in_progress(
    session: Session,
):
    create_anime(session)

    report = audit_scope_v3.build_scope_v3_report(
        session=session,
        anime_title="Test Anime",
    )

    assert report["chapter_records"] == 0
    assert report["title_completion"] == 0.0
    assert report["arc_completion"] == 0.0
    assert report["audit_status"] == "IN PROGRESS"


def test_missing_title_is_reported(
    session: Session,
):
    anime = create_anime(session)

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=10,
        chapter_title=None,
    )

    report = audit_scope_v3.build_scope_v3_report(
        session=session,
        anime_title="Test Anime",
    )

    assert report["missing_titles"] == 1
    assert report["title_completion"] == 0.0
    assert report["missing_title_chapters"] == [10]
    assert report["audit_status"] == "IN PROGRESS"


def test_missing_arc_is_reported(
    session: Session,
):
    anime = create_anime(session)

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=20,
        manga_arc=None,
    )

    report = audit_scope_v3.build_scope_v3_report(
        session=session,
        anime_title="Test Anime",
    )

    assert report["missing_arcs"] == 1
    assert report["arc_completion"] == 0.0
    assert report["missing_arc_chapters"] == [20]
    assert report["audit_status"] == "IN PROGRESS"


def test_missing_source_url_is_reported(
    session: Session,
):
    anime = create_anime(session)

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=30,
        source_url=None,
    )

    report = audit_scope_v3.build_scope_v3_report(
        session=session,
        anime_title="Test Anime",
    )

    assert report["missing_source_urls"] == 1
    assert (
        report["source_url_completion"]
        == 0.0
    )
    assert (
        report["missing_source_url_chapters"]
        == [30]
    )
    assert report["audit_status"] == "IN PROGRESS"


def test_unknown_anime_raises(
    session: Session,
):
    with pytest.raises(
        ValueError,
        match='Anime not found: "Unknown Anime"',
    ):
        audit_scope_v3.build_scope_v3_report(
            session=session,
            anime_title="Unknown Anime",
        )


def test_duplicate_number_helper():
    duplicates = (
        audit_scope_v3
        .find_duplicate_chapter_numbers(
            [1, 2, 2, 3, 3, 3]
        )
    )

    assert duplicates == [2, 3]


def test_cli_writes_json_report(
    monkeypatch,
    tmp_path,
    session: Session,
    capsys,
):
    anime = create_anime(
        session,
        title="One Piece",
    )

    create_chapter(
        session=session,
        anime=anime,
        chapter_number=1,
        chapter_title="Romance Dawn",
        manga_arc="Romance Dawn Arc",
        source_url=(
            "https://onepiece.fandom.com/wiki/"
            "Chapter_1"
        ),
    )

    report_path = (
        tmp_path
        / "scope_v3_audit.json"
    )

    monkeypatch.setattr(
        audit_scope_v3,
        "SessionLocal",
        lambda: session,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "audit_scope_v3",
            "--anime",
            "One Piece",
            "--expected-start",
            "1",
            "--expected-end",
            "1",
            "--json-report",
            str(report_path),
        ],
    )

    audit_scope_v3.main()

    output = capsys.readouterr().out

    assert "Anime                 : One Piece" in output
    assert "Metadata Audit Status : PASS" in output
    assert report_path.exists()

    report = json.loads(
        report_path.read_text(
            encoding="utf-8"
        )
    )

    assert report["anime"] == "One Piece"
    assert report["chapter_records"] == 1
    assert report["audit_status"] == "PASS"

    assert report["coverage_audit_status"] == "PASS"
    assert report["dataset_status"] == "PASS"

def test_finds_missing_chapter_numbers():
    missing = (
        audit_scope_v3
        .find_missing_chapter_numbers(
            chapter_numbers=[
                1,
                2,
                4,
                6,
            ],
            expected_start=1,
            expected_end=6,
        )
    )

    assert missing == [3, 5]

def test_complete_expected_range_passes(
    session: Session,
):
    anime = create_anime(session)

    for chapter_number in range(
        1,
        6,
    ):
        create_chapter(
            session=session,
            anime=anime,
            chapter_number=chapter_number,
        )

    report = (
        audit_scope_v3
        .build_scope_v3_report(
            session=session,
            anime_title="Test Anime",
            expected_start=1,
            expected_end=5,
        )
    )

    assert (
        report["expected_chapter_count"]
        == 5
    )
    assert report["missing_chapters"] == 0
    assert (
        report["missing_chapter_numbers"]
        == []
    )
    assert (
        report["coverage_completion"]
        == 100.0
    )
    assert (
        report["coverage_audit_status"]
        == "PASS"
    )
    assert report["dataset_status"] == "PASS"

def test_missing_expected_chapters_are_reported(
    session: Session,
):
    anime = create_anime(session)

    for chapter_number in [
        1,
        2,
        4,
        5,
    ]:
        create_chapter(
            session=session,
            anime=anime,
            chapter_number=chapter_number,
        )

    report = (
        audit_scope_v3
        .build_scope_v3_report(
            session=session,
            anime_title="Test Anime",
            expected_start=1,
            expected_end=5,
        )
    )

    assert report["missing_chapters"] == 1
    assert (
        report["missing_chapter_numbers"]
        == [3]
    )
    assert (
        report["coverage_completion"]
        == 80.0
    )
    assert (
        report["coverage_audit_status"]
        == "IN PROGRESS"
    )
    assert (
        report["metadata_audit_status"]
        == "PASS"
    )
    assert (
        report["dataset_status"]
        == "IN PROGRESS"
    )

def test_expected_range_requires_both_bounds(
    session: Session,
):
    create_anime(session)

    with pytest.raises(
        ValueError,
        match=(
            "Expected end chapter is required"
        ),
    ):
        audit_scope_v3.build_scope_v3_report(
            session=session,
            anime_title="Test Anime",
            expected_start=1,
        )


def test_expected_range_rejects_reversed_bounds(
    session: Session,
):
    create_anime(session)

    with pytest.raises(
        ValueError,
        match=(
            "Expected start chapter must be "
            "less than or equal to expected end"
        ),
    ):
        audit_scope_v3.build_scope_v3_report(
            session=session,
            anime_title="Test Anime",
            expected_start=5,
            expected_end=1,
        )