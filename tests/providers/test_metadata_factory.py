import pytest

from scraper.providers.fandom_metadata_provider import (
    FandomMetadataProvider,
)
from scraper.providers.metadata_factory import (
    create_metadata_provider,
)


def test_create_fandom_metadata_provider():
    provider = create_metadata_provider(
        "fandom"
    )

    assert isinstance(
        provider,
        FandomMetadataProvider,
    )


def test_unknown_metadata_provider():
    with pytest.raises(ValueError):
        create_metadata_provider(
            "unknown"
        )