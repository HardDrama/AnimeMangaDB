from time import perf_counter

from scraper.models.refresh_result import RefreshResult
from scraper.services.episode_metadata_service import (
    EpisodeMetadataService,
)


class EpisodeRefreshPipeline:
    """
    Refreshes metadata for a single existing episode.
    """

    def __init__(
        self,
        metadata_service: EpisodeMetadataService | None = None,
    ):
        self.metadata_service = (
            metadata_service
            or EpisodeMetadataService()
        )

    def refresh_episode(
        self,
        episode,
    ) -> RefreshResult:
        started_at = perf_counter()

        result = RefreshResult(
            success=False,
            provider=None,
        )

        metadata = self.metadata_service.get_metadata(
            episode
        )

        result.metadata = metadata

        if (
            metadata.title
            or metadata.arc
            or metadata.source_url
        ):
            result.success = True

        result.warnings.append(
            "Episode refresh pipeline is not implemented yet."
        )

        result.elapsed_seconds = (
            perf_counter() - started_at
        )

        return result