from scraper.utils.metadata_override_loader import (
    load_metadata_overrides,
)


def test_load_one_piece_metadata_overrides():
    overrides = load_metadata_overrides(
        "configs/overrides/one_piece.json"
    )

    assert isinstance(overrides, dict)