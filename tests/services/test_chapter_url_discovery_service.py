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

def test_discovered_link_index_is_cached():
    html = """
    <html>
        <body>
            <a
                href="/wiki/Chapter_One"
                title="Example (chapter 1)"
            >
                Chapter 1
            </a>
            <a
                href="/wiki/Chapter_Two"
                title="Example (chapter 2)"
            >
                Chapter 2
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

    service.discover_url(1)
    service.discover_url(2)

    assert len(
        browser_client.requested_urls
    ) == 1

def test_discovery_uses_exact_chapter_number():
    html = """
    <html>
        <body>
            <a
                href="/wiki/Chapter_210"
                title="Lee's Secret!! (chapter 210)"
            >
                Chapter 210
            </a>

            <a
                href="/wiki/Chapter_2"
                title="The Second Chapter (chapter 2)"
            >
                Chapter 2
            </a>
        </body>
    </html>
    """

    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    service = ChapterUrlDiscoveryService(
        config=config,
        browser_client=FakeBrowserClient(
            html
        ),
    )

    url = service.discover_url(
        chapter_number=2
    )

    assert (
        url
        == "https://naruto.fandom.com/wiki/Chapter_2"
    )

def test_discovery_does_not_match_partial_number():
    html = """
    <html>
        <body>
            <a
                href="/wiki/Chapter_362"
                title="The Ultimate Art!! (chapter 362)"
            >
                Chapter 362
            </a>
        </body>
    </html>
    """

    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    service = ChapterUrlDiscoveryService(
        config=config,
        browser_client=FakeBrowserClient(
            html
        ),
    )

    assert (
        service.discover_url(
            chapter_number=3
        )
        is None
    )

def test_extracts_exact_chapter_numbers():
    assert (
        ChapterUrlDiscoveryService
        ._extract_chapter_numbers(
            "Example Title (chapter 210)"
        )
        == {210}
    )

def test_numbered_list_discovery_is_scoped_to_tankobon():
    html = """
    <html>
        <body>
            <h2>
                <span
                    class="mw-headline"
                    id="Tankōbon"
                >
                    Tankōbon
                </span>
            </h2>

            <h3>
                <span
                    class="mw-headline"
                    id="Part_I"
                >
                    Part I
                </span>
            </h3>

            <table>
                <tr>
                    <td>
                        <ul>
                            <li>
                                001.
                                <a href="/wiki/Naruto_Uzumaki!!_(chapter_1)">
                                    Naruto Uzumaki!!
                                </a>
                            </li>
                            <li>
                                002.
                                <a href="/wiki/Konohamaru!!">
                                    Konohamaru!!
                                </a>
                            </li>
                        </ul>
                    </td>
                </tr>
            </table>

            <h3>
                <span
                    class="mw-headline"
                    id="Part_II"
                >
                    Part II
                </span>
            </h3>

            <table>
                <tr>
                    <td>
                        <ul>
                            <li>
                                245.
                                <a href="/wiki/Homecoming!!">
                                    Homecoming!!
                                </a>
                            </li>
                        </ul>
                    </td>
                </tr>
            </table>

            <h2>
                <span
                    class="mw-headline"
                    id="Spin-offs"
                >
                    Spin-offs
                </span>
            </h2>

            <h3>
                <span
                    class="mw-headline"
                    id="Sasuke_Retsuden"
                >
                    Sasuke Retsuden
                </span>
            </h3>

            <table>
                <tr>
                    <td>
                        <ul>
                            <li>
                                001.
                                <a href="/wiki/Chapter_1_(Sasuke_Retsuden)">
                                    Chapter 1
                                </a>
                            </li>
                            <li>
                                002.
                                <a href="/wiki/Chapter_2_(Sasuke_Retsuden)">
                                    Chapter 2
                                </a>
                            </li>
                        </ul>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """

    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    service = ChapterUrlDiscoveryService(
        config=config,
        browser_client=FakeBrowserClient(html),
    )

    assert (
        service.discover_url(1)
        == (
            "https://naruto.fandom.com/wiki/"
            "Naruto_Uzumaki!!_(chapter_1)"
        )
    )

    assert (
        service.discover_url(2)
        == "https://naruto.fandom.com/wiki/Konohamaru!!"
    )

    assert (
        service.discover_url(245)
        == "https://naruto.fandom.com/wiki/Homecoming!!"
    )