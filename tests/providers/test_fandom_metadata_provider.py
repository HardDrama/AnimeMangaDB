from scraper.models.episode_metadata import EpisodeMetadata
from scraper.providers.fandom_metadata_provider import (
    FandomMetadataProvider,
)


class FakeProvider:
    def build_episode_url(self, episode_number):
        return f"https://example.com/{episode_number}"


class FakeBrowserClient:
    def __init__(self):
        self.called = False

    def fetch_html(self, url):
        self.called = True
        return "<html></html>"


class DummyEpisode:
    episode_number = 1


def test_fandom_metadata_provider_uses_provider_and_browser():
    fake_provider = FakeProvider()
    fake_browser = FakeBrowserClient()

    provider = FandomMetadataProvider(
        provider=fake_provider,
        browser_client=fake_browser,
    )

    metadata = provider.get_episode_metadata(
        DummyEpisode()
    )

    assert metadata.source_url == "https://example.com/1"
    assert fake_browser.called is True

    assert isinstance(
        metadata,
        EpisodeMetadata,
    )