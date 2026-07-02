from scraper.utils.config_loader import load_provider_config


def test_provider_config_loads_scraper_settings():
    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    assert config.scraper.max_episodes == 5
    assert config.scraper.start_episode == 11
    assert config.scraper.end_episode == 15
    assert config.scraper.full_crawl is False