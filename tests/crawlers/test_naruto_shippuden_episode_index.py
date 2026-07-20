from scraper.crawlers.naruto_shippuden_episode_index import (
    NarutoShippudenEpisodeIndexCrawler,
)


def test_crawler_initializes():
    crawler = NarutoShippudenEpisodeIndexCrawler(
        "https://naruto.fandom.com",
    )

    assert crawler.base_url == "https://naruto.fandom.com"


def test_returns_episode_reference_list_type():
    crawler = NarutoShippudenEpisodeIndexCrawler(
        "https://naruto.fandom.com",
    )

    assert hasattr(crawler, "get_episode_list")