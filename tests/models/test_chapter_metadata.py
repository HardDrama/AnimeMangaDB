from datetime import datetime

from scraper.models.chapter_metadata import ChapterMetadata


def test_chapter_metadata_supports_scope_v3_fields():
    timestamp = datetime.now()

    metadata = ChapterMetadata(
        chapter_number=1,
        chapter_title="Romance Dawn",
        manga_arc="Romance Dawn Arc",
        source_url="https://example.com/chapter/1",
        last_updated=timestamp,
    )

    assert metadata.chapter_number == 1
    assert metadata.chapter_title == "Romance Dawn"
    assert metadata.manga_arc == "Romance Dawn Arc"
    assert metadata.source_url == "https://example.com/chapter/1"
    assert metadata.last_updated == timestamp


def test_chapter_metadata_allows_partial_results():
    metadata = ChapterMetadata(
        chapter_number=2,
    )

    assert metadata.chapter_title is None
    assert metadata.manga_arc is None
    assert metadata.source_url is None
    assert metadata.last_updated is None