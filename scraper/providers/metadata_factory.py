from scraper.providers.fandom_metadata_provider import (
    FandomMetadataProvider,
)


def create_metadata_provider(
    provider_name: str,
):
    if provider_name == "fandom":
        return FandomMetadataProvider()

    raise ValueError(
        f"Unsupported metadata provider: {provider_name}"
    )