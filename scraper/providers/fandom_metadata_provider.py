from scraper.models.episode_metadata import EpisodeMetadata
from scraper.providers.metadata_provider import MetadataProvider


class FandomMetadataProvider(MetadataProvider):
    """
    Retrieves fresh metadata from a Fandom episode page.
    """

    def __init__(
        self,
        provider=None,
        browser_client=None,
        extractor=None,
    ):
        self.provider = provider
        self.browser_client = browser_client
        self.extractor = extractor

    def get_episode_metadata(
        self,
        episode,
    ) -> EpisodeMetadata:
        episode_url = None

        if self.provider is not None:
            episode_url = self.provider.build_episode_url(
                episode.episode_number
            )

        return EpisodeMetadata(
            source_url=episode_url,
        )