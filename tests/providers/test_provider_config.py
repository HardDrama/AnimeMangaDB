from scraper.utils.config_loader import load_provider_config


def test_provider_config_loads_scraper_settings():
    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    assert config.scraper.max_episodes == 5
    assert config.scraper.start_episode == 11
    assert config.scraper.end_episode == 15
    assert config.scraper.full_crawl is False

def test_provider_config_loads_naruto_config():
    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    assert config.series == "Naruto"
    assert config.base_url == "https://naruto.fandom.com"
    assert config.episode_path == "/wiki/Episode_{episode}"
    assert config.scraper.max_episodes == 5
    assert config.scraper.full_crawl is False
    assert config.scraper.config_path == "configs/fandom/naruto.json"