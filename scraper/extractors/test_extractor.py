from scraper.core.base_extractor import BaseExtractor
from scraper.models import EpisodeData


class TestExtractor(BaseExtractor):

    def fetch_page(self, url: str) -> str:
        return "<html></html>"
    
    def parse_episode(self, html: str) -> str:
        return EpisodeData(
            anime_title="Test Anime",
            episode_number=1,
            episode_title="Pilot",
            manga_start=1,
            manga_end=1,
            arc="Test Arc",
            source_url="https://example.com",
        )