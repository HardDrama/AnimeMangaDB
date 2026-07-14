import pytest

from scraper.utils.metadata_exception_loader import (
    get_arc_not_applicable_episodes,
    get_manga_arc_not_applicable_chapters,
    is_arc_not_applicable,
    is_manga_arc_not_applicable,
    load_metadata_exceptions,
)


def test_load_naruto_metadata_exceptions():
    exceptions = load_metadata_exceptions(
        "configs/exceptions/naruto.json"
    )

    assert exceptions["anime"] == "Naruto"

    arc_not_applicable = (
        get_arc_not_applicable_episodes(
            exceptions
        )
    )

    assert len(arc_not_applicable) == 14
    assert 101 in arc_not_applicable
    assert 208 in arc_not_applicable


def test_arc_not_applicable_lookup():
    exceptions = load_metadata_exceptions(
        "configs/exceptions/naruto.json"
    )

    assert is_arc_not_applicable(
        101,
        exceptions,
    )

    assert not is_arc_not_applicable(
        1,
        exceptions,
    )


def test_missing_metadata_exception_file():
    with pytest.raises(FileNotFoundError):
        load_metadata_exceptions(
            "configs/exceptions/does_not_exist.json"
        )


def test_loads_naruto_chapter_metadata_exceptions():
    exceptions = load_metadata_exceptions(
        "configs/exceptions/naruto.json"
    )

    chapter_exceptions = (
        get_manga_arc_not_applicable_chapters(
            exceptions
        )
    )

    assert chapter_exceptions == {
        700
    }

    assert is_manga_arc_not_applicable(
        700,
        exceptions,
    )

    assert not is_manga_arc_not_applicable(
        699,
        exceptions,
    )


def test_missing_chapter_metadata_section_is_empty():
    exceptions = {
        "anime": "Test Anime",
        "arc_not_applicable": [
            1,
        ],
    }

    assert (
        get_manga_arc_not_applicable_chapters(
            exceptions
        )
        == set()
    )


def test_duplicate_chapter_exceptions_are_normalized():
    exceptions = {
        "chapter_metadata": {
            "manga_arc_not_applicable": [
                700,
                700,
                "700",
            ]
        }
    }

    assert (
        get_manga_arc_not_applicable_chapters(
            exceptions
        )
        == {
            700
        }
    )


def test_invalid_chapter_exception_value_raises():
    exceptions = {
        "chapter_metadata": {
            "manga_arc_not_applicable": [
                "not-a-number",
            ]
        }
    }

    with pytest.raises(
        ValueError,
        match=(
            "Chapter metadata exception values "
            "must be integers"
        ),
    ):
        get_manga_arc_not_applicable_chapters(
            exceptions
        )


def test_invalid_chapter_exception_container_raises():
    exceptions = {
        "chapter_metadata": {
            "manga_arc_not_applicable": 700,
        }
    }

    with pytest.raises(
        ValueError,
        match="must be a list",
    ):
        get_manga_arc_not_applicable_chapters(
            exceptions
        )