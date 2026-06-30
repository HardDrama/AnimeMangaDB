from scraper.core.text_parser import extract_all_numbers


def test_extract_all_numbers():
    assert extract_all_numbers("Chapter 1096") == [1096]
    assert extract_all_numbers("Chapters 1096-1098") == [1096, 1098]
    assert extract_all_numbers("No chapters") == []