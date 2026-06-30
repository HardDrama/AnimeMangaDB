from scraper.core.parser import HtmlParser
from scraper.core.selector_engine import SelectorEngine
from scraper.core.extract import required_text
from scraper.models import EpisodeData, ProviderConfig
from scraper.core.text_parser import extract_chapter_numbers

import scraper.core.text_parser as tp

print("TEXT PARSER MODULE:", tp.__file__)
print("FUNCTION:", tp.extract_chapter_numbers("Chapter 1096"))


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

        chapter_node = soup.select_one("div[data-source='chapter'] a")

        print("DEBUG CHAPTER NODE:", chapter_node)

        if chapter_node:
            print("DEBUG CHAPTER TEXT:", chapter_node.get_text())

        # 2. Create selector engine
        engine = SelectorEngine(soup, self.config)

        # 3. Extract fields
        title = required_text(engine, "title")

        chapter_text = chapter_node.get_text() if chapter_node else ""

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