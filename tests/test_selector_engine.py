from pathlib import Path

from scraper.core.parser import HtmlParser
from scraper.core.selector_engine import SelectorEngine
from scraper.utils.config_loader import load_provider_config


def test_selector_engine_title():

    html = Path(
        "tests/fixtures/fandom_sample.html"
    ).read_text(
        encoding="utf-8"
    )

    soup = HtmlParser().parse(html)

    config = load_provider_config(
        "configs/fandom/one_piece.json"
    )

    engine = SelectorEngine(soup, config)

    assert engine.get_text("title") == "Episode 1130"