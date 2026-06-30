from scraper.core.parser import HtmlParser
from scraper.core.selector_engine import SelectorEngine
from scraper.core.extract import required_text
from scraper.models import EpisodeData, ProviderConfig
from scraper.core.text_parser import extract_chapter_numbers


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

        print(repr(chapter_text))

        # 4. Transform data
        chapter_numbers = extract_chapter_numbers(chapter_text)

        if len(chapter_numbers) == 0:
            manga_start = None
            manga_end = None

        elif len(chapter_numbers) == 1:
            manga_start = chapter_numbers[0]
            manga_end = chapter_numbers [0]

        else:
            manga_start = chapter_numbers[0]
            manga_end = chapter_numbers[-1]

        # 5. Build EpisodeData
        return EpisodeData(
            anime_title=self.config.series,
            episode_number=episode_number,
            episode_title=title,
            manga_start=manga_start,
            manga_end=manga_end,
            arc=None,
            source_url=source_url,
        )