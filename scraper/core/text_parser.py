print("LOADED TEXT PARSER FILE")
import re


def extract_first_number(text: str) -> int | None:
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def extract_all_numbers(text: str) -> list[int]:
    return [int(x) for x in re.findall(r"\d+", text)]


def extract_chapter_numbers(text: str) -> list[int]:
    """
    Extract chapter numbers while ignoring page numbers.
    """
    matches = re.findall(r"Chapter\s*(\d+)", text, flags=re.IGNORECASE)
    return [int(m) for m in matches]