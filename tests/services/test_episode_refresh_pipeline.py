from scraper.models.episode_metadata import EpisodeMetadata
from scraper.services.episode_refresh_pipeline import (
    EpisodeRefreshPipeline,
)


class FakeMetadataService:
    def get_metadata(self, episode):
        return EpisodeMetadata(
            title="Fresh Title",
            arc="Fresh Arc",
            source_url="https://example.com/episode/1",
        )


class DummyEpisode:
    episode_number = 1


def test_refresh_pipeline_uses_metadata_service():
    pipeline = EpisodeRefreshPipeline(
        metadata_service=FakeMetadataService()
    )

    result = pipeline.refresh_episode(DummyEpisode())

    assert result.metadata.title == "Fresh Title"
    assert result.metadata.arc == "Fresh Arc"
    assert result.metadata.source_url == (
        "https://example.com/episode/1"
    )
    assert result.success is True
    assert result.elapsed_seconds >= 0