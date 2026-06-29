from scraper.core.base_extractor import BaseExtractor
from scraper.core.parser import HtmlParser
from scraper.models import EpisodeData


class ExampleExtractor(BaseExtractor):
    """
    Simple extractor used to learn BeautifulSoup.
    """

    def fetch_page(self, url: str) -> str:
        raise NotImplementedError(
            "ExampleExtractor does not download pages."
        )

    def parse_episode(self, html: str) -> EpisodeData:

        soup = HtmlParser().parse(html)

        title = soup.title.text.strip()

        return EpisodeData(
            anime_title=title,
            episode_number=1,
            episode_title=title,
            manga_start=None,
            manga_end=None,
            arc=None,
            source_url="https://example.com",
        )