from scraper.database.models_shared_manga import (
    Anime,
)
from scraper.models.chapter_metadata import (
    ChapterMetadata,
)
from scraper.providers.chapter_metadata_provider import (
    ChapterMetadataProvider,
)
from scraper.repositories.manga_repository_shared_manga import (
    MangaRepository,
)
from scraper.services.chapter_url_discovery_service import (
    ChapterUrlDiscoveryService,
)


class ChapterMetadataIngestionService:
    """
    Shared-manga runtime candidate for the complete Scope v3
    chapter metadata ingestion pipeline.

    Discovery
        ↓
    Provider
        ↓
    MangaRepository
    """

    def __init__(
        self,
        discovery_service: ChapterUrlDiscoveryService,
        provider: ChapterMetadataProvider,
        repository: MangaRepository,
    ):
        self.discovery_service = discovery_service
        self.provider = provider
        self.repository = repository

    def ingest(
        self,
        anime: Anime,
        chapter_number: int,
    ):
        source_url = self.discovery_service.discover_url(
            chapter_number
        )

        if source_url is None:
            raise RuntimeError(
                "Unable to discover URL for "
                f"Chapter {chapter_number}."
            )

        metadata: ChapterMetadata = (
            self.provider.get_chapter_metadata(
                chapter_number=chapter_number,
                source_url=source_url,
            )
        )

        return (
            self.repository
            .save_chapter_metadata_for_anime(
                anime=anime,
                metadata=metadata,
            )
        )
