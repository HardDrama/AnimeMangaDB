from time import perf_counter

from scraper.models.refresh_result import RefreshResult


class EpisodeRefreshPipeline:
    """
    Refreshes metadata for a single existing episode.
    """

    def refresh_episode(
        self,
        episode,
    ) -> RefreshResult:
        started_at = perf_counter()

        result = RefreshResult(
            success=False,
            provider=None,
        )

        result.warnings.append(
            "Episode refresh pipeline is not implemented yet."
        )

        result.elapsed_seconds = perf_counter() - started_at

        return result