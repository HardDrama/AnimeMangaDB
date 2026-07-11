from scraper.utils.metadata_override_loader import (
    load_metadata_overrides,
)


def test_load_one_piece_metadata_overrides():
    overrides = load_metadata_overrides(
        "configs/overrides/one_piece.json"
    )

    assert len(overrides) == 7

    expected_arcs = {
        240: "Water 7 Arc",
        267: "Enies Lobby Arc",
        663: "Dressrosa Arc",
        864: "Whole Cake Island Arc",
        1065: "Wano Country Arc",
        1167: "Elbaph Arc",
        1168: "Elbaph Arc",
    }

    for episode_number, expected_arc in expected_arcs.items():
        override = overrides[episode_number]

        assert override.episode_number == episode_number
        assert override.arc == expected_arc
        assert override.episode_title is None
        assert override.reason is not None