from scraper.crawlers.naruto_episode_index import NarutoEpisodeIndexCrawler


def test_naruto_episode_index_uses_title_based_urls():
    crawler = NarutoEpisodeIndexCrawler(
        "https://naruto.fandom.com"
    )

    episodes = crawler.get_episode_list()

    assert episodes[0] == (
        1,
        "https://naruto.fandom.com/wiki/Enter:_Naruto_Uzumaki!",
    )