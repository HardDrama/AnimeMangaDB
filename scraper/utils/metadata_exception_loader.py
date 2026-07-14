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

def get_manga_arc_not_applicable_chapters(
    exceptions: dict,
) -> set[int]:
    chapter_metadata = exceptions.get(
        "chapter_metadata",
        {},
    )

    chapter_numbers = chapter_metadata.get(
        "manga_arc_not_applicable",
        [],
    )

    if not isinstance(
        chapter_numbers,
        list,
    ):
        raise ValueError(
            "chapter_metadata."
            "manga_arc_not_applicable "
            "must be a list."
        )

    normalized_numbers = set()

    for chapter_number in chapter_numbers:
        if isinstance(
            chapter_number,
            bool,
        ):
            raise ValueError(
                "Chapter metadata exception values "
                "must be integers."
            )

        try:
            normalized_number = int(
                chapter_number
            )
        except (
            TypeError,
            ValueError,
        ) as error:
            raise ValueError(
                "Chapter metadata exception values "
                "must be integers."
            ) from error

        if normalized_number <= 0:
            raise ValueError(
                "Chapter metadata exception values "
                "must be positive integers."
            )

        normalized_numbers.add(
            normalized_number
        )

    return normalized_numbers


def is_manga_arc_not_applicable(
    chapter_number: int,
    exceptions: dict,
) -> bool:
    return chapter_number in (
        get_manga_arc_not_applicable_chapters(
            exceptions
        )
    )