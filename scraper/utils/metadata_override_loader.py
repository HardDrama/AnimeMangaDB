import json
from pathlib import Path

from scraper.models.episode_metadata_override import (
    EpisodeMetadataOverride,
)


def load_metadata_overrides(
    path: str,
) -> dict[int, EpisodeMetadataOverride]:
    override_path = Path(path)

    if not override_path.exists():
        raise FileNotFoundError(
            f"Metadata override file not found: {path}"
        )

    data = json.loads(
        override_path.read_text(
            encoding="utf-8",
        )
    )

    episode_data = data.get("episodes", {})

    overrides: dict[int, EpisodeMetadataOverride] = {}

    for episode_number_text, values in episode_data.items():
        episode_number = int(episode_number_text)

        overrides[episode_number] = EpisodeMetadataOverride(
            episode_number=episode_number,
            episode_title=values.get("episode_title"),
            arc=values.get("arc"),
            reason=values.get("reason"),
        )

    return overrides