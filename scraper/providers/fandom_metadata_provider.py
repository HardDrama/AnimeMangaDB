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

        html = None

        if (
            episode_url is not None
            and self.browser_client is not None
        ):
            html = self.browser_client.fetch_html(
                episode_url
            )

        episode_data = None

        if (
            html is not None
            and self.extractor is not None
        ):
            episode_data = self.extractor.parse(
                html=html,
                episode_number=episode.episode_number,
                source_url=episode_url,
            )

        if episode_data is not None:
            return EpisodeMetadata(
                title=episode_data.episode_title,
                arc=episode_data.arc,
                source_url=episode_data.source_url,
            )

        return EpisodeMetadata(
            source_url=episode_url,
        )