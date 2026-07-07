from scraper.models.episode_metadata import EpisodeMetadata
from scraper.providers.fandom_metadata_provider import (
    FandomMetadataProvider,
)


class DummyEpisode:
    episode_number = 1


def test_fandom_metadata_provider_returns_episode_metadata():
    provider = FandomMetadataProvider()

    metadata = provider.get_episode_metadata(
        DummyEpisode()
    )

    assert isinstance(
        metadata,
        EpisodeMetadata,
    )

    assert metadata.title is None
    assert metadata.arc is None
    assert metadata.source_url is None