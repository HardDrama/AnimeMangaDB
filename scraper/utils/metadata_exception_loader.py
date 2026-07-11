import json
from pathlib import Path


def load_metadata_exceptions(
    path: str,
) -> dict:
    exception_path = Path(path)

    if not exception_path.exists():
        raise FileNotFoundError(
            f"Metadata exception file not found: {path}"
        )

    return json.loads(
        exception_path.read_text(
            encoding="utf-8",
        )
    )


def get_arc_not_applicable_episodes(
    exceptions: dict,
) -> set[int]:
    episode_numbers = exceptions.get(
        "arc_not_applicable",
        [],
    )

    return {
        int(episode_number)
        for episode_number in episode_numbers
    }


def is_arc_not_applicable(
    episode_number: int,
    exceptions: dict,
) -> bool:
    return episode_number in (
        get_arc_not_applicable_episodes(
            exceptions
        )
    )