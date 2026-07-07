from scraper.providers.metadata_factory import (
    create_metadata_provider,
)
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
        self.metadata_provider = metadata_provider

    def get_metadata(
        self,
        episode,
    ) -> EpisodeMetadata:
        provider = self.metadata_provider

        if provider is None:
            provider = create_metadata_provider(
                episode.anime.provider
            )

        return provider.get_episode_metadata(
            episode
        )