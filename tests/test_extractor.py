from pathlib import Path

from scraper.extractors.example_extractor import ExampleExtractor


def test_example_extractor():

    html = Path(
        "tests/fixtures/example.html"
    ).read_text(
        encoding="utf-8"
    )

    extractor = ExampleExtractor()

    episode = extractor.parse_episode(html)

    assert episode.anime_title == "Example Domain"