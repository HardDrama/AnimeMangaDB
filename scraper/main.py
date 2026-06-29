from pathlib import Path

from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.utils.config_loader import load_provider_config


def main():

    html = Path(
        "tests/fixtures/one_piece_episode_1130.html"
    ).read_text(
        encoding="utf-8"
    )

    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    extractor = FandomExtractor(config)

    episode = extractor.parse(html)

    print(episode.model_dump_json(indent=4))


if __name__ == "__main__":
    main()