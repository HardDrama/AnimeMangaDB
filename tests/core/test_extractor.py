from pathlib import Path

from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.utils.config_loader import load_provider_config


def test_fandom_extractor_parses_episode_fixture():
    html = Path(
        "tests/fixtures/one_piece_episode_1130.html"
    ).read_text(encoding="utf-8")

    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    extractor = FandomExtractor(config)

    episode = extractor.parse(
        html=html,
        episode_number=1130,
        source_url="https://onepiece.fandom.com/wiki/Episode_1130",
    )

    assert episode.anime_title == "One Piece"
    assert episode.episode_number == 1130
    assert episode.episode_title == "Episode 1130"
    assert episode.manga_start == 1096
    assert episode.manga_end == 1096
    assert episode.arc == "Egghead Arc"