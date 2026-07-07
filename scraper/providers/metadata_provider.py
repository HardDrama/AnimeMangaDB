from abc import ABC, abstractmethod

from scraper.models.episode_metadata import EpisodeMetadata


class MetadataProvider(ABC):
    """
    Retrieves fresh metadata for a single episode.
    """

    @abstractmethod
    def get_episode_metadata(
        self,
        episode,
    ) -> EpisodeMetadata:
        """
        Retrieve fresh metadata for one episode.
        """
        raise NotImplementedError