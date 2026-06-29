from abc import ABC, abstractmethod

from scraper.models import ProviderConfig


class BaseProvider(ABC):
    """
    Base class for all provider types (Fandom, MediaWiki, etc.).
    """

    def __init__(self, config: ProviderConfig):
        self.config = config

    @abstractmethod
    def build_episode_url(self, episode_number: int) -> str:
        """Build the URL for an episode page."""
        raise NotImplementedError