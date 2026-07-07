from scraper.models.episode_metadata import EpisodeMetadata
from scraper.providers.fandom_metadata_provider import (
    FandomMetadataProvider,
)


class RecordingProvider:
    def __init__(self):
        self.calls = []

    def build_episode_url(self, episode_number):
        self.calls.append(("url", episode_number))
        return f"https://example.com/{episode_number}"


class RecordingBrowser:
    def __init__(self):
        self.calls = []

    def fetch_html(self, url):
        self.calls.append(("fetch", url))
        return "<html>fake page</html>"


class RecordingExtractor:
    def __init__(self):
        self.calls = []

    def parse(
        self,
        html,
        episode_number,
        source_url,
    ):
        self.calls.append(
            (
                "parse",
                episode_number,
                source_url,
            )
        )

        return type(
            "EpisodeData",
            (),
            {
                "episode_title": "Episode Title",
                "arc": "Egghead",
                "source_url": source_url,
            },
        )()


class DummyEpisode:
    episode_number = 1130


def test_provider_orchestrates_dependencies():
    provider = RecordingProvider()
    browser = RecordingBrowser()
    extractor = RecordingExtractor()

    metadata_provider = FandomMetadataProvider(
        provider=provider,
        browser_client=browser,
        extractor=extractor,
    )

    metadata = metadata_provider.get_episode_metadata(
        DummyEpisode()
    )

    assert provider.calls == [
        ("url", 1130)
    ]

    assert browser.calls == [
        ("fetch", "https://example.com/1130")
    ]

    assert extractor.calls == [
        (
            "parse",
            1130,
            "https://example.com/1130",
        )
    ]

    assert isinstance(metadata, EpisodeMetadata)
    assert metadata.title == "Episode Title"
    assert metadata.arc == "Egghead"