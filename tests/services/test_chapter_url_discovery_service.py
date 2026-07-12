import pytest

from scraper.services.chapter_url_discovery_service import (
    ChapterUrlDiscoveryService,
)
from scraper.utils.config_loader import (
    load_provider_config,
)


class FakeBrowserClient:
    def __init__(
        self,
        html: str,
    ):
        self.html = html
        self.requested_urls = []

    def fetch(
        self,
        source_url: str,
    ) -> str:
        self.requested_urls.append(
            source_url
        )

        return self.html


def test_builds_numbered_one_piece_url():
    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    service = ChapterUrlDiscoveryService(
        config=config
    )

    url = service.discover_url(
        chapter_number=50
    )

    assert (
        url
        == "https://onepiece.fandom.com/wiki/Chapter_50"
    )


def test_discovers_naruto_chapter_link():
    html = """
    <html>
        <body>
            <a
                href="/wiki/I_Will%E2%80%A6!!"
                title="I Will…!! (chapter 50)"
            >
                Chapter 50
            </a>
        </body>
    </html>
    """

    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    browser_client = FakeBrowserClient(
        html
    )

    service = ChapterUrlDiscoveryService(
        config=config,
        browser_client=browser_client,
    )

    url = service.discover_url(
        chapter_number=50
    )

    assert (
        url
        == "https://naruto.fandom.com/wiki/I_Will%E2%80%A6!!"
    )

    assert browser_client.requested_urls == [
        "https://naruto.fandom.com/wiki/List_of_Volumes"
    ]


def test_discovered_link_strategy_requires_browser():
    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    service = ChapterUrlDiscoveryService(
        config=config
    )

    assert (
        service.discover_url(
            chapter_number=50
        )
        is None
    )


def test_returns_none_when_chapter_link_missing():
    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    service = ChapterUrlDiscoveryService(
        config=config,
        browser_client=FakeBrowserClient(
            "<html><body></body></html>"
        ),
    )

    assert (
        service.discover_url(
            chapter_number=999999
        )
        is None
    )


def test_rejects_unsupported_strategy():
    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    config.chapter_metadata.url_strategy = (
        "unsupported"
    )

    service = ChapterUrlDiscoveryService(
        config=config
    )

    with pytest.raises(
        ValueError,
        match=(
            "Unsupported chapter URL strategy"
        ),
    ):
        service.discover_url(
            chapter_number=1
        )