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