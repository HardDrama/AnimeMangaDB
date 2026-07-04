from abc import ABC, abstractmethod

from scraper.models import EpisodeReference


class BaseEpisodeIndexCrawler(ABC):
    """
    Base interface for episode index crawlers.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def get_episode_list(self) -> list[EpisodeReference]:
        """
        Return discovered episode references.
        """
        raise NotImplementedError