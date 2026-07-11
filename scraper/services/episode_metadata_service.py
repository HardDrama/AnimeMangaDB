from scraper.providers.metadata_factory import (
    create_metadata_provider,
)
from scraper.models.episode_metadata import EpisodeMetadata
from scraper.providers.metadata_provider import MetadataProvider
from scraper.utils.metadata_override_loader import (
    load_metadata_overrides,
)


class EpisodeMetadataService:
    """
    Retrieves fresh metadata for a single episode.
    """

    def __init__(
        self,
        metadata_provider: MetadataProvider | None = None,
        override_path: str | None = None,
    ):
        self.metadata_provider = metadata_provider
        self.override_path = override_path

    def get_metadata(
        self,
        episode,
    ) -> EpisodeMetadata:
        provider = self.metadata_provider

        if provider is None:
            provider = create_metadata_provider(
                episode.anime.provider
            )

        metadata = provider.get_episode_metadata(
            episode
        )

        override_path = self.override_path

        if override_path is None:
            anime = getattr(
                episode,
                "anime",
                None,
            )

            anime_title = getattr(
                anime,
                "title",
                None,
            )

            if anime_title is not None:
                override_path = (
                    f"configs/overrides/"
                    f"{anime_title.lower().replace(' ', '_')}.json"
                )

        if override_path is not None:
            try:
                overrides = load_metadata_overrides(
                    override_path
                )
            except FileNotFoundError:
                overrides = {}
        else:
            overrides = {}

        override = overrides.get(
            episode.episode_number
        )

        if override is not None:
            if metadata.title is None:
                metadata.title = override.episode_title

            if metadata.arc is None:
                metadata.arc = override.arc

        return metadata