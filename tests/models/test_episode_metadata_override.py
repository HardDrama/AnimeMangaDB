from scraper.models.episode_metadata_override import (
    EpisodeMetadataOverride,
)


def test_episode_metadata_override():
    override = EpisodeMetadataOverride(
        episode_number=240,
        arc="Example Arc",
        reason="Arc is missing from the live source metadata.",
    )

    assert override.episode_number == 240
    assert override.episode_title is None
    assert override.arc == "Example Arc"
    assert (
        override.reason
        == "Arc is missing from the live source metadata."
    )