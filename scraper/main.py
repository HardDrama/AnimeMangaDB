from pathlib import Path

from scraper.extractors.fandom_extractor import FandomExtractor
from scraper.providers.fandom_provider import FandomProvider
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

    provider = FandomProvider(config)

    extractor = FandomExtractor(config)

    episode = extractor.parse(
        html=html,
        episode_number=1130,
        source_url=provider.build_episode_url(1130),
    )

    print(episode.model_dump_json(indent=4))


if __name__ == "__main__":
    main()

from scraper.core.text_parser import extract_all_numbers

print(extract_all_numbers("Chapter 1096"))
print(extract_all_numbers("Chapters 1096-1098"))
print(extract_all_numbers("Nothing here"))