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

        result.provider = getattr(
            episode,
            "provider",
            None,
        )

        anime = getattr(episode, "anime", None)

        if anime:
            result.provider = anime.provider

        try:
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

        except Exception as exc:
            result.warnings.append(
                f"Metadata retrieval failed: {exc}"
            )

        if not result.success:
            result.warnings.append(
                "No metadata was returned for this episode."
            )

        result.elapsed_seconds = (
            perf_counter() - started_at
        )

        return result