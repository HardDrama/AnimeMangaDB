from scraper.models.episode_metadata import EpisodeMetadata
from scraper.providers.fandom_metadata_provider import (
    FandomMetadataProvider,
)
from scraper.providers.metadata_provider import MetadataProvider


class EpisodeMetadataService:
    """
    Retrieves fresh metadata for a single episode.
    """

    def __init__(
        self,
        metadata_provider: MetadataProvider | None = None,
    ):
        self.metadata_provider = (
            metadata_provider
            or FandomMetadataProvider()
        )

    def get_metadata(
        self,
        episode,
    ) -> EpisodeMetadata:
        return self.metadata_provider.get_episode_metadata(
            episode
        )