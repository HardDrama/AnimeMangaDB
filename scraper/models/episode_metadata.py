from dataclasses import dataclass


@dataclass
class EpisodeMetadata:
    """
    Fresh metadata retrieved for an episode.

    All fields are optional so providers can return
    only the information they successfully retrieve.
    """

    title: str | None = None
    arc: str | None = None
    source_url: str | None = None