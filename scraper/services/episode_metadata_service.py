from scraper.models.episode_metadata import (
    EpisodeMetadata,
)


class EpisodeMetadataService:
    """
    Retrieves fresh metadata for a single episode.
    """

    def get_metadata(
        self,
        episode,
    ):
        return EpisodeMetadata()