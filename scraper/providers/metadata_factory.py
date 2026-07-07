from scraper.core.browser_client import BrowserClient
from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.providers.fandom_metadata_provider import (
    FandomMetadataProvider,
)
from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config


def create_metadata_provider(
    provider_name: str,
    config_path: str = "configs/fandom/one_piece.json",
):
    if provider_name == "fandom":
        config = load_provider_config(config_path)

        return FandomMetadataProvider(
            provider=FandomProvider(config),
            browser_client=BrowserClient(),
            extractor=FandomExtractor(config),
        )

    raise ValueError(
        f"Unsupported metadata provider: {provider_name}"
    )