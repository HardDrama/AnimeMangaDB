from sqlalchemy.orm import Session

from scraper.crawlers.factory import create_episode_index_crawler
from scraper.extractors.factory import create_extractor
from scraper.models import ProviderConfig
from scraper.providers.factory import create_provider
from scraper.repositories.factory import create_episode_repository


class ScraperServices:
    def __init__(
        self,
        config: ProviderConfig,
        session: Session,
    ):
        self.provider = create_provider(config)
        self.extractor = create_extractor(config)
        self.crawler = create_episode_index_crawler(config)
        self.repository = create_episode_repository(session)