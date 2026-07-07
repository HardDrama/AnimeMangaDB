from dataclasses import dataclass, field

from scraper.models.episode_metadata import EpisodeMetadata


@dataclass
class RefreshResult:
    """
    Result of refreshing metadata for a single episode.
    """

    metadata: EpisodeMetadata = field(
        default_factory=EpisodeMetadata
    )

    success: bool = False

    provider: str | None = None

    warnings: list[str] = field(
        default_factory=list
    )

    elapsed_seconds: float = 0.0

    changed_fields: list[str] = field(
        default_factory=list
    )