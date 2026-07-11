import pytest

from scraper.utils.metadata_exception_loader import (
    get_arc_not_applicable_episodes,
    is_arc_not_applicable,
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