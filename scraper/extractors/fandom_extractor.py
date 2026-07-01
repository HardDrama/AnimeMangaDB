from scraper.core.parser import HtmlParser
from scraper.core.selector_engine import SelectorEngine
from scraper.core.extract import required_text
from scraper.models import EpisodeData, ProviderConfig
from scraper.core.text_parser import extract_chapter_numbers


class FandomExtractor:

    def __init__(self, config: ProviderConfig):
        self.config = config

    def parse(self, html: str, episode_number: int, source_url: str) -> EpisodeData:

        soup = HtmlParser().parse(html)

        engine = SelectorEngine(soup, self.config)

        title = required_text(engine, "title")

        chapter_node = soup.select_one("div[data-source='chapter'] a")

        chapter_text = chapter_node.get_text() if chapter_node else ""

        chapter_numbers = extract_chapter_numbers(chapter_text)

        manga_start = chapter_numbers[0] if len(chapter_numbers) >= 1 else None
        manga_end = chapter_numbers[-1] if len(chapter_numbers) >= 1 else None

        return EpisodeData(
            anime_title=self.config.series,
            episode_number=episode_number,
            episode_title=title,
            manga_start=manga_start,
            manga_end=manga_end,
            arc=None,
            source_url=source_url,
        )