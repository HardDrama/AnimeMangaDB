from scraper.core.parser import HtmlParser
from scraper.core.selector_engine import SelectorEngine
from scraper.core.extract import required_text
from scraper.models import EpisodeData, ProviderConfig
from scraper.core.text_parser import extract_first_number


class FandomExtractor:

    def __init__(self, config: ProviderConfig):
        self.config = config

    def parse(
        self,
        html: str,
        episode_number: int,
        source_url: str,
    ) -> EpisodeData:

        # 1. Parse HTML
        soup = HtmlParser().parse(html)

        # 2. Create selector engine
        engine = SelectorEngine(soup, self.config)

        # 3. Extract fields
        title = required_text(engine, "title")

        chapter_text = required_text(engine, "chapter")

        # 4. Transform data
        chapter_number = extract_first_number(chapter_text)

        # 5. Build EpisodeData
        return EpisodeData(
            anime_title=self.config.series,
            episode_number=episode_number,
            episode_title=title,
            manga_start=chapter_number,
            manga_end=chapter_number,
            arc=None,
            source_url=source_url,
        )