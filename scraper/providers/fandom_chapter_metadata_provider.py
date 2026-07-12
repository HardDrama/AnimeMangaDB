from scraper.models.chapter_metadata import ChapterMetadata
from scraper.providers.chapter_metadata_provider import (
    ChapterMetadataProvider,
)
from scraper.models.provider_config import ProviderConfig


class FandomChapterMetadataProvider(
    ChapterMetadataProvider
):
    """
    Retrieves chapter metadata from a discovered Fandom URL.

    URL discovery and HTML extraction are separate
    responsibilities and will be implemented in later steps.
    """

    def __init__(
        self,
        config: ProviderConfig,
        browser_client=None,
        extractor=None,
    ):
        self.config = config
        self.browser_client = browser_client
        self.extractor = extractor

    def get_chapter_metadata(
        self,
        chapter_number: int,
        source_url: str,
    ) -> ChapterMetadata:
        html = None

        if self.browser_client is not None:
            html = self.browser_client.fetch(
                source_url
            )

        if (
            html is not None
            and self.extractor is not None
        ):
            return self.extractor.parse(
                html=html,
                chapter_number=chapter_number,
                source_url=source_url,
            )

        return ChapterMetadata(
            chapter_number=chapter_number,
            source_url=source_url,
        )