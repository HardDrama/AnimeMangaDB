from dataclasses import dataclass


@dataclass(slots=True)
class EpisodeMetadataOverride:
    episode_number: int
    episode_title: str | None = None
    arc: str | None = None
    reason: str | None = None