from scraper.core.browser_client import BrowserClient
from scraper.extractors.fandom_chapter_metadata_extractor import (
    FandomChapterMetadataExtractor,
)
from scraper.providers.fandom_chapter_metadata_provider import (
    FandomChapterMetadataProvider,
)
from scraper.utils.config_loader import load_provider_config


def create_chapter_metadata_provider(
    provider_name: str,
    config_path: str,
    browser_client=None,
    extractor=None,
):
    if provider_name == "fandom":
        config = load_provider_config(
            config_path
        )

        configured_browser = (
            browser_client
            if browser_client is not None
            else BrowserClient()
        )

        configured_extractor = extractor

        if configured_extractor is None:
            if config.chapter_selectors is None:
                raise ValueError(
                    "Chapter selectors are not configured."
                )

            configured_extractor = (
                FandomChapterMetadataExtractor(
                    selectors=config.chapter_selectors
                )
            )

        return FandomChapterMetadataProvider(
            config=config,
            browser_client=configured_browser,
            extractor=configured_extractor,
        )

    raise ValueError(
        "Unsupported chapter metadata provider: "
        f"{provider_name}"
    )