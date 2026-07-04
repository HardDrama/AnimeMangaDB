from scraper.models import ProviderConfig
from scraper.providers.base_provider import BaseProvider
from scraper.providers.fandom_provider import FandomProvider


def create_provider(
    config: ProviderConfig,
) -> BaseProvider:
    return FandomProvider(config)