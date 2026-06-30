import re


def extract_first_number(text: str) -> int | None:
    """
    Extract the first integer from a string.

    Examples:
        "Chapter 1096" -> 1096
        "Chapter 1096 (p. 2-17)" -> 1096
        "No chapter" -> None
    """

    match = re.search(r"\d+", text)

    if match is None:
        return None

    return int(match.group())


def extract_all_numbers(text: str) -> list[int]:
    """
    Extract every integer from a string.

    Examples:
        "Chapter 1096" -> [1096]
        "Chapters 1096-1098" -> [1096, 1098]
        "No chapter" -> []
    """

    return [int(x) for x in re.findall(r"\d+", text)]

def extract_chapter_numbers(text: str) -> list[int]:
    """
    Extract chapter numbers while ignoring page numbers.
    """

    import re

    matches = re.findall(
        r"Chapter[s]?\s+(\d+)",
        text,
        flags=re.IGNORECASE,
    )

    return [int(match) for match in matches]

import re


def extract_chapter_numbers(text: str) -> list[int]:
    """
    Extract manga chapter numbers from text.

    Examples:
        Chapter 1096 (p. 2-17)
            -> [1096]

        Chapter 24 (p. 15-19)
        Chapter 25 (p. 2-19)
            -> [24, 25]
    """

    matches = re.findall(
        r"Chapter[s]?\+(\d+)",
        text,
        flags=re.IGNORECASE,
    )

    return [int(x) for x in matches]