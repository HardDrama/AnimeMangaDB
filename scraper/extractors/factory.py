from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.models import ProviderConfig


def create_extractor(
    config: ProviderConfig,
) -> FandomExtractor:
    return FandomExtractor(config)