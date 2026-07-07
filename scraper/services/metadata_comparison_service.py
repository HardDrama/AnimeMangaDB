from scraper.models.metadata_comparison_result import (
    MetadataComparisonResult,
)
from scraper.models.metadata_difference import (
    MetadataDifference,
)


class MetadataComparisonService:
    """
    Compares stored episode metadata against live metadata.
    """

    def compare(
        self,
        episode,
        metadata,
    ) -> MetadataComparisonResult:
        result = MetadataComparisonResult()

        current_source_url = (
            str(episode.source_url)
            if episode.source_url is not None
            else None
        )

        live_source_url = (
            str(metadata.source_url)
            if metadata.source_url is not None
            else None
        )

        if episode.episode_title != metadata.title:
            result.differences.append(
                MetadataDifference(
                    field="title",
                    current_value=episode.episode_title,
                    live_value=metadata.title,
                )
            )

        if episode.arc != metadata.arc:
            result.differences.append(
                MetadataDifference(
                    field="arc",
                    current_value=episode.arc,
                    live_value=metadata.arc,
                )
            )

        if current_source_url != live_source_url:
            result.differences.append(
                MetadataDifference(
                    field="source_url",
                    current_value=current_source_url,
                    live_value=live_source_url,
                )
            )

        return result