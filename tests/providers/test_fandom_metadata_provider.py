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

    def fetch(self, url):
        self.called = True
        return "<html></html>"


class FakeExtractor:
    def __init__(self):
        self.called = False

    def parse(
        self,
        html,
        episode_number,
        source_url,
    ):
        self.called = True

        return type(
            "EpisodeData",
            (),
            {
                "episode_title": "Fresh Title",
                "arc": "Fresh Arc",
                "source_url": source_url,
            },
        )()


class DummyEpisode:
    episode_number = 1


def test_fandom_metadata_provider_uses_provider_browser_and_extractor():
    fake_provider = FakeProvider()
    fake_browser = FakeBrowserClient()
    fake_extractor = FakeExtractor()

    provider = FandomMetadataProvider(
        provider=fake_provider,
        browser_client=fake_browser,
        extractor=fake_extractor,
    )

    metadata = provider.get_episode_metadata(
        DummyEpisode()
    )

    assert fake_browser.called is True
    assert fake_extractor.called is True

    assert metadata.title == "Fresh Title"
    assert metadata.arc == "Fresh Arc"
    assert metadata.source_url == "https://example.com/1"

    assert isinstance(
        metadata,
        EpisodeMetadata,
    )