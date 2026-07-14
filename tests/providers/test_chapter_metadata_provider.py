import pytest

from scraper.models.chapter_metadata import ChapterMetadata
from scraper.providers.chapter_metadata_factory import (
    create_chapter_metadata_provider,
)
from scraper.providers.fandom_chapter_metadata_provider import (
    FandomChapterMetadataProvider,
)


class FakeBrowserClient:
    def fetch(
        self,
        source_url: str,
    ) -> str:
        return "<html>chapter</html>"


class FakeChapterExtractor:
    def parse(
        self,
        html: str,
        chapter_number: int,
        source_url: str,
    ) -> ChapterMetadata:
        return ChapterMetadata(
            chapter_number=chapter_number,
            chapter_title="Test Chapter",
            manga_arc="Test Manga Arc",
            source_url=source_url,
        )


def test_fandom_provider_returns_partial_metadata():
    provider = FandomChapterMetadataProvider(
        config={
            "series": "Test Anime",
        }
    )

    metadata = provider.get_chapter_metadata(
        chapter_number=1,
        source_url="https://example.com/chapter/1",
    )

    assert metadata.chapter_number == 1
    assert metadata.chapter_title is None
    assert metadata.manga_arc is None
    assert (
        metadata.source_url
        == "https://example.com/chapter/1"
    )


def test_fandom_provider_uses_browser_and_extractor():
    provider = FandomChapterMetadataProvider(
        config={
            "series": "Test Anime",
        },
        browser_client=FakeBrowserClient(),
        extractor=FakeChapterExtractor(),
    )

    metadata = provider.get_chapter_metadata(
        chapter_number=50,
        source_url="https://example.com/chapter/50",
    )

    assert metadata.chapter_number == 50
    assert metadata.chapter_title == "Test Chapter"
    assert metadata.manga_arc == "Test Manga Arc"


def test_factory_loads_one_piece_configuration():
    provider = create_chapter_metadata_provider(
        provider_name="fandom",
        config_path="configs/fandom/one_piece.json",
    )

    assert isinstance(
        provider,
        FandomChapterMetadataProvider,
    )
    assert provider.config.series == "One Piece"
    assert provider.config.chapter_metadata is not None
    assert (
        provider.config.chapter_metadata.url_strategy
        == "numbered"
    )
    assert (
        provider.config.chapter_metadata.chapter_path
        == "/wiki/Chapter_{chapter}"
    )
    assert provider.config.chapter_selectors is not None
    assert provider.browser_client is not None
    assert provider.extractor is not None


def test_factory_loads_naruto_configuration():
    provider = create_chapter_metadata_provider(
        provider_name="fandom",
        config_path="configs/fandom/naruto.json",
    )

    assert (
        provider.config.chapter_metadata.index_subsection_ids
        == [
            "Part_I",
            "Part_II",
        ]
    )

    assert provider.config.series == "Naruto"
    assert provider.config.chapter_metadata is not None
    assert (
        provider.config.chapter_metadata.url_strategy
        == "numbered_list_items"
    )
    assert (
        provider.config.chapter_metadata.index_section_id
        == "Tankōbon"
    )
    assert (
        provider.config.chapter_metadata.chapter_path
        is None
    )
    assert provider.config.chapter_selectors is not None
    assert provider.browser_client is not None
    assert provider.extractor is not None


def test_factory_rejects_unsupported_provider():
    with pytest.raises(
        ValueError,
        match=(
            "Unsupported chapter metadata provider"
        ),
    ):
        create_chapter_metadata_provider(
            provider_name="unsupported",
            config_path=(
                "configs/fandom/one_piece.json"
            ),
        )