from scraper.models.episode_metadata import EpisodeMetadata
from scraper.providers.fandom_metadata_provider import (
    FandomMetadataProvider,
)


class FakeProvider:
    def __init__(self):
        self.called = False

    def build_episode_url(self, episode_number):
        self.called = True
        return f"https://example.com/{episode_number}"


class DummyEpisode:
    episode_number = 1


def test_fandom_metadata_provider_uses_provider():
    fake_provider = FakeProvider()

    provider = FandomMetadataProvider(
        provider=fake_provider,
    )

    metadata = provider.get_episode_metadata(
        DummyEpisode()
    )

    assert metadata.source_url == "https://example.com/1"

    assert fake_provider.called is True

    assert isinstance(
        metadata,
        EpisodeMetadata,
    )