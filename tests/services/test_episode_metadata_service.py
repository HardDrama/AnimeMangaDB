from scraper.models.episode_metadata import EpisodeMetadata
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)


class FakeMetadataProvider:
    def get_episode_metadata(self, episode):
        return EpisodeMetadata(
            title="Fresh Title",
            arc="Fresh Arc",
            source_url="https://example.com/episode/1",
        )


class DummyEpisode:
    episode_number = 1


def test_returns_episode_metadata():
    service = EpisodeMetadataService(
        metadata_provider=FakeMetadataProvider()
    )

    metadata = service.get_metadata(
        DummyEpisode()
    )

    assert isinstance(
        metadata,
        EpisodeMetadata,
    )

    assert metadata.title == "Fresh Title"
    assert metadata.arc == "Fresh Arc"
    assert metadata.source_url == "https://example.com/episode/1"