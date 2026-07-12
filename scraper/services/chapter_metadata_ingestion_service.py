from scraper.database.models import Anime
from scraper.models.chapter_metadata import ChapterMetadata
from scraper.repositories.episode_repository import EpisodeRepository
from scraper.services.chapter_url_discovery_service import (
    ChapterUrlDiscoveryService,
)
from scraper.providers.chapter_metadata_provider import (
    ChapterMetadataProvider,
)


class ChapterMetadataIngestionService:
    """
    Coordinates the complete Scope v3 chapter metadata
    ingestion pipeline.

    Discovery
        ↓
    Provider
        ↓
    Repository
    """

    def __init__(
        self,
        discovery_service: ChapterUrlDiscoveryService,
        provider: ChapterMetadataProvider,
        repository: EpisodeRepository,
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
                f"Unable to discover URL for "
                f"Chapter {chapter_number}."
            )

        metadata: ChapterMetadata = (
            self.provider.get_chapter_metadata(
                chapter_number=chapter_number,
                source_url=source_url,
            )
        )

        return self.repository.save_chapter_metadata(
            anime=anime,
            metadata=metadata,
        )