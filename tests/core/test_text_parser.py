from scraper.core.text_parser import (
    extract_first_number,
    extract_all_numbers,
    extract_chapter_numbers,
)


def test_extract_first_number():
    assert extract_first_number("Chapter 1096") == 1096


def test_extract_first_number_returns_none():
    assert extract_first_number("No chapter data") is None


def test_extract_all_numbers():
    assert extract_all_numbers("Chapters 1096-1098") == [1096, 1098]


def test_extract_chapter_numbers_single():
    assert extract_chapter_numbers("Chapter 1096") == [1096]


def test_extract_chapter_numbers_ignores_page_numbers():
    assert extract_chapter_numbers("Chapter 1096 (p. 2-17)") == [1096]


def test_extract_chapter_numbers_no_match():
    assert extract_chapter_numbers("No manga equivalent") == []