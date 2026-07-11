import pytest

from scraper.utils.metadata_override_loader import (
    load_metadata_overrides,
)


def test_load_metadata_overrides():
    overrides = load_metadata_overrides(
        "tests/fixtures/metadata_overrides_sample.json"
    )

    assert len(overrides) == 2

    episode_240 = overrides[240]

    assert episode_240.episode_number == 240
    assert episode_240.episode_title is None
    assert episode_240.arc == "Example Arc"

    episode_267 = overrides[267]

    assert episode_267.episode_number == 267
    assert (
        episode_267.episode_title
        == "Example Episode Title"
    )
    assert episode_267.arc is None


def test_missing_metadata_override_file():
    with pytest.raises(FileNotFoundError):
        load_metadata_overrides(
            "tests/fixtures/does_not_exist.json"
        )