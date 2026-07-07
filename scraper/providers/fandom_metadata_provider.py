from scraper.models.episode_metadata import EpisodeMetadata
from scraper.providers.metadata_provider import MetadataProvider


class FandomMetadataProvider(MetadataProvider):
    """
    Retrieves fresh metadata from a Fandom episode page.
    """

    def get_episode_metadata(
        self,
        episode,
    ) -> EpisodeMetadata:
        return EpisodeMetadata()