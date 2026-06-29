from abc import ABC, abstractmethod

from scraper.models import EpisodeData


class BaseExtractor(ABC):
    """
    Abstract base class for all wiki extractors.
    """

    @abstractmethod
    def fetch_page(self, url: str) -> str:
        """
        Download the HTML for a page.
        """
        pass

    @abstractmethod
    def parse_episode(self, html: str) -> EpisodeData:
        """
        Parse the HTML and return an EpisodeData object.
        """
        pass