from scraper.models.episode_metadata import EpisodeMetadata
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)


class DummyEpisode:
    episode_number = 1


def test_returns_episode_metadata():
    service = EpisodeMetadataService()

    metadata = service.get_metadata(
        DummyEpisode()
    )

    assert isinstance(
        metadata,
        EpisodeMetadata,
    )

    assert metadata.title is None
    assert metadata.arc is None
    assert metadata.source_url is None