from scraper.crawlers.factory import create_episode_index_crawler
from scraper.crawlers.fandom_episode_index import FandomEpisodeIndexCrawler
from scraper.crawlers.naruto_episode_index import NarutoEpisodeIndexCrawler
from scraper.crawlers.naruto_shippuden_episode_index import (
    NarutoShippudenEpisodeIndexCrawler,
)
from scraper.utils.config_loader import load_provider_config


def test_factory_selects_naruto_shippuden_crawler():
    config = load_provider_config("configs/fandom/naruto_shippuden.json")

    crawler = create_episode_index_crawler(config)

    assert isinstance(crawler, NarutoShippudenEpisodeIndexCrawler)


def test_factory_preserves_naruto_crawler():
    config = load_provider_config("configs/fandom/naruto.json")

    crawler = create_episode_index_crawler(config)

    assert isinstance(crawler, NarutoEpisodeIndexCrawler)


def test_factory_preserves_one_piece_crawler():
    config = load_provider_config("configs/fandom/one_piece.json")

    crawler = create_episode_index_crawler(config)

    assert isinstance(crawler, FandomEpisodeIndexCrawler)
