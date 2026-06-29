from scraper.providers.fandom_provider import FandomProvider
from scraper.utils.config_loader import load_provider_config


def test_build_episode_url():

    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    provider = FandomProvider(config)

    url = provider.build_episode_url(1130)

    assert (
        url
        == "https://onepiece.fandom.com/wiki/Episode_1130"
    )