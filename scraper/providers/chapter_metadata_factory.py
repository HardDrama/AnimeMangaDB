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
    """
    Create a chapter metadata provider for a series.

    config_path is intentionally required so the factory
    never silently defaults to One Piece.
    """

    if provider_name == "fandom":
        config = load_provider_config(
            config_path
        )

        return FandomChapterMetadataProvider(
            config=config,
            browser_client=browser_client,
            extractor=extractor,
        )

    raise ValueError(
        "Unsupported chapter metadata provider: "
        f"{provider_name}"
    )