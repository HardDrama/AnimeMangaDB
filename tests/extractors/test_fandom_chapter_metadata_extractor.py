from pathlib import Path

from scraper.extractors.fandom_chapter_metadata_extractor import (
    FandomChapterMetadataExtractor,
)
from scraper.utils.config_loader import load_provider_config


FIXTURE_DIR = Path("tests/fixtures")


def read_fixture(
    filename: str,
) -> str:
    return (
        FIXTURE_DIR
        .joinpath(filename)
        .read_text(encoding="utf-8")
    )


def test_extracts_one_piece_chapter_1():
    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    assert config.chapter_selectors is not None

    extractor = FandomChapterMetadataExtractor(
        selectors=config.chapter_selectors
    )

    metadata = extractor.parse(
        html=read_fixture(
            "one_piece_chapter_1.html"
        ),
        chapter_number=1,
        source_url=(
            "https://onepiece.fandom.com/wiki/Chapter_1"
        ),
    )

    assert metadata.chapter_number == 1
    assert (
        metadata.chapter_title
        == "Romance Dawn —The Dawn of the Adventure—"
    )
    assert metadata.manga_arc == "Romance Dawn Arc"
    assert metadata.last_updated is not None


def test_extracts_one_piece_chapter_50():
    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    assert config.chapter_selectors is not None

    extractor = FandomChapterMetadataExtractor(
        selectors=config.chapter_selectors
    )

    metadata = extractor.parse(
        html=read_fixture(
            "one_piece_chapter_50.html"
        ),
        chapter_number=50,
        source_url=(
            "https://onepiece.fandom.com/wiki/Chapter_50"
        ),
    )

    assert metadata.chapter_number == 50
    assert metadata.chapter_title is not None
    assert metadata.manga_arc == "Baratie Arc"


def test_extracts_naruto_chapter_1():
    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    assert config.chapter_selectors is not None

    extractor = FandomChapterMetadataExtractor(
        selectors=config.chapter_selectors
    )

    metadata = extractor.parse(
        html=read_fixture(
            "naruto_chapter_1.html"
        ),
        chapter_number=1,
        source_url=(
            "https://naruto.fandom.com/wiki/"
            "Naruto_Uzumaki!!_(chapter_1)"
        ),
    )

    assert metadata.chapter_number == 1
    assert metadata.chapter_title == "Naruto Uzumaki!!"
    assert (
        metadata.manga_arc
        == "Prologue — Land of Waves"
    )


def test_extracts_naruto_chapter_50():
    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    assert config.chapter_selectors is not None

    extractor = FandomChapterMetadataExtractor(
        selectors=config.chapter_selectors
    )

    metadata = extractor.parse(
        html=read_fixture(
            "naruto_chapter_50.html"
        ),
        chapter_number=50,
        source_url=(
            "https://naruto.fandom.com/wiki/"
            "I_Will%E2%80%A6!!"
        ),
    )

    assert metadata.chapter_number == 50
    assert metadata.chapter_title == "I Will…!!"
    assert metadata.manga_arc == "Chūnin Exams (Arc)"


def test_missing_metadata_remains_none():
    config = load_provider_config(
        "configs/fandom/naruto.json"
    )

    assert config.chapter_selectors is not None

    extractor = FandomChapterMetadataExtractor(
        selectors=config.chapter_selectors
    )

    metadata = extractor.parse(
        html="<html><body></body></html>",
        chapter_number=700,
        source_url="https://example.com/chapter/700",
    )

    assert metadata.chapter_title is None
    assert metadata.manga_arc is None