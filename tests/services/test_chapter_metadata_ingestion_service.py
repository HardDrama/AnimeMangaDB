from datetime import datetime

import pytest

from scraper.models.chapter_metadata import ChapterMetadata
from scraper.services.chapter_metadata_ingestion_service import (
    ChapterMetadataIngestionService,
)


class FakeAnime:
    id = 1


class FakeDiscoveryService:

    def discover_url(
        self,
        chapter_number,
    ):
        return (
            f"https://example.com/chapter/{chapter_number}"
        )


class MissingDiscoveryService:

    def discover_url(
        self,
        chapter_number,
    ):
        return None


class FakeProvider:

    def get_chapter_metadata(
        self,
        chapter_number,
        source_url,
    ):
        return ChapterMetadata(
            chapter_number=chapter_number,
            chapter_title="Test Chapter",
            manga_arc="Test Arc",
            source_url=source_url,
            last_updated=datetime.now(),
        )


class FailingProvider:

    def get_chapter_metadata(
        self,
        chapter_number,
        source_url,
    ):
        raise RuntimeError(
            "Provider failed."
        )


class FakeRepository:

    def __init__(self):
        self.saved = None

    def save_chapter_metadata(
        self,
        anime,
        metadata,
    ):
        self.saved = (
            anime,
            metadata,
        )
        return metadata


def test_ingests_chapter_metadata():
    repository = FakeRepository()

    service = ChapterMetadataIngestionService(
        discovery_service=FakeDiscoveryService(),
        provider=FakeProvider(),
        repository=repository,
    )

    anime = FakeAnime()

    metadata = service.ingest(
        anime=anime,
        chapter_number=1,
    )

    assert metadata.chapter_number == 1
    assert metadata.chapter_title == "Test Chapter"
    assert repository.saved is not None


def test_missing_discovery_raises():
    service = ChapterMetadataIngestionService(
        discovery_service=MissingDiscoveryService(),
        provider=FakeProvider(),
        repository=FakeRepository(),
    )

    with pytest.raises(
        RuntimeError,
        match="Unable to discover URL",
    ):
        service.ingest(
            anime=FakeAnime(),
            chapter_number=1,
        )


def test_provider_failure_propagates():
    service = ChapterMetadataIngestionService(
        discovery_service=FakeDiscoveryService(),
        provider=FailingProvider(),
        repository=FakeRepository(),
    )

    with pytest.raises(
        RuntimeError,
        match="Provider failed",
    ):
        service.ingest(
            anime=FakeAnime(),
            chapter_number=1,
        )