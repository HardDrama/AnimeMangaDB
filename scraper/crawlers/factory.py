from scraper.crawlers.base_episode_index import BaseEpisodeIndexCrawler
from scraper.crawlers.fandom_episode_index import FandomEpisodeIndexCrawler
from scraper.crawlers.naruto_episode_index import NarutoEpisodeIndexCrawler
from scraper.models import ProviderConfig


def create_episode_index_crawler(
    config: ProviderConfig,
) -> BaseEpisodeIndexCrawler:
    if config.series == "Naruto":
        return NarutoEpisodeIndexCrawler(config.base_url)

    return FandomEpisodeIndexCrawler(config.base_url)