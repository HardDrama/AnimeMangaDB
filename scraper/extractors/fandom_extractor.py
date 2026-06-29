from scraper.core.parser import HtmlParser
from scraper.core.selector_engine import SelectorEngine
from scraper.core.extract import required_text
from scraper.models import EpisodeData, ProviderConfig


class FandomExtractor:

    def __init__(self, config: ProviderConfig):
        self.config = config

    def parse(self, html: str) -> EpisodeData:

        soup = HtmlParser().parse(html)

        engine = SelectorEngine(
            soup,
            self.config,
        )

        title = required_text(
            engine,
            "title",
        )

        return EpisodeData(
            anime_title=self.config.series,
            episode_number=0,
            episode_title=title,
            manga_start=None,
            manga_end=None,
            arc=None,
            source_url=self.config.base_url
        )